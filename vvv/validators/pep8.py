"""

Python (pep8)
====================

Validator name: ``pep8``

Validate Python files using PEP8.

Supported files
----------------

* \*.py

Options
-----------

The default pep8 checks are very strict.
Example ``validation-options.yaml``::

    pep8:
        command-line: --ignore E501

    linelength:
        length: 250

host-python-env
++++++++++++++++

If ``true`` do not create a virtualenv for running pep8, but install pep8 using
the active ``python`` environment where vvv is run.

Default is ``false``.

.. note ::

    If you change this you need run ``vvv --reinstall``.

pep8-command
+++++++++++++++++++++

A path spec pointing to used ``pep8`` command.

Use this command to run pep8. This is for cases where ``host-python-env``
is not enough to tame your Python package dependencies.

If this option starts with . it is considered to be a directory reference relative to the project root.

If this option starts with / it is considered to be absolute directory reference.

Otherwise normal path look behavior is used (UNIX ``which`` commmand behavior).

Example::

    pep8:
      enabled: true
      python3k: false
      # Points to buildout/bin/pep8 command two levels below project folder
      pep8-command: ../../bin/pep8

command-line
++++++++++++

Give pep8 command line options.

Default is empty.

python3k
++++++++++++

If true set-up pep8 for Python 3.x. The default is Python 2.x.

.. note ::

    If you change this you need run ``vvv --reinstall``.

More info
------------

* http://pypi.python.org/pypi/pep8/

"""


from __future__ import absolute_import, division, print_function, unicode_literals

# Python imports
import os

# Local imports
from vvv.plugin import Plugin
from vvv import utils

from vvv import sysdeps

DEFAULT_COMMAND_LINE = ""


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
        self.host_python = None

        #: Configuration file option
        self.pep8_command = None

        #: Location of virtualenv.py if operating system cannot supply working one
        self.virtualenv_cmd = None

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = self.options.get_string_option(self.id, "command-line", DEFAULT_COMMAND_LINE)

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

        if not self.host_python:
            sysdeps.create_virtualenv(self.logger, self.virtualenv_cmd, self.virtualenv, py3=self.python3k)

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
            return True     # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False
