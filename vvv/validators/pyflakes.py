"""

Python (pyflakes)
====================

Validator name: ``pyflakes``

Validate Python files using Pyflakes.

Supported files
----------------

* \*.py

Options
-----------

host-python-env
++++++++++++++++

If ``true`` do not create a virtualenv for running pyflakes, but install pyflakes using
the active ``python`` environment where vvv is run.

Default is ``false``.

.. note ::

    If you change this you need run ``vvv --reinstall``.

pyflakes-command
+++++++++++++++++++++

A path spec pointing to used ``pyflakes`` command.

Use this command to run pyflakes. This is for cases where ``host-python-env``
is not enough to tame your Python package dependencies.

If this option starts with . it is considered to be a directory reference relative to the project root.

If this option starts with / it is considered to be absolute directory reference.

Otherwise normal path look behavior is used (UNIX ``which`` commmand behavior).

Example::

    pyflakes:
      enabled: true
      # Points to buildout/bin/pyflakes command two levels below project folder
      pyflakes-command: ../../bin/pyflakes

command-line
++++++++++++

Give pyflakes command line options.

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


class PyflakesPlugin(Plugin):
    """
    Pyflakes driver.
    """

    def __init__(self):

        Plugin.__init__(self)

        #: Configuration file option
        self.extra_options = None

        #: Virtualenv path used to run pyflakes
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
            self.hint = "Python source code did not pass Pyflakes validator. Please fix issues or disable warnings in .py file itself or validation-options.yaml file."

        self.virtualenv_cmd = os.path.join(self.installation_path, "virtualenv.py")

        self.host_python = self.options.get_boolean_option(self.id, "host-python-env", False)

        pyflakes_command = self.options.get_string_option(self.id, "pyflakes-command", None)

        self.pyflakes_command = self.resolve_pyflakes(pyflakes_command)

        #: Path to the virtual env location,
        # vary by Python version so we don't get conflicting envs
        self.virtualenv = os.path.join(self.installation_path, "pyflakes-virtualenv-python2")

    def get_default_matchlist(self):
        """
        These files go into the validator.
        """
        return [
            "*.py",
        ]

    def check_is_installed(self):
        """
        See if we have installed working virtualenv for pyflakes
        """

        if self.host_python:
            return sysdeps.which("pyflakes")

        exists = os.path.exists(os.path.join(self.virtualenv, "bin", "pyflakes"))

        self.logger.debug("pyflakes virtualenv status: %s" % "good" if exists else "bad")
        return exists

    def resolve_pyflakes(self, cmd):
        """
        Resolve location to pyflakes command.

        :param cmd: Command spec according to rules
        """

        if not cmd:
            return None

        if cmd.startswith("."):
            cmd = os.path.abspath(os.path.join(self.project_path, cmd))

        # abspath, which, do not need special handling

        return cmd

    def check_requirements(self):

        if not self.pyflakes_command:
            sysdeps.has_virtualenv(needed_for="Pyflakes validator")

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

        if self.pyflakes_command:
            return

        if not self.host_python:
            sysdeps.create_virtualenv(self.logger, self.virtualenv_cmd, self.virtualenv, py3=False)

        self.run_virtualenv_command("easy_install pyflakes", raise_error=True)

    def validate(self, fname):
        """
        Run installed pyflakes validator against a file.
        """

        options = self.extra_options

        if self.pyflakes_command:
            exitcode, output = utils.shell(self.logger, '%s %s "%s"' % (self.pyflakes_command, options, fname))
        else:
            exitcode, output = self.run_virtualenv_command('pyflakes %s "%s"' % (options, fname))

        if exitcode == 0:
            return True     # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False
