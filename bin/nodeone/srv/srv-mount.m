#!/bin/bash

# @package NodeOne SRV
# @description Mount srv folder


include "$MODULE_ROOT/srv.api"


srv-mount_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    if srv_is_mounted; then
        echo "There is already a mount."
        
        return 1
    fi
    
    _srv_mount_nfs
    
    return $?
}



# Private functions

_srv_mount_nfs() {
    local _GUEST_HOST=$(alias_get 'guest.host')
    local _GUEST_SRV_FOLDER=$(alias_get 'guest.srv_folder')
    local _HOST_SRV_FOLDER=$(alias_get 'host.srv_folder')
    
    sudo mount_nfs -oactimeo=0 "${_GUEST_HOST}:${_GUEST_SRV_FOLDER}" "${_HOST_SRV_FOLDER}"
    
    return $?
}
