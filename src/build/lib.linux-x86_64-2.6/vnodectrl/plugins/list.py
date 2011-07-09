from vnodectrl.base import VnodectrlPlugin
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import sys; sys.path.append('..')

COMMANDS = {
	"list-nodes" : {
		"description": "List nodes",
		"plugin": "ListPlugin",
		"name": "list-nodes",
		"arguments": {
			"provider" : "The provider to list nodes from, for instance ec2-europe."
		}
	},
	"list-images" : {
		"description": "List images",
		"plugin": "ListPlugin",
		"name": "list-images",
		"arguments": {
			"provider" : "The provider to list nodes from, for instance ec2-europe."
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
						self.listNodes(conn)
					elif cmd == "list-images":
						self.listImages(conn)
				except NameError, e:
					print ">> Fatal Error: %s" % e
					print "   (Hint: modify secrets.py.dist)"
					return 1
				except Exception, e:
					print ">> Fatal error: %s" % e
					return 1
	def listNodes(self, conn):
		nodes = conn.list_nodes()
		for node in nodes:
			print "name: {0}\t id: {1}\t IP: {2}\t".format(node.name, node.id, node.public_ip)
	
	def listImages(self, conn):
		images = conn.list_images()
		for image in images:
			print "name: {0}\t id: {1}".format(image.name, image.id)
