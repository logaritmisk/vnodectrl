from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements
import sys; sys.path.append('..')
import json

COMMANDS = {
	"list-nodes" : {
		"description": "List nodes",
		"plugin": "ListPlugin",
		"name": "list-nodes",
		"requirements": libcloud_requirements,
		"arguments": {
			"provider" : "The provider to list nodes from, for instance ec2-europe."
		},
		"options": {
			"format": {
			 	"option": "--format",
				"default": "default",
				"description": "The format to output the data in. valid ones are:\njson\ndefault"
			}
		}
	},
	"list-images" : {
		"description": "List images",
		"plugin": "ListPlugin",
		"name": "list-images",
		"arguments": {
			"provider" : "The provider to list nodes from, for instance ec2-europe."
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

class ListPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;
		
	def execute(self, cmd, args, options):
		for driver,settings in self.config["drivers"].iteritems():
			if args.count(driver) > 0 or len(args) == 1:
				try:
					conn = self.connect(driver, settings["id"], settings["key"])
					if cmd == "list-nodes":
						self.listNodes(conn, options.format)
					elif cmd == "list-images":
						self.listImages(conn, options.format)
				except NameError, e:
					print ">> Fatal Error: %s" % e
					print "   (Hint: modify secrets.py.dist)"
					return 1
				except Exception, e:
					print ">> Fatal error: %s" % e
					return 1
	def listNodes(self, conn, format='default'):
		nodes = conn.list_nodes()
		for node in nodes:
			print "name: {0}\t id: {1}\t IP: {2}\t".format(node.name, node.id, node.public_ip)
	
	def listImages(self, conn, format='default'):
		images = conn.list_images()
		if format == 'default':
			for image in images:
				print "name: {0}\t id: {1}".format(image.name, image.id)
		elif format == 'json':
			json_images = []
			for image in images:
				json_images.append({'name': image.name, 'id': image.id})
			print json.dumps(json_images)