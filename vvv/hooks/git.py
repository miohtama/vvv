"""

    Git commit hook integration.

    This module contains 

    - Precommit hook installer

    - Precommit hook command itself (setup.py entry point)

    http://book.git-scm.com/5_git_hooks.html

"""

# Python core
import os
import sys
import stat
import logging

# Third party
import plac

# Local
from vvv import utils
from vvv import main


#: Command giving you git staging list
#: http://stackoverflow.com/a/10164204/315168
GIT_COMMIT_LIST = "git diff-index -z --cached HEAD --name-only"

PRECOMMIT_HOOK_TEMPLATE = """#!/bin/sh
#
# Please feel free to add any additional VVV command line switches for this command
#
%s
"""

def get_precommit_command():
    """
    Get the location of installed VVV command.

    Assume we are installed via setup.py script entry point and VVV script lies in the same folder with us
    """

    current_path = os.path.dirname(os.path.join(os.getcwd(), sys.argv[0]))

    hook = os.path.join(current_path, "vvv-git-pre-commit-hook")
    if not os.path.exists(hook):
        return None

    return hook

def setup_hook():
    """ 
    Install git precommit hook.

    Use --silent option if you want to supress output if the hook already exists. E.g.::

    vvv-install-git-pre-commit-hook . --silent

    In silent mode exit code is always 0.
    """

    command = get_precommit_command()
    if not command:
        sys.exit("Cannot find vvv command associated with precommit hook installer")

    if len(sys.argv) < 2:
        sys.exit("Please give a path as argument")

    silent = False

    path = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2] == "--silent":
            silent = True

    if not os.path.exists(os.path.join(path, ".git")):
        if not silent:
            print("Not a git repo: %s" % path)
            sys.exit(1)
        else:
            sys.exit(0)

    path = os.path.abspath(path)
    
    cmdline = "%s %s" % (command, path)    

    precommit = os.path.join(path, ".git", "hooks", "pre-commit")

    if os.path.exists(precommit):
        if not silent:
            print("Precommit hook already exists: %s" % precommit)
            print("Manually add in the command:")
            print(cmdline)
            sys.exit(1)
        else:
            sys.exit(0)

    hook = PRECOMMIT_HOOK_TEMPLATE % cmdline
    
    f = open(precommit, "wt")
    f.write(hook)
    f.close()

    # Make hook executable
    mode = os.stat(precommit).st_mode
    mode += stat.S_IXOTH + stat.S_IXGRP + stat.S_IXUSR
    os.chmod(precommit, mode)

    if not silent:
        print("Installed git precommit hook %s" % precommit)
    sys.exit(0)


        
def precommit_hook():
    """
    Run pre-commit hook.

    Pass all command line options to VVV main process and add filename as the last paramter to these. 

    Validate all files. If any of the files fail then abort the commit.
    """


    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    logger = logging.getLogger("precommit-hook")

    # Assume repository root is the single argument
    if len(sys.argv) < 2:
        sys.exit("Missing git repository as argument")

    repo_path = sys.argv[-1]

    if not os.path.exists(repo_path):
        sys.exit("Repositoty path does not exist: %s" % repo_path)

    # Get git diff-index output for the repo
    with utils.temporary_working_directory(repo_path):
        exit_code, diff_output = utils.shell(logger, GIT_COMMIT_LIST) 

    if exit_code != 0:
        print("Failed to execute: %s" % GIT_COMMIT_LIST)
        print(diff_output)
        sys.exit(1) 

    # Output is just new line separated list of filenames
    files = diff_output.split("\0")

    success = True

    for f in files:

        # Empty newline after list
        if f == "":
            continue

        f = os.path.join(repo_path, f)

        if not os.path.exists(f):
            # Cannot validate files which do not exist
            # Git delete list?
            continue

        # Pass arguments to VVV + add file from commit list
        args = sys.argv[1:-1] + [f]

        # Call VVV for this file
        result = plac.call(main.main, args)

        # Validation failed
        if result != 0:
            success = False


    # Signal git that the fecal has hitted the rotatory device etc.
    if not success:
        sys.exit("VVV validatoin and linting failed")

