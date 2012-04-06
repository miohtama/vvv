=============================
VVV - Very Valid Versioning 
=============================

VVV provides prepackaged validation and linting tools which are simple to install and integrate with software versiong control.

VVV is designed to be used with Github and Travis CI (simple setup), 
but will work with other version control systems (more complex setup).

.. contents :: :local:

Goals
======

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

Insllation and running
============================

Installation locally
--------------------------------------

Running by hand
--------------------------------------

Configuration
--------------------------------------

Validation options
--------------------

In your project root add ``validation-options.yaml``. If this file does not exist default settings are used as described below. 

Integrating with local Git repository
--------------------------------------

TODO

Integrating with Travis CI
--------------------------------------

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

Each entry point is a Python module with certain format.

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

Other
-----

* `Sphinx function signatures <http://sphinx.pocoo.org/domains.html#signatures>`_

 

	

