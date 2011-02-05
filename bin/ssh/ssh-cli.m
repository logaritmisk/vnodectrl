#!/bin/bash

# @package SSH
# @description Start ssh session to guest


include "${MODULE_ROOT}/ssh.api"


ssh-cli_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    local _HOST=$(alias_get "guest.host")
    local _USERNAME=$(alias_get "guest.username")
    
    ssh -qt $_USERNAME@$_HOST
    
    return $?
}
