#! /usr/bin/env python3
"""

    Very vine versioning

"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Python imports
import os
import logging
from traceback import format_exception
import sys
import shutil

# Third party
import plac
from pkg_resources import iter_entry_points

# Local imports
from .reporter import Reporter, FirstError
from .walker import Walker
from .config import Config

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

#: sys.exit() value used for bad command line options
BAD_COMMAND_LINE_EXIT_CODE = 64


class BadCommmandLineError(RuntimeError):
    """
    Risen when the command line option do not make sense.
    """


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
        self.options = self.files = self.verbose = self.target = \
        self.installation = self.reinstall = self.suicidal = \
        self.include = self.regex_debug = self.quiet = self.print_files = None

        #: Parsed option file data as Config object
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

        #: Are we scanning a full source code tree or just one file
        self.project_tree_scan = False

        #: Absolute path where we found the project root (option files)
        self.project_path = None

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

    def set_project_path(self, path):
        """
        Helper method to shortcut project path determination, used by test cases.
        """
        self.project_path = path

    def determine_project_path(self):
        """
        Where is the root of this source code project.
        """

        if not self.project_path:

            # We have options file
            if self.options:
                self.project_path = os.path.dirname(os.path.abspath(self.options))
            else:
                # Assume current working directory
                self.project_path = os.getcwd()

    def determine_target(self):
        """
        Are we matching against a single file or recurse to directory
        """

        assert self.target

        if os.path.isdir(self.target):
            self.project_tree_scan = True
        else:
            self.project_tree_scan = False

    def init_plugins(self):
        """
        Initialize all plug-ins.

        Set plug-in data installation path inside local .vvv installation folder.

        Allow plug-in to read its own options.
        """

        assert self.project_path
        assert os.path.exists(self.project_path)

        for plugin_id, instance in self.plugins.items():

            try:

                plugin_installation = os.path.join(self.installation, plugin_id)

                instance.init(
                    plugin_id=plugin_id,
                    main=self,
                    reporter=self.reporter,
                    options=self.options_data,
                    files=self.files_data,
                    installation_path=plugin_installation,
                    walker=self.walker,
                    project_path=self.project_path
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

        logger.info("Running vvv against %s" % path)

        # Walk tree
        for fpath in self.walker.walk_project_files(path, self.project_path, self.matchlist):

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

        if self.options and os.path.exists(self.options):
            self.options_data = Config(self.options)
            self.options_data.load()
        else:
            logger.warn("No validation-options.yaml config file found, using defaults")
            self.options_data = Config()

        logger.debug("Using files config file: %s" % self.files)

        if self.files and os.path.exists(self.files):
            self.files_data = Config(self.files)
            self.files_data.load()
        else:
            raise BadCommmandLineError("Given validation-files.yaml does not exist")

    def check_is_processable(self, fpath):
        """
        Checks that a file is not on all files blacklist.

        Normally directory walker does this when walking thru files.
        But we might directly refer to individual files thru commit hook.
        For these files, we need to check if they can be procesed or not.
        """

        # XXX: Individual plug-ins need this check also
        return self.walker.is_whitelisted(fpath, self.project_path, self.matchlist)

    def process(self, fpath):
        """
        Run all validators against one file.

        :param fpath: Any path to a file

        :return True: if the process should be aborted
        """

        assert self.project_path

        abs_path = os.path.join(self.project_path, fpath)

        relative = os.path.relpath(abs_path, self.project_path)

        if self.print_files:
            logger.info(abs_path)

        for plugin_id, p in self.plugins.items():
            try:
                p.run(relative)
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
        Set-up global options (not specific to plug-in)
        """

        # Set-up global whitelist and blacklist
        self.matchlist = self.walker.get_match_list(self.files_data, "all", default=DEFAULT_MATCHLIST)

    def post_process_options(self):
        """
        Set option file real location and VVV installation path.
        """

        if self.target is None:
            self.target = os.getcwd()

        if self.options is None:
            self.options = Config.find_config_file(self.target, "validation-options.yaml")

        if self.files is None:
            self.files = Config.find_config_file(self.target, "validation-files.yaml")

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

    def validate_files(self):
        """
        Who let the dogs out?

        http://www.youtube.com/watch?v=He82NBjJqf8
        """

        if self.project_tree_scan:
            # Full tree
            logger.debug("Scanning tree: %s" % self.target)
            self.walk(self.target)
        else:
            # Single file
            if not self.check_is_processable(self.target):
                logger.warn("Single target was not scan whitelist: %s" % self.target)
                return

            logger.debug("Scanning single file: %s" % self.target)
            self.process(self.target)

    def run(self):
        """
        Run the show.

        XXX: Split to several parts which can be called individually,
        so that we can have better control over this from unit tests.

        :return: System exit return code
        """

        try:
            self.post_process_options()

            self.setup_output()

            self.read_config()

            self.find_plugins()

            self.prepare()

            self.setup_options()

            self.determine_project_path()

            self.determine_target()

            self.init_plugins()

            if self.reinstall:
                self.nuke()

        except BadCommmandLineError as cmd_line_error:
            print(cmd_line_error, file=sys.stderr)
            return BAD_COMMAND_LINE_EXIT_CODE

        self.validate_files()

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
            #logger.info("All files ok")
            return 0

@plac.annotations( \
    options=("Validation options file. Default is validation-options.yaml", 'option', 'o', None, None, "validation-options.yaml"),
    files=("Validation allowed files list file. Default is validation-files.yaml", "option", "f", None, None, "validation-files.yaml"),
    installation=("Where automatically downloaded files are kept. Defaults to hidden .vvv directory in home folder", "option", "i", None, None, ".vvv"),
    verbose=("Give verbose output", "flag", "v"),
    reinstall=("Redownload and configure all validation software", "flag", "ri"),
    suicidal=("Die on first error", "flag", "s"),
    printfiles=("Output scanned files to stdout", "flag", "print"),
    regexdebug=("Print out regex matching information to debug file list regular expressions", "flag", "rd"),
    quiet=("Only output fatal internal errors to stdout", "flag", "q"),
    target=("Path to a project folder or a file. Use . for the current working directory.", "positional", None, None, None, "YOUR-SOURCE-CODE-FOLDER"),
    )
def main(options, files, installation, verbose, reinstall, suicidal, printfiles, regexdebug, quiet, target):
    """
    A convenience utility for software source code validation and linting.

    More info: https://github.com/miohtama/vvv

    Example how to scan the current source tree for issues:

        vvv .
    """

    # Application starting point without parsing the command line.

    # http://plac.googlecode.com/hg/doc/plac.html#scripts-with-default-arguments

    vvv = VVV(options=options, files=files, verbose=verbose, target=target,
              installation=installation, reinstall=reinstall, quiet=quiet,
              suicidal=suicidal, include=None, regex_debug=regexdebug, print_files=printfiles)
    sys.exit(vvv.run())


def entry_point():
    """
    Application starting point which parses command line.

    Can be used from other modules too.
    """
    exit_code = plac.call(main)
    sys.exit(exit_code)

if __name__ == "__main__":
    entry_point()
