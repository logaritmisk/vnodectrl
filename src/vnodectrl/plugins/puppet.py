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
		"flags": {
			"interactive": {
				"on": ['-i', '--interactive'],
				"default": False
			}
		}
	},
}

class PuppetPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;
		
	def execute(self, cmd, args, options):
		driver, settings = self.getDriverFromArg(args, 1, options.interactive);
		conn = self.connect(driver, settings["id"], settings["key"])
		puppet_node = self.getNodeFromArg(args, 2, driver, conn, options.interactive, "Select puppet node:")
		master_node = self.getNodeFromArg(args, 3, driver, conn, options.interactive, "Select master node:")
		puppet_string = get_connection_string(puppet_node)
		master_string = get_connection_string(master_node)
		master_ip = master_node.public_ip[0]
		puppet_args = {"host_string": puppet_string}
		if "keyname" in puppet_node.extra:
			key = find_key_file(puppet_node.extra['keyname'])
			if key:
				puppet_args['key_filename'] = key
		with fabric.api.settings(**puppet_args):
			self.puppetConnect(master_ip)
	
	def puppetConnect(self, master_ip):
		"""
		Connect the puppet client to the master.
		"""
		run('puppet agent --server {0} --waitforcert 60 --test'.format(master_ip))
	
	def puppetAccept(self, client_ip):
		"""
		Accept a client.
		"""
		run('puppet cert --sign --test'.format(client_ip))


		