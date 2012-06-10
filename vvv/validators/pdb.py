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

from vvv.textlineplugin import TextLinePlugin

#: Common Python ways to invoke hardcoded breakpoint
MARKERS = ["pdb.set_trace()", "ipdb.set_trace()"]

class PdbPlugin(TextLinePlugin):
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

    def process_line(self, fname, line_number, line):
        """

        """        

        # Ignore comments
        if line.strip().startswith("#"):
            return

        
        for m in MARKERS:
            if m in line:
                self.reporter.report_detailed(self.id, logging.ERROR, fname, line_number, None, None, "Line contains pdb breakpoint", excerpt=line)
                return True

        return False        

