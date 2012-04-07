Installation 
============================

.. contents :: :local:

Prerequisites
----------------

Runs on OSX and Linux. Windows is not (yet) supported. 
Requires Python 3 environment to run. 

Installing locally
--------------------------------------

`virtualenv based <http://pypi.python.org/pypi/virtualenv>` installation is recommended. 
virtualenv is a tool to manage self-contained Python software installations without
need to install Python packages in your system folders using super-user priviledges.

You create a local Python package repository
where VVV and all it dependencies are downloaded from `PyPi <http://pypi.python.org>`_.

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
