from vnodectrl.base import VnodectrlPlugin
from vnodectrl import utils

COMMANDS = {
	"deploy" : {
		"description": "Deploy a project",
		"plugin": "DeployPlugin",
		"name": "deploy",
		"arguments": {
			"provider": "The provider you want to deploy to, for instance ec2-europe",
		},
	},
}

class DeployPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		if len(args) < 2:
			print "You must specify the provider you want to deploy to."
			return False
		
		driver = args[1]
		if utils.get_provider(driver) == False:
			print "The provider you specified doesn't exist"
			return False
		
		settings = self.config["drivers"].get(args[1], False)
		if settings == False:
			print "You have no configuration for the driver you specified in your configuration file"
			return False
		
		deploy_settings = self.config.get("deployment", False)
		if deploy_settings == False:
			print "No deployment settings found. Check your .vnodectrl file."
			return False
		
		if driver in deploy_settings:
			try:
				conn = self.connect(driver, settings["id"], settings["key"])
				for name, settings in deploy_settings[driver].iteritems():
					size = settings.get("size", False)
					size = self.getSize(driver, conn, size)
					if size == False:
						print "The size you specified does not exist. Please select a valid size"
					image = self.getImage(driver, conn, str(settings["image"]))
					if image == False:
						print "The image you selected does not exist."
					print "Creating node {0}. Selected size: {1} ({2})\tSelected image: {3} ({4})".format(name, size.id, size.name, image.id, image.name)
					node = conn.create_node(name=name, image=image, size=size)
					print node.__dict__
					print "node {0} created".format(node.name)
			except NameError, e:
				print ">> Fatal Error: %s" % e
				return False
			except Exception, e:
				print ">> Fatal error: %s" % e
				return False
		else:
			print "The driver selected is not present in the .vnodectrl file."
