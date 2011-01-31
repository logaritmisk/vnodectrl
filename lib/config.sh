#!/bin/bash


include "lib/variable.sh"


readonly VNODECTRL_CONFIG_PATH="${VNODECTRL_PATH_USER}/config"



# Public functions

config_set() {
    variable_set "${VNODECTRL_CONFIG_PATH}" "$@"
    
    return $?
}

config_get() {
    variable_get "${VNODECTRL_CONFIG_PATH}" "$@"
    
    return $?
}



# Private functions

vnodectrl_config_init() {
    if [ ! -f "${VNODECTRL_CONFIG_PATH}" ]; then
        touch "${VNODECTRL_CONFIG_PATH}"
    fi
}



# On init

vnodectrl_config_init
