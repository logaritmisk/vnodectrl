#!/bin/bash


_vnodectrl_api_dispatch() {
    local api HOOK=${1?'Error: missing parameter'}
    
    
    shift
    
    for api in $(plugins_api_loaded); do
        if is_function ${api}_${HOOK}; then
            ${api}_${HOOK} "$@"
        fi
    done
    
    return 0
}
