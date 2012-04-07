=============================
VVV - Very Valid Versioning 
=============================

VVV provides easy to integrate validation and linting tools to prevent bad stuff committed in your software project.

VVV is designed to be used with Github and Travis CI (simple setup), 
but will work with other version control systems (more complex setup).

.. contents :: :local:

Benefits
=========

* Prevent people (accidentally) committing files which do not comply project coding conventions and policies.
  Automatically guide committers to the policy guidelines and let them fix errors themselves, instead of having
  post-commit personal coaching.

* Install for your project code repository with UNIX shell one-liner

* Provide sane default validation and linting options for all popular programming languages and file formats

* Run VVV as continuous integration service with systems like Travis CI or Jenkins and shoot down bad code push ins

What vvv doesn't do

* This is not automated testing services. We just scan files for **policy** violations, not for
  programming errors. For this, use proper unit testing facilities.

Features
=========

* Set-up for your software repository with two files ``validation-options.yaml`` (pass in options for validators) and ``validation-violations.yaml`` (blacklist)

* Automatically download and install in validator software, no matter whether they are written in Javascript, Java, etc., on demand.  

* Guarantee tab and whitespace policies 

Installation and running
============================

Prerequisites
----------------

Runs on OSX and Linux. Windows is not (yet) supported. 
Requires Python 3 environment to run. 

Installing locally
--------------------------------------

`virtualenv based <>` installation is recommended. You create a local Python package repository
where **vvv** and all it dependencies are downloaded from `PyPi <http://pypi.python.org>`_.

Installing prerequisites (Ubuntu)::

    TODO

Installing prerequisites (OSX, `Macports <http://www.macports.org>`_)::

    sudo port install python32  
    sudo port install py32-distribute py32-virtualenv py32-pip

Then create environment e.g. in your home folder::

    # Use Py3.2 - not default Python version which tends to be py2
    cd ~
    virtualenv-3.2 vvv-venv
    source vvv-venv/bin/activate

    easy_install vvv

Running 
--------------------------------------

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
--------------------------

Please use ``--help`` switch to see up-to-date command line help::

    ~/vvv-venv/bin/vvv --help

Configuration
--------------------------------------

Configuration files are in your project folder root.

Configuration files are specified in `YAML syntax <http://ess.khhq.net/wiki/YAML_Tutorial>`_.

Configuration file
+++++++++++++++++++++++++

In your project root add ``validation-options.yaml``. If this file does not exist default settings are used as described below. 

``validation-options.yaml`` example::

    tabs:

        # Disable hard tab rejector for this project
        enable: false

    css:

        hint: Your CSS files did not pass W3C validator. Please see README.txt for project CSS coding conventions.


Available configuration file options
++++++++++++++++++++++++++++++++++++++++++++++++++

The configuration file has one section per each validator.

Each validator can has its own settings, but there exist some options which are available for each validator.

**Global options**

*enable*: true or false. Default true. Whether globally enable a validator in your project.

*hint*: Helpful message printed user if this validator fails. Can be multiline.

For validator specific options please consult validators manual. 

File whitelisting and blacklisting
++++++++++++++++++++++++++++++++++++++

``validation-violations.yaml`` allows you to flag files for going for validation or to be ignored.
It's main purpose is to ignore files which do not conform your policies 100%.
This is e.g. useful if your source code repository contains third party library files which 
do not inherit your project coding conventions.

The file contains path specs which follow `.gitignore regex rules <http://linux.die.net/man/5/gitignore>`_ matching guidelines.

There is one global ``all`` section with blacklist and whitelist and then validator specific sections by the validator id. 

Example::

    all:
        whitelist: 
            *
        blacklist:  
            .svn
            .git
            .DS_Store
            *.egg-info
            .metadata

    css:
        whitelist:
            *.css

The order of rules

* Global blacklist (ignore version control, metadata, etc. folders by default)

* Global whitelist (all files by default)

* Validator specific blacklist

* Validator specific whitelist (e.g. *.css files for CSS validator)

Validators won't try to process binary files.

Integrating with local Git repository
--------------------------------------

Here are instructions how to set-up pre-commit hook with Git.
This prevents you to commit files violating policy.

If you have a local installation using virtualenv::

    cd ~/yourprojectrepo
    ln -s hooks/pre-commit/vvv ~/vvv-virtualenv/scripts/git-pre-commit-hook

More info 

* http://book.git-scm.com/5_git_hooks.html

Integrating with Travis CI
--------------------------------------

TODO

Coding conventions guide
========================================================

Example coding conventions
--------------------------------------

* http://docs.jquery.com/JQuery_Core_Style_Guidelines

Validation facilities
--------------------------------------

* `JSHint <http://www.jshint.com/>`_

* `JSLint <http://www.jslint.com/>`_

* `W3C CSS validator <http://jigsaw.w3.org/css-validator/DOWNLOAD.html>`_

Developing
============================

Extending
--------------------------------------

vvv accepts plug-ins as Python eggs. Yo'll declare plug-in integration points in your egg setup.py ``entry_points`` section.
Then just install your eggs in the same virtualenv with **vvv** and it will automatically pick them up.

Setting up development environment
--------------------------------------

Python 3.2 needed + setuptools + virtualenv needed, as instructed in Installation section.

Setting up VVV in development mode::

    source venv/bin/activate
    python setup.py develop

Running VVV in development mode::

    source venv/bin/activate
    cd ~/repo
    vvv
    

Creating plug-in
-------------------

Each entry point is a Python module with certain format.

See ``plugin.py`` for more information.

Other
-----

* `Sphinx function signatures <http://sphinx.pocoo.org/domains.html#signatures>`_

 

    

