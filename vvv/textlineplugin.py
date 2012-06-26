"""

    Base class for plug-ins operating on Python on per text line basis

"""

# ABCMeta workarounds, still waiting for pylint patches
# pylint: disable=R0201, W0102, R0921, W0611

import io

from .plugin import Plugin


def _open(file, flags):
    """
    Python 2.x / Python 3 cross-compatible file opener.

    Ignore UTF-8 errors (otherwise readline() would raise an exception).

    Don't try to undertand other encodings.
    """
    return io.open(file, flags, encoding="utf-8", errors="replace")


class TextLinePlugin(Plugin):
    """
    Plug-in which operates on text lines natively on Python.
    """

    def process_line(self, fname, line_number, line):
        """
        Handle one line of source text.

        Use self.reporter.report_detailed() to report any errors, then return True.

        :param fname: Filename

        :param line_number: The line number

        :param line: Line as unicode string

        :return: True if errors where encountered on the line
        """
        raise NotImplementedError("Subclass must implement")

    def validate(self, fname):
        """
        Tabs validator code runs in-line.
        """

        errors = False

        i = 0

        with _open(fname, "rt") as f:

            for line in f:
                i += 1
                if self.process_line(fname, i, line):
                    errors = True

        return not errors
