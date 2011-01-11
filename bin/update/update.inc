#!/bin/bash

# @docstring Update vnodectrl


update_exec() {
    local GIT_INIT="git init"
    local GIT_CHECKOUT="git checkout -q ${VNODECTRL_REPOSITORY_BRANCH}"
    local GIT_UPDATE="git pull ${VNODECTRL_REPOSITORY_URL} ${VNODECTRL_REPOSITORY_BRANCH}"


    if ! `which git > /dev/null`; then
        echo "You have to install git to update vnodectrl"
    
        return 1
    fi


    cd $VNODECTRL_PATH_ROOT

    if [ -d .git ]; then
        eval $GIT_CHECKOUT
    else
        eval $GIT_INIT
    fi

    eval $GIT_UPDATE


    return 0
}
