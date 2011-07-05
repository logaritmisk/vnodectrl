'''
Created on 5 jul 2011

@author: fabsor
'''
import json
from base import VnodectrlPlugin
COMMANDS = {
    "list-plugins" : {
        "description": "List all available plugins in different formats",
        "plugin": "PluginInfo",
        "name": "list-plugins"
    }
}

class PluginInfo(VnodectrlPlugin):
    '''
    This plugin returns information on available vnodectrl commands in
    different formats.
    '''
    def __init__(self, config):
        '''
        Constructor
        '''
        self.config = config;
    def execute(self, cmd, args, options):
        from vnodectrl import commands
        json_export = []
        for command, options in commands.iteritems():
            # Delete module, since it's not serializable. 
            del options['module']
            options['command'] = command
            json_export.append(options)
        print json.dumps(json_export)
            