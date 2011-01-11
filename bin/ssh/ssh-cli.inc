#!/bin/bash

# @docstring Opens ssh session to guest


# Implementation of hook_exec
#
# @author Anders Olsson
ssh-cli_exec() {
    local GUEST_USER=$(identity_get "guest_user")
    local GUEST_ADDR=$(identity_get "guest_addr")
    
    
    ssh $GUEST_USER@$GUEST_ADDR
    
    return 0
}
