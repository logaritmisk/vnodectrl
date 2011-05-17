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
					Driver = get_driver(utils.getProvider(str(driver)))
					conn = Driver(str(settings["id"]), str(settings["key"]))
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
			print "Provider: {0}\t name: {1}\t ip: {2}".format(driver,node.name, node.public_ip[0])
	
	def listImages(self, conn):
		images = conn.list_images()
		for image in images[:10]:
			print "name: {0}".format(image.name)
