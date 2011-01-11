#!/bin/bash

# @docstring Control apache2 on guest system
# @dependencies ssh


# Implementation of hook_exec
#
# @author Anders Olsson
apache2_exec() {
    local COMMAND=${1?'Error: missing parameter'}
    
    ssh_remote_exec "%sudo% /etc/init.d/apache2 ${COMMAND}"

    return $?
}
