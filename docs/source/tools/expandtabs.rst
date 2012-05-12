========================================================
Expand tabs
========================================================

.. contents :: :local:
 :depth: 2

Introduction
-------------

VVV package provides command ``vvv-expand-tabs`` command
to batch convert text files to use spaces (soft tabs) instead of hard tabs.
It provides in-place replacement, so it can be easily used against source trees.

Usage
--------

Use with ``find`` UNIX command.

Active VVV virtualenv first::

    . ~/vvv-venv/bin/activate

With ``find`` and ``xargs`` you can easily convert the whole project 
tree away from hard tabs. Use ``--tabsize`` command line argument to tell what kind of hard tab size the source files where using::

    
    # Find all ascii files and convert them to use tabs,
    # but watch out not to hit Makefile or any other file needing hard tabs!
    find . -name "*" -type f -print | xargs file | grep ASCII | cut -d: -f1 | xargs vvv-expand-tabs --inplace --tabsize=4 

.. note ::

    Since the modification is done in-place back-up your files first.

You can also try UNIX ``expand`` command, but it does not supports in-place conversion.
