#!/bin/bash

# @package Core
# @description Update vnodectrl


backup_exec() {    
    if ! alias_loaded -s; then
        return 2
    fi
    
    dispatch '%post' '%pre' 'backup'
    
    return 0
}
