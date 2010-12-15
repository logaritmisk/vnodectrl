# VNodeCtrl

### Install
    $ ./install.sh

### Remove
    $ ./remove.sh

### Usage
    $ vnodectrl

### Sync srv files
To sync files you use

    $ vnodectrl srv {host|guest|unison}



### API

    # basic variable functions
    vnode_variable_get <file> <variable> [default]
    vnode_variable_set <file> <variable> <value>

    # wraps vnode_variable_(get|set)
    vnode_config_get <variable> [default]
    vnode_config_set <variable> <value>
