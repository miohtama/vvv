"""

	Check tab policy.

"""

import logging

from vvv.plugin import Plugin

from vvv.utils import 

class TabsPlugin(Plugin):
	"""
	"""

	def validate(self, fname):
		"""
		"""

		i = 0
		f = open(fname, "rt")
		for line in f:
			i += 1
			if "\t" in line:
				self.reporter.report_detailed(fname, logging.ERROR, None, "Line contains tabs", None)
		f.close()