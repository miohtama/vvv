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

def get_match_option(yaml, section, entry = None, default=[]):
    
    if entry:
        opt = get_option(yaml, section, entry, default)
    else:
        opt = yaml.get(section, default)

    # Split space or new line separated list to pieces
    if type(opt) != list:
        opt = opt.split() 

    g = ExceptionGlobster(opt)

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
