import sys; sys.path.append('..')
import utils
import json
from os import getenv
from os.path import isfile
from vnodectrl.prompts import *
try:
	from libcloud.compute.types import Provider
	from libcloud.compute.providers import get_driver
	import libcloud.security
   	libcloud.security.VERIFY_SSL_CERT = True
except ImportError:
	'''
	'''

class VnodectrlOptions:
	def options(self):
		"""
		Declare all options here.
		"""

class VnodectrlPlugin:
	format = 'default'
	
	def commands(self):
		"""
		Declare all commands here.
		"""
	def help(self, cmd):
		"""
		Specify help for a specific command here.
		"""

	def execute(self, cmd):
		"""
		Act on a particular command here
		"""
	def connect(self, driver, user_id = "NaN", key = "NaN"):
		"""
		Connect with a particular driver using a userid
		and a key.
		"""
		try:
			driver_class = get_provider(driver)
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
			if available_node.id == node:
				return available_node
		return False
	
	def printError(self, error):
		if self.format == 'json':
			print json.dumps({'status': 'error', 'message': error});
		else:
			print error
		return False;

	def printMessage(self, message):
		if self.format == 'json':
			return
		print message
	
	def printSuccess(self, message):
		if (self.format == 'json'):
			print json.dumps({'status': 'ok', 'message': message});
		else:
			print message
		return True
	
	def printNode(self, node):
		if self.format == 'json':
			json_result = {
				'status': 'ok',
				'node': {
					'id': node.id,
					'private_ips': node.private_ip,
					'public_ips': node.public_ip,
					'name': node.name,
					'extra': node.extra
				}
			}
			print json.dumps(json_result)
		else:
			print "{0}: {1}".format(node.id, node.name)
			print "Private IP addresses:"
			for ip in node.private_ip:
				print "\t{0}".format(ip)
			print "Public IP addresses:"
			for ip in node.public_ip:
				print "\t{0}".format(ip)
			print "Extra:"
			for key, value in node.extra.iteritems():
				print "\t{0}: {1}".format(key, value)
	
	def getDriverFromArg(self, args, arg_index, interactive = True):
		driver = False
		settings = False
		if len(args) > arg_index:
			driver = args[arg_index]
			settings = self.config["drivers"].get(args[1], False)
		if not settings and interactive:
			driver, settings = dict_prompt(self.config["drivers"], "Driver")
		return driver, settings
	
	def getNodeFromArg(self, args, arg_index, driver, conn, interactive = False, message="Select node:"):
		node = False
		if len(args) > arg_index: 
			node = self.getNode(driver, conn, args[arg_index])
		if not node and interactive:
			nodes = conn.list_nodes()
			return node_prompt(nodes, message=message)
		return node
	def getSizeFromArg(self, args, arg_index, driver, conn, interactive = False, message="Select size:"):
		size = False
		if len(args) > arg_index: 
			size = size = self.getSize(driver, conn, args[arg_index])
		if not size and interactive:
			sizes = conn.list_sizes()
			return size_prompt(sizes, message=message)
		return size
	def getImageFromArg(self, args, arg_index, driver, conn, interactive = False, message = "Enter the name of the image. Enter 0 to cancel."):
		image = False
		if len(args) > arg_index: 
			image = self.getImage(driver, conn, args[arg_index])
		if not image and interactive:
			return self.imagePrompt(driver, conn, message)
		return image
	
	def imagePrompt(self, driver, conn, message):
		print message
		image = str(raw_input())
		if image == 0:
			return False
		image = self.getImage(driver, conn, image)
		if not image:
			return self.imagePrompt(driver, conn)
		return image	

class VnodectrlException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def libcloud_requirements():
	'''
	This function can be used to determine if libcloud exists.
	It also loads all required modules that might not be present
	in the system.
	It returns True if the requirements are met and false otherwise.
	'''
	try:
		from libcloud.compute.types import Provider
		from libcloud.compute.providers import get_driver
		return True
	except ImportError:
		return False
	
def get_provider(driver):
	'''
	Get a provider based on the string in the config.
	'''
	drivers = {
		"ec2-europe": Provider.EC2_EU_WEST,
		"virtualbox": "virtualbox"
		# Just fill out the rest of the gang later on.
	}
	# Try to import the virtualbox driver. Some clients might not have
	# virtualbox installed, so if they don't, just remove the driver.
	try:
		import virtualbox
	except ImportError:
		del drivers['virtualbox']

	if driver in drivers:
		real_driver = drivers[driver]
		# The Virtualbox driver is not really included in liblcoud,
		# so we add it ourselves here.
		if driver == "virtualbox":
			return virtualbox.VirtualBoxNodeDriver	
		
		return get_driver(real_driver)
	
	return False

def get_connection_string(node, remote_user="ubuntu"):
	"""
	Get the connection string for a particular node.
	"""
	connection_string = node.public_ip[0];
	return "{0}@{1}".format(remote_user, connection_string)

def find_key_file(name):
	"""
	Find a key file for a specific keypair, if it is available.
	"""
	home_key_file = "{0}/.vnodectrl.d/3.x/keys/{1}.pem".format(getenv("HOME"), name);
	global_key_file = "/etc/vnodectrl/keys/{0}.pem".format(name);
	if isfile(home_key_file):
		return home_key_file
	elif isfile(global_key_file):
		return global_key_file
	return False