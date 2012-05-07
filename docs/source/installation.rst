Installation 
============================

.. contents :: :local:

.. highlight:: console

Prerequisites
----------------

Runs on OSX and Linux. Windows is not (yet) supported. 
Requires Python 3 environment to run. 

Installing locally using virtualenv
--------------------------------------

`virtualenv based <http://pypi.python.org/pypi/virtualenv>`_ installation is recommended. 
virtualenv is a tool to manage self-contained Python software installations without
need to install Python packages in your system folders using super-user priviledges.
Becuse VVV is still much in development, this kind of installation allows
fast update cycles without messing with system files or distribution packages.

This creates a local Python package repository
where VVV and all it dependencies are downloaded from `PyPi <http://pypi.python.org>`_.

Ubuntu
+++++++++

Tested on Ubuntu 10.04 and should work on are later versions. 

Installing prerequisites by creating ``vvv-venv`` virtualenv in your home folder::

    sudo apt-get install python3 python3-setuptools 
    # Please enter the following commands as non-root user 
    cd ~
    wget "https://raw.github.com/pypa/virtualenv/master/virtualenv.py"
    python3 virtualenv.py vvv-venv
    source vvv-venv/bin/activate
    pip install vvv

.. note ::

    Later Ubuntus may provide virtualenv package directly for Python 3 and
    you do not need to wget anything. 
    When writing of this it was not the case.

OSX
+++++++++

Installing prerequisites (OSX, `Macports <http://www.macports.org>`_)::

    sudo port install python32  
    sudo port install py32-distribute py32-virtualenv py32-pip

Then create environment e.g. in your home folder::

    # Use Py3.2 - not default Python version which tends to be py2
    cd ~
    virtualenv-3.2 vvv-venv
    source ~/vvv-venv/bin/activate
    pip install vvv

Running 
++++++++++

Now when virtualenv is active (activated with the ``source`` command above), your ``PATH``
environment variable pulls in ``vvv`` command from that folder::

    source ~/vvv-venv/bin/activate # Do once per shell session
    # See that we get command line help
    vvv    

Just ``cd`` to the any source tree and type in the command::
    
    vvv .

VVV will validate your source code.

Now you can proceed to :doc:`configuring VVV for your project </configuration>`,
to get rid of those pesky validation errors.

Installing trunk version
++++++++++++++++++++++++++++

If you want to use GitHub trunk version do::

    source ~/vvv-venv/bin/activate
    git clone git://github.com/miohtama/vvv.git
    cd vvv
    python setup.py develop

This will install vvv development version under ``vvv-venv`` virtualenv.

Automatically pulled in software
--------------------------------------

Each target programming language may require its own system-wide
dependencies before you can run the validtor.

You'll get an error message when running VVV if you are lacking something.
If you get such an error for more information installing 
the dependencies please see :doc:`prerequisites </prerequisites>`. 

vvv will automatically try to install software needed to run the
validator. This software is installed locally in hidden ``.vvv``
folder in your home folder.

In the case this installation becomes damaged e.g.
because you interrupt download and configuration with CTRL+C
you can always recreate all downloaded files with the folllowing command::

    vvv --reinstall .



