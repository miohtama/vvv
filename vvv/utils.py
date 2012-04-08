"""

    Helper functions.

"""


# Python imports
import fnmatch
import re
import os

# Third party
import yaml
from .bzrlib.globster import ExceptionGlobster

class ShellCommandFailed(Exception):
    """ Executing a shell command failed """

def match_file(logger, fullpath, matchlist):
    """
    Bzr style file matching.

    http://doc.bazaar.canonical.com/beta/en/user-reference/ignore-help.html

    :param matchlist: Globster object
    """
            
    if matchlist.match(fullpath):
        logger.debug("File %s matches by pattern %s" % (fullpath, matchlist.orignal_pattern))
        return True
    else:
        logger.debug("File %s is ignored by pattern %s" % (fullpath, matchlist.orignal_pattern))
        return False

def get_option(yaml, section, entry, default=None):
    """
    Convert YAML tree entry to a Python list.

    If section does not exist return empty list.
    
    http://pyyaml.org/wiki/PyYAMLDocumentation#Blocksequences 
    """

    section = yaml.get(section, {})
    entry = section.get(entry, default)

    return entry

def get_list_option(yaml, section, entry, default=[]):
    return get_option(yaml, section, entry, default)

def get_boolean_option(yaml, section, entry, default=False):
    return get_option(yaml, section, entry, default)

def get_int_option(yaml, section, entry, default=0):
    return get_option(yaml, section, entry, default)    

def get_string_option(yaml, section, entry, default=""):
    return get_option(yaml, section, entry, default)

def get_match_option(yaml, section, entry = None, default=[], debug=False):
    
    if entry:
        opt = get_option(yaml, section, entry, default)
    else:
        opt = yaml.get(section, default)

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

def shell(logger, cmd, raise_error=False):
    """
    Run a shell command.

    :param cmd: Shell line to be executed

    :return: Tuple (return code, interleaved stdout and stderr output as string)
    """    

    logger.debug("Running command line: %s" % cmd)

    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # XXX: Support stderr interleaving
    out, err = process.communicate()

    out = out.decode("utf-8")
    err = err.decode("utf-8")

    if raise_error and process.returncode != 0:
        logger.error("Command output:")
        logger.error(out + err)
        raise ShellCommandFailed("The following command did not succeed: %s" % cmd)

    return (process.returncode, out + err)    

