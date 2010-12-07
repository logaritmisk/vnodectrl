#!/bin/bash

_vnodectrl_scripts() {
	BIN=/opt/vnodectrl.d/bin
	
	find $BIN -type f -perm -100 -exec basename {} \;
}

_vnodectrl() {
	COMPREPLY=( $(compgen -W "$(_vnodectrl_scripts)" -- ${COMP_WORDS[COMP_CWORD]}) )
}

complete -F _vnodectrl vnodectrl
