"""

    Helper functions.

"""

# Dangerous default value [] as argument
# pylint: disable=W0102 

# Python imports
import os
import subprocess
import tempfile

# Third party
import yaml
from .bzrlib.globster import ExceptionGlobster

class ShellCommandFailed(Exception):
    """ Executing a shell command failed """

def match_file(fullpath, matchlist):
    """
    Bzr style file matching.

    http://doc.bazaar.canonical.com/beta/en/user-reference/ignore-help.html

    :param matchlist: Globster object
    """
            
    return matchlist.match(fullpath)

def get_option(config, section_name, entry, default=None):
    """
    Convert YAML tree entry to a Python list.

    If section does not exist return empty list.
    
    http://pyyaml.org/wiki/PyYAMLDocumentation#Blocksequences 

    :param config: Configuration as Python dict
    """

    section = config.get(section_name, {})

    if type(section) == str:
        raise RuntimeError("Expected configuration file block, but found a string option instead %s: %s" % (section_name, entry))

    entry = section.get(entry, default)

    return entry

def get_list_option(config, section, entry, default=[]):
    """
    Read YAML config which is list-line
    """
    return get_option(config, section, entry, default)

def get_boolean_option(config, section, entry, default=False):
    """
    Read YAML true/false config 
    """
    return get_option(config, section, entry, default)

def get_int_option(config, section, entry, default=0):
    """
    Read YAML int config 
    """
    return get_option(config, section, entry, default)    

def get_string_option(config, section, entry, default=""):
    """
    Read YAML string config 
    """
    return get_option(config, section, entry, default)

def get_match_option(config, section, entry = None, default=[], debug=False):
    """
    Read YAML config which is a block string of file ignore patterns  
    """    
    if entry:
        opt = get_option(config, section, entry, default)
    else:
        opt = config.get(section, default)

    if type(opt) == str:
        # Split space or new line separated list to pieces
        opt = opt.split() 
    elif type(opt) == list:
        pass
    else:
        raise RuntimeError("Bad option data for %s %s" % (section, entry))

    g = ExceptionGlobster(opt, debug)

    g.orignal_pattern = opt

    return g

def load_yaml_file(fpath):
    """
    Try to load YAML config file and return empty dict if the file does not exist.
    """
    # Return empty options
    if not os.path.exists(fpath):
        return {}

    f = open(fpath, "rt")
    try:
        tree = yaml.load(f)
        return tree
    finally:
        f.close()

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
    # A-wooo! Mira, python no necesita el "except:". Achis... Que listo es.
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
