from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements
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
		}
	},
	"ssh-security-group": {
		"description": "Get the ssh security group",
		"plugin": "SSHPlugin",
		"name": "connection-string",
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
		node = args[2]
		settings = self.config["drivers"].get(args[1], False)
		conn = self.connect(driver, settings["id"], settings["key"])
		# Fetch the appropriate node.
		node = self.getNode(driver, conn, node)
		if args[0] == 'ssh-connection-string':
			return self.connectionString(node, options)
		elif args[0] == 'ssh-security-group':
			print node.extra['keyname']
		
	def connectionString(self, node, options):
		"""
		get the connection string
		"""
		connection_string = node.public_ip[0];
		if options.remote_user is not None:
			connection_string = "{0}@{1}".format(options.remote_user, connection_string)
		print connection_string
		