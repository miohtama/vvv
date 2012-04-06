"""


"""


class Reporter:
	"""
	Simple output collector from plug-ins-
	"""

	def __init__(self):

		#: List of output lines or line blocks
		self.raw_output = []

		
		#: List of hints to fix errors - outputted as last
		self.hints = []


	def report_detailed(self, plugin_id, severity, path, line, id, msg, details):
		"""

		:param plugin_id: Which validator failed - later used to display hint message to the user

		:param path: File path relative to the repo root as string

		:param severity: One of Python logging.* constants

		:param id: Error message id if any or None

		:param line: Line number as integer

		:param msg: One line error message 

		:param details: Multi-line error messags like a traceback (usually hidden in details view) or None
		"""
		if id is None:
			id = "validation error"

		self.raw_output.append("%s %d: [%s] %s" % (path, line, id, msg))
		
	def report_unstructured(self, plugin_id, output):
		"""
		Dump text output as is from the validator
		"""
		self.raw_output.append(output)
		
	def report_internal_error(self, plugin_id, msg):
		"""
		Report exception fired from a plug-in.

		Internal error message does not trigger user hint message.
		"""

		msg = "Internal error occured when running validator %s\n" % plugin_id
		msg += msg

		self.report_unstructured(msg)

	def hint_user(self, hint_message):
		"""
		Give user a hint how to proceed to fix the errors.

		:param hint_message: Hinting info as multi-line string
		"""
		self.hints.append(hint_message)

	def get_output_as_text(self):
		return "\n".join(self.raw_output) + "\n".join(self.hints)