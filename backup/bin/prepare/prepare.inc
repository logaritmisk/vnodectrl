#!/bin/bash

# @docstring Prepare guest system


# Implementation of hook_exec
#
# @author Anders Olsson
prepare_exec() {
    local GUEST_USER=$(identity_get 'guest_user')
    local GUEST_PASS=$(identity_get 'guest_pass')
    local GUEST_ADDR=$(identity_get 'guest_addr')
    
    local is_prepared=false force_prepare=false ROOT_PATH=$(plugin_path "prepare" true)
    
        
    while getopts_long "f" opt \
    	force no_argument "" "$@"
    do
    	case "$opt" in
    		f|force)
    			force_prepare=true
    		;;
    	esac
    done
    
    shift "$(($OPTLIND - 1))"
    
    
    if ! prepare_authorize_host; then
    	echo "Faild to authorize host ($GUEST_USER@$GUEST_ADDR)"
    	
    	return 1
    fi
    
    is_prepared=$(prepare_is_prepared)
    
    if [ ! $is_prepared == '0' ] || ( $force_prepare ); then
        if [ ! $is_prepared == '0' ]; then
    	    echo "This guest isn't prepared."
    	else
    	    echo "This guest has been prepared before."
    	fi
    	
    	read -en1 -p "Do you want to prepare it? (Y/n): " choice
    	echo         ""
    	
    	if [[ "${choice-'Y'}" =~ ^[Yy]$ ]]; then
    	    ssh_remote_exec "$(cat ${ROOT_PATH%/*}/src/server_prepare.sh | sed 's/%guest_pass%/$GUEST_PASS/g')"
    	    
    	    
    	    
    	    
    		scp "${ROOT_PATH%/*}/src/server_prepare.sh" $GUEST_USER@$GUEST_ADDR:~/ > /dev/null 2>&1
    		
    		if [ $? -ne 0 ]; then
    			echo "Faild to prepare guest. (SCP)"
    			
    			return 1
    		fi
    		
    		ssh_remote_exec "~/server_prepare.sh \"$GUEST_PASS\""
    		
    		if [ $? -ne 0 ]; then
    			echo "Faild to prepare guest. (SSH)"
    			
    			return 1
    		fi
    		
    		ssh_remote_exec "rm ~/server_prepare.sh"
    	else
    		return 1
    	fi
    fi
    
    prepare_authorize_guest
    
    return 0
}
