===================================
 Running and integration 
===================================

.. contents :: :local:

Introduction 
===================================

VVV will run and try to download, detects validators by filetype
in your source code repository and will try to download
needed validators automatically if they are not installed.
Installation is on-demand - if your project does not 
contain PHP files no PHP validator will be installed.

However sometimes automatic installation is little bit
tricky in which case yo'll get an error message 
with a link to friendly installation instructions for a specific validator.

Running by hand
==================

Here are instructions how to execute VVV in your 
project folder manually.

* Go to your source folder::

    cd ~/mycodeproject

* Execute command from your virtualenv::

    ~/vvv/scripts/vvv 

Tada. That's it, assuming the sane defaults work for you.

Command line options
===================================

Please use ``--help`` switch to see up-to-date command line help::

    ~/vvv-venv/bin/vvv --help

Integrating with Git 
===================================

Local repository
------------------

Here are instructions how to set-up pre-commit hook with Git.
This prevents you to commit files violating policy.

If you have a local installation using virtualenv::

    cd ~/yourprojectrepo
    ln -s hooks/pre-commit/vvv ~/vvv-virtualenv/scripts/git-pre-commit-hook

More info 

* http://book.git-scm.com/5_git_hooks.html

Integration with Subversion
===================================

Integrating with Travis CI
===================================

TODO