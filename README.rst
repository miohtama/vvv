========================================
VVV - validation and linting integrator
========================================

VVV is a tool for easy validation and linting integration for your software project
containing multiple kinds of files. It integrates with version control and
prevents committing files containing bad formatting or syntax errors.

An example use case would be a web project containing HTML, CSS, Javascript
and backend programming language files: with VVV you can check with a single command
all files conform the policy you set.

.. contents :: :local:

Usage
==============

Example output from validating the demo repository where we find errors in a Python and a CSS file.
You enter the folder and run ``vvv`` against the current folder (``.``) ::

    $ vvv .
    Running vvv against .
    /Users/moo/code/vvv/demo/demo.py validation output:
    ************* Module demo
    E0602:  1,9: Undefined variable 'get_magic'

    W3C CSS Validator results for file:/Users/moo/code/vvv/demo/foobar.css

    Line : 2 .foo
           Property backgrnd doesn&#39;t exist :
           yellow


Installation
==============

VVV is writte in in `Python <http://www.python.org>`_ programming language and is compatible with
**Python interpreter 2.7 or later, including 3.x series**.

Installating instructions for `Windows <http://miohtama.github.com/vvv/installation.html#windows>`_ -
`Linux <http://miohtama.github.com/vvv/installation.html#linux-ubuntu-debian>`_ -
`OSX <http://miohtama.github.com/vvv/installation.html#osx>`_.

Benefits
=========

* Enforce coding conventions across multiple developers

* Enable linting and validators support for your software project with a single command

* Automatically guide committers to policy guidelines and let them fix errors themselves, instead of having
  post-commit personal coaching.

* Provide sane default validation and linting options for all popular programming languages and file formats

* Run VVV as continuous integration service with systems like Travis CI or Jenkins and shoot down bad code push-ins

What VVV doesn't do

* This is not automated testing tool. We just scan files against a **policy**, not for
  programming errors. Linting tools tend to pick up programming errors, too though,
  like mistyped names.

Features
=========

* Set-up for your software repository with two files ``validation-options.yaml`` (configuration) and ``validation-files.yaml`` (whitelist/blacklist)

* VVV automatically downloads and locally installs required software - you don't need to spend time hunting downloads or distribution packages

* Check file against hard tabs and whitespace policies - no more different tab width ever

* Prevent committing hard source code breakpoints, like Python's ``import pdb ; pdb.set_trace()``

* Support (on its way) for Subversion, Git, Github, Travis CI, Jenkings and other popular version control and continuous integration
  systems

Documentation and code
=========================

Please see the `VVV documentation <http://miohtama.github.com/vvv/>`_.

`Source code is available on Github <https://github.com/miohtama/vvv>`_. Please use Github issue tracker
to contact the authors.

Explore different `linting and validators available <http://miohtama.github.com/vvv/validators.html>`_.

Continuous integration status
================================

Current trunk continuous integration status with Travis CI

.. image :: https://secure.travis-ci.org/miohtama/vvv.png

Author
===============

Mikko Ohtamaa (`blog <http://opensourcehacker.com>`_, `Twitter <http://twitter.com/moo9000>`_)

Please use Github issue tracker to contact the authors in the project related matters.



