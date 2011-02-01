#!/bin/bash

# @package NodeOne SRV
# @description Unmount srv folder


include "$MODULE_ROOT/srv.api"


srv-umount_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    if ! srv_is_mounted; then
        echo "There is no mount."
        
        return 1
    fi
    
    local _HOST_SRV_FOLDER=$(alias_get 'host.srv_folder')
    
    sudo umount "${_HOST_SRV_FOLDER}"
    
    return $?
}
