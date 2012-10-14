"""

Python (zptlint)
====================

Validator name: ``zptlint``

Validate Python files using zptlint.

Supported files
----------------

* \*.pt

Options
-----------

host-python-env
++++++++++++++++

If ``true`` do not create a virtualenv for running zptlint, but install zptlint using
the active ``python`` environment where vvv is run.

Default is ``false``.

.. note ::

    If you change this you need run ``vvv --reinstall``.

zptlint-command
+++++++++++++++++++++

A path spec pointing to used ``zptlint`` command.

Use this command to run zptlint. This is for cases where ``host-python-env``
is not enough to tame your Python package dependencies.

If this option starts with . it is considered to be a directory reference relative to the project root.

If this option starts with / it is considered to be absolute directory reference.

Otherwise normal path look behavior is used (UNIX ``which`` commmand behavior).

Example::

    zptlint:
      enabled: true
      # Points to buildout/bin/zptlint command two levels below project folder
      zptlint-command: ../../bin/zptlint

command-line
++++++++++++

Give zptlint command line options.

Default is empty.

"""


from __future__ import absolute_import, division, print_function, unicode_literals

# Python imports
import os

# Local imports
from vvv.plugin import Plugin
from vvv import utils

from vvv import sysdeps

DEFAULT_COMMAND_LINE = ""


class ZptlintPlugin(Plugin):
    """
    zptlint driver.
    """

    def __init__(self):

        Plugin.__init__(self)

        #: Configuration file option
        self.extra_options = None

        #: Virtualenv path used to run zptlint
        self.virtualenv = None

        #: Configuration file option
        self.host_python = None

        #: Configuration file option
        self.paflakes_command = None

        #: Location of virtualenv.py if operating system cannot supply working one
        self.virtualenv_cmd = None

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = self.options.get_string_option(self.id, "command-line", DEFAULT_COMMAND_LINE)

        if not self.hint:
            self.hint = "Python source code did not pass zptlint validator. Please fix issues or disable warnings in validation-options.yaml file."

        self.virtualenv_cmd = os.path.join(self.installation_path, "virtualenv.py")

        self.host_python = self.options.get_boolean_option(self.id, "host-python-env", False)

        zptlint_command = self.options.get_string_option(self.id, "zptlint-command", None)

        self.zptlint_command = self.resolve_zptlint(zptlint_command)

        #: Path to the virtual env location,
        # vary by Python version so we don't get conflicting envs
        self.virtualenv = os.path.join(self.installation_path, "zptlint-virtualenv-python2")

    def get_default_matchlist(self):
        """
        These files go into the validator.
        """
        return [
            "*.pt",
            "*.xml",
            "*.zcml",
        ]

    def check_is_installed(self):
        """
        See if we have installed working virtualenv for zptlint
        """

        if self.host_python:
            return sysdeps.which("zptlint")

        exists = os.path.exists(os.path.join(self.virtualenv, "bin", "zptlint"))

        self.logger.debug("zptlint virtualenv status: %s" % "good" if exists else "bad")
        return exists

    def resolve_zptlint(self, cmd):
        """
        Resolve location to zptlint command.

        :param cmd: Command spec according to rules
        """

        if not cmd:
            return None

        if cmd.startswith("."):
            cmd = os.path.abspath(os.path.join(self.project_path, cmd))

        # abspath, which, do not need special handling

        return cmd

    def check_requirements(self):

        if not self.zptlint_command:
            sysdeps.has_virtualenv(needed_for="Zptlint validator")

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

        if self.zptlint_command:
            return

        if not self.host_python:
            sysdeps.create_virtualenv(self.logger, self.virtualenv_cmd, self.virtualenv, py3=False)

        self.run_virtualenv_command("easy_install zptlint", raise_error=True)

    def validate(self, fname):
        """
        Run installed zptlint validator against a file.
        """

        options = self.extra_options

        if self.zptlint_command:
            exitcode, output = utils.shell(self.logger, '%s %s "%s"' % (self.zptlint_command, options, fname))
        else:
            exitcode, output = self.run_virtualenv_command('zptlint %s "%s"' % (options, fname))

        if not output:
            return True     # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False
