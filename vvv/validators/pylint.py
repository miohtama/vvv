"""

Python (pylint)
====================

Validator name: ``pylint``

Validate Python files against Pylint.

Installation
----------------

A temporarily *virtualenv* environment is automatically created
where pylint command and its dependencies are is installed. 

.. warning ::

    Currently Pylint is in horribly broken state. You MUST 
    use Python 2.7 and corresponding virtualenv command to install it.

Supported files
----------------

* \*.py

Options
-----------

No options.

More info
------------

* http://pypi.python.org/pypi/pylint

* http://www.logilab.org/card/pylint_manual

"""

# Python imports
import os
from collections import OrderedDict

# Local imports
from vvv.plugin import Plugin
from vvv import utils 

from vvv import sysdeps
from vvv import download

class PylintPlugin(Plugin):
    """
    """

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = utils.get_string_option(self.options, self.id, "options", None)

        if not self.hint:
            self.hint = "Python source code did not pass Pylint validator http://www.logilab.org/card/pylint_manual"

        #: Path to the virtual env location
        self.virtualenv = os.path.join(self.installation_path, "pylint-virtualenv")

    def get_default_matchlist(self):
        """
        These files go into the validator.
        """
        return [
            "*.py",
        ]

    def check_is_installed(self):
        """
        See if we have installed working virtualenv for pylint
        """
        exists = os.path.exists(os.path.join(self.virtualenv, "bin", "pylint"))

        self.logger.debug("Pylint virtualenv status: %s" % "good" if exists else "bad")
        return exists

    def check_requirements(self):
        sysdeps.has_virtualenv(needed_for="Pylint validator")

    def install(self):
        """
        Download & install the validator app.

        ARGFADSFASF WHY *"#€"#€" NOTHING CANNOT WORK IN THIS WORLD?

        http://www.logilab.org/82417

        http://comments.gmane.org/gmane.comp.python.logilab/1193
        """

        pkg = "pylint-0.25.1"

        python = "python2.7"
        easy_install = "easy_install"

        sysdeps.create_virtualenv(self.logger, self.virtualenv, py3=False)

        # Extract and download manually
        pylint_download_path = os.path.join(self.installation_path, "pylint-extract.tar.gz")
        pylint_extract_path = os.path.join(self.installation_path, "pylint-extract", pkg)
 
        download.download_and_extract_gz(self.logger, pylint_download_path, "http://pypi.python.org/packages/source/p/pylint/pylint-0.25.1.tar.gz")

        sysdeps.run_virtualenv_command(self.logger, self.virtualenv, "easy_install logilab-common", raise_errors=True)
        sysdeps.run_virtualenv_command(self.logger, self.virtualenv, "easy_install logilab-astng", raise_errors=True)
        sysdeps.run_virtualenv_command(self.logger, self.virtualenv, "cd %s ; NO_SETUPTOOLS=1 %s setup.py install --no-compile" % (pylint_extract_path, python), raise_errors=True)

    def validate(self, fname):
        """
        Run installed pylint validator against a file.
        """
        exitcode, output = sysdeps.run_virtualenv_command(self.logger, self.virtualenv, 'pylint "%s"' % fname)

        if exitcode == 0:
            return True # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False


