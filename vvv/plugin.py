"""

	VVV plug-in base.

"""

from abc import ABCMeta, abstractmethod
import logging

from fnmatch import fnmatch

from utils import is_binary_file, get_boolean_option, get_list_option


class Plugin(metaclass=ABCMeta):
	"""
	Base class for VVV plug-ins.

	Use self.logger for debug output.

	Use self.reporter for user visible output.
	"""
		
	def init(self, id, main, reporter, options, violations, installation_path):
		"""

		:param id: internal id is externally set and comes from setup.py entry point name 

		:param main: Main VVV instance. You should not rely on this, but use explicitly passed in parameters.

		:param options: Validation options file

		:param violations: Validation violations file
		"""
		self.id = id
		self.main = main
		self.logger = logging.getLogger("vvv")
		self.reporter = reporter
		self.installation_path = installation_path		

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

	def get_whitelist(self):
		"""
		"""

	def get_blacklist(self):
		"""
		"""

	def match(self, fullpath):		
		"""
		Check if a path matches plug-in filtering options.
		"""

				 
	def setup_options(self):
		"""
		Initialize method after all plug-ins are loaded.
		
		Read options file for local options. 
		"""

		self.setup_global_options()
		self.setup_local_options()

	def setup_global_options(self):
		"""
		Set-up options global to all plug-ins

		* is enabled

		* whitelist 

		* blacklist
		"""

		self.enabled = get_boolean_option(self.options, self.id, "enabled", False)		
		self.whitelist = get_list_option(self.violations, self.id, "whitelist", False)		
		self.blacklist = get_list_option(self.violations, self.id, "blacklist", False)		

	def setup_local_options(self):
		"""
		Subclass **should** override this for 
		"""

	def check_install(self):
		"""
		Check if we need to download & install stuff to run this validatdor.

		:param installation_path: Where we dump all automatically downloaded stuff

		:return: True if install must be called
		"""

	def install(self, installation_path):
		"""
		Download & install the validator app.

		"""

	def install_on_demand(self):
		if self.check_install():
			self.install()		


	@abstractmethod
	def validate(self, fullpath)
		"""
		Run the validator against a file.

		Output results to the self.reporter.
		"""
		raise NotImplementedError("Subclass must implement")

	def run(self, fullpath):
		"""
		:return: True if file was processed 
		"""

		if not self.enabled:
			return False

		if not self.match(fullpath):
			return False

		if is_binary_file(fullpath) and not self.is_binary_friendly():
			self.logger.debug("%s: skipping binary file %s" % (self.id, fullpath))
			return False

		self.install_on_demand()

		return self.validate(fullpath)

	def run_command_line(self, cmdline):
		"""
		Run a command line command and capture output to the reporter.
		"""

