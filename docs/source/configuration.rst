===================================
 Configuration
===================================

.. contents :: :local:

Introduction
===================================

VVV can be configuredin two ways

* VVV configuration files are in your software project folder are shared between
  the developers of the project (``validation-options.yaml`` and ``validation-files.yaml``)

* VVV command line parameters are specific to each run / integration environment where VVV is executed

Configuration files are specified in `YAML syntax <http://ess.khhq.net/wiki/YAML_Tutorial>`_.

Configuration file
===================================

In your project root add ``validation-options.yaml``. If this file does not exist default settings are used as described below. 

``validation-options.yaml`` example::

    tabs:

        # Disable hard tab rejector for this project
        enable: false

    css:

        hint: Your CSS files did not pass W3C validator. Please see README.txt for project CSS coding conventions.

Available configuration file options
======================================================================

The configuration file has one section per each validator.

Each validator can has its own settings, but there exist some options which are available for each validator.

**Global options**

*enable*: true or false. Default true. Whether globally enable a validator in your project.

*hint*: Helpful message printed user if this validator fails. Can be multiline.

For validator specific options please consult validators manual. 

Example ``validation-options.yaml``::

    tabs:
        enable false

    css:
        enable false

    linelength:
        length: 250      

    jslint:
        hint: This project follows jQuery Core Javascript coding conventions http://docs.jquery.com/JQuery_Core_Style_Guidelines

File whitelisting and blacklisting
===================================

``validation-files.yaml`` allows you to whitelist and blacklist files for validation.
It's main purpose is to ignore files which do not conform your policies 100%.
This is e.g. useful if your source code repository contains third party library files which 
do not inherit your project coding conventions.

The file contains YAML sections which follow `Bazaar ignore path matching rules <http://doc.bazaar.canonical.com/beta/en/user-reference/ignore-help.html>`_.

.. note::

    Unlike with Bazaar path specs are inclusive (list of matched), not exclusive (list of ignored files)

There is one global ``all`` section with blacklist and whitelist and then validator specific sections by the validator id. 

Example ``validation-files.yaml``::

    # Don't match hidden dotted files/folders
    # Don't match generated folders
    # Don't match test data (which is bad intentionally)
    all: | 
      *
      !RE:.*\/\..*|^\..*
      !**/build/**  
      !venv
      !**/__pycache__
      !*.egg-info
      !tests/validators
      !tests/test-installation-environment

    # Sphinx generated conf.py does not pass pylint validation.
    # https://bitbucket.org/birkenfeld/sphinx/issue/909/generated-default-confpy-does-not-pass
    # bzrlib files come from outside the project.
    # expand_tabs come from outside the project
    pylint: |
      *.py
      !docs/source/conf.py
      !vvv/bzrlib/*
      !scripts/expand_tabs.py

    # pdb validator has set_trace() inside strings
    pdb: |
      *.py
      !vvv/validators/pdb.py


    # Include all text files, ignore hard tab checking for Makefiles
    tabs:
        *
        !Makefile
        !*.mk

Validators won't try to process binary files.

More info

* http://kashfarooq.wordpress.com/2009/09/15/ignoring-files-and-folders-with-bazaar-source-control/


