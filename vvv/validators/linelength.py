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

from vvv.textlineplugin import TextLinePlugin


class LineLengthPlugin(TextLinePlugin):
    """
    Line length driver.
    """

    def __init__(self):

        TextLinePlugin.__init__(self)

        #: Configuration file option
        self.line_length = None

    def get_default_matchlist(self):
        return ["*"]

    def setup_local_options(self):

        self.line_length = self.options.get_int_option(self.id, "length", 80)

        if not self.hint:
            self.hint = "Text file line length must not exceed %d characteres per line" % self.line_length

    def process_line(self, fname, line_number, line):
        """
        Check that line does not contain evil spaces.
        """

        if len(line) > self.line_length:
            self.reporter.report_detailed(self.id, logging.ERROR, fname, line_number, None, None, "Line is too long, %d characters" % len(line), excerpt=line)
            return True

        return False
