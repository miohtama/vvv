"""

Python (pylint)
====================

Validator name: ``pylint``

Lint Python files using Pylint.

Installation
----------------

.. warning::

    pylint installation is broken for Python 3.x - please see notes below

A temporarily *virtualenv* environment is automatically created
where pylint command and its dependencies are is installed.
However this is not very good way to run pylint, as if you
are using any third party libraries pylint cannot import them
and thus fails.

It is recommended to use ``host-python-env`` option -
this whill install pylint to a Python environment
which you enable before running.

Example (assuming you have ``host-python-env`` set in ``validate-options.yaml``)::

    # Activate virtualenv
    source venv/bin/activate

    # Run vvv and install pylint to now activate Python env
    vvv --reinstall

The default pylint checks are very strict. You might want to see a more relaxed configuration example::

* https://github.com/miohtama/vvv/blob/master/validation-options.yaml

Supported files
----------------

* \*.py

Options
-----------

Example ``validation-options.yaml``::

    pylint:
        python3k: true

        command-line: --reports=n

host-python-env
++++++++++++++++

If ``true`` do not create a virtualenv for running pylint, but install pylint using
the active ``python`` environment where vvv is run.

Default is ``false``.

.. note ::

    If you change this you need run ``vvv --reinstall``.

pylint-command
+++++++++++++++++++++

A path spec pointing to used ``pylint`` command.

Use this command to run pylint. This is for cases where ``host-python-env``
is not enough to tame your Python package dependencies.

If this option starts with . it is considered to be a directory reference relative to the project root.

IF this option starts with / it is considered to be absolute directory reference.

Otherwise normal path look behavior is used (UNIX ``which`` commmand behavior).

Example::

    pylint:
      enabled: true
      python3k: false
      # Points to buildout/bin/pylint command two levels below project folder
      pylint-command: ../../bin/pylint

command-line
++++++++++++

Give pylint command line options.

Default::

    --reports=n --include-ids=y

configuration
+++++++++++++

Pass in pylint configuration file data.
This is a block of text which gets passed in as pylint .rc file.
For rc file example run command::

    pylint --generate-rcfile

python3k
++++++++++++

If true set-up pylint for Python 3.x. The default is Python 2.x.

.. note ::

    If you change this you need run ``vvv --reinstall``.

Other
------------

To disable warning per source code file one can add pylint hints in the .py files using ``pylint:`` directives like::

    # :R0201: *Method could be a function*
    # W0102 Dangerous default value [] as argument
    # R0921 Abstract class not referenced
    # :W0611: *Unused import %s*
    # pylint: disable=R0201, W0102, R0921, W0611

These can be function or module level scoped.

To see all pylint error and warning message ids::

    pylint --list-msgs

And to find a message id::

    pylint --list-msgs|grep -i "Dangerous default"
    :W0102: *Dangerous default value %s as argument*

* http://www.logilab.org/ticket/91764


pylint bugs
------------

Currently you need to manually fix logilab-astng package for Python 3 with trunk version.

The error::

      File "/Users/moo/code/vvv/dist/test/lib/python3.2/site-packages/logilab_astng-0.23.1-py3.2.egg/logilab/astng/scoped_nodes.py", line 249, in file_stream
        return file(self.file)
    NameError: global name 'file' is not defined

If you are using a .vvv virtualenv::

    cd ~/.vvv
    source pylint/pylint-virtualenv/bin/activate
    hg clone http://hg.logilab.org/logilab/astng
    cd astng
    python setup.py install

If you are using ``host-python-env`` option::

    source YOURVIRTUALENV/bin/activate
    hg clone http://hg.logilab.org/logilab/astng
    cd astng
    python setup.py install

* http://comments.gmane.org/gmane.comp.python.logilab/1193

After this re-run vvv and everything should go ok.

More info
------------

* http://pypi.python.org/pypi/pylint

* http://www.logilab.org/card/pylint_manual

* http://www.logilab.org/4736
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Python imports
import os

# Local imports
from vvv.plugin import Plugin
from vvv import utils

from vvv import sysdeps
from vvv import download

DEFAULT_COMMAND_LINE = "--reports=n --include-ids=y"

DEFAULT_CONFIG = """

"""


class PylintPlugin(Plugin):
    """
    Pylint driver.
    """

    def __init__(self):

        Plugin.__init__(self)

        #: Configuration file option
        self.extra_options = None

        #: Virtualenv path used to run pylint
        self.virtualenv = None

        #: Configuration file option
        self.python3k = None

        #: Configuration file option
        self.pylint_configuration = None

        #: Configuration file option
        self.host_python = None

        #: Configuration file option
        self.pylint_command = None

        #: Location of virtualenv.py if operating system cannot supply working one
        self.virtualenv_cmd = None

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = self.options.get_string_option(self.id, "command-line", DEFAULT_COMMAND_LINE)

        self.pylint_configuration = self.options.get_string_option(self.id, "configuration", "")

        if not self.hint:
            self.hint = "Python source code did not pass Pylint validator. Please fix issues or disable warnings in .py file itself or validation-options.yaml file."

        self.virtualenv_cmd = os.path.join(self.installation_path, "virtualenv.py")

        self.python3k = self.options.get_boolean_option(self.id, "python3k", False)

        self.host_python = self.options.get_boolean_option(self.id, "host-python-env", False)

        pylint_command = self.options.get_string_option(self.id, "pylint-command", None)

        self.pylint_command = self.resolve_pylint(pylint_command)

        #: Path to the virtual env location,
        # vary by Python version so we don't get conflicting envs
        self.virtualenv = os.path.join(self.installation_path, "pylint-virtualenv-%s" % "python3k" if self.python3k else "python2")

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

        if self.host_python:
            return sysdeps.which("pylint")

        exists = os.path.exists(os.path.join(self.virtualenv, "bin", "pylint"))

        self.logger.debug("Pylint virtualenv status: %s" % "good" if exists else "bad")
        return exists

    def resolve_pylint(self, cmd):
        """
        Resolve location to pylint command.

        :param cmd: Command spec according to rules
        """

        if not cmd:
            return None

        if cmd.startswith("."):
            cmd = os.path.abspath(os.path.join(self.project_path, cmd))

        # abspath, which, do not need special handling

        return cmd

    def check_requirements(self):

        if not self.pylint_command:
            sysdeps.has_virtualenv(needed_for="Pylint validator")

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

        ARGFADSFASF WHY NOTHING CANNOT WORK IN THIS WORLD?

        http://www.logilab.org/82417

        http://comments.gmane.org/gmane.comp.python.logilab/1193
        """

        if self.pylint_command:
            return

        # XXX: Prefix virtualenv name by version so we can have multiple pylints installed
        # in .vvv once

        pkg = "pylint-0.25.1"

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

        if self.pylint_command:
            # Use given Python commamnd
            python = self.pylint_command

        # Extract and download manually
        pylint_download_path = os.path.join(self.installation_path, "pylint-extract.tar.gz")
        pylint_extract_path = os.path.join(self.installation_path, "pylint-extract", pkg)

        if not os.path.exists(pylint_extract_path):
            # If path exist, assume it's prior working download
            download.download_and_extract_gz(self.logger, pylint_download_path, "http://pypi.python.org/packages/source/p/pylint/pylint-0.25.1.tar.gz")

        self.run_virtualenv_command("easy_install logilab-common", raise_error=True)

        # Use py3k patched logilab-astng
        self.run_virtualenv_command("easy_install https://github.com/downloads/miohtama/vvv/logilab-astng-0.23.1-py3-patched.tar.gz", raise_error=True)
        self.run_virtualenv_command("cd %s ; NO_SETUPTOOLS=1 %s setup.py install --no-compile" % (pylint_extract_path, python), raise_error=True)

    def validate(self, fname):
        """
        Run installed pylint validator against a file.
        """

        with utils.temp_config_file(self.pylint_configuration) as config_fname:

            options = self.extra_options
            if not "--rcfile" in options:
                options += " --rcfile=%s" % config_fname

            if self.pylint_command:
                exitcode, output = utils.shell(self.logger, '%s %s "%s"' % (self.pylint_command, options, fname))
            else:
                exitcode, output = self.run_virtualenv_command('pylint %s "%s"' % (options, fname))

        if exitcode == 0:
            return True # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False


