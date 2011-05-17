import base
from base import VnodectrlPlugin

COMMANDS = {
	"list-drivers" : {
		"description": "List Drivers",
		"plugin": "ConfigPlugin",
		"name": "list-drivers"
	}
}
	
class ConfigPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;

	def execute(self, cmd):
		for driver in self.config['drivers'].keys():
			print driver
