#! /usr/bin/env python3
"""

    vvv entrypoint

"""

# Python imports
import os
import logging
from traceback import format_exception
import sys
import shutil

# Third party
from pkg_resources import iter_entry_points
import yaml

# Local imports
from .reporter import Reporter, FirstError
from .utils import load_yaml_file, get_list_option, match_file, get_match_option

logger = logging.getLogger("vvv")

#: Ignore known common project, temp, etc. files by default
DEFAULT_MATCHLIST = [

    # Blacklist all UNIX hidden files
    "!.*",

    # Python 3k generated files
    "!__pycache__",

    # Python 2 generated files
    "!*.pyc",

    # Match everything
    "*"
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
        # Copy in all arguments given to the constructor
        self.__dict__.update(kwargs)

        # Map of plug-ins id -> plugin instance
        self.plugins = dict()

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
            
            #import pdb; pdb.set_trace()
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
        for id, instance in self.plugins.items():
            
            try:

                plugin_installation = os.path.join(self.installation, id)
        
                instance.init(
                    id = id,
                    main = self,
                    reporter = self.reporter,
                    options = self.options_data,
                    violations = self.violations_data,
                    installation_path = plugin_installation
                )

                instance.setup_options()
            except Exception as e:
                logger.error("Could not initialize plug-in: %s", id)
                raise e             

    def walk(self, path):
        """
        Walk a project tree and run plug-ins.
        
        http://docs.python.org/library/os.html?highlight=walk#os.walk
        """

        # XXX: Optimize this to not to walk into folders which are blacklisted

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                fpath = os.path.join(root, name)
                if match_file(logger, fpath, self.matchlist):
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
            logger.debug("No options config file found")

        logger.debug("Using violations config file: %s" % self.violations)
        self.violations_data = load_yaml_file(self.violations)
        if self.violations_data == {}:
            logger.debug("No violations config file found")

    def process(self, fpath):
        """
        Run all validators against one file.

        :return True: if the process should be aborted
        """

        for id, p in self.plugins.items():
            try:
                p.run(fpath)
            except FirstError as fe:
                logger.info("Aborting on the first error")
                return True
            except Exception as e:
                etype, value, tb = sys.exc_info()
                msg = ''.join(format_exception(etype, value, tb))
                self.reporter.report_internal_error(id, msg)
                
                if self.suicidal:
                    raise e

        return False

    def setup_options(self):
        """
        """

        # Set-up global whitelist and blacklist
        self.matchlist = get_match_option(self.violations_data, "all", default=DEFAULT_MATCHLIST)

    def post_process_options(self):
        """
        Set option defaults.
        """

        if self.project is None:
            self.project = os.getcwd()

        if self.options is None:
            self.options = os.path.join(self.project, "validation-options.yaml")

        if self.violations is None:
            self.violations = os.path.join(self.project, "validation-violations.yaml")

        if self.installation is None:
            self.installation = os.path.join(self.project, ".vvv")

    def nuke(self):
        """
        Purge all downloads etc. by deleting the installation folder.
        """
        logger.info("Removing existing downloads and installations")
        shutil.rmtree(self.installation)

    def run(self):
        """ """

        if self.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        self.post_process_options()

        self.read_config()

        self.setup_options()

        self.find_plugins()

        self.reporter = Reporter(suicidal=self.suicidal)

        self.init_plugins()

        if self.reinstall:
            self.nuke()

        self.walk(self.project)

        self.report()

    def report(self):
        """
        Give output what we found and set sys exit code.
        """
        text = self.reporter.get_output_as_text()

        if text != "":
            print(text)
            sys.exit(2)
        else:
            sys.exit(0)


def main(
    options : ("Validation options file. Default is validation-options.yaml", 'option', 'c'),
    violations : ("Validation allowed violations list file. Default is validation-violations.yaml", "option", "b"),
    verbose : ("Give verbose output", "flag", "v"),
    project : ("Path to a project folder. Defaults to the current working directory.", "option", "p"),
    installation : ("Where to download & install binaries need to run the validators. Defaults to the repository root .vvv folder", "option", "i"),
    reinstall : ("Redownload and configure all validation software", "flag", "r"),
    suicidal : ("Die on first error", "flag")
    ):
    """ 

    Application starting point without parsing the command line.

    http://plac.googlecode.com/hg/doc/plac.html#scripts-with-default-arguments
    """
    vvv = VVV(options=options, violations=violations, verbose=verbose, project=project, 
              installation=installation, reinstall=reinstall, 
              suicidal=suicidal)
    vvv.run()


def entry_point():
    """
    Application starting point which parses command line.

    Can be used from other modules too.
    """
    import plac; plac.call(main)

if __name__ == "__main__":
    print("foo")
    entry_point()