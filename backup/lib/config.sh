#!/bin/bash


include "lib/util.sh"


readonly VNODECTRL_CONFIG_PATH="${VNODECTRL_PATH_USER}/config"



# Public function

config_set() {
    variable_set $VNODECTRL_CONFIG_PATH "$@"
    
    return 0
}

config_get() {
    variable_get $VNODECTRL_CONFIG_PATH "$@"
    
    return 0
}



# Private function

_vnodectrl_config_init() {
    if [ ! -f $VNODECTRL_CONFIG_PATH ]; then
        touch $VNODECTRL_CONFIG_PATH
    fi
}
