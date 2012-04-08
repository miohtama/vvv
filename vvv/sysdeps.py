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

def get_virtualenv_py3k_command():
    """
    ... they don't make this easy for us ...
    """   

    # Depends on OSX/Linux dist which command to use
    versions = [
        # Macports
        "virtualenv-3.4", "virtualenv-3.3", "virtualenv-3.2", 

        # Ubuntu
        "virtualenv-32"
    ]
    for v in versions:
        if which(v):
            return v

def get_virtualenv_py2_command():            
    versions = ["virtualenv-2.7", "virtualenv2.7"]
    for v in versions:
        if which(v):
            return v

def create_virtualenv(logger, target, egg_spec=None, py3=True, python=None):
    """
    Creates a Python virtualenv and installs a single package there with dependencies.
    
    Note that we cannot use default "virtualenv" command as this most likely breaks
    on OSX with its mostly broken old Python installations. Get Python from Macports.

    :param target: Target folder

    :param egg_spec: Python egg specification to be installed in venv, name or name with version. E.g. pylint==0.25.1

    :param python: Use custom Python interpreter to run virtualenv
    """

    if os.path.exists(target):
        logger.debug("Virtualenv exists: %s" % target)
        return

    if py3:
        venv_cmd = get_virtualenv_py3k_command()
        if not venv_cmd:
            raise RuntimeError("Ooops could not found virtualenv for Python 3.x")
    else:
        venv_cmd = get_virtualenv_py2_command()
        if not venv_cmd:
            raise RuntimeError("Ooops could not found virtualenv for Python 2.x")
            
    if python:
        shell(logger, "%s -p %s %s" % (venv_cmd, python, target), raise_error=True)
    else:
        shell(logger, "%s %s" % (venv_cmd, target), raise_error=True)

    if egg_spec:
        shell(logger, 'source %s/bin/activate ; easy_install "%s"' % (target, egg_spec), raise_error=True)

def run_virtualenv_command(logger, target, command, raise_errors=False):
    return shell(logger, 'source %s/bin/activate ; %s' % (target, command), raise_error=raise_errors)

