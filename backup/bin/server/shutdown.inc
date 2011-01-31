#!/bin/bash

# @docstring Shutdown guest system
# @dependencies ssh


# Implementation of hook_exec
#
# @author Anders Olsson
shutdown_exec() {
    echo         "This will shutdown the server."
    read -en1 -p "Do you want to continue? (Y/n): " choice
    
    if [[ ! "${choice-'Y'}" =~ ^[Yy]$ ]]; then
    	exit 1
    fi
    
    ssh_remote_exec "%sudo% shutdown -P 0"
    
    return $?
}
