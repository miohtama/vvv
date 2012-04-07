"""

	Check that line length does not exceed certain threshold.

"""

import logging

from vvv.plugin import Plugin

from vvv.utils import get_int_option

class LineLengthPlugin(Plugin):
	"""
	"""

	def get_default_matchlist(self):
		return ["*"]

	def setup_local_options(self):

		self.line_length = get_int_option(self.options, self.id, "length", 76)

		if not self.hint:
			self.hint = "Text file line length must not exceed %d characteres per line" % self.line_length

	def validate(self, fname):
		"""
		Tabs validator code runs in-line.
		"""

		errors = False

		i = 0
		f = open(fname, "rt")
		for line in f:
			i += 1
			if len(line) >= self.line_length:
				errors = True
				self.reporter.report_detailed(self.id, logging.ERROR, fname, i, None, None, "Line is too long, %d characters" % len(line), excerpt=line)

		f.close()

		return not errors