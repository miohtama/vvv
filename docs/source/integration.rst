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

Automatically installed files
====================================

By default, VVV keeps automatically downloaded 
validator binaries in hidden
``.vvv`` folder in your project root. You can override
this setting with command line switches.

Also use ``--reinstall`` option as described below
to purge and reinstall files in this folder if needed.

Running by hand
==================

Here are instructions how to execute VVV in your 
project folder manually.

* Go to your source folder::

    cd ~/mycodeproject

* Execute command from your virtualenv::

    vvv 

Tada. That's it, assuming the sane defaults work for you.

Command line options
===================================

Please use ``--help`` switch to see up-to-date command line help::

    vvv --help

Important command line options    
------------------------------------

Reinstall - download and reinstall all automatically
installed software in the case you had to abort the previous run
and incomplete files 

Verbose - output a lot of troubleshooting information::

	vvv -v

Reinstall - reinstall all automatically downloaded files in ``.vvv`` folder::

	vvv --reinstall	

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

TODO

Integrating with Travis CI
===================================

TODO