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

Example ``validation-options.yaml``::

    pylint:
        python3k: true

        command-line: --reports=n


command-line
++++++++++++

Give pylint command line options.

configuration
+++++++++++++

Pass in pylint configuration file data.
This is a block of text which gets passed in as pylint .rc file.
For rc file example run command::   

    pylint --generate-rcfile 

python3k
++++++++++++

If true set-up pylint for Python 3.x. The default is Python 2.x.

No that if you change this you need run ``vvv --reinstall``.

Other
------------

To disable warning per source code file one can add pylint hints in the .py file::

    

To see all pylint error and warning message ids::

    pylint --list-msgs    

And to find a message id::

    pylint --list-msgs|grep -i "Dangerous default"
    :W0102: *Dangerous default value %s as argument*

* http://www.logilab.org/ticket/91764


pylint bugs
------------

Currently you need to manually fix logilab-astng package for Python 3 with truk astng::

    cd .vvv
    source source pylint/pylint-virtualenv/bin/activate
    hg clone http://hg.logilab.org/logilab/astng
    cd astng
    python setup.py install

* http://comments.gmane.org/gmane.comp.python.logilab/1193

More info
------------

* http://pypi.python.org/pypi/pylint

* http://www.logilab.org/card/pylint_manual

* http://www.logilab.org/4736
"""

# Python imports
import os
import tempfile

# Local imports
from vvv.plugin import Plugin
from vvv import utils 

from vvv import sysdeps
from vvv import download

DEFAULT_COMMAND_LINE = "--reports=n"

DEFAULT_CONFIG = """

"""

class PylintPlugin(Plugin):
    """
    """

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = utils.get_string_option(self.options, self.id, "command-line", DEFAULT_COMMAND_LINE)

        self.pylint_configuration = utils.get_string_option(self.options, self.id, "configuration", "")

        if not self.hint:
            self.hint = "Python source code did not pass Pylint validator. Please fix issues or disable warnings in .py file itself or validation-options.yaml file."

        #: Path to the virtual env location
        self.virtualenv = os.path.join(self.installation_path, "pylint-virtualenv")

        self.python3k = utils.get_boolean_option(self.options, self.id, "python3k", False)

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

        if self.python3k:
            python = "python3.2"
            easy_install = "easy_install"
        else:
            python = "python2.7"
            easy_install = "easy_install"

        sysdeps.create_virtualenv(self.logger, self.virtualenv, py3=self.python3k)

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

        f = tempfile.NamedTemporaryFile(mode="wt", delete=False)

        try:
            
            f.write(self.pylint_configuration)
            f.close()

            options = self.extra_options
            if not "--rcfile" in options:
                options += " --rcfile=%s" % f.name

            exitcode, output = sysdeps.run_virtualenv_command(self.logger, self.virtualenv, 'pylint %s "%s"' % (options, fname))
        finally:
            f.unlink(f.name)

        if exitcode == 0:
            return True # Validation ok
        else:
            self.reporter.report_unstructured(self.id, output, fname=fname)
            return False


