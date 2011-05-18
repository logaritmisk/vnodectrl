import base
from base import VnodectrlPlugin

from libcloud.compute.types import Provider
from libcloud.providers import get_driver
import sys; sys.path.append('..')
import utils

COMMANDS = {
	"list-nodes" : {
		"description": "List nodes",
		"plugin": "ListPlugin",
		"name": "list-nodes"
	},
	"list-images" : {
		"description": "List nodes",
		"plugin": "ListPlugin",
		"name": "list-images"
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
			print "name: {0}\t instance: {1}\t ip: {2}\t status: {3}\t type: {4}".format(node.name, node.extra["imageId"], node.public_ip[0], node.extra["status"], node.extra["instancetype"])
	
	def listImages(self, conn):
		images = conn.list_images()
		for image in images:
			print "name: {0}\t id: {1}".format(image.name, image.id)
