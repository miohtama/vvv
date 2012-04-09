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
            
configuration
++++++++++++++

Pass in ``.jshintrc`` configuration options.

* `Information about jshint options <http://www.jshint.com/options/>`_

* `Example configuration <https://github.com/jshint/node-jshint/blob/master/.jshintrc>`_

command-line
++++++++++++++

Pass in extra arguments for the jshint command line.

More info
------------

* http://www.jshint.com/

"""

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

        # Extra options passed to the validator
        self.extra_options = None

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = utils.get_string_option(self.options, self.id, "command-line", DEFAULT_COMMAND_LINE)

        self.configuration = utils.get_string_option(self.options, self.id, "configuration", "")

        if not self.hint:
            self.hint = "Javascript source code did not pass JSLint validator - http://www.jshint.com/"

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
        sysdeps.has_node("Node.js must be installed in order to run JSLint Javascript validator")

        sysdeps.has_exe("jshint", 
                        "jshint must be installed via npm in order to run Javascript validation", 
                        "Install jshint: https://github.com/jshint/node-jshint/"
                        )

    def validate(self, fname):
        """
        Run installed jshint against a file.
        """

        with utils.temp_config_file(self.configuration) as config_fname:
            
            # https://github.com/jshint/node-jshint/

            options = self.extra_options
            if not "--config" in options:
                options += " --config=%s" % config_fname

            exitcode, output = utils.shell(self.logger, 'jshint "%s" %s' % (fname, options))

            if "error" in output:
                self.reporter.report_unstructured(self.id, output, fname=fname)
                return False

        return True