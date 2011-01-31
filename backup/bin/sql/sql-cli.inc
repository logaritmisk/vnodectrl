#!/bin/bash

# @docstring Opens sql session on guest
# @dependencies ssh


# Implementation of hook_exec
#
# @author Anders Olsson
sql-cli_exec() {
    ssh_remote_exec "mysql -uroot"
    
    return 0
}
