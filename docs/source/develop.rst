============================
Extend and develop 
============================

.. contents :: :local:

Introduction
============================

vvv is programmed in Python and targets Python 3.2 and newer versions.

.. note ::

    Validators largerly use whatever tools the targe programming language supports and 
    VVV only provides stub modules which execute shell processes
    and then parse output. Not much Python knowledge is needed in order to expand VVV.  

vvv accepts plug-ins as Python eggs. Yo'll declare plug-in integration points in your egg setup.py ``entry_points`` section.
Then just install your eggs in the same virtualenv with **vvv** and it will automatically pick them up.

Setting up development environment
========================================================

Python 3.2 needed + setuptools + virtualenv needed, as instructed in Installation section.

Setting up VVV in development mode::

    source venv/bin/activate
    python setup.py develop

Running VVV in development mode::

    source venv/bin/activate
    cd ~/repo
    vvv
    
Creating plug-in
============================

Each entry point is a Python module with certain format.

See ``plugin.py`` for more information.

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

    VVV_TEST_REINSTALL=false VVV_TEST_OUTPUT=verbose python -m unittest discover