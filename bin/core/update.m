#!/bin/bash

# @package Core
# @description Update vnodectrl


update_exec() {    
    if ! which -s "git"; then
        echo "You have to install git to update vnodectrl"
        
        return 1
    fi
    
    if [ -d .git ]; then
        _update_git_init
    else
        _update_git_checkout
    fi
    
    _update_git_update
    
    return 0
}



# Private functions

_update_git_init() {
    local _GIT_INIT="sudo git init"
    
    cd "${VNODECTRL_PATH_ROOT}" && eval "${_GIT_INIT}"
}

_update_git_checkout() {
    local _GIT_CHECKOUT="sudo git checkout -q ${VNODECTRL_REPOSITORY_BRANCH}"
    
    cd "${VNODECTRL_PATH_ROOT}" && eval "${_GIT_CHECKOUT}"
}

_update_git_update() {
    local _GIT_UPDATE="sudo git pull ${VNODECTRL_REPOSITORY_URL} ${VNODECTRL_REPOSITORY_BRANCH}"
    
    cd "${VNODECTRL_PATH_ROOT}" && eval "${_GIT_UPDATE}"
}
