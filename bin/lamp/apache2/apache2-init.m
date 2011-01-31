#!/bin/bash

# @package LAMP
# @description Control apache2


apache2-init_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    # require_alias false "guest.host" "guest.username" "guest.password"
    
    local _HOST=$(alias_get "guest.host")
    local _USERNAME=$(alias_get "guest.username")
    
    ssh -qt $_USERNAME@$_HOST "/etc/init.d/apache2 ${2}"
    
    return $?
}
