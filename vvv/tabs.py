"""

	Check tab policy.

"""

import logging

from vvv.plugin import Plugin

class TabsPlugin(Plugin):
	"""
	"""

	def setup_local_options(self):
		if not self.hint:
			self.hint = "Adjust your text editor settings to save tabs as spaces.\nhttp://dougneiner.com/post/641596410/tabs-vs-spaces"

	def get_default_blacklist(self):
		"""
		These files require hard tabs
		"""
		return [
			"Makefile",
			"*.mk"
		]

	def validate(self, fname):
		"""
		Tabs validator code runs in-line.
		"""

		errors = False

		i = 0
		f = open(fname, "rt")
		for line in f:
			i += 1
			if "\t" in line:
				errors = True
				self.reporter.report_detailed(fname, logging.ERROR, None, "Line contains hard tabs", None)
		f.close()

		return not errors