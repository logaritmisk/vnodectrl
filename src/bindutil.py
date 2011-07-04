import os
import re

# We store our helpers in here so that other people can add their own helpers by
# adding them to this dictionary.
BIND_HELPERS = {
    "ubuntu" : "UbuntuBindHelper"
}

def get_bind_helper(identifier):
    helper = getattr(__name__, BIND_HELPERS[identifier]);
    return helper;
    

class BindHelper:
    """
    Base class for Bind Helpers.
    It serves as an interface for other BindHelpers.
    """
    def getZones(self):
        """
        Get a list of zones that we can manipulate, each zone is it's
        own subclass.
        """
        return {}


class UbuntuBindHelper:
    """
    This class can get information about the current BIND configuration
    given an Ubuntu BIND configuration directory. This is very non-generic stuff.
    """
    def __init__(self, conf_path):
        self.conf_path = conf_path
        # Zone path is the conf path + /zones by default.
        self.zone_path = "{0}/{1}".format(conf_path, "/zones");
    
    def getZones(self):
        # Load zones if we haven't already.
        self.loadZones()

    def getZone(self, domain):
        return self.zones[domain];

    def loadZones(self, path):
        """
        Load all zones by looking for zone files in the specified zones directory.
        """
        files = os.listdir(path);
        for zone_file in files:
            # Build full path
            full_path = "{0}/{1}".format(self.zone_path, zone_file)
            # If this is a file, scan it for contents and add them to the zones.
            # otherwise, we look recursively for other zones.
            if os.path.isdir(path):
                self.LoadZones(path)
            else:
                zone = self.parseZone(full_path)
                self.zones[zone.name] = zone

            
    def parseZone(self, zone_file):
        """
        Parses a zone. This is a very brute force and incomplete attempt at doing
        so, better parsing mechanics are needed later on.
        """
        handler = open(zone_file)
        try:
            content = handler.readLines();
            ttl = re.search('$TTL ([0-9]+[h|D|Y])', content).group(1)
            nameservers = re.split('IN SOA ([A-Za-z0-9_\.-]+*)', content);
            domain = re.search('([A-Za-z0-9_\.-]+)\s?', content).group(1)
            serials = re.search('\(\s?([0-9]+)\n([0-9]+[d|m|s|Y|m|M|D]\n)[0,3]\s?\)')
            serial = serials.group(0)
            slave_refresh = serials.group(1)
            slave_retry = serials.group(2)
            slave_expiration = serials.group(2)
            maximum_cache_age = serials.group(4)
            records = re.split("[([A-Za-z0-9_\.-]+*)\n?]+", content);
            return BindZone(domain, serial, nameservers, ttl, slave_refresh, slave_retry, slave_expiration, maximum_cache_age, records);
        finally:
            handler.close()
        return False

class BindZone:
    """
    This class represents a DNS Zone. It has some
    nice utility functions that can be used for adding and removing
    domains etc.
    """
    def __init__(self, domain, serial, nameservers,ttl='1h', slave_refresh='1d', slave_retry='2h', slave_expiration='4w', maximum_cache_age='1h', records={}):
        self.ttl = ttl
        self.domain = domain
        self.serial = serial
        self.slave_refresh = slave_refresh
        self.slave_retry = slave_retry
        self.slave_expiration = slave_expiration
        self.maximum_cache_age = maximum_cache_age
        self.nameservers = nameservers
        self.records = records

    def addRecord(self, ip, record_type, name):
        self.records[name] = {'ip' : ip, 'type': record_type, 'name' : name}

    def getRecords(self):
        return self.records

    def compile_records(self):
        record_str = ''
        for record in self.records:
            record_str.append("{0}\t{1}\t{2}".format(record['ip'], record['type'], record['name']))
        return record_str

    def __str__(self):
        records = self.compile_records();
        "$ORIGIN {domain}\n\
        $TTL {ttl}\n\
        {domain} IN SOA {nameservers} (\n\
        {serial}\n\
        {slave_referesh}\n\
        {slave_retry}\n\
        {slave_expiration}\n\
        {maximum_cache_age}\n\
        )\n\
        {records}".format(domain=self.domain, ttl=self.ttl, serial=self.serial, self_refresh=self.self_refresh, slave_retry=self.slave_retry, slave_expiration=self.slave_expiration, maximum_cache_age=self.maximum_cache_age, records=records)
        
