import os
import os.path
import json
from libcloud.compute.types import Provider

def getConfig(path):
	try:
		data = open(path);
		return json.load(data)
	except Exception, e:
		return False

def getProvider(driver):
	"""
	Get a provider based on the string in the config.
	"""
	drivers = {
		"ec2-europe": Provider.EC2_EU_WEST
		# Just fill out the rest of the gang later on.
	}
	return drivers.get(driver, False)

def getDeploymentConfig(path = os.getcwd()):
	"""
	Get deployment configuration.
	"""
	deployfile = "{0}/.vnodectrl".format(path)
	if path == '/':
		return False
	if os.path.isfile(deployfile):
		return getConfig(deployfile)
	else:
		return getDeploymentConfig(os.path.split(path)[0])
