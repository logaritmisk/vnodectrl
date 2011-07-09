from vnodectrl.base import VnodectrlPlugin
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import sys; sys.path.append('..')
from vnodectrl import utils

COMMANDS = {
	"create-node" : {
		"description": "Create node",
		"plugin": "NodeCreatePlugin",
		"name": "create-node",
		"arguments": {
			"provider" : "The provider you want to use, for instance ec2-europe",
			"image" : "The image to use for this instance. For a list of images, use vnodectrl list-images.",
			"size" : "The size of the instance you want to create.",
			"name" : "The name of the image to create."
		}
	},
	"destroy-node": {
		"description": "Destroy node",
		"plugin": "NodeDestroyPlugin",
		"name": "destroy-node",
		"arguments" : {
			"provider" : "The provider of the node.",
			"node": "The ID of the node."
		}
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
		if utils.get_provider(driver) == False:
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
		if utils.get_provider(driver) == False:
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
