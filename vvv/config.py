"""

    Convenience wrapper around YAML config file parsing.


"""

# Dangerous default value [] as argument
# pylint: disable=W0102

# Python imports
import os

# Third party
import yaml

# Local imports
from .bzrlib.globster import ExceptionGlobster


class ConfigException(Exception):
    """
    Having bad input in a config file.
    """


class Config:
    """
    Hold one YAML config file inside.

    Assume config file structure is like::

        # section = top level item
        section:

            # entry = second level item
            entry1: foo

            entry2
                - foo
                - bar

    """

    def __init__(self, filename):
        """
        :param filename: Full path to the config file or None if we don't read any options
        """

        #: abs path to the config file
        self.filename = filename

        #: parsed config data as Python dict - default to empty
        self.config = dict()

    def load(self):
        """
        Try to load YAML config file and return empty dict if the file does not exist.
        """
        fpath = self.filename

        # We might not have config file at all if upwind
        # path look-up has failed in find_config_file()
        if fpath:

            # Return empty options
            if not os.path.exists(fpath):
                return

            f = open(fpath, "rt")
            try:
                self.config = yaml.safe_load(f)
            finally:
                f.close()

        # If the file is empty yaml.safe_load() sets result to None
        if self.config is None:
            self.config = dict()

    def get_option(self, section_name, entry, default=None):
        """
        Convert YAML tree entry to a Python list.

        If section does not exist return empty list.

        http://pyyaml.org/wiki/PyYAMLDocumentation#Blocksequences

        :param config: Configuration as Python dict
        """

        config = self.config

        section = config.get(section_name, {})

        if type(section) == str:
            raise RuntimeError("Expected configuration file block, but found a string option instead %s: %s" % (section_name, entry))

        entry = section.get(entry, default)

        return entry

    def get_list_option(self, section, entry, default=[]):
        """
        Read YAML config which is list-line
        """
        return self.get_option(section, entry, default)

    def get_boolean_option(self, section, entry, default=False):
        """
        Read YAML true/false config
        """
        return self.get_option(section, entry, default)

    def get_int_option(self, section, entry, default=0):
        """
        Read YAML int config
        """
        return self.get_option(section, entry, default)

    def get_string_option(self, section, entry, default=""):
        """
        Read YAML string config
        """
        return self.get_option(section, entry, default)

    def get_match_option(self, section, entry=None, default=[], debug=False):
        """
        Read YAML config which is a block string of file ignore pattern.


        """
        if entry:
            opt = self.get_option(section, entry, default)
        else:
            opt = self.config.get(section, default)

        if type(opt) == str:
            # Split space or new line separated list to pieces
            opt = opt.split()
        elif type(opt) == list:
            pass
        else:
            raise ConfigException("Bad option data for %s %s" % (section, entry))

        g = ExceptionGlobster(opt, debug)

        g.orignal_pattern = opt

        return g

    @classmethod
    def find_config_file(cls, start_path, filename):
        """
        Recurses to parent paths and tries to find a filename.

        :return: Full path to found config file or None
        """

        levels = 100

        if not os.path.isdir(start_path):
            start_path = os.path.dirname(start_path)

        path = start_path

        while not os.path.ismount(path):

            config_file = os.path.join(path, filename)
            if os.path.exists(config_file):
                return config_file

            old_path = path
            path = os.path.abspath(os.path.join(path, os.path.pardir))
            if old_path == path:
                # Hit the C:\ root?
                return None

            levels -= 1
            if levels <= 0:
                raise ConfigException("Too much recursion to parents when trying to find a config file: %s" % filename)

        # Hit a mount point
        return None
