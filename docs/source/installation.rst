Installation
============================

.. contents :: :local:

.. highlight:: console

Prerequisites
----------------

Python 2.7 or higher, including Python 3.x series.

For individual validators you might need to configure :doc:`Java or NodeJS </prerequisites>`.
Further information available after the installation.

Installing VVV using virtualenv
--------------------------------------

`virtualenv based <http://pypi.python.org/pypi/virtualenv>`_ installation is recommended.

virtualenv is a tool to manage self-contained Python software installations without
need for super-user priviledges.

Windows
+++++++++

Tested on Windows 7 with Python 2.7

Make sure ``virtualenv`` is installed::

    pip install virtualenv

Installing prerequisites by creating vvv-venv virtualenv in your home folder::

    cd %HOME%
    virtualenv vvv-venv
    .\venv-vvv\Scripts\activate
    pip install vvv

Or if you are using PowerShell::

    cd ~
    virtualenv vvv-env
    .\venv-vvv\Scripts\activate.ps1
    pip install vvv

Linux (Ubuntu / Debian)
++++++++++++++++++++++++++

Tested on Ubuntu 10.04 and should work on are later versions.

Installing prerequisites by creating ``vvv-venv`` virtualenv in your home folder::

    sudo apt-get install python-virtualenv
    # Please enter the following commands as non-root user
    cd ~
    virtualenv vvv-venv
    . ./vvv-venv/bin/activate
    pip install vvv

.. note ::

    Red Hat, CentOS users can adapt these instructions for
    your own package manager. If you are using VVV on these platforms
    please contact the author via issue tracker to provide exact
    installation instructions.

OSX
+++++++++

OSX 10.7 Lion or later comes with compatible Python 2.7.

To install VVV into a current folder::

    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py vvv-venv
    . vvv-venv/bin/activate
    pip install vvv

For older OSX versions you might need to use a package manager
like `Macports <http://www.macports.org>`_ to install a compatible
Python interpreter::

    sudo port install python32
    sudo port install py32-distribute py32-virtualenv py32-pip

Running
---------

VVV is installed under virtualenv. When you *activate* this virtualenv
your command-line *PATH* environment variable is modified so that
the active command line session starts using commandss from virtualenv.

This must be done once per each command line session.

To activate virtualenv under UNIX::

    . vvv-venv/bin/activate

To activate virtualenv under Windows::

    .\venv-vvv\Scripts\activate

Now when the virtualenv is active you have ``vvv`` command available.
Type it to see the command line help text::

    vvv

Now you can test ``vvv`` against your source tree.
Just ``cd`` to the any source tree and type in the command::

    vvv .

VVV will validate your source code.

From here you can proceed to :doc:`configuring VVV for your project </configuration>`,
to make VVV to conform your project policy.

Installing trunk version
--------------------------

If you want to use GitHub trunk version do::

    . ~/vvv-venv/bin/activate
    git clone git://github.com/miohtama/vvv.git
    cd vvv
    python setup.py develop

This will install vvv development version under ``vvv-venv`` virtualenv.

Software downloaded and installed by vvv command
----------------------------------------------------

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



