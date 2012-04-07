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

* This is not automated testing services. We just scan files for **policy** files, not for
  programming errors. For this, use proper unit testing facilities.

Features
=========

* Set-up for your software repository with two files ``validation-options.yaml`` (pass in options for validators) and ``validation-files.yaml`` (blacklist)

* Automatically download and install in validator software, no matter whether they are written in Javascript, Java, etc., on demand.  

* Guarantee tab and whitespace policies 

Documentation
===============

Please see the `VVV documentation on readthedocs.org <http://foobar>`_



    

