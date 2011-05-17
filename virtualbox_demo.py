#!/usr/bin/env python

# from libcloud.compute.types import Provider
# from libcloud.providers import get_driver

from time import sleep
from pprint import pprint

from virtualbox import VirtualBoxNodeDriver


def main():
	vbox_driver = VirtualBoxNodeDriver()
	
	nodes = vbox_driver.list_nodes()
	pprint(nodes)
    
	images = vbox_driver.list_images(['nodeone-virtual0.ovf'])
	pprint(images)
	
	sizes = vbox_driver.list_sizes()
	pprint(sizes)
	
	node = vbox_driver.create_node(name='my-new-awesome-node', image=images[0], size=sizes[0])
	pprint(node)
	
	sleep(25)
	
	nodes = vbox_driver.list_nodes()
	pprint(nodes)
	
	result = vbox_driver.shutdown_node(node)
	pprint(result)
	
	result = vbox_driver.destroy_node(node)
	pprint(result)
	
	nodes = vbox_driver.list_nodes()
	pprint(nodes)
    
	result = vbox_driver.startup_node(nodes[0])
	pprint(result)
	
	result = vbox_driver.shutdown_node(nodes[0])
	pprint(result)
	

if __name__ == '__main__':
	main()
