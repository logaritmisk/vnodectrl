#!/bin/bash

# @docstring Mount guest system


mount_identity_alter() {
    input_choice "Do you want to mount using NFS or SSHFS? (NFS)" "NFS|SSHFS" "NFS"
}

# Implementation of hook_exec
#
# @author Anders Olsson
mount_exec() {
    local GUEST_ADDR=$(vnode_identity_get 'guest_addr')
    local SRV_FOLDER=$(vnode_identity_get 'srv_folder')
    
    
    if mount_is_mounted; then
        echo "There is already a mount."
        return 1
    fi
    
    mount_mount_nfs
    
    return $?
}
