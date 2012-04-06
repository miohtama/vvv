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

* Install VVV locally for your cloned Git repository with UNIX shell one-liner. 

* Run VVV as continuous integration service with systems like Travis CI or Jenkins

* Provide sane default validation and liting options for all popular programming languages and file formats

No-goals
==========

* This is not automated testing services. We just scan files for **policy** violations, not for
  programming errors. 

Validation source me

Features
=========

* Set-up for your software repository with two files ``validation-options.yaml`` (pass in options for validators) and ``validation-violations.yaml`` (blacklist)

* Automatically download and install in validator software, no matter whether they are written in Javascript, Java, etc., on demand.  

* Guarantee tab and whitespace policies 

Installation and running
============================

Installing locally
--------------------------------------

`virtualenv based <>` installation is recommended. You create a local Python package repository
where **vvv** and all it dependencies are downloaded from `PyPi <http://pypi.python.org>`_.

Installing prerequisites (Ubuntu)::

	TODO

Installing prerequisites (OSX, `Macports <http://www.macports.org>`_)::

	sudo port install python32 	
	sudo port install py32-distribute
	sudo port install py32-virtualenv

Then create environment e.g. in your home folder::

	# Use Py3.2 - not default Python version which tends to be py2
	cd ~
	virtualenv-3.2 vvv-venv
	source vvv-venv/bin/activate

	easy_install vvv

Running by hand
--------------------------------------

* Go to your source folder::

	cd ~/mycodeproject

* Execute command from your virtualenv::

	~/vvv/scripts/vvv 

Tada. That's it, assuming the sane defaults work for you.

Configuration
--------------------------------------

Configuration files are in your project folder root.

Configuration files are specified in `YAML syntax <http://ess.khhq.net/wiki/YAML_Tutorial>`_.

Configuration options
+++++++++++++++++++++++++

In your project root add ``validation-options.yaml``. If this file does not exist default settings are used as described below. 

``validation-options.yaml`` example::

File whitelisting and blacklisting
++++++++++++++++++++++++++++++++++++++

``validation-violations.yaml`` allows you to flag files for validation or to be ignored.
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

TODO

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

vvv accepts plug-ins as Python eggs. You'll declare plug-in integration points in your egg setup.py ``entry_points`` section.
Then just install your eggs in the same virtualenv with **vvv** and it will automatically pick them up.

Setting up development environment
--------------------------------------

Python 3.2 needed + setuptools + virtualenv needed.

Setting up requirements (OSX, Macports)::

	sudo port install python32 	
	sudo port install py32-distribute
	sudo port install py32-virtualenv

Example::

	# Use Py3.2 - not default Python version which tends to be py2
	virtualenv-3.2 venv
	source venv/bin/activate

Creating plug-in
-------------------

Each entry point is a Python module with certain format.

Other
-----

* `Sphinx function signatures <http://sphinx.pocoo.org/domains.html#signatures>`_

 

	

