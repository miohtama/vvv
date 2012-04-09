"""

Python (pdb breakpoints)
==========================

Validator name:: ``pdb``

Do not allow Python pdb breakpoints in committed files.

E.g. this will fail::

    def foo(self):
            import pdb ; pdb.set_trace()

We match for pdb.set_trace() in uncommented lines.
        
Supported files
----------------

* *.py

Options
-----------

No options.

"""

import logging

from vvv.plugin import Plugin

class TabsPlugin(Plugin):
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

    def validate(self, fname):
        """
        Tabs validator code runs in-line.
        """

        errors = False

        i = 0
        f = open(fname, "rt")
        for line in f:
            i += 1
            if "\t" in line:
                errors = True
                self.reporter.report_detailed(self.id, logging.ERROR, fname, i, None, None, "Line contains hard tabs", excerpt=line)
        f.close()

        return not errors