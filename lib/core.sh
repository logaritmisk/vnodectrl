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
    local _post=false
    local _pre=false
    
    while [ "${1:0:1}" == "%" ]; do
        case "${1:1}" in
            'post') _post=true ;;
            'pre') _pre=true ;;
            *) break ;;
        esac
        
        shift
    done
    
    local _HOOK="${1?'Error: missing parameter'}"
    local _module
    
    shift
    
    for _module in $(module_get_loaded); do
        if [ ${_post} ] && is_function "${_module}_${_HOOK}_post"; then
            "${_module}_${_HOOK}_post" "$@"
        fi
        
        if is_function "${_module}_${_HOOK}"; then
            "${_module}_${_HOOK}" "$@"
        fi
        
        if [ ${_pre} ] && is_function "${_module}_${_HOOK}_pre"; then
            "${_module}_${_HOOK}_pre" "$@"
        fi
    done
    
    return 0
}