from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements, get_connection_string
import sys; sys.path.append('..')
from fabric.api import settings, run, sudo
COMMANDS = {
	"puppet-connect" : {
		"description": "Connect a node to a puppet master",
		"plugin": "PuppetPlugin",
		"name": "puppet-connect",
		"requirements": libcloud_requirements,
		"arguments": {
			"driver": "Driver",
			"puppet": "The node to connect",
			"master": "The master node"
		},
	},
}

class PuppetPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;
		
	def execute(self, cmd, args, options):
		driver = args[1]
		puppet_name = args[2]
		master_name = args[3]
		settings = self.config["drivers"].get(args[1], False)
		conn = self.connect(driver, settings["id"], settings["key"])
		puppet_node = self.getNode(driver, conn, puppet_name)
		master_node = self.getNode(driver, conn, master_name)
		puppet_string = get_connection_string(puppet_node)	
		master_string = get_connection_string(master_node)
		with settings(host_string=puppet_string):
			run('echo hej')
		


		