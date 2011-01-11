#!/bin/bash

# @docstring Unmount guest system


umount_exec() {
    local guest_addr=$(vnode_identity_get 'guest_addr')
    local srv_folder=$(vnode_identity_get 'srv_folder')


    if ! mount_is_mounted; then
        echo "There is no mount."
        return 1
    fi


    mount_umount


    return $?
}
