#!/bin/bash


include "lib/variable.sh"


readonly VNODECTRL_ALIAS_PATH="${VNODECTRL_PATH_USER}/alias"
export   VNODECTRL_ALIAS_ACTIVE



# Public functions

alias_exists() {
    local _ALIAS="${1?'Error: missing parameter'}"
    
    [ ! -f "${VNODECTRL_ALIAS_PATH}/${_ALIAS}" ] && return 1
    
    return 0
}

alias_use() {
    local _ALIAS="${1?'Error: missing parameter'}"
    
    if ! alias_exists "${_ALIAS}"; then
        error 1 "invalid alias"
    fi
    
    VNODECTRL_ALIAS_ACTIVE="${_ALIAS}"
    
    return 0
}

# -s = silent
alias_loaded() {
    alias_exists "${VNODECTRL_ALIAS_ACTIVE}" || return 1
    
    [ "${1}" != "-s" ] && echo "${VNODECTRL_ALIAS_ACTIVE}"
    
    return 0
}

alias_set() {
    local _alias
    
    if [ "${0:0:1}" == "@" ]; then
        _alias="${0:1}" && shift
    elif [ -n "${VNODECTRL_ALIAS_ACTIVE}" ]; then
        _alias="${VNODECTRL_ALIAS_ACTIVE}"
    else
        error 0 "no active alias found"
    fi
    
    if ! alias_exists "${_alias}"; then
        error 1 "invalid alias"
    fi
    
    variable_set "${VNODECTRL_ALIAS_PATH}/${_alias}" "$@"
    
    return $?
}

alias_get() {
    local _alias
    
    if [ "${0:0:1}" == "@" ]; then
        _alias="${0:1}" && shift
    elif [ -n "${VNODECTRL_ALIAS_ACTIVE}" ]; then
        _alias="${VNODECTRL_ALIAS_ACTIVE}"
    else
        error 0 "no active alias found"
    fi
    
    if ! alias_exists "${_alias}"; then
        error 1 "invalid alias"
    fi
    
    variable_get "${VNODECTRL_ALIAS_PATH}/${_alias}" "$@"
    
    return $?
}



# Private functions

vnodectrl_alias_init() {
    [ ! -d "${VNODECTRL_ALIAS_PATH}" ] && mkdir -p "${VNODECTRL_ALIAS_PATH}"
}



# On init

vnodectrl_alias_init
