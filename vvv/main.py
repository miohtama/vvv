#! /usr/bin/env python3
"""

	vvv entrypoint

"""

# Python imports
import os
import logging
from traceback import format_exception
import sys

# Third party
from pkg_resources import iter_entry_points
import yaml

# Local imports
from reporter import Reporter
from utils import load_yaml_file, get_list_option, match_file, 

logger = logging.getLogger("vvv")

#: Ignore known common project, temp, etc. files by default
DEFAULT_BLACKLIST = [
	".git",
	".svn",
	".bzr",
	".DS_Store"
]

DEFAULT_WHITELIST = [
	"*"
]

class VVV(object):
	""" 
	Vi like this main class vor this project.
	"""

	def __init__(**kwargs):
		# Copy in all arguments given to the constructor
		self.__dict.__update(kwargs)

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
	        
	        try:
	        	# Construct the plug-in instance
	        	plugin = loader()
	        	logger.debug("Loaded plug-in: %s", loader)
	        	self.plugins.append(plugin)
	        except Exception, e:
	        	logger.error("Could not load plug-in: %s", loader)
	        	raise e

	def init_plugins(self):
		"""
		"""
		for id, instance in self.plugins.items():
			
			try:
				instance.init(
					id = id,
					main = self,
					reporter = self.reporter,
					options = self.options_data,
					violations = self.violations_data,
					installation_path = self.installation
				)

				instance.setup_options()
	        except Exception, e:
	        	logger.error("Could not initialize plug-in: %s", id)
	        	raise e				

	def walk(self, path):
		"""
		Walk a project tree and run plug-ins.
		
		http://docs.python.org/library/os.html?highlight=walk#os.walk
		"""

		# XXX: Optimize this to not to walk into folders which are blacklisted

		for root, dirs, files in os.walk(top, topdown=False):
		    for name in files:
		        fpath = os.path.join(root, name)
		        if match_file(fpath, self.whitelist, self.blacklist):
					self.run(fpath)		        	

	def read_config(self):
		"""
		Load config files.
		"""
		self.options_data = load_yaml_file(self.options)
		self.violations_data = load_yaml_file(self.violations)

	def process(self, fpath):
		"""
		Run validators against a file.
		"""

		for id, p in self.plugins.items():
			try:
				p.validate(fpath)
			except Exception, e:

				etype, value, tb = sys.exc_info()
			    msg = ''.join(format_exception(etype, value, tb, limit))
				self.reporter.internal_error(id, msg)

	def setup_options(self):
		"""
		"""

		# Set-up global whitelist and blacklist
		self.blacklist = get_yaml_list_option(self.violations_data, "all", "blacklist")
		self.whitelist = get_yaml_list_option(self.violations_data, "all", "whitelist")

		if self.blacklist == []:
			self.blacklist = DEFAULT_BLACKLIST

		if self.whitelist == []:
			self.whitelist = DEFAULT_WHITELIST

	def post_process_options(self):
		"""
		Set option defaults.
		"""

		if self.project is None:
			self.project = os.getcwd()

		if self.options is None:
			self.options = os.path.join(self.project, "validation-options.yaml")

		if self.violations is None:
			self.violations = os.path.join(self.violations, "validation-violations.yaml")

		if self.installation is None:
			self.installation = os.path.join(self.project, ".vvv")
	
	def run(self):
		""" """

		if self.verbose:
			logging.basicConfig(level=logging.DEBUG)
		else:
			logging.basicConfig(level=logging.WARN)

		self.post_process_options()

		self.setup_options()

		self.read_config()

		self.find_plugins()

		self.init_plugins()

		self.reporter = Reporter()

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
	project : ("Path to a project folder. Defaults to the current working directory.", "option", "p")
	installation : ("Where to download & install binaries need to run the validators. Defaults to the repository root .vvv folder", "option", "i")
	):
	""" 

	Parse command line arguments using plac.

	http://plac.googlecode.com/hg/doc/plac.html#scripts-with-default-arguments
	"""
	vvv = VVV(options=options, violations=violations, verbose=verbose, project=project, installation=installation)
	vvv.run()



if __name__ == "__main__":
	import plac; plac.call(main)