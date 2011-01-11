#!/bin/bash

# @docstring Restart guest system
# @dependencies ssh


# Implementation of hook_exec
#
# @author Anders Olsson
reboot_exec() {
    echo         "This will reboot the server."
    read -en1 -p "Do you want to continue? (Y/n): " choice
    
    if [[ ! "${choice-'Y'}" =~ ^[Yy]$ ]]; then
    	exit 1
    fi
    
    ssh_remote_exec "%sudo% reboot"
    
    return $?
}
