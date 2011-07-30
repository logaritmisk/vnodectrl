from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements, get_connection_string, find_key_file
from fabric.api import run, sudo
from vnodectrl.prompts import dict_prompt, node_prompt
import fabric.api
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
		if len(args) > 1:
			settings = self.config["drivers"].get(args[1], False)
		else:
			driver, settings = dict_prompt(self.config["drivers"], "Driver")
			if not driver:
				return False
		conn = self.connect(driver, settings["id"], settings["key"])
		if len(args) > 2: 
			puppet_node = self.getNode(driver, conn, args[2])
		else:
			nodes = conn.list_nodes()
			puppet_node = node_prompt(nodes, message="Select the puppet node:")
		if len(args) > 3:
			master_node = self.getNode(driver, conn, puppet_name)
		else:
			if not nodes:
				nodes = conn.list_nodes() 
			master_node = node_prompt(nodes, message="Select the master node:")

		puppet_string = get_connection_string(puppet_node)
		master_string = get_connection_string(master_node)
		puppet_args = {"host_string": puppet_string}
		if "keyname" in puppet_node.extra:
			key = find_key_file(puppet_node.extra['keyname'])
			if key:
				puppet_args['key_filename'] = key
		with fabric.api.settings(**puppet_args):
			self.puppetConnect()
	
	def puppetConnect(self):
		run('echo hej')
		


		