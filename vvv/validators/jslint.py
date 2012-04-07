"""

Javascript (jslint)
====================

Validator name: ``jslint``

Validate Javascript files using Douglas Crockford's jslint.js.

Prerequisites
----------------
      
Your system supports Node.js.      

Please see :doc:`prerequisites </prerequisites>`.

Installation
----------------

You must use Node ``npm`` to install ``node-jslinst`` package.

* https://github.com/reid/node-jslint

Supported files
----------------

* \*.js

Options
-----------

No options.

More info
------------

* http://www.jslint.com/

"""

from vvv.plugin import Plugin
from vvv.utils import get_string_option

from vvv import sysdeps
from vvv import download

class JSLintPlugin(Plugin):
    """
    """

    def setup_local_options(self):
        """ """

        # Extra options passed to the validator
        self.extra_options = get_string_option(self.options, self.id, "extra", None)

        if not self.hint:
            self.hint = "Javascript source code did not pass JSLint validator - http://www.jslint.com/"

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
        sysdeps.has_node(needed_for="Node.js must be installed in order to run JSLint Javascript validator")

        sysdeps.has_exe("jslint", 
                        "jslint must be installed via npm in order to run Javascript validation", 
                        "Install jslint: https://github.com/reid/node-jslint"
                        )

    def validate(self, fname):
        """
        Run installed jslint against a file.
        """
        return self.run_command_line(["jslint", fname])