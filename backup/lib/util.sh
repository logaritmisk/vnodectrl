#!/bin/bash


variable_get() {
    local var FILE=${1?'Error: missing paramater'} KEY=${2?'Error: missing parameter'}
    
    
    if [ ! -f "${FILE}" ]; then
        return 1
    fi
    
    var=$(grep -o "^${KEY}=.*$" ${FILE} | sed -E 's/.*=//')
    
    echo ${var-$3}
    
    return 0
}

variable_set() {
    local FILE=${1?'Error: missing parameter'} KEY=${2?'Error: missing parameter'} VALUE=$3
    
    
    if [ ! -f $FILE ]; then
        return 1
    fi
    
    sed "/^${KEY}=.*$/d" "${FILE}" > /tmp/a && mv /tmp/a "${FILE}"
    
    if [ -n "${VALUE}" ]; then
        echo "${KEY}=${VALUE}" | tee -a "${FILE}" > /dev/null
    fi
    
    return 0
}

is_function() {
    local NAME=${1?'Error: missing paramter'}
    
    
    if type -t $NAME > /dev/null; then
        return 0
    fi
    
    return 1
}

dispatch() {
    local plugin HOOK=${1?'Error: missing parameter'}
    
    
    shift
    
    for plugin in $(plugins_loaded); do
        if is_function ${plugin}_${HOOK}; then
            ${plugin}_${HOOK} "$@"
        fi
    done
    
    return 0
}

array_sort() {
    local A=${1?'Error: missing paramter'} B=${2?'Error: missing parameter'} e i
    
    
    while read e; do eval "$B"'[${#'"$B"'[@]}]=$e'; done < <(eval 'echo -e "$(for ((i=0; i < ${#'"$A"'[@]}; i++)); do echo ${'"$A"'[$i]}; done)" | sort')
}
