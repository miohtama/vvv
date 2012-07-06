"""

Python (pep8)
====================

Validator name: ``pep8``

"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Python imports
import os

# Local imports
from vvv.plugin import Plugin
from vvv import utils

from vvv import sysdeps
from vvv import download

DEFAULT_COMMAND_LINE = ""

DEFAULT_CONFIG = """

"""


class PEP8Plugin(Plugin):
    """
    PEP8 driver.
    """

    def __init__(self):

        Plugin.__init__(self)

        #: Configuration file option
        self.extra_options = None

        #: Virtualenv path used to run pep8
        self.virtualenv = None

        #: Configuration file option
        self.python3k = None

        #: Configuration file option
#        self.pep8_configuration = None

        #: Configuration file option
        self.host_python = None

        #: Configuration file option
        self.pep8_command = None

        #: Location of virtualenv.py if operating system cannot supply working one
        self.virtualenv_cmd = None

    def setup_local_options(self):
        # Extra options passed to the validator
        self.extra_options = self.options.get_string_option(self.id, "command-line", DEFAULT_COMMAND_LINE)

#        self.pep8_configuration = self.options.get_string_option(self.id, "configuration", "")

        if not self.hint:
            self.hint = "Python source code did not pass PEP8 validator. Please fix issues or disable warnings in .py file itself or validation-options.yaml file."

        self.virtualenv_cmd = os.path.join(self.installation_path, "virtualenv.py")

        self.python3k = self.options.get_boolean_option(self.id, "python3k", False)

        self.host_python = self.options.get_boolean_option(self.id, "host-python-env", False)

        pep8_command = self.options.get_string_option(self.id, "pep8-command", None)

        self.pep8_command = self.resolve_pep8(pep8_command)

        #: Path to the virtual env location,
        # vary by Python version so we don't get conflicting envs
        self.virtualenv = os.path.join(self.installation_path, "pep8-virtualenv-%s" % "python3k" if self.python3k else "python2")

    def get_default_matchlist(self):
        """
        These files go into the validator.
        """
        return [
            "*.py",
        ]

    def check_is_installed(self):
        """
        See if we have installed working virtualenv for pep8
        """

        if self.host_python:
            return sysdeps.which("pep8")

        exists = os.path.exists(os.path.join(self.virtualenv, "bin", "pep8"))

        self.logger.debug("pep8 virtualenv status: %s" % "good" if exists else "bad")
        return exists

    def resolve_pep8(self, cmd):
        """
        Resolve location to pep8 command.

        :param cmd: Command spec according to rules
        """

        if not cmd:
            return None

        if cmd.startswith("."):
            cmd = os.path.abspath(os.path.join(self.project_path, cmd))

        # abspath, which, do not need special handling

        return cmd

    def check_requirements(self):

        if not self.pep8_command:
            sysdeps.has_virtualenv(needed_for="PEP8 validator")

    def run_virtualenv_command(self, cmd, raise_error=False):
        """
        Run cmd under host Python or our own virtualenv
        """

        if self.host_python:
            return utils.shell(self.logger, cmd, raise_error=raise_error)
        else:
            return sysdeps.run_virtualenv_command(self.logger, self.virtualenv, cmd, raise_error=raise_error)

    def install(self):
        """
        Download & install the validator app.
        """

        if self.pep8_command:
            return

        if self.python3k:
            python = "python3.2"
        else:
            # General virtualenv'ed Python
            python = "python"

        if self.host_python:
            # Use whatever python command is currently active
            python = "python"
        else:
            sysdeps.create_virtualenv(self.logger, self.virtualenv_cmd, self.virtualenv, py3=self.python3k)

        if self.pep8_command:
            # Use given Python commamnd
            python = self.pep8_command

        self.run_virtualenv_command("easy_install pep8", raise_error=True)

    def validate(self, fname):
        """
        Run installed pep8 validator against a file.
        """

        options = self.extra_options

        if self.pep8_command:
            exitcode, output = utils.shell(self.logger, '%s %s "%s"' % (self.pep8_command, options, fname))
        else:
            exitcode, output = self.run_virtualenv_command('pep8 %s "%s"' % (options, fname))

        if exitcode == 0:
            return True # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False


