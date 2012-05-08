============================
Extend and develop 
============================

.. contents :: :local:

.. highlight:: console

Introduction
============================

VVV is programmed in Python and targets Python 3.2 and newer versions.

.. note ::

    Validators largerly use whatever tools the targe programming language supports and 
    VVV only provides stub modules which execute shell processes
    and then parse output. Not much Python knowledge is needed in order to expand VVV.  

VVV accepts plug-ins as Python eggs. Yo'll declare plug-in integration points in your egg setup.py ``entry_points`` section.
Then just install your eggs in the same virtualenv with VVV and it will automatically pick them up.

Setting up development environment
========================================================

Python 3.2 needed + setuptools + virtualenv needed, as instructed in Installation section.

Setting up VVV in development mode::

    # Fork on Github first, then replace the line below using address to your own repo
    git clone git://github.com/miohtama/vvv.git
    cd vvv
    virtualenv -p python3.2 venv
    source venv/bin/activate
    python setup.py develop
    
    # Set-up precommit hook to lint vvv's own files
    vvv-install-git-pre-commit-hook

Running VVV in development mode against your code repository::

    # Activate virtualenv
    cd vvv
    source venv/bin/activate
    # Run trunk vvv against your repo
    cd ~/repo
    vvv
    
Creating plug-in
============================

Each entry point is a Python module with certain format.

* Fork on GitHub

* Copy existing plug-in .py file as template (``jshint.py`` preferred)

* Add new entry points in setup.py

* Run ``python setup.py develop`` to activate the entry points

* Add test cases in ``tests/validators`` 

* See tests pass

* See VVV code itself passes the validation

* Send merge request

Other
-----

* `Sphinx function signatures <http://sphinx.pocoo.org/domains.html#signatures>`_

Running tests
===========================

To run tests::

    source venv/bin/activate
    cd tests
    python -m unittest discover

To debug further runs without triggering reinstall & download::

    VVV_TEST_SKIP_REINSTALL=true VVV_TEST_OUTPUT=verbose python -m unittest discover

To run a single test / test group you can use a filter which uses substring match against test names::

    VVV_TEST_SKIP_REINSTALL=true VVV_TEST_FILTER=css python -m unittest discover

... or ...::

    VVV_TEST_SKIP_REINSTALL=true VVV_TEST_OUTPUT=verbose VVV_TEST_FILTER=css_simple_pass python -m unittest discover
        
.. note ::

    All slashes and dashes are converted to underscores in test case names.
    
TODO: Use HTTP proxy (polipo) to speed up tests by caching downloads locally.        

Validating code
==========================

Your can self-validate the vvv codebase::

    source venv/bin/activate

    vvv .

Releasing egg
==========================

Use `jarn.mkrelease <http://pypi.python.org/pypi/jarn.mkrelease>`_::

    source PYTHON2-VENV/bin/activate
    easy_install mkrelease
    mkrelease -C -T -d pypi .  

.. note ::
    
    For mkrelease you need to Python 2.x virtualenv.

mkrelease bug::

      File "/Users/moo/code/vvv/venv/lib/python3.2/site-packages/jarn.mkrelease-3.5-py3.2.egg/jarn/mkrelease/mkrelease.py", line 237
        except getopt.GetoptError, e:
                                 ^
    SyntaxError: invalid syntax

Publishing docs
============================

rtfd.org does not seem to support Python 3 auto import modules.

To publish docs on GitHub::

    . venv/bin/activate
    easy_install Sphinx
    sh scripts/publish-docs.sh    
