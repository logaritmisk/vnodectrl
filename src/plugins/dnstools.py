import base
from base import VnodectrlPlugin	
import bindutil
import dns.zone
COMMANDS = {
	"dns-record-add" : {
		"description": "Add DNS record",
		"plugin": "DNSPlugin",
		"name": "bind-record-add"
	},
	"dns-record-delete" : {
		"description": "Delete DNS record.",
		"plugin": "DNSPlugin",
		"name": "dns-record-delete"
	},
	"dns-record-list" : {
		"description": "List DNS Records in zone.",
		"plugin": "DNSPlugin",
		"name": "dns-record-list"						
	}
}

class DNSPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		"""
		Main dispatcher for all commands.
		"""
		self.zone = dns.zone.from_file(str(self.config['dns']['zone_file']), str(self.config['dns']['domain']));
		self.listRecords();
		
	def listRecords(self):
		"""
		Print all records in the zone
		"""
		print "Records in zone:"
		for name, node in self.zone.nodes.items():
			print name
