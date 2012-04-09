"""

Restructred Text (rst)
=======================

Validator name: ``rst``

Check that .rst files do not contain syntax errors using `docutils <http://docutils.sourceforge.net//>`_.

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

None.


"""
import os

from vvv.plugin import Plugin

from vvv import utils
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

    def setup_local_options(self):
        """ """
        if not self.hint:
            self.hint = "Restructed text files contained errors"

        self.virtualenv = os.path.join(self.installation_path, "docutils-virtualenv")

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
        return os.path.exists(self.virtualenv)

    def install(self):
        """
        """
        sysdeps.create_virtualenv(self.logger, self.virtualenv, egg_spec="docutils==0.8.1")

    def validate(self, fname):
        """
        Run installed jshint against a file.
        """

        exitcode, output = sysdeps.run_virtualenv_command(self.logger, self.virtualenv, "vvv-validate-rst %s" % fname)
        
        if exitcode != 0:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False

        return True


