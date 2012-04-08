"""

    Helper functions.

"""

# Dangerous default value [] as argument
# pylint: disable=W0102 

# Python imports
import os
import subprocess

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

    # Split space or new line separated list to pieces
    if type(opt) != list:
        opt = opt.split() 

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

