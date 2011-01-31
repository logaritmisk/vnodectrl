#!/bin/bash

# @docstring Sync files between host and guest
# @dependencies ssh


# Implementation of hook_exec
#
# @author Anders Olsson
srv-sync_exec() {
    if mount_is_mounted; then
        echo "Can't sync srv folder while mount is up."
        echo "Please unmount with 'vnodectrl umount' and try again."
        
        return 1
    fi
    
    case $1 in
    	host)
    		srv_sync_host
    	;;
    	guest)
            srv_sync_guest
    	;;
    	unison)
            srv_sync_unison
    	;;
    esac
    
    return $?
}
