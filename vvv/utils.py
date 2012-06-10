"""

    Helper functions.

"""

# Python imports
import os
import subprocess
import tempfile

class ShellCommandFailed(Exception):
    """ Executing a shell command failed """

def match_file(fullpath, matchlist):
    """
    Bzr style file matching.

    http://doc.bazaar.canonical.com/beta/en/user-reference/ignore-help.html

    :param matchlist: Globster object
    """
            
    return matchlist.match(fullpath)


def is_binary_file(fpath):
    """
    Check if file is binary or not.

    We use our faulty heurestic here. Make this better, please.
    The same logic as with git diff, they claim.

    http://stackoverflow.com/a/3002505/315168
    """

    fin = open(fpath, 'rb')

    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if b'\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    finally:
        fin.close()

    return False

def shell(logger, cmdline, raise_error=False):
    """
    Run a shell command.

    :param cmd: Shell line to be executed

    :return: Tuple (return code, interleaved stdout and stderr output as string)
    """    

    logger.debug("Running command line: %s" % cmdline)

    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # XXX: Support stderr interleaving
    out, err = process.communicate()

    # :E1103: *%s %r has no %r member (but some types could not be inferred)*
    # pylint: disable=E1103 
    out = out.decode("utf-8")
    err = err.decode("utf-8")

    if raise_error and process.returncode != 0:
        logger.error("Command output:")
        logger.error(out + err)
        raise ShellCommandFailed("The following command did not succeed: %s" % cmdline)

    return (process.returncode, out + err)    

class TempConfigFile:
    """
    Content guard which creates a temporary file which can be passed as ini/rc file to the executed command.

    http://effbot.org/zone/python-with-statement.htm

    :return: File object
    """
    def __init__(self, config_data):
        self.config_data = config_data
        self.f = None

    def __enter__(self):
        """
        :return: Full path to a temporary config file
        """
        self.f = tempfile.NamedTemporaryFile(mode="wt", delete=False)
        self.f.write(self.config_data)
        self.f.close()        
        return self.f.name

    def __exit__(self, exit_type, value, traceback):
        self.f.unlink(self.f.name)

def temp_config_file(config_data):
    return TempConfigFile(config_data)


class TemporaryWorkingDirectory:
    """
    Temporary change working directory and fall back to the current directory when the commands have been executed.
    """

    def __init__(self, folder):
        self.folder = folder
        self.old_folder = None

    def __enter__(self):
        """
        """
        self.old_folder = os.getcwd()
        os.chdir(self.folder)

    def __exit__(self, exit_type, value, traceback):
        """
        """
        os.chdir(self.old_folder)

def temporary_working_directory(folder):
    """
    Context manager which temporarily cds to another folder
    """
    return TemporaryWorkingDirectory(folder)


def snip_output(output, marker):
    """
    Remove tailing lines of the output after encountering certain marker string in the output.

    :param output: Command output as a string

    :param marker: Marker string after which all lines can be dropped
    """
    passed = []
    filtering = False
    for line in output.split("\n"):

        if marker in line:
            filtering = True

        if not filtering:
            passed.append(line)


    return "\n".join(passed)


