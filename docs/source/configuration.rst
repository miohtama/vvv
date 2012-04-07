===================================
 Configuration
===================================

.. contents :: :local:

Introduction
--------------------------------------

VVV can be configuredin two ways

* Configuration files are in your project folder are shared between
  all the developers and tell what validation policies your project has

* VVV command line parameters are specific to each run / integration environment where VVV is executed

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

``validation-files.yaml`` allows you to flag files for going for validation or to be ignored.
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

* Validator specific whitelist (e.g. \*.css files for CSS validator)

Validators won't try to process binary files.



