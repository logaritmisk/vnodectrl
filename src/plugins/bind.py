import base
from base import VnodectrlPlugin
import bindutil

COMMANDS = {
	"bind-zone-add" : {
		"description": "Add DNS zone",
		"plugin": "BindPlugin",
		"name": "bind-zone-add"
	},		
	"bind-record-add" : {
		"description": "Add DNS record",
		"plugin": "BindPlugin",
		"name": "bind-add"
	},
	"bind-record-delete" : {
		"description": "Delete DNS record.",
		"plugin": "BindPlugin",
		"name": "bind-remove"
	},
	"bind-zone-list" : {
		"description": "list DNS Zones",
		"plugin": "BindPlugin",
		"name": "bind-list"
	}
}

class BindPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		"""
		Main dispatcher for all commands.
		"""
		# We will always need a BindHelper class to help us here.
		helper_class = bindutil.get_bind_helper("ubuntu")
		self.bind = helper_class("/etc/bind")
		self.bindZoneList(options)
	
	def bindZoneList(self, config):
		print self.bind.getZones()
