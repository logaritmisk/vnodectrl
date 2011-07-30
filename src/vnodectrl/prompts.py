"""
This module contains some prompts that are used in various places throughout the program
"""

def dict_prompt(dictionary, type):
    print "Select a {0}:".format(type)
    print "0. Cancel"
    items = dictionary.items()
    i = 1
    for name in dictionary.iterkeys():
        print "{0}. {1}".format(i, name)
        i += 1
    option = int(input())
    if option == 0:
        return False
    items_len = len(items)
    if len(items) >= option:
        return items[option-1]
    return dict_prompt(dictionary, type)

def node_prompt(nodes, message="Select a node:"):
    print message
    print "0. Cancel"
    i = 1
    for node in nodes:
        print "{0}. {1}".format(i, "{0}({1})".format(node.name, node.id))
        i += 1
    option = int(input())
    if option == 0:
        return False
    if len(nodes) >= option:
        return nodes[option-1]
    return node_prompt(nodes, message)