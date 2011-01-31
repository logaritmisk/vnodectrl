#!/bin/bash


include "lib/util.sh"


declare -a VNODECTRL_PLUGIN_API_LOADED
declare -a VNODECTRL_PLUGIN_INC_LOADED


# Public functions

plugin_is_enabled() {
    local item plugin=${1?'Error: missing parameter'} type=${2-'INC'}
    
    
    for item in ${VNODECTRL_PLUGIN_INC_LOADED[@]}; do
        [ "${plugin}" == "${item%%:*}" ] && { return 0; }
    done
    
    return 1
}

plugin_file() {
    local item path type PLUGIN=${1?'Error: missing parameter'} FULL_PATH=${2-false}
    
    
    ( $FULL_PATH ) && path="${VNODECTRL_PATH_BIN}/"
        
    if [ "${PLUGIN%%*.}" = "api" ]; then
        type="VNODECTRL_PLUGIN_API_LOADED"
    else
        type="VNODECTRL_PLUGIN_INC_LOADED"
    fi
    
    for item in ${VNODECTRL_PLUGIN_INC_LOADED[@]}; do
        [ "${PLUGIN}" == "${item%%:*}" ] && { echo "${path}${item##*:}"; return 0; }
    done
    
    return 1
}

plugin_path() {
    local PATH=$(plugin_file "$@")
    
    
    echo ${PATH%/*}
    
    return 0
}

plugin_attr() {
    local PLUGIN=${1?'Error: missing parameter'} REGEX="^[ \t]*#[ \t]*@${2?'Error: missing parameter'}[ \t]" attr
    
    
    if ! plugin_is_enabled "${PLUGIN}"; then
        return 0
    fi
    
    attr=$(grep -Eoi "${REGEX}(.*?)" $(plugin_file "${PLUGIN}" true) | sed "s/${REGEX}//")
    
    if [ -z "$attr" ]; then
        echo ${3-''}
        
        return 1
    fi
    
    echo $attr
    
    return 0
}

plugins_loaded() {
    local item plugins
    
    
    for item in ${VNODECTRL_PLUGIN_INC_LOADED[@]}; do
        plugins[${#plugins[@]}]="${item%%:*}"
    done
    
    echo ${plugins[@]}
    
    return 0
}

plugins_api_loaded() {
    local item plugins
    
    
    for item in ${VNODECTRL_PLUGIN_API_LOADED[@]}; do
        plugins[${#plugins[@]}]="${item%%:*}"
    done
    
    echo ${plugins[@]}
    
    return 0
}



# Private functions

_vnodectrl_plugin_inc_load() {
    local file entries
    
    
    for file in $(find $1 -type f -iname "*.inc"); do
        file=${file##$1/}
        
        include "bin/${file}"
        
        if is_function "`basename ${file%%.*}`_exec"; then
            entries[${#entries[@]}]="`basename ${file%%.*}`:${file}"
        fi
    done
    
    VNODECTRL_PLUGIN_INC_LOADED=( ${entries[@]} )
    
    return 0
}

_vnodectrl_plugin_api_load() {
    local file entries
    
    
    for file in $(find $1 -type f -iname "*.api"); do
        file=${file##$1/}
        
        include "bin/${file}"
        
        entries[${#entries[@]}]="`basename ${file%%.*}`:${file}"
    done
    
    VNODECTRL_PLUGIN_API_LOADED=( ${entries[@]} )
    
    return 0
}
