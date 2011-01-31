#!/bin/bash

# @package Core
# @description Manage alias


include "lib/input.sh"


alias_exec() {    
    while [ -n "${1}" ]; do
        if alias_loaded -s; then
            case "${1}" in
                -e) shift; _alias_edit_values; return $? ;;
                -l) shift; _alias_list_values; return $? ;;
            esac
            
            if [ -n "${2}" ]; then
                _alias_set_value "${1}" "${2}"
            else
                _alias_get_value "${1}"
            fi
        else
            case "${1}" in
                -c) shift; _alias_create "$@"; return $? ;;
                -a) shift; _alias_list; return $? ;;
            esac
        fi
        
        return 1
    done
    
    return 0
}



# Private functions

_alias_sanitize() {
    echo "${1?'Error: missing parameter'}" | sed -E 's/[^a-zA-Z0-9._-]//g'
}

_alias_create() {
    local _ALIAS
    
    input_machinename _ALIAS "Alias: "
    
    echo "${_ALIAS}"
    
    return 0
}

_alias_list() {
    local _f
    
    for _f in $VNODECTRL_ALIAS_PATH/*; do
        [ -f $_f ] || continue
        
        echo "${_f##*/}"
    done
    
    return 0
}

_alias_set_value() {
    local _KEY=$(_alias_sanitize "${1?'Error: missing parameter'}")
    local _VALUE=$(_alias_sanitize "${2'Error: missing parameter'}")

    alias_set "${_KEY}" "${_VALUE}"

    return $?
}

_alias_get_value() {
    local _KEY=$(_alias_sanitize "${1?'Error: missing parameter'}")

    alias_get "${_KEY}"

    return $?
}

_alias_edit_values() {
    local _EDITOR="${EDITOR:-vi}"
        
    if ! which -s "${_EDITOR}"; then
        return 1
    fi
    
    "${_EDITOR}" "${VNODECTRL_ALIAS_PATH}/$(alias_loaded)"
    
    return $?
}

_alias_list_values() {
    cat "${VNODECTRL_ALIAS_PATH}/$(alias_loaded)"
    
    return $?
}
