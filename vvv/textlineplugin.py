"""

    Base class for plug-ins operating on Python on per text line basis

"""

# ABCMeta workarounds, still waiting for pylint patches
# pylint: disable=R0201, W0102, R0921, W0611

import sys

from .plugin import Plugin


def _open(file, flags, encoding):
    """
    Python 2.x encoding compatible shim.
    """
    if sys.version_info[0] >= 3:
        return open(file, flags, encoding=encoding)
    else:
        return open(file, flags)


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

        with _open(fname, "rt", encoding="utf-8") as f:

            try:
                for line in f:
                    i += 1
                    if self.process_line(fname, i, line):
                        errors = True
            except UnicodeDecodeError:
                # UnicodeDecodeError: 'utf8' codec can't decode byte 0xa5 in position 2: invalid start byte
                # TODO: For now, how to handle? Should attempt to detect encoding?
                self.logger.warn("Bad encoding: %s" % fname)

        return not errors
