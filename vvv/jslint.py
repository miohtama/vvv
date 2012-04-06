"""

	Javascript validation via jslint.

"""

"""

	CSS validation using W3C validator.

	Requirements: 

	http://www.codestyle.org/css/tools/W3C-CSS-Validator.shtml

	http://jigsaw.w3.org/Distrib/jigsaw_2.2.6.tar.gz

	http://www.nic.funet.fi/pub/mirrors/apache.org//velocity/engine/1.7/velocity-1.7.tar.gz

	http://www.nic.funet.fi/pub/mirrors/apache.org//xerces/j/source/Xerces-J-src.2.11.0.tar.gz



"""

import collections import OrderedDict

from vvv.plugin import Plugin
from vvv.utils import get_string_option

from vvv import sysdeps
from vvv import download

class JSLintPlugin(Plugin):
	"""
	"""

	def setup_local_options(self):
		""" """

		# Extra options passed to the validator
		self.extra_options = get_string_option(self.options, self.id, "extra", None)

		if not self.hint:
			self.hint = "Javascript source code did not pass JSLint validator - http://www.jslint.com/"

	def get_default_whitelist(self):
		"""
		These files require hard tabs
		"""
		return [
			"*.js",
		]

	def check_requirements(self):
		"""
		"""
		sysdeps.has_node(needed_for="Node.js must be installed in order to run JSLint Javascript validator")
		sysdeps.has_exe("jslint", 
						"jslint must be installed via npm in order to run Javascript validation", 
						"Install jslint: https://github.com/reid/node-jslint"
						)

	def validate(self, fname):
		"""
		Run installed jslint against a file.
		"""
		return self.run_command_line("jslint %s" % (fname))