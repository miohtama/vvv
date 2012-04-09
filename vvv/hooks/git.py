"""

    Git commit hook integration.

    http://book.git-scm.com/5_git_hooks.html

"""
import os
import sys
import stat

from vvv import sysdeps

PRECOMMIT_HOOK_TEMPLATE = """#!/bin/sh
%s
"""

def get_vvv_command():
    return sysdeps.which("vvv")

def setup_hook():
    """ 
    Install git precommit hook.
    """

    command = get_vvv_command()
    if not command:
        print("Cannot find vvv command")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Please give a path as argument")
        sys.exit(1)     

    path = sys.argv[1]

    if not os.path.exists(os.path.join(path, ".git")):
        print("Not a git repo: %s" % path)
        sys.exit(1)

    path = os.path.abspath(path)
    
    cmdline = "%s %s" % (command, path)    

    precommit = os.path.join(path, ".git", "hooks", "precommit")

    if os.path.exists(precommit):
        print("Precommit hook already exists: %s" % precommit)
        print("Manually add in the command:")
        print(cmdline)
        sys.exit(1)

    hook = PRECOMMIT_HOOK_TEMPLATE % cmdline
    
    f = open(precommit, "wt")
    f.write(hook)
    f.close()

    # Make hook executable
    mode = os.stat(precommit).st_mode
    mode += stat.S_IXOTH + stat.S_IXGRP + stat.S_IXUSR
    os.chmod(precommit, mode)

    print("Installed git precommit hook %s" % precommit)
    sys.exit(0)
        
