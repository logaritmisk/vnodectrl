#!/bin/bash

# @package Core
# @description Update vnodectrl


update_exec() {    
    if ! which -s "git"; then
        echo "You have to install git to update vnodectrl"
        
        return 1
    fi
    
    local _GIT_INIT="git init"
    local _GIT_CHECKOUT="git checkout -q ${VNODECTRL_REPOSITORY_BRANCH}"
    local _GIT_UPDATE="git pull ${VNODECTRL_REPOSITORY_URL} ${VNODECTRL_REPOSITORY_BRANCH}"
    
    cd "${VNODECTRL_PATH_ROOT}"
    
    if [ -d .git ]; then
        eval "${_GIT_CHECKOUT}"
    else
        eval "${_GIT_INIT}"
    fi
    
    eval "${_GIT_UPDATE}"
    
    return 0
}
