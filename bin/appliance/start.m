#!/bin/bash

# @package LAMP
# @description Control apache2


start_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    local _APPLIANCE=$(alias_get "guest.appliance")
    
    echo "Starting VirtualBox appliance ${_APPLIANCE} as headless"
    
    VBoxHeadless -s "${_APPLIANCE}"
    
    return $?
}
