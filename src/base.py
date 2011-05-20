from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
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
	def connect(self, driver, user_id = "NaN", key = "NaN"):
		"""
		Connect with a particular driver using a userid
		and a key.
		"""
		try:
			driver_class = utils.getProvider(driver)
			# Temporary to get support
			if driver == "virtualbox":
				conn = driver_class()
			else:
				conn = driver_class(str(user_id), str(key))
			return conn
		except NameError, e:
			print ">> Fatal Error: %s" % e
			return False
		except Exception, e:
			print ">> Fatal error: %s" % e
			return False
	
	def getSize(self, driver, conn, size = False):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		sizes = conn.list_sizes()
		
		# If size is false, let's not care about what size we use.
		if size is False:
			return sizes[0]
		
		size = str(size)
		for available_size in sizes:
			if available_size.id == size:
				return available_size
		return False
		
	def getImage(self, driver, conn, image):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		
		# Virtualbox drivers dont really know about the different images,
		# Instead they force you to add the drivers in list_images.
		# Dirrrty hack harr.
		if str(driver) == 'virtualbox':
			images = conn.list_images([image])
			return images[0]
		
		images = conn.list_images()
		for available_image in images:
			if available_image.id == image:
				return available_image
		return False
	
	def getNode(self, driver, conn, node):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		nodes = conn.list_nodes()
		for available_node in nodes:
			if available_node.name == node:
				return available_image
		return False		

class VnodectrlException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
