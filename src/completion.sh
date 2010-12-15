_vnodectrl() {
    COMPREPLY=( $(compgen -W "$(${COMP_WORDS[0]} --completion=${COMP_WORDS[1]:-'core'} ${COMP_WORDS[@]:2})" -- ${COMP_WORDS[COMP_CWORD]}) )
}

complete -F _vnodectrl vnodectrl
