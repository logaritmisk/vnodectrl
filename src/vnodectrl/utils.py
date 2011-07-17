import os.path
import json
import plugins
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

def get_config(path):
	'''
	Get configuration in the form of a dictionary
	from a configuration file on the given path.
	'''
	try:
		data = open(path);
		return json.load(data)
	except Exception, e:
		print "Syntax error: {0}".format(e)
		return False

def get_provider(driver):
	'''
	Get a provider based on the string in the config.
	'''
	drivers = {
		"ec2-europe": Provider.EC2_EU_WEST,
		"virtualbox": "virtualbox"
		# Just fill out the rest of the gang later on.
	}
	# Try to import the virtualbox driver. Some clients might not have
	# virtualbox installed, so if they don't, just remove the driver.
	try:
		import virtualbox
	except ImportError:
		del drivers['virtualbox']

	if driver in drivers:
		real_driver = drivers[driver]
		# The Virtualbox driver is not really included in liblcoud,
		# so we add it ourselves here.
		if driver == "virtualbox":
			return virtualbox.VirtualBoxNodeDriver	
		
		return get_driver(real_driver)
	
	return False

def get_deployment_config(path = os.getcwd()):
	'''
	Get deployment configuration.
	'''
	deployfile = "{0}/.vnodectrl".format(path)
	if path == '/':
		return False
	if os.path.isfile(deployfile):
		print deployfile
		return get_config(deployfile)
	else:
		return get_deployment_config(os.path.split(path)[0])

def get_commands():
	'''
	Get all vnodectrl plugins available.
	'''
	commands = {}
	modules = []
	# Load Core plugins
	for plugin in plugins.__all__:
		module = getattr(plugins, plugin)
		modules.append(module)
		for command, options in module.COMMANDS.iteritems():
			options['module'] = module
			commands[command] = options
	return commands
	# @todo: Let users specify packates from which we should fetch
	# other plugins not in the core distribution.
	
	
