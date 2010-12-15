_vnodectrl() {
    local c plugin='core' args=''

    if [ $COMP_CWORD -gt 1 ]; then    
    	c="${COMP_WORDS[1]}"

	    if [[ $c == -i ]]; then
    	    if [ $COMP_CWORD -gt 2 ]; then
	            plugin="${COMP_WORDS[3]:-core}"
	            args=${COMP_WORDS[@]:4}
    	    else
	            plugin=''
	        fi
	    elif [[ $c == -h ]] || [[ $c == --help ]]; then
	        plugin=''
    	fi
	fi

    if [ -n "$plugin" ]; then
        COMPREPLY=( $(compgen -W "$(${COMP_WORDS[0]} --completion=$plugin $args)" -- ${COMP_WORDS[COMP_CWORD]}) )
    fi
}

complete -F _vnodectrl vnodectrl
