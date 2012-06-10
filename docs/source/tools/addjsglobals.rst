========================================================
Batch add Javascript global hints
========================================================

.. contents :: :local:
 :depth: 2

Introduction
-------------

VVV package provides command ``vvv-add-js-globals`` which can be used to 
batch add ``/* global */`` hints to Javascript files.
The tool is designed to situations where you adapt linting practices
to your project and several JS files are in dire need of updating.

.. image:: /images/globals.png

Above is an example screenshot of a sad, but normal situtation when adapting a linter. 
`However, the situation is was not incurable <https://github.com/miohtama/Krusovice/commit/87e81fe8efce2a0e93de534fde8599600080b847>`_.

``vvv-add-js-globals``:

* Supports jslint / jshint syntax

* Adds globals line to files where it does not exist

* Retrofits new globals to existing globals line

.. warning ::

    Use carefully. The tool operates on text lines only and does not
    parse Javascript. It may break Javascript files if used

Usage
--------

Use with ``find`` UNIX command.

Active VVV virtualenv first::

    . ~/vvv-venv/bin/activate

Example how to scan the current source tree add add ``/* globals jQuery, $ */`` in every file::

    find . -iname "*.js" | xargs vvv-add-js-globals "$, jQuery" 

Another example - add console global to all JS files under tests::

    find tests -iname "*.js" -print  -exec vvv-add-js-globals "console" {} \;  

Another example - add console global to all JS files in the source tree, but exclude files in thirdparty/ folder::

    find . -iname "*.js" -not -path "*thirdparty*"  -print  -exec vvv-add-js-globals "console" {} \;  