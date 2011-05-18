import base
from base import VnodectrlPlugin

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import sys; sys.path.append('..')
import utils

COMMANDS = {
	"create-node" : {
		"description": "Create node",
		"plugin": "NodeCreatePlugin",
		"name": "create-node"
	},
	"destroy-node": {
		"description": "Destroy node",
		"plugin": "NodeDestroyPlugin",
		"name": "create-node"
	}
}

class NodeCreatePlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		if len(args) < 5:
			print "You must specify your provider and an image to use."
			return False
		
		driver = args[1]
		if utils.getProvider(driver) == False:
			print "The provider you specified doesn't exist"
			return False
		
		image = args[2]
		size = args[3]
		name = args[4]
		settings = self.config["drivers"].get(args[1], False)
		
		if settings == False:
			print "You have no configuration for the driver you specified in your configuration file"
			return False
		try:
			conn = self.connect(driver, settings["id"], settings["key"])
			size = self.getSize(conn, size)
			if size == False:
				print "The size you specified does not exist. Please select a valid size"
			image = self.getImage(conn, image)
			if image == False:
				print "The image you selected does not exist."
			print "Selected size: {0} ({1})\nSelected image: {2} ({3})".format(size.id, size.name, image.id, image.name)
			print "Creating node..."
			node = conn.create_node(name=name, image=image, size=size)
			print node
		except NameError, e:
			print ">> Fatal Error: %s" % e
			print "   (Hint: modify secrets.py.dist)"
			return False
		except Exception, e:
			print ">> Fatal error: %s" % e
			return False

class NodeDestroyPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		if len(args) < 2:
			print "You must specify your provider and the node id."
			return False
		
		driver = args[1]
		if utils.getProvider(driver) == False:
			print "The provider you specified doesn't exist"
			return False
		
		node = args[2]
		settings = self.config["drivers"].get(args[1], False)
		
		if settings == False:
			print "You have no configuration for the driver you specified in your configuration file"
			return False
		try:
			conn = self.connect(driver, settings["id"], settings["key"])
			actual_node = self.getNode(conn, node)
			if (actual_node == False):
				print "The node you specified does not exist."
			print "Deleting node: {0}".format(actual_node.name)
			conn.destroy_node(actual_node)
			print "Node destroyed."
		except NameError, e:
			print ">> Fatal Error: %s" % e
			return False
		except Exception, e:
			print ">> Fatal error: %s" % e
			return False
	
	def getNode(self, conn, node):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		nodes = conn.list_nodes()
		for available_node in nodes:
			if available_node.name == node:
				return available_node
		return False
