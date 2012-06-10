"""

    VVV plug-in base code which all plug-ins should extend and utilize.

"""

from __future__ import absolute_import, division, print_function, unicode_literals

# :R0201: *Method could be a function*
# We use dummy methods which subclasses can override
# W0102 Dangerous default value [] as argument
# R0921 Abstract class not referenced
# :W0611: *Unused import %s*
# pylint: disable=R0201, W0102, R0921, W0611

# Python imports
import logging
import os
import subprocess

# Local imports
from vvv import utils
# TODO: Factor there to use utils. prefix
from .utils import is_binary_file, match_file


class Plugin(object):
    """
    Base class for VVV plug-ins. Inherit from this class to add a new validator to VVV.

    Use self.logger for debug output.

    Use self.reporter for user visible output.

    Methods you should override are ``validate()`` and ``setup_local_options()``.
    """

    def __init__(self):

        #: Option file hint if the validation fails
        self.hint = None

        self.logger = self.matchlist = self.enabled = None

        self.id = self.main = self.reporter = self.options = self.files = self.installation_path = self.project_path = self.walker = None

    def init(self, plugin_id, main, reporter, options, files, installation_path, walker, project_path):
        """

        :param plugin_id: internal id is externally set and comes from setup.py entry point name

        :param main: Main VVV instance. You should not rely on this, but use explicitly passed in parameters.

        :param options: Config instance of global options file

        :param installation_path: Main application creates own folder for each plug-in where they can install stuff

        :parma walker: Project tree walker and file filtering helper

        :param files: Config instance of files whitelist / blacklist

        :param project_path: Path to the project root directory (where the config files are)
        """
        assert project_path
        self.id = plugin_id
        self.main = main
        self.options = options
        self.files = files
        self.logger = logging.getLogger("vvv")
        self.reporter = reporter
        self.installation_path = installation_path
        self.walker = walker
        self.project_path = project_path

    def is_active(self):
        """
        :return False: If this plug-in is not active for the current run
        """
        return self.enabled

    def is_binary_friendly(self):
        """
        :return True: If this plug-in must check binary files, otherwise skipped to speed up operations.
        """
        return False

    def get_default_matchlist(self):
        """
        Plug-in specific whitelist
        """
        return []

    def match(self, fullpath):
        """
        Check if a path matches plug-in filtering options.
        """
        return match_file(fullpath, self.matchlist)

    def setup_options(self):
        """
        Initialize method after all plug-ins are loaded.

        Read options file for local options.
        """

        self.setup_global_options()
        self.setup_local_options()
        self.finish_options()

    def setup_global_options(self):
        """
        Set-up options global to all plug-ins

        * plug-in is enabled

        * plug-in file match list

        * plug-in failed hint text
        """

        self.enabled = self.options.get_boolean_option(self.id, "enabled", True)

        self.matchlist = self.walker.get_match_list(self.files, self.id, None, default=self.get_default_matchlist())
        # Hint message how to fix errors
        self.hint = self.options.get_string_option(self.id, "hint", None)

    def setup_local_options(self):
        """
        Subclass **should** override this for
        """

    def finish_options(self):
        """
        Turn read options to Python objects if needed after both global and local config has been merged.
        """

    def check_is_installed(self):
        """
        Check if we need to download & install stuff to run this validatdor.

        :param installation_path: Where we dump all automatically downloaded stuff

        :return: False if install must be called
        """
        return True

    def check_requirements(self):
        """ Check that system has necessary facilities (like java) to run the validator.

        Throw any exception if something is missing.
        """

    def init_installation(self):
        """
        """
        if not os.path.exists(self.installation_path):
            os.makedirs(self.installation_path)

    def install(self):
        """
        Download & install the validator app.
        """

    def install_on_demand(self):
        """
        See if we are already installed. If not install required binary blobs and other crap to run this validator.
        """
        if not self.check_is_installed():
            self.logger.info("Installing software for validator: %s" % self.id)
            self.check_requirements()
            self.init_installation()
            self.install()
        else:
            self.logger.debug("Plug-in was already installed: %s" % self.id)

    def validate(self, fullpath):
        """
        Run the validator against a file.

        Output results to the self.reporter.

        :return: True if the validation success
        """
        raise NotImplementedError("Subclass must implement")

    def hint_to_fix_errors(self):
        """
        Give user the note how to fix errors after a failed validation.
        """

        if self.hint:
            self.reporter.hint_user(self.hint)

    def run(self, project_root_relative_path):
        """
        :return: True if file was processed
        """

        assert self.project_path, "Project path must be determined before a plug-in can run"

        assert not project_root_relative_path.startswith("/"), "Cannot work on absolute paths"

        if not self.enabled:
            return False

        if not self.match(project_root_relative_path):
            if self.walker.debug:
                self.logger.info("No plug-in match %s on %s" % (self.id, project_root_relative_path))
            return False

        fullpath = os.path.join(self.project_path, project_root_relative_path)

        if is_binary_file(fullpath) and not self.is_binary_friendly():
            self.logger.debug("%s: skipping binary file %s" % (self.id, fullpath))
            return False

        self.install_on_demand()

        self.logger.debug("Applying plug-in %s on %s" % (self.id, fullpath))

        if not self.validate(fullpath):
            self.hint_to_fix_errors()

    def run_command_line(self, cmdline, env={}, bad_string=None, snip_string=None):
        """
        Run a command line command and capture output to the reporter.

        :param cmdline: List of arguments

        :param bad_string: If detected in output assume there were validation errors. One string of list of strings.
        """

        success = True

        subenv = os.environ.copy()
        subenv.update(env)

        self.logger.debug("Running command line: %s" % cmdline)
        self.logger.debug("Env: %s" % subenv)

        if type(bad_string) == str:
            bad_string = [bad_string]

        process = subprocess.Popen(cmdline, env=subenv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = process.communicate()

        # :E1103: *%s %r has no %r member (but some types could not be inferred)*
        # pylint: disable=E1103

        out = out.decode("utf-8")
        err = err.decode("utf-8")

        # TODO: Interleave here?
        combined = out + "\n" + err

        self.logger.debug(combined)

        if bad_string:
            for match in bad_string:
                if match in combined:
                    success = False

        if snip_string:
            # Remove trailing unneeded messages
            combined = utils.snip_output(combined, snip_string)

        if not success:
            self.reporter.report_unstructured(self.id, combined)

        return success
