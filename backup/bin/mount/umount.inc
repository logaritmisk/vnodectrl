#!/bin/bash

# @package Mount
# @description Unmount guest system


# Implementation of hook_exec
#
# @author Anders Olsson
umount_exec() {
    if ! mount_is_mounted; then
        echo "There is no mount."
        return 1
    fi
    
    mount_umount
    
    return $?
}
