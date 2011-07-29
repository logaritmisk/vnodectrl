from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements
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
		node = args[2]
		settings = self.config["drivers"].get(args[1], False)
		conn = self.connect(driver, settings["id"], settings["key"])
		# Fetch the appropriate node.
		node = self.getNode(driver, conn, node)
		if args[0] == 'ssh-connection-string':
			return self.connectionString(node, options)
		elif args[0] == 'ssh-ec2-keyfile':
			home_key_file = "{0}/.vnodectrl.d/3.x/keys/{1}.pem".format(getenv("HOME"), node.extra['keyname']);
			global_key_file = "/etc/vnodectrl/keys/{0}.pem".format(node.extra['keyname']);
			if isfile(home_key_file):
				print home_key_file
			elif isfile(global_key_file):
				print global_key_file
			else:
				print "The key file is not present on this system."
		
	def connectionString(self, node, options):
		"""
		get the connection string
		"""
		connection_string = node.public_ip[0];
		if options.remote_user is not None:
			connection_string = "{0}@{1}".format(options.remote_user, connection_string)
		print connection_string
		