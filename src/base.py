from libcloud.compute.types import Provider
from libcloud.providers import get_driver
import sys; sys.path.append('..')
import utils

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
	def connect(self, driver, user_id, key):
		"""
		Connect with a particular driver using a userid
		and a key.
		"""
		try:
			real_driver = utils.getProvider(str(driver))
			driver_class = get_driver(real_driver);
			conn = driver_class(str(user_id), str(key))
			return conn
		except NameError, e:
			print ">> Fatal Error: %s" % e
			return False
		except Exception, e:
			print ">> Fatal error: %s" % e
			return False

class VnodectrlException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
