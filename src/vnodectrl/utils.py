import os.path
import json
import plugins


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
			# If there is a 
			if 'requirements' not in options or options['requirements']():
				options['module'] = module
				commands[command] = options
	return commands
	# @todo: Let users specify packates from which we should fetch
	# other plugins not in the core distribution.
	
def get_main_config():
	'''
	Get the main configuration file.
	'''
	# Check if this user has their own vnodectrl configuration.
	config_file = "{0}/.vnodectrl.d/3.x/vnodectrl.conf".format(os.getenv("HOME"));
	if os.path.exists(config_file):
		return get_config(config_file)
	# Otherwise load the global configuration file.
	return get_config('/etc/vnodectrl/vnodectrl.conf')
	