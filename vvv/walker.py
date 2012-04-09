"""

    Smart way of walking directories and matching with advanced fnmath lists


    http://koti.mbnet.fi/tynninen/mustanaamio_index/fingerpori/fingerpori.html

"""

# Dangerous default value [] as argument
# pylint: disable=W0102 

import os

from vvv import utils

def make_project_root_relative(abspath, project_abs_path):
    """
    We must deal with paths relative to the project root and os.walk() cannot spit out such
    """
    return abspath[len(project_abs_path)+1:]

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


    def walk_project_files(self, project_path, matchlist):
        """
        Walk project root and spit out project root relative output.

        Unlike os.walk() do not enter into directories which are on the ignore list.
        """

        files = []
                
        def recurse(path):
            """
            Handle each folder 
            """
            for name in os.listdir(path):
                fpath = os.path.join(path, name)
                relative = make_project_root_relative(fpath, project_path)

                if relative.startswith("./"):
                    relative = relative[2:]

                self.logger.debug("Scanning %s" % relative)
            
                if not utils.match_file(relative, matchlist):
                    if self.debug:
                        self.logger.info("Ignoring %s by global match list", relative)
                    continue
                
                if os.path.isdir(fpath):
                    recurse(fpath)                
                else:
                    files.append(relative)                 
                

        recurse(project_path)
        
        return files          


    def get_match_option(self, yaml, section, entry=None, default=[]):
        """
        Read a file match list option from a config line.

        Set-up debugging on the regex matcher object if enabled.

        :return: Globster matching object
        """
        return utils.get_match_option(yaml, section, entry=entry, default=default, debug=self.debug)