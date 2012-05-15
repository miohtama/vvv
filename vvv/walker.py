"""

    Smart way of walking directories and matching with advanced fnmath lists


    http://koti.mbnet.fi/tynninen/mustanaamio_index/fingerpori/fingerpori.html

"""

# Dangerous default value [] as argument
# pylint: disable=W0102 

import os

from vvv import utils

class Walker:
    """
    Convenience class for path walk and regex filtering.

    Follows little bit bad programming practices by not separating concerns, 
    but makes like a little bit easier.
    """

    def __init__(self, logger, debug):
        """
        :param debug: Print out regex debugging information
        """
        self.logger = logger
        self.debug = debug


    def walk_project_files(self, target_path, project_path, matchlist):
        """
        Walk project root and spit out project root relative output.

        Unlike os.walk() do not enter into directories which are on the ignore list.
        """

        files = []
               
        project_path = os.path.abspath(project_path)

        def recurse(path):
            """
            Handle each folder 
            """
            for name in os.listdir(path):
                
                fpath = os.path.abspath(os.path.join(path, name))

                relative = os.path.relpath(fpath, project_path)

                if relative.startswith("./"):
                    relative = relative[2:]

                self.logger.debug("Scanning %s" % (relative))

                if not utils.match_file(relative, matchlist):
                    if self.debug:
                        self.logger.info("Ignoring %s by global match list", relative)
                    continue
                
                if os.path.isdir(fpath):
                    recurse(fpath)                
                else:
                    files.append(relative)
                

        recurse(target_path)
        
        return files          

    @staticmethod
    def is_whitelisted(fpath, project_path, matchlist):
        """
        Check whether an individual file is whitelisted or blacklisted.
        """

        project_path = os.path.abspath(project_path)

        path = fpath

        # Walk each part of the path from top to project root and see
        # that each path part is on the whitelist
        while path and path != "/":

            # Get project root relative presentation of the file
            abspath = os.path.abspath(os.path.join(project_path, path))
            relative = os.path.relpath(abspath, project_path)

            if relative == ".":
                # Reached project_path root
                return True

            if not utils.match_file(relative, matchlist):
                return False

            # Unused var
            # pylint: disable=W0612 

            # http://docs.python.org/library/os.path.html#os.path.split
            path, tail = os.path.split(path)

        return True

    def get_match_list(self, config, section, entry=None, default=[]):
        """
        Read a file match list option from a config line.

        Set-up debugging on the regex matcher object if enabled.

        :param config: Config object 

        :return: Globster matching object
        """
        return config.get_match_option(section, entry=entry, default=default, debug=self.debug)