#!/bin/bash


include "lib/core.sh"


# Public functions

variable_set() {
    local FILE=${1?'Error: missing parameter'} KEY=${2?'Error: missing parameter'} VALUE=$3
    
    
    if [ ! -f $FILE ]; then
        error 1 "file doesn't exists"
    fi
    
    sed "/^${KEY}=.*$/d" "${FILE}" > /tmp/a && mv /tmp/a "${FILE}"
    
    if [ -n "${VALUE}" ]; then
        echo "${KEY}=${VALUE}" | tee -a "${FILE}" > /dev/null
    fi
    
    
    return 0
}

variable_get() {
    local var FILE=${1?'Error: missing paramater'} KEY=${2?'Error: missing parameter'}
    
    
    if [ ! -f "${FILE}" ]; then
        error 1 "file doesn't exists"
    fi
    
    var=$(grep -o "^${KEY}=.*$" ${FILE} | sed -E 's/.*=//')
    
    echo ${var-$3}
    
    
    return 0
}
