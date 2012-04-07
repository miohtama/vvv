"""

Python (pylint)
====================

Validator name: ``pylint``

Validate Python files against Pylint.

Installation
----------------

A temporarily *virtualenv* environment is automatically created
where pylint command and its dependencies are is installed. 

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

    def check_install(self):
        """
        See if the last file is downloaded and extracted
        """
        sysdeps.virtualenv_exists(self.virtualenv)

    def check_requirements(self):
        sysdeps.has_virtualenv(needed_for="Pylint validator")

    def install(self):
        """
        Download & install the validator app.
        """
        sysdeps.create_virtualenv(self.logger, self.virtualenv, "pylint==0.25.1")

    def validate(self, fname):
        """
        Run installed pylint validator against a file.
        """
        sysdeps.run_virtualenv_command(self.logger, self.virtualenv, 'pylint "%s"' % fname)
