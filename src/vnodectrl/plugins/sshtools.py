from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements, get_connection_string
from os.path import isfile
from os import getenv
import sys; sys.path.append('..')
import json
COMMANDS = {
	"ssh-connection-string" : {
		"description": "Get a working ssh connection string",
		"plugin": "SSHPlugin",
		"name": "connection-string",
		"requirements": libcloud_requirements,
		"arguments": {
			"driver": "Driver",
			"node" : "Id of the machine to get a connection string for",
		},
	    "options": {
			"remote_user": {
				"option": "--remote-user",
				"default": "ubuntu",
				"description": "The remote user that should be returned."
			},
			"interactive": {
				"option": "--interactive",
				"default": True,
				"description": "Provide interactive help if necessary."
			}
		}
	},
	"ssh-ec2-keyfile": {
		"description": "Get the path to tge ssh key file if it's available for this user.",
		"plugin": "SSHPlugin",
		"name": "ssh-ec2-keypair",
		"requirements": libcloud_requirements,
		"arguments": {
			"driver": "Driver",
			"node" : "Id of the machine to get a connection string for",
		},
	}
}

class SSHPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;
		
	def execute(self, cmd, args, options):
		driver = args[1]
		settings = self.config["drivers"].get(args[1], False)
		conn = self.connect(driver, settings["id"], settings["key"])
		if len(args) > 2:
			node = args[2]
			node = self.getNode(driver, conn, node)
			print self.processNode(cmd, args, options, node)
		else:
			nodes = conn.list_nodes()
			for current_node in nodes:
				print "{0}({1}): {2}".format(current_node.name, current_node.id, self.processNode(cmd, args, options, current_node))
	
	def processNode(self, cmd, args, options, node):
		if args[0] == 'ssh-connection-string':
			return get_connection_string(node, options.remote_user)
		elif args[0] == 'ssh-ec2-keyfile':
			home_key_file = "{0}/.vnodectrl.d/3.x/keys/{1}.pem".format(getenv("HOME"), node.extra['keyname']);
			global_key_file = "/etc/vnodectrl/keys/{0}.pem".format(node.extra['keyname']);
			if isfile(home_key_file):
				return home_key_file
			elif isfile(global_key_file):
				return global_key_file
			else:
				return "The key file is not present on this system."
		