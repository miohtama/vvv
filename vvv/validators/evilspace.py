"""

Evil spacebar buster
==========================

Validator name:: ``evilspace``

Make sure text files do not contain no-break space (NBS) character.

* ALT + spacebar inserts non-breaking spacebar on Linux systems. It kind of makes sense ALT means alternative and
  evil space is the alter ego of normal space. Its invisibly grins when your code falls apart.

* OPTION + spacebar inserts non-breaking spacebar on OSX systems

* It is totally possible that you accidentally type plenty of these characters if you are workign on non-US keyboard
  when you frequently need to press ALT to for characters for proramming grammar. Example. ``if(foobar || foobar2) {``.

* Non-breaking spacebar (NBSP) character cannot be distinguished from normal space, as they both are, well..., invisible

* A lot of compilers, linters, Javascript compressors, etc. cannot handle this character properly and fall into very interesting failure modes
  which are hard to debug

* This is especially important when creating Javascript code because browsers threat NBS differently

Supported files
----------------

All text files.

Options
-----------

No options.

More info
-------------

* `Insight and instructions how to disable ALT + spacebar character on OSX  <http://apple.stackexchange.com/questions/34672/whats-altspacebar-character-and-how-to-disable-it/>`_.

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from vvv.textlineplugin import TextLinePlugin

VERY_EVIL_SPACE = "\xa0"


class EvilSpacePlugin(TextLinePlugin):
    """
    Pdb breakpoints not allowed in the code.
    """

    def setup_local_options(self):
        if not self.hint:
            self.hint = "Detected non-breaking spacebar characters in files"

    def get_default_matchlist(self):
        """
        """
        return [
            "*",
        ]

    def process_line(self, fname, line_number, line):
        """
        Check that line does not contain evil spaces.
        """

        if VERY_EVIL_SPACE in line:
            self.reporter.report_detailed(self.id, logging.ERROR, fname, line_number, None, None, "Line contains non-breaking space character (alt+spacebar)", excerpt=line)
            return True

        return False

