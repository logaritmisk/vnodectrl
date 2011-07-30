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
			 	"option": ["--format"],
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
				"option": ["--format"],
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
		data = {}
		for driver,settings in self.config["drivers"].iteritems():
			if args.count(driver) > 0 or len(args) == 1:
				try:
					conn = self.connect(driver, settings["id"], settings["key"])
					if conn:
						if cmd == "list-nodes":
							data[driver] = self.listNodes(conn, options.format)
						elif cmd == "list-images":
							data[driver] = self.listImages(conn, options.format)						
				except NameError, e:
					print ">> Fatal Error: %s" % e
					return 1
				except Exception, e:
					print ">> Fatal error: %s" % e
					return 1
		if options.format == 'json':
			print json.dumps(data)
		else:
			for driver, content in data.iteritems():
				print ('{0}:').format(driver)
				for item in content:
					print "\t{0}".format(item)
			
	def listNodes(self, conn, format='default'):
		nodes = conn.list_nodes()
		node_list = []
		for node in nodes:
			if format == 'json':
				for image in images:
					node_list.append({'name': image.name, 'id': image.id})
			else:
				node_list.append("name: {0}\t id: {1}\t IP: {2}\t".format(node.name, node.id, node.public_ip))
		return node_list
	
	def listImages(self, conn, format='default'):
		images = conn.list_images()
		image_list = []
		if format == 'json':
			for image in images:
				image_list.append({'name': image.name, 'id': image.id})
		else:
			for image in images:
				image_list.append("name: {0}\t id: {1}".format(image.name, image.id))
		return image_list