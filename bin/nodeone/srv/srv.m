#!/bin/bash

# @package NodeOne SRV


srv_backup() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    echo "srv_backup"
    
    return $?
}
