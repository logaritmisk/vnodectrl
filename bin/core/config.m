#!/bin/bash

# @package Core
# @description Config vnodectrl


config_exec() {
    while [ -n "${1}" ]; do
        case "${1}" in
            -e) _config_edit_values; return $? ;;
            -l) _config_list_values; return $? ;;
        esac
        
        if [ -n "${2}" ]; then
            _config_set_value "${1}" "${2}"
        else
            _config_get_value "${1}"
        fi
        
        return $?
    done
    
    return 0
}



# Private functions

_config_sanitize() {
    echo "${1?'Error: missing parameter'}" | sed -E 's/[^--._a-zA-Z0-9]//g'
}

_config_set_value() {
    local _KEY=$(_config_sanitize "${1?'Error: missing parameter'}")
    local _VALUE=$(_config_sanitize "${2'Error: missing parameter'}")

    config_set "${_KEY}" "${_VALUE}"

    return $?
}

_config_get_value() {
    local _KEY=$(_config_sanitize "${1?'Error: missing parameter'}")

    config_get "${_KEY}"

    return $?
}

_config_edit_values() {
    local _EDITOR="${EDITOR:-vi}"
    
    if ! which -s "${_EDITOR}"; then
        return 1
    fi
    
    "${_EDITOR}" "${VNODECTRL_CONFIG_PATH}"
    
    return $?
}

_config_list_values() {
    cat "${VNODECTRL_CONFIG_PATH}"
    
    return $?
}
