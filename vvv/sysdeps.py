"""

    System-wide dependency checker.

    Check for things like is Java present, is node present, etc.

"""

# Python imports
import os
import subprocess

# Local imports
from .utils import shell

class HasNotCommand(Exception):
    """
    """

def which(program):
    """
    http://stackoverflow.com/a/377028/315168
    """

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def has_exe(name, needed_for="validator", instructions=""):
    """
    Check whether a command is installed on the system or not and provide user friendly failure.
    """
    if not which(name):     
        raise HasNotCommand("Your system does not have %s installed which is needed to run %s. %s" % (name, needed_for, install_instructions))

def has_java(needed_for):
    """
    """
    return has_exe("java", needed_for)

def has_node(needer_for):
    """
    """
    return has_exe("nodejs", needed_for, "Install Node.js using your OS package manager https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager")

def has_spidermoney(needed_for):
    return has_exe("js", needed_for)

def has_virtualenv(needed_for):
    return has_exe("virtualenv", needed_for)

def virtualenv_exists(target):
    """
    Check if a specific virtualenv is installed

    :param target: Path to a virtualenv 
    """
    target = "%s/bin/activate" % target
    return os.path.exists(target)

def create_virtualenv(logger, target, egg_spec):
    """
    Creates a Python virtualenv and installs a single package there with dependencies.
    
    :param target: Target folder

    :param egg_spec: Egg specification, name or name with version. E.g. pylint==0.25.1
    """

    if os.path.exists(target):
        return

    shell("virtualenv %s" % target, raise_error=True)

    shell('source %s/bin/activate ; easy_install "%s"' % (target, egg_spec), raise_error=True)

def run_virtualenv_command(logger, target, command):
    shell('source %s/bin/activate ; %s' % (target, command), raise_error=True)
