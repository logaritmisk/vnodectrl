from vnodectrl.base import VnodectrlPlugin
from vnodectrl.base import libcloud_requirements
import sys; sys.path.append('..')
import json
from vnodectrl import utils
from vnodectrl import base
from dns.rdatatype import NULL

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
				"option": ["-f", "--format"],
				"default": "default",
				"description": "The format to output the data in. valid ones are:\njson\ndefault"
			},
			"ec2_securitygroup": {
				"option": ["--ec2-securitygroup"],
				"default": None,
				"description": "The EC2 Security group this node should belong to. This is only applicable for EC2"
			},
			"ec2_keypair": {
				"option": ["--ec2-keypair"],
				"default": None,
				"description": "The EC2 keypair this node should belong to."
			}				
		},
		"flags": {
			"interactive": {
				"on": ['-i', '--interactive'],
				"default": False
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
				"option": ["--format"],
				"default": "default",
				"description": "The format to output the data in. valid ones are:\njson\ndefault"
			}
		}
	},
	"node-info": {
		"description": "Get node information",
		"plugin": "NodeInfoPlugin",
		"name": "node-info",
		"requirements": libcloud_requirements,
		"arguments" : {
			"provider" : "The provider of the node.",
			"node": "The ID of the node."
		},
		"options": {
			"format": {
				"option": ["-f", "--format"],
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
		if not options.interactive and len(args) < 5:
			return self.printError("You must specify your provider and an image to use.")
		
		driver, settings = self.getDriverFromArg(args, 1, options.interactive)	
		conn = self.connect(driver, settings["id"], settings["key"])
		image = self.getImageFromArg(args, 2, driver, conn, options.interactive)
		size = self.getSizeFromArg(args, 3, driver, conn, options.interactive)
		name = args[4]
		try:
			self.printMessage("Selected size: {0} ({1})\nSelected image: {2} ({3})".format(size.id, size.name, image.id, image.name))
			self.printMessage("Creating node...")
			parameters = {
				'name': name,
				'image': image,
				'size': size
			}
			if options.ec2_securitygroup is not None:
				parameters["ex_securitygroup"] = options.ec2_securitygroup
			if options.ec2_keypair is not None:
				parameters["ex_keyname"] = options.ec2_keypair
			node = conn.create_node(**parameters)
			self.printMessage(node)
			self.printNode(node)
		except NameError, e:
			return self.printError(">> Fatal Error: %s" % e)
		except Exception, e:
			return self.printError(">> Fatal error: %s" % e)
		

class NodeDestroyPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		self.format = options.format
		if len(args) < 2:
			return self.printError("You must specify your provider and the node id.")
		
		driver = args[1]
		if base.get_provider(driver) == False:
			return self.printError("The provider you specified doesn't exist")
		
		node = args[2]
		settings = self.config["drivers"].get(args[1], False)
		
		if settings == False:
			return self.printError("You have no configuration for the driver you specified in your configuration file")
		try:
			conn = self.connect(driver, settings["id"], settings["key"])
			actual_node = self.getNode(conn, node)
			if (actual_node == False):
				return self.printError("The node you specified does not exist.")
			self.printMessage("Deleting node: {0}".format(actual_node.name))
			conn.destroy_node(actual_node)
			return self.printSuccess("Node destroyed");
		except NameError, e:
			return self.printError(">> Fatal Error: %s" % e)
		except Exception, e:
			return self.printError(">> Fatal error: %s" % e)
	
	def getNode(self, conn, node):
		# TODO: There are way more elegant ways
		# to do this in python, I just can't be
		# bothered to look them up atm.
		nodes = conn.list_nodes()
		for available_node in nodes:
			if available_node.name == node:
				return available_node
		return False

class NodeInfoPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config

	def execute(self, cmd, args, options):
		self.format = options.format
		if len(args) < 2:
			return self.printError("You must specify your provider and the node id.")
		
		driver = args[1]
		if base.get_provider(driver) == False:
			return self.printError("The provider you specified doesn't exist")
		
		node = args[2]
		settings = self.config["drivers"].get(args[1], False)
		
		if settings == False:
			return self.printError("You have no configuration for the driver you specified in your configuration file")
		
		try:
			conn = self.connect(driver, settings["id"], settings["key"])
			actual_node = self.getNode(driver, conn, node)
			if (actual_node == False):
				return self.printError("The node you specified does not exist.")
			self.printNode(actual_node)
		except NameError, e:
			return self.printError(">> Fatal Error: %s" % e)
		except Exception, e:
			return self.printError(">> Fatal error: %s" % e)
