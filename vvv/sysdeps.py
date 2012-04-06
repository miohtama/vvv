"""

	System-wide dependency checker.

	Check for things like is Java present, is node present, etc.

"""

import os

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

def has_exe(name, needed_for="validator"):
	"""
	Check whether a command is installed on the system or not and provide user friendly failure.
	"""
	if not which(name):
		raise HasNotCommand("Your system does not have %s installed which is needed to run %s" % (name, needed_for))

def has_java(needed_for):
	"""
	"""
	return has_exe("java", needed_for)
