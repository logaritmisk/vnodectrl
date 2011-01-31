#!/bin/bash

# @package Mount
# @description Mount guest system

# Implementation of hook_exec
#
# @author Anders Olsson
mount_exec() {
    if mount_is_mounted; then
        echo "There is already a mount."
        
        return 1
    fi
    
    mount_mount_nfs
    
    return $?
}
