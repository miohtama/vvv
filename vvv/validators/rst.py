"""

Restructred Text (rst)
=======================

Validator name: ``rst``

Check that .rst files do not contain syntax errors using `docutils <http://docutils.sourceforge.net//>`_.
Restructured format is used by `Sphinx documentatio tool <http://sphinx.pocoo.org/>`_ and 
also supported by Github README files.

.. note ::

    Unknown restructured directives errors are ignored, mainly because systems like Sphinx
    add their own directives.

Installation
----------------

Works out of the box.

Supported files
----------------

* \*.rst

Options
-----------

python3k
++++++++++++

If true set-up pylint for Python 3.x. The default is Python 2.x.

.. note ::

    If you change this you need run ``vvv --reinstall``.


More information
----------------

* https://github.com/miohtama/vvv/blob/master/vvv/scripts/validaterst.py

"""
import os

from vvv.plugin import Plugin

from vvv import sysdeps

#: Command-line options given to jshint always
DEFAULT_COMMAND_LINE = ""

class RestructuredTextPlugin(Plugin):
    """
    docutils driver.

    Install docutils in a virtualenv and then call vvv supplied script to run the validation.
    """            

    def __init__(self):
        Plugin.__init__(self)

        #: Path to the virtual env location
        self.virtualenv = None

        #: Location of virtualenv.py if operating system cannot supply working one
        self.virtualenv_cmd = None

        #: Configuration file option
        self.python3k = None

    def setup_local_options(self):
        """ """
        if not self.hint:
            self.hint = "Restructed text files contained errors"

        self.virtualenv_cmd = os.path.join(self.installation_path, "virtualenv.py")

        self.python3k = self.options.get_boolean_option(self.id, "python3k", False)

        #: Path to the virtual env location,
        # vary by Python version so we don't get conflicting envs
        self.virtualenv = os.path.join(self.installation_path, "docutils-virtualenv-{}".format("python3k" if self.python3k else "python2"))

    def get_default_matchlist(self):
        """
        These files require hard tabs
        """
        return [
            "*.rst",
        ]

    def check_requirements(self):
        sysdeps.has_virtualenv(needed_for="RestructuredText docutils validation")

    def check_is_installed(self):
        """
        See if we have installed working virtualenv for docutils
        """
        has_created_virtualenv =  os.path.exists(self.virtualenv)
        return has_created_virtualenv

    def install(self):
        """
        """
        self.logger.info("Installing %s" % self.virtualenv)
        sysdeps.create_virtualenv(self.logger, self.virtualenv_cmd, self.virtualenv, egg_spec="docutils==0.8.1", py3=self.python3k)
#        sysdeps.run_virtualenv_command(self.logger, self.virtualenv, "easy_install Pygments", raise_error=True)

    def validate(self, fname):
        """
        Run .rst against our custom validation script.
        """

        binloc = os.path.join(sysdeps.get_bin_path(), "vvv-validate-rst")

        exitcode, output = sysdeps.run_virtualenv_command(self.logger, self.virtualenv, "%s %s" % (binloc, fname))

        if exitcode != 0:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False

        return True


