"""

Python (pdb breakpoints)
==========================

Validator name:: ``pdb``

Do not allow Python pdb breakpoints in the committed files.

E.g. this will fail::

    def foo(self):
            import pdb ; pdb.set_trace()

The validator match for ``pdb.set_trace()`` in uncommented lines.
        
Supported files
----------------

``*.py``

Options
-----------

No options.

"""

import logging

from vvv.plugin import Plugin

class PdbPlugin(Plugin):
    """
    Pdb breakpoints not allowed in the code.
    """

    def setup_local_options(self):
        if not self.hint:
            self.hint = "Remove/comment out import pdb ; pdb.set_trace() statements before committing files\n"

    def get_default_matchlist(self):
        """
        """
        return [
            "*.py",
        ]

    def validate(self, fname):
        """
        Check each line for pdb statement and bark if one present and not commented out
        """

        errors = False

        i = 0
        f = open(fname, "rt")
        for line in f:
            i += 1
        
            if "pdb.set_trace()" in line:
                if not line.strip().startswith("#"):
                    errors = True
                    self.reporter.report_detailed(self.id, logging.ERROR, fname, i, None, None, "Line contains pdb breakpoint", excerpt=line)
        
        f.close()

        return not errors