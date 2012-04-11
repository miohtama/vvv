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

`Travis CI <http://about.travis-ci.org/>`_ is continuous integration and build service
which is free for open source projects to use.

VVV and Travic CI can be very easily integrated to your project:

* Travis CI will automatically run after you commit changes to your project on Github 
  (as the writing of thisGithub is the only supported VCS)

* Travis CI will run VVV validation checks against your source code and reports possible violations.
  Note that this does not prevent bad commits - you will just get notification afterwards
  when bad stuff got in from the door already. But it's still much better than running
  validations, linting and tests by hand.

.. note ::

    You don't need to install any software or set-up any infrastructure. Travis CI
    is provided free software-as-a-service for open source projects and all you 
    need to do this to register in Travis CI and drop one file in your
    public source code repository.

All you need to do is to

* Login to `travis-ci.org <http://travis-ci.org/>`_ using your Github credentials

* Turn on Travis for your repository - Travis will automatically list all your Github projects

* Then visit the GitHub service hooks page for that project and paste your GitHub username and 
  Travis token into the settings for the Travis service if it is not already pre-filled. 
  (should not be needed unless your repo belongs to Github organization)

* Drop ``.travis.yml`` having the option to run VVV in your repository root (example below) 

* Drop ``validation-options.yaml`` and ``validation-files.yaml`` policies in your repository root (optional, but you most likely want to tune validation error levels)

* You can also `include automatically generated status image to your Github README <http://about.travis-ci.org/docs/user/status-images/>`_

* After you push in ``.travis.yml`` for the first time it will trigger the build which you can 
  see on `travis-ci.org <http://travis-ci.org/>`_ *My Repositories* tab. It should appear there in seconds. 

Example ``.travis.yaml`` using the latest VVV release from `pypi.python.org <http://pypi.python.org>`_::

    language: python

    python:
      - "3.2"

    # command to install dependencies
    # - because we validate ourselves this is special
    install:
      - pip install vvv --use-mirrors

    # command to run tests
    script: vvv .

Example ``.travis.yml`` using the latest `VVV trunk from Github <https://github.com/miohtama/vvv>`_::

    language: python

    python:
      - "3.2"

    # command to install dependencies
    # - because we validate ourselves this is special
    install:
      - pip install git://github.com/miohtama/vvv.git

    # command to run tests
    script: vvv .

.. note ::

    Travis CI uses .yml extension, VVV uses .yaml extension. VVV is better.

More info

* http://about.travis-ci.org/docs/user/getting-started/

* http://about.travis-ci.org/docs/user/build-configuration/

* https://github.com/travis-ci/travis-lint
