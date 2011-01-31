#!/bin/bash


# Public functions

cursor_get() {
    local _STTY
    local _POS
    
    exec < /dev/tty
    _STTY=$(stty -g)
    stty raw -echo min 0
    
    echo -en "\033[6n" > /dev/tty
    
    IFS=';' read -r -d R -a _POS
    stty "${_STTY}"
    
    echo "$((${_POS[1]} - 1)):$((${_POS[0]:2} - 1))"
}

cursor_set() {
    tput cup "${2?'Error: missing parameter'}" "${1?'Error: missing parameter'}"
}

error() {
    local INFO=( $(caller ${1:0}) )
    local MSG="$2"
    local CODE="${3:-1}"
    
    
    if [ -n "$MSG" ] ; then
        echo "${INFO[2]}: line ${INFO[0]}: ${INFO[1]}: ${MSG}; exiting with status ${CODE}"
    else
        echo "${INFO[2]}: line ${INFO[0]}: ${INFO[1]}: exiting with status ${CODE}"
    fi
    
    
    exit "${CODE}"
}

is_function() {
    local NAME=${1?'Error: missing paramter'}
    
    
    if type -t $NAME > /dev/null; then
        return 0
    fi
    
    
    return 1
}

dispatch() {
    local HOOK=${1?'Error: missing parameter'}
    
    local module
    
    
    shift
    
    for module in $(module_get_loaded); do
        if is_function "${module}_${HOOK}"; then
            "${module}_${HOOK}" "$@"
        fi
    done
    
    
    return 0
}