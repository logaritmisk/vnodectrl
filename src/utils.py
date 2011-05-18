import json
from libcloud.compute.types import Provider

def getConfig(path):
	data = open(path);
	return json.load(data);


def getProvider(driver):
	"""
	Get a provider based on the string in the config.
	"""
	drivers = {
		"ec2-europe": Provider.EC2_EU_WEST
		# Just fill out the rest of the gang later on.
	}
	return drivers.get(driver, False);
