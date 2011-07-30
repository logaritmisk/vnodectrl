"""
Main file that can be executed directly.
"""
import os
import sys
import vnodectrl.plugins
from vnodectrl import utils
from optparse import OptionParser
from vnodectrl.plugins import *

def main(args):
    commands = {}
    # Locate the configuration.
    configuration = utils.get_main_config()
    if configuration == False:
        print "No configuration available. Make sure everything is installed properly"
        return 1

    # Locate deployment instructions.
    configuration["deployment"] = utils.get_deployment_config()

    # Get all commands.
    commands = utils.get_commands()
    if len(args) > 1:
        primary_command = args[1];
        command_info = commands.get(primary_command, None);
        if command_info != None:
            parser = OptionParser()
            if "options" in command_info:
                for option_name, option in command_info["options"].iteritems():
                    if "type" not in option:
                        option['type'] = 'string'
                    parser.add_option(*option["option"], action="store", type=option['type'], default=option["default"])
            if "flags" in command_info:
                for flag_name, flag_option in command_info["flags"].iteritems():
                    if 'on' in flag_option:
                        parser.add_option(*flag_option['on'], action="store_true", dest=flag_name)
                    if 'off' in flag_option:
                        parser.add_option(*flag_option['off'], action="store_false", dest=flag_name)
            
            (options, command_args) = parser.parse_args() 
            plugin_class = getattr(command_info['module'], command_info['plugin'])
            plugin = plugin_class(configuration)
            return plugin.execute(primary_command, command_args, options)
        else:
            print "Unrecognized command"

    else:
        print "Available Commands:\n"
        for command, options in commands.iteritems():
            print "{0}\t{1}".format(command, options['description']);

sys.exit(main(sys.argv))
