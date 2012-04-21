"""

Line length
====================

Validator name: ``linelength``

Check that that text file lines are not too long.

Prerequisites
----------------

Built-in - no external software needed.

Supported files
----------------

* All text files.

Options
-----------

length
+++++++

Set maximum allowed line length. Defaults to ``80`` columns.

Example ``validator-options.yaml``::

    # Allow long text lines
    linelength:
        length: 250

More info
------------

* http://www.kernel.org/doc/Documentation/CodingStyle

"""

import logging

from vvv.plugin import Plugin

class LineLengthPlugin(Plugin):
    """
    Line length driver.
    """

    def __init__(self):

        Plugin.__init__(self)
        
        #: Configuration file option
        self.line_length = None
            

    def get_default_matchlist(self):
        return ["*"]

    def setup_local_options(self):

        self.line_length = self.options.get_int_option(self.id, "length", 80)

        if not self.hint:
            self.hint = "Text file line length must not exceed %d characteres per line" % self.line_length

    def validate(self, fname):
        """
        Tabs validator code runs in-line.
        """

        errors = False

        i = 0
        f = open(fname, "rt", encoding="ascii")
        try:
            for line in f:
                i += 1
                if len(line) > self.line_length:
                    errors = True
                    self.reporter.report_detailed(self.id, logging.ERROR, fname, i, None, None, "Line is too long, %d characters" % len(line), excerpt=line)
        except UnicodeDecodeError:
            # UnicodeDecodeError: 'utf8' codec can't decode byte 0xa5 in position 2: invalid start byte
            # For now, how to handle?
            pass

        f.close()

        return not errors