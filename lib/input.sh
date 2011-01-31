#!/bin/bash


include "lib/core.sh"


input_string() {
    local _RETURN="${1?'Error: missing parameter'}"
    local _PROMPT="${2?'Error: missing parameter'}"
    local _VALIDATE="${3}"
    
    local _input
    
    while true; do
        tput sc
        
        read -ep "${_PROMPT}" _input
        
        [ -z "${_VALIDATE}" ] && break
        [[ "${_input}" =~ ^${_VALIDATE}$ ]] && break
        
        tput rc
        tput el
    done
    
    eval "$_RETURN='$_input'"
    
    return 0
}

input_machinename() {
    input_string "${1}" "${2}" "[a-zA-Z0-9._-]*"
    
    return $?
}
