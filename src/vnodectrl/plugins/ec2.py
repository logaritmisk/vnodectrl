from vnodectrl.base import VnodectrlPlugin, libcloud_requirements
from vnodectrl.base import libcloud_requirements
import sys; sys.path.append('..')
COMMANDS = {
	"ec2-describe-keypair" : {
		"description": "Get a working ssh connection string",
		"plugin": "EC2KeyPairPlugin",
		"name": "ec2-describe-keypair",
		"requirements": libcloud_requirements,
		"arguments": {
			"driver": "Driver",
			"name": "keypair name"
		},
	},
	"ec2-create-keypair" : {
		"description": "Create a keypair",
		"plugin": "EC2KeyPairPlugin",
		"name": "ec2-describe-keypair",
		"requirements": libcloud_requirements,
		"arguments": {
			"driver": "Driver",
			"name": "keypair name"
		},
	},		
}

class EC2KeyPairPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config;
		
	def execute(self, cmd, args, options):
		driver = args[1]
		keypair = args[2]
		settings = self.config["drivers"].get(args[1], False)
		conn = self.connect(driver, settings["id"], settings["key"])
		if args[0] == 'ec2-describe-keypair':
			print conn.ex_describe_keypairs(keypair)
		elif args[0] == 'ec2-create-keypair':
			print conn.ex_create_keypair(keypair)


		