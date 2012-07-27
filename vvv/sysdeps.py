"""

    Dependency checker and installer for system-wide commands.

    Check for things like is Java present, is node present, etc.
    and installs packages for these systems.

"""

# Python imports
import os
import sys

# Local imports
from .utils import shell, temporary_working_directory
from .download import download

class HasNotCommand(Exception):
    """
    Thrown when OS lacks a command we'd like to use
    """

def which(program):
    """
    http://stackoverflow.com/a/377028/315168
    """

    def is_exe(fpath):
        """
        Check if we can execute the command
        """
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath = os.path.dirname(program)
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
        raise HasNotCommand("Your system does not have %s installed which is needed to run %s. %s" % (name, needed_for, instructions))

def has_java(needed_for):
    """
    Check java is installed
    """
    return has_exe("java", needed_for)

def has_node(needed_for):
    """
    Check for sane Node.js installation
    """
    how = "Install Node.js using your OS package manager https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager"
    return has_exe("node", needed_for, how) and has_exe("npm", needed_for, how)


def has_virtualenv(needed_for):
    """
    Check python virtualenv is installed
    """

    venvs = [ "virtualenv-3.2", "virtualenv-2.7", "virtualenv"]

    for v in venvs:
        if which(v):
            return True

    return has_exe("virtualenv", needed_for)

def virtualenv_exists(target):
    """
    Check if a specific virtualenv is installed

    :param target: Path to a virtualenv 
    """
    target = "%s/bin/activate" % target
    return os.path.exists(target)


def get_py3k_command():
    """
    Get command to run Python 3.

    ... they don't make this easy for us ...
    """   

    # Depends on OSX/Linux dist which command to use
    versions = [
        # Macports
        "python-3.2", 

        # Ubuntu
        "python3.2", "python3.1", "python3",
    ]
    for v in versions:
        if which(v):
            return v

def get_py2_command():
    """
    Get command to run Python 3.

    ... they don't make this easy for us ...
    """   

    # Depends on OSX/Linux dist which command to use
    versions = [
        # Macports
        "python-2.7", "python-2.6", 

        # Ubuntu
        "python2.7", "python2.6"
    ]
    for v in versions:
        if which(v):
            return v            

def get_virtualenv_py3k_command():
    """
    Get command to create Python 3 virtualenv.

    ... they don't make this easy for us ...
    """   

    # Depends on OSX/Linux dist which command to use
    versions = [
        # Macports
        "virtualenv-3.4", "virtualenv-3.3", "virtualenv-3.2", 
    ]
    for v in versions:
        if which(v):
            return v

def get_virtualenv_py2_command():            
    """
    Get command to create Python 3 virtualenv.
    """
    versions = ["virtualenv-2.7", "virtualenv2.7"]
    for v in versions:
        if which(v):
            return v

def install_virtualenv_command(logger, path):
    """ 
    Use virtualenv bootstrap script becase we cannot rely on ``virtualenv`` command working
    with Python 3 on various operating systems like Ubuntu.
    """
    download(logger, path, "https://raw.github.com/pypa/virtualenv/master/virtualenv.py")


def create_virtualenv(logger, venv_target, target, egg_spec=None, py3=True):
    """
    Creates a Python virtualenv and installs a single package there with dependencies.
    
    Note that we cannot use default "virtualenv" command as this most likely breaks
    on OSX with its mostly broken old Python installations. Get Python from Macports.

    :param venv_target: Where to place virtualenv.py if needs to be downloaded

    :param target: Target folder

    :param egg_spec: Python egg specification to be installed in venv, name or name with version. E.g. pylint==0.25.1

    :param python: Use custom Python interpreter to run virtualenv
    """

    if os.path.exists(target):
        logger.debug("Virtualenv exists: %s" % target)
        return

    if not venv_target.endswith("virtualenv.py"):
        raise RuntimeError("You must give virtualenv.py location for download")

    # Try get OS virtualenv command
    if py3:
        venv_cmd = get_virtualenv_py3k_command()
    else:
        venv_cmd = get_virtualenv_py2_command()

    if not venv_cmd:
        # Operating system does not provide working virtualenv command,
        # download virtualenv.py

        install_virtualenv_command(logger, venv_target)

        if py3:
            venv_cmd = get_py3k_command()
            if not venv_cmd:
                raise RuntimeError("Did not find installed Python 3 on the system")
        else:
            venv_cmd = get_py2_command()           
            if not venv_cmd:
                raise RuntimeError("Did not find installed Python 2 on the system")

        venv_cmd += " " + venv_target 
            
    # Execute virtualenv.py
    shell(logger, "%s %s" % (venv_cmd, target), raise_error=True)

    # Install eny eggs if needed
    if egg_spec:
        shell(logger, '. %s/bin/activate ; easy_install "%s"' % (target, egg_spec), raise_error=True)

def run_virtualenv_command(logger, target, command, raise_error=False):
    """
    Run a shell command having target virtualenv active
    """
    # use "." instead of "source" beacuse Popen uses /bin/sh by default, "source" is /bin/bash specific
    return shell(logger, '. %s/bin/activate ; %s' % (target, command), raise_error=raise_error)

def install_npm(logger, target, package, raise_error=False):
    """
    Installs node NPM package.

    Runs NPM command and creates local package installation under target folder
    """
    with temporary_working_directory(target):
        return shell(logger, 'npm install  %s' % package, raise_error=raise_error)

def get_bin_path():
    """
    Get the path where VVV scripts lie.

    Assume we are installed via setup.py script entry point and VVV script lies in the same folder with us    
    """

    current_path = os.path.dirname(os.path.join(os.getcwd(), sys.argv[0]))

    if "vvv/tests" in current_path:
        # Test runner uses non setup.py entry points, 
        # which cause great confusion. 
        # For now, we handle this as an ugly special case - 
        # tests actually could not potentially access these scripts
        #  vvv runnable did not exist at /Users/moo/code/vvv/tests/vvv
        current_path = os.path.join(current_path, "..", "venv", "bin")

    # Sanity check
    vvv = os.path.join(current_path, "vvv")
    if not os.path.exists(vvv):

        # Then try this trick, assume we are running in activated virtualenv
        # Like in the case of Travis-CI
        vvv = which("vvv")
        if vvv:
            return os.path.dirname(vvv)


        raise RuntimeError("vvv runnable did not exist at %s" % current_path)
        
    return current_path

