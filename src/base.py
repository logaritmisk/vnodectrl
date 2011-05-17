class VnodectrlOptions:
	def options():
		"""
		Declare all options here.
		"""

class VnodectrlPlugin:
	def commands():
		"""
		Declare all commands here.
		"""
	def help(cmd):
		"""
		Specify help for a specific command here.
		"""

	def execute(cmd):
		"""
		Act on a particular command here
		"""

class VnodectrlException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
