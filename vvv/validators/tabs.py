"""

Tab policy
====================

Validator name: ``tabs``

Do not allow hard tabs in committed files.
Instead, use soft tabs and spaces.


To allow hard tabs in any file add the following in your ``validator-options.yaml``::

    tabs:
        enable: false

To allow hard tabs in specific files use ``validator-files.yaml``::

    tabs:
      Makefile
      *.mk 

Mass converting tabs to spaces 
--------------------------------

VVV provides a Python script to expand tabs to spaces in-place.

See :doc:`vvv-expand-tabs </tools/expandtabs>`.

Supported files
----------------

* All text files, Makefiles are excluded by default

Options
-----------

No options.

More info
------------

* http://dougneiner.com/post/641596410/tabs-vs-spaces

"""

import logging

from vvv.textlineplugin import TextLinePlugin

class TabsPlugin(TextLinePlugin):
    """
    Hard tab banisher plug-in.
    """

    def setup_local_options(self):
        if not self.hint:
            self.hint = "Adjust your text editor settings to indent using spaces instead of hard tabs.\nUse a converter to convert existing tabs to spaces.\nhttp://dougneiner.com/post/641596410/tabs-vs-spaces"

    def get_default_matchlist(self):
        """
        These files require hard tabs
        """
        return [
            "*",
            "!Makefile",
            "!*.mk"
        ]

    def process_line(self, fname, line_number, line):
        """

        """        
        if "\t" in line:
            self.reporter.report_detailed(self.id, logging.ERROR, fname, line_number, None, None, "Line contains hard tabs", excerpt=line)
            return True

        return False