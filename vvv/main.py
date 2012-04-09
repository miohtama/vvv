#! /usr/bin/env python3
"""

    Very vine versioning

"""

# Python imports
import os
import logging
from traceback import format_exception
import sys
import shutil

# Third party
from pkg_resources import iter_entry_points

# Local imports
from .reporter import Reporter, FirstError
from .utils import load_yaml_file
from .walker import Walker

# XXX: Factor this to VVV main class attribute
logger = logging.getLogger("vvv")

#: Regular expression to match all dotted files and folders
#: 1. Match anything after slash which starts with .
#: 2. Match anything which starts with . (root level dotted files)
# http://regex.larsolavtorvik.com/
MATCH_DOTTED_FILES_AND_FOLDERS_REGEX = r".*\/\..*|^\..*"

# http://docs.python.org/library/logging.html
LOG_FORMAT = "%(message)s"

#: Ignore known common project, temp, etc. files by default
DEFAULT_MATCHLIST = [
  r"*",
  "!" + MATCH_DOTTED_FILES_AND_FOLDERS_REGEX,
  r"!__pycache__"
]

class VVV(object):
    """ 
    Vi like this main class vor this project.

    Load plug-ins based on Python setup.py entry point information.

    Parse options.

    Initialize plug-ins.

    Run project walker.

    For each file run validator, the validator will install own binaries if needed.
    """

    def __init__(self, **kwargs):


        #: Command line options
        self.options = self.files = self.verbose = self.project = \
        self.installation = self.reinstall = self.suicidal = \
        self.include = self.regex_debug = self.quiet = self.print_files = None

        #: Parsed option file data
        self.options_data = self.files_data = None

        #: Global file matchlist
        self.matchlist = None

        #: Reporter instance collecting output
        self.reporter = None

        #: File tree walker and match helper
        self.walker = None

        # Copy in all arguments given to the constructor
        self.__dict__.update(kwargs)

        #: Map of plug-ins id -> plugin instance
        self.plugins = dict()

        #: Store test runner output, so that (test) drivers of vvv can print this 
        self.output = None

    def load_config(self):
        """
        """
        self.options_data = load_yaml_file(self.options)

    def find_plugins(self):
        """ 
        Scan all system installed eggs for plug-ins.

        We use entry point "vvv" where each entry point points to a constructor of a plug-in.

        http://wiki.pylonshq.com/display/pylonscookbook/Using+Entry+Points+to+Write+Plugins
        """

        for loader in iter_entry_points(group='vvv', name=None):
            
            try:
                # Construct the plug-in instance
                name = loader.name
                klass = loader.load()
                instance = klass()
                logger.debug("Loaded plug-in: %s", name)
                self.plugins[name] = instance
            except Exception as e:
                logger.error("Could not load plug-in: %s", loader)
                raise e

    def init_plugins(self):
        """
        Initialize all plug-ins.

        Set plug-in data installation path inside local .vvv installation folder.

        Allow plug-in to read its own options.
        """
        for plugin_id, instance in self.plugins.items():
            
            try:

                plugin_installation = os.path.join(self.installation, plugin_id)
        
                instance.init(
                    plugin_id = plugin_id,
                    main = self,
                    reporter = self.reporter,
                    options = self.options_data,
                    files = self.files_data,
                    installation_path = plugin_installation,
                    project_path = self.project,
                    walker = self.walker
                )

                instance.setup_options()
            except Exception as e:
                logger.error("Could not initialize plug-in: %s", plugin_id)
                raise e             

    def walk(self, path):
        """
        Walk a project tree and run plug-ins.
        
        http://docs.python.org/library/os.html?highlight=walk#os.walk
        """

        # XXX: Optimize this to not to walk into folders which are blacklisted

        logger.info("Running vvv against %s" % path)

        for fpath in self.walker.walk_project_files(path, self.matchlist):

            if self.print_files:
                logger.info(fpath)
                    
            if self.process(fpath):
                return True             

        return False                 

    def read_config(self):
        """
        Load config files.
        """
        
        logger.debug("Using options config file: %s" % self.options)
        self.options_data = load_yaml_file(self.options)

        if self.options_data == {}:
            logger.warn("No validation-options.yaml config file found, using defaults")

        logger.debug("Using files config file: %s" % self.files)
        self.files_data = load_yaml_file(self.files)
        if self.files_data == {}:
            logger.warn("No validation-files.yaml config file found, using defaults")

    def process(self, fpath):
        """
        Run all validators against one file.

        :return True: if the process should be aborted
        """

        for plugin_id, p in self.plugins.items():
            try:
                p.run(fpath)
            except FirstError:
                logger.info("Aborting on the first error")
                return True
            except Exception as e:
                etype, value, tb = sys.exc_info()
                msg = ''.join(format_exception(etype, value, tb))
                self.reporter.report_internal_error(plugin_id, msg)
                
                if self.suicidal:
                    raise e

        return False

    def setup_options(self):
        """
        """

        # Set-up global whitelist and blacklist
        self.matchlist = self.walker.get_match_option(self.files_data, "all", default=DEFAULT_MATCHLIST)

    def post_process_options(self):
        """
        Set option defaults.
        """

        if self.project is None:
            self.project = os.getcwd()

        if self.options is None:
            self.options = os.path.join(self.project, "validation-options.yaml")

        if self.files is None:
            self.files = os.path.join(self.project, "validation-files.yaml")

        if self.installation is None:
            home = os.environ.get("HOME", None)
            if not home:
                raise RuntimeError("No home folder")

            self.installation = os.path.join(home, ".vvv")

    def nuke(self):
        """
        Purge all downloads etc. by deleting the installation folder.

        https://www.youtube.com/watch?v=2s1MspmfEwg
        """
        logger.warn("Removing existing downloads and installations: %s" % self.installation)
        if os.path.exists(self.installation):
            shutil.rmtree(self.installation)

    def prepare(self):
        """
        Prepare for a run.
        """
        self.reporter = Reporter(suicidal=self.suicidal)

        self.walker = Walker(logger, self.regex_debug)

    def setup_output(self):
        """
        Set how we deal with output.
        """
        if self.quiet:
            logging.basicConfig(level=logging.ERROR, stream=sys.stdout, format=LOG_FORMAT)
        elif self.verbose:
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=LOG_FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=LOG_FORMAT)

    def run(self):
        """
        Run the show. 

        XXX: Split to several parts which can be called individually,
        so that we can have better control over this from unit tests.

        :return: System exit return code
        """
        self.post_process_options()

        self.setup_output()

        self.read_config()

        self.find_plugins()

        self.prepare()

        self.setup_options()

        self.init_plugins()

        if self.reinstall:
            self.nuke()

        self.walk(self.project)

        return self.report()

    def report(self):
        """
        Give output what we found and set sys exit code.
        """
        self.output = self.reporter.get_output_as_text()

        if self.output != "":
            logger.info(self.output)
            return 2
        else:
            logger.info("All files ok")
            return 0


def main(
    options : ("Validation options file. Default is validation-options.yaml", 'option', 'o', None, None, "validation-options.yaml"),
    files : ("Validation allowed files list file. Default is validation-files.yaml", "option", "f", None, None, "validation-files.yaml"),
    installation : ("Where automatically downloaded files are kept. Defaults to hidden .vvv directory in home folder", "option", "i", None, None, ".vvv"),
    verbose : ("Give verbose output", "flag", "v"),
    reinstall : ("Redownload and configure all validation software", "flag", "ri"),
    suicidal : ("Die on first error", "flag", "s"),
    printfiles : ("Output scanned files to stdout", "flag", "print"),
    regexdebug : ("Print out regex matching information to debug file list regular expressions", "flag", "rd"),
    quiet : ("Only output fatal internal errors to stdout", "flag", "q"), 
    project_folder : ("Path to a project folder. Use . for the current working directory.", "positional", None, None, None, "YOUR-SOURCE-CODE-FOLDER"),
    ):
    """ 
    A convenience utility for software source code validation and linting.

    More info: https://github.com/miohtama/vvv

    Example how to scan the current source tree for issues:

        vvv .
    """

    # Application starting point without parsing the command line.

    # http://plac.googlecode.com/hg/doc/plac.html#scripts-with-default-arguments


    vvv = VVV(options=options, files=files, verbose=verbose, project=project_folder, 
              installation=installation, reinstall=reinstall, quiet = quiet,
              suicidal=suicidal, include = None, regex_debug=regexdebug, print_files=printfiles)
    sys.exit(vvv.run())


def entry_point():
    """
    Application starting point which parses command line.

    Can be used from other modules too.
    """

    import plac
    plac.call(main)

if __name__ == "__main__":
    print("foo")
    entry_point()