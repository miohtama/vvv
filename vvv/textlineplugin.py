"""

    Base class for plug-ins operating on Python on per text line basis

"""

# ABCMeta workarounds, still waiting for pylint patches
# pylint: disable=R0201, W0102, R0921, W0611


# Python imports
from abc import ABCMeta, abstractmethod

from .plugin import Plugin


class TextLinePlugin(Plugin, metaclass=ABCMeta):
    """
    Plug-in which operates on text lines natively on Python.
    """ 

    @abstractmethod
    def process_line(self, fname, line_number, line):
        """
        Handle one line of source text.

        Use self.reporter.report_detailed() to report any errors, then return True.

        :param fname: Filename

        :param line_number: The line number

        :param line: Line as unicode string

        :return: True if errors where encountered on the line
        """

    def validate(self, fname):
        """
        Tabs validator code runs in-line.
        """

        errors = False

        i = 0

        with open(fname, "rt", encoding="utf-8") as f:

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