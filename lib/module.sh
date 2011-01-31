#!/bin/bash


export VNODECTRL_MODULE_LOADED


# Public functions

module_path() {
    local MODULE=${1?'Error: missing parameter'}
    
    local item
    local path
    
    if ! module_is_loaded "${MODULE}"; then
        error 1 "invalid module"
    fi
    
    ( ${2-false} ) && path="${VNODECTRL_PATH_BIN}/"
    
    for item in ${VNODECTRL_MODULE_LOADED[@]}; do
        [ "${MODULE}" == "${item%%:*}" ] && { echo "${path}${item##*:}"; return 0; }
    done
    
    return 1
}

module_root() {
    local _PATH=$(module_path "$@")
    
    echo ${_PATH%/*}
    
    return 0
}

module_attr() {
    local MODULE=${1?'Error: missing parameter'}
    local REGEX="^[ \t]*#[ \t]*@${2?'Error: missing parameter'}[ \t]"
    
    local attr
    
    if ! module_is_loaded "${MODULE}"; then
        error 1 "invalid module"
    fi
    
    attr=$(grep -Eoi "${REGEX}(.*?)" $(module_path "${MODULE}" true) | sed "s/${REGEX}//")
    
    if [ -z "$attr" ]; then
        echo ${3-''}
        
        return 1
    fi
    
    echo $attr
    
    return 0
}

module_is_loaded() {
    local MODULE=${1?'Error: missing parameter'}
    
    local item
    
    for item in ${VNODECTRL_MODULE_LOADED[@]}; do
        [ "${MODULE}" == "${item%%:*}" ] && { return 0; }
    done
    
    return 1
}

module_get_loaded() {
    local item
    local items
    
    for item in ${VNODECTRL_MODULE_LOADED[@]}; do
        items[${#items[@]}]="${item%%:*}"
    done
    
    echo ${items[@]}
    
    return 0
}



# Private functions

vnodectrl_module_load() {
    local _PATH="${1?'Error: missing parameter'}"
    
    local item
    local items
    
    if [ -z "${_PATH}" ] || [ ! -d "${_PATH}" ]; then
        error 1 "not a valid path"
    fi
    
    for item in $(find "${_PATH}" -type f -iname "*.m"); do
        item=${item##$_PATH/}
        
        include "bin/${item}"
        
        items[${#items[@]}]="`basename ${item%%.*}`:${item}"
    done
        
    VNODECTRL_MODULE_LOADED=( ${items[@]} )
    
    return 0
}



# On init

vnodectrl_module_load "${VNODECTRL_PATH_ROOT}/bin"
