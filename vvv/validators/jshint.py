"""

Javascript (jshint)
====================

Validator name: ``jshint``

Lint Javascript files using `jshint <http://www.jshint.com/>`_.

Prerequisites
----------------
      
Your system supports Node.js and must have jshint package installed.

Please see :doc:`prerequisites </prerequisites>`.

Installation
----------------

You must use Node ``npm`` to install ``node-jshint`` package.

:: 

    sudo npm install -g jshint

* https://github.com/jshint/node-jshint/


Supported files
----------------

* \*.js

Options
-----------

Options for ``jshint`` section in ``validation-options.yaml``.

Example ``validation-options.yaml``::

    jshint:
        configuration: |
            {
                eqeqeq : true
            }
            
.. warning::

    Make sure **configuration** is valid JSON. *jshint* silently ignores these options otherwise. 

configuration
++++++++++++++

Pass in ``.jshintrc`` configuration options.

* `Information about jshint options <http://www.jshint.com/options/>`_

* `Example configuration <https://github.com/jshint/node-jshint/blob/master/.jshintrc>`_

command-line
++++++++++++++

Pass in extra arguments for the jshint command line.

Mass adding global hints
--------------------------------

VVV provides a Python script to add ``/* global */`` hints to several Javascript files once.

See :doc:`vvv-add-js-globals </tools/addjsglobals>`.

More info
------------

* http://www.jshint.com/

"""

import os

from vvv.plugin import Plugin

from vvv import utils
from vvv import sysdeps

#: Command-line options given to jshint always
DEFAULT_COMMAND_LINE = ""

class JSHintPlugin(Plugin):
    """
    jshint driver
    """            

    def __init__(self):

        Plugin.__init__(self)

        #: Configuration file Text
        self.configuration = None

        #: Commandl line options passed to the validator from the config file
        self.extra_options = None

        #: Where jshint has been installed via npm
        self.jshint_path = None 

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = self.options.get_string_option(self.id, "command-line", DEFAULT_COMMAND_LINE)

        self.configuration = self.options.get_string_option(self.id, "configuration", "")

        if not self.hint:
            self.hint = "Javascript source code did not pass JSHint linting - http://www.jshint.com/"

        # Install directly under this plug-in path
        self.jshint_path = self.installation_path

    def get_jshint_bin(self):
        """
        :return: Location of jshint launch command
        """
        return os.path.join(self.jshint_path, "node_modules", "jshint", "bin", "hint")

    def get_default_matchlist(self):
        """
        These files require hard tabs
        """
        return [
            "*.js",
        ]

    def check_requirements(self):
        """
        """
        sysdeps.has_node("Node.js must be installed in order to run JHLint Javascript validator")


    def check_is_installed(self):
        """
        See if we have installed working virtualenv for pylint
        """
        return os.path.exists(self.get_jshint_bin())

    def install(self):
        """ """
        sysdeps.install_npm(self.logger, self.jshint_path, "jshint", raise_error=True)

    def validate(self, fname):
        """
        Run installed jshint against a file.
        """

        with utils.temp_config_file(self.configuration) as config_fname:
            
            # https://github.com/jshint/node-jshint/

            options = self.extra_options
            if not "--config" in options:
                if self.configuration and self.configuration.strip() != "":
                    # Make sure we don't pass empty config file as jshint seems to choke on it
                    options += " --config '%s'" % config_fname

            # W:100,10:Unused variable'
            # pylint: disable = W0612    

            exitcode, output = utils.shell(self.logger, 'node %s "%s" %s' % (self.get_jshint_bin(), fname, options))

            if "error" in output:
                self.reporter.report_unstructured(self.id, output, fname=fname)
                return False

        return True