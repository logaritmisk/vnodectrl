#!/bin/bash


readonly   VNODECTRL_IDENTITY_PATH="${VNODECTRL_PATH_USER}/conf.d"
declare -a VNODECTRL_IDENTITY_EXISTING
declare    VNODECTRL_IDENTITY_ACTIVE



# Public functions

identity_create() {
    echo "create identity $1"
    
    return 0
}

identity_delete() {
    return 0
}

identity_list() {
    echo ${VNODECTRL_IDENTITY_EXISTING[@]}
    
    return 0
}

identity_exists() {
    local IDENTITY=${1?'Error: missing parameter'}
    
    
    [[ " $(identity_list) " =~ " ${IDENTITY} " ]] && return 0
    
    return 1
}

identity_path() {
    local IDENTITY=${1?'Error: missing parameter'} path
    
    
    if ! identity_exists $IDENTITY; then
        return 1
    fi
    
    path="${VNODECTRL_IDENTITY_PATH}/${IDENTITY}"
    
    if [ ! -f "${path}" ]; then
        return 1
    fi
    
    echo $path
    
    return 0
}

identity_use() {
    return 0
}

identity_active() {
    echo $VNODECTRL_IDENTITY_ACTIVE
    
    return 0
}

identity_set() {
    if ! identity_exists $VNODECTRL_IDENTITY_ACTIVE; then
        return 1
    fi
    
    variable_set $(identity_path $VNODECTRL_IDENTITY_ACTIVE) "$@"
    
    return 0
}

identity_get() {
    if ! identity_exists $VNODECTRL_IDENTITY_ACTIVE; then
        return 1
    fi
    
    variable_get "$(identity_path $VNODECTRL_IDENTITY_ACTIVE)" "$@"
    
    return 0
}



# Private function

_vnodectrl_identity_init() {
    if [ ! -d $VNODECTRL_IDENTITY_PATH ]; then
        mkdir -p $VNODECTRL_IDENTITY_PATH
    fi
    
    
    while [ -z "$(config_get 'identity_default')" ]; do _identity_default_choose; done
    
    
    VNODECTRL_IDENTITY_EXISTING=( $(_identity_conf_list) )
    VNODECTRL_IDENTITY_ACTIVE=$(config_get 'identity_default')
}

_identity_conf_list() {
    local entries file
    
    
    for file in $VNODECTRL_IDENTITY_PATH/*; do
        [ -f $file ] || continue
        
        entries[${#entries[@]}]=${file##*/}
    done
    
    echo ${entries[@]}
    
    return 0
}

_identity_default_choose() {
    local input IDENTITIES=$(_identity_conf_list)
    
    
    if [ ${#IDENTITIES[@]} -eq 0 ]; then
        echo         "No identities could be found."
        read -en1 -p "Do you want to create one? (Y/n) " input
        
        if [[ "${input-'Y'}" =~ ^[Yy]$ ]]; then
            identity_create
        else
            exit 0
        fi
    elif [ ${#IDENTITIES[@]} -eq 1 ]; then
        echo         "There is no default identity."
        read -en1 -p "Do you want to use '${IDENTITIES[0]}' as default? (Y/n) " input
        
        if [[ "${input-'Y'}" =~ ^[Yy]$ ]]; then
            config_set "identity_default" "${IDENTITIES[0]}"
        else
            exit 0
        fi
    else
        echo "There is no default identity."
        echo "Multiple"
        
        exit 0
    fi
}
