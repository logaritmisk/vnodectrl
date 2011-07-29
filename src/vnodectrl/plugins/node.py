from vnodectrl.base import VnodectrlPlugin
from vnodectrl.base import libcloud_requirements
import sys; sys.path.append('..')
import json
from vnodectrl import utils
from vnodectrl import base

COMMANDS = {
	"create-node" : {
		"description": "Create node",
		"plugin": "NodeCreatePlugin",
		"name": "create-node",
		"requirements": libcloud_requirements,
		"arguments": {
			"provider" : "The provider you want to use, for instance ec2-europe",
			"image" : "The image to use for this instance. For a list of images, use vnodectrl list-images.",
			"size" : "The size of the instance you want to create.",
			"name" : "The name of the image to create."
		},
		"options": {
			"format": {
				"option": "--format",
				"default": "default",
				"description": "The format to output the data in. valid ones are:\njson\ndefault"
			}
		}					
	},
	"destroy-node": {
		"description": "Destroy node",
		"plugin": "NodeDestroyPlugin",
		"name": "destroy-node",
		"requirements": libcloud_requirements,
		"arguments" : {
			"provider" : "The provider of the node.",
			"node": "The ID of the node."
		},
		"options": {
			"format": {
				"option": "--format",
				"default": "default",
				"description": "The format to output the data in. valid ones are:\njson\ndefault"
			}
		}
	}
}

class NodeCreatePlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		self.format = options.format
		if len(args) < 5:
			self.printError("You must specify your provider and an image to use.")
			return self.finalize()
		
		driver = args[1]
		if base.get_provider(driver) == False:
			return self.printError("The provider you specified doesn't exist")
			
		
		image = args[2]
		size = args[3]
		name = args[4]
		settings = self.config["drivers"].get(args[1], False)
		
		if settings == False:
			return self.printError("You have no configuration for the driver you specified in your configuration file")
		try:
			conn = self.connect(driver, settings["id"], settings["key"])
			size = self.getSize(driver, conn, size)
			if size == False:
				return self.printError("The size you specified does not exist. Please select a valid size")
			image = self.getImage(driver, conn, image)
			if image == False:
				return self.printError("The image you selected does not exist.")
			self.printMessage("Selected size: {0} ({1})\nSelected image: {2} ({3})".format(size.id, size.name, image.id, image.name))
			self.printMessage("Creating node...")
			node = conn.create_node(name=name, image=image, size=size)
			self.printMessage(node)
			self.printNode(node)
		except NameError, e:
			return self.printError(">> Fatal Error: %s" % e)
		except Exception, e:
			return self.printError(">> Fatal error: %s" % e)
		
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
	def printNode(self, node):
		if self.format == 'json':
			json_result = {
				'status': 'ok',
				'node': {
					'id': node.id,
					'name': node.name,
					'extra': node.extra
				}
			}
			print json.dumps(json_result)
		else:
			print "{0}: {1}".format(node.id, node.name)
			print "extra:"
			for key, value in node.extra.iteritems():
				print "{0}: {1}".format(key, value)

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
