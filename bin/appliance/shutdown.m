#!/bin/bash

# @package LAMP
# @description Control apache2


shutdown_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    guest_eval "%sudo% shutdown -P 0"
    
    return $?
}
