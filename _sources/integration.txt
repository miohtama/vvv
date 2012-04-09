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

In the case validators cannot be automatically installed due to system 
dependencies (e.g. Java) you'll get an error message 
with a link to friendly installation instructions for a specific validator.

Automatically installed files
====================================

By default, :doc:`VVV keeps automatically downloaded </installation>`
software in hidden ``.vvv`` folder. You can override
the folder location with a command line switch.

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

If you have :doc:`a local installation using virtualenv </installation>`::

    # Activate the virtualenv
    source ~/vvv-venv/bin/activate

    # Run pre-commit hook installation
    vvv-install-git-pre-commit-hook

After this git will run vvv for all local commits and aborts
the commit if the incoming files contain validation errors.

.. note ::

    Currently vvv does not optimize and check only commited files.
    This will be future feature.    

More info 

* http://book.git-scm.com/5_git_hooks.html

Integration with Subversion
===================================

Local hook
------------------

``svn`` client-side command does not offer a way to execute hooks.
You can probably work around this with ``alias svn``
but I have not yet figured out how.

* `SVN client side options <http://svnbook.red-bean.com/en/1.7/svn.advanced.confarea.html>`_

Server-side hook
------------------

Subversion server allows you to install pre-commit hook which runs code
checks on the server when the client pushes in a potential commit.

TODO

Integrating with Travis CI
===================================

TODO