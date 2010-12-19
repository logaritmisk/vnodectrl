_vnodectrl() {
    COMPREPLY=( $(compgen -W "$(${COMP_WORDS[0]} --completion "$COMP_CWORD" ${COMP_WORDS[@]})" -- ${COMP_WORDS[COMP_CWORD]}) )
}

complete -F _vnodectrl vnodectrl
