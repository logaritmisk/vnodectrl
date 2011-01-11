#!/bin/bash

# The first argument is sudo password for current user
# @author Anders Olsson (logaritmisk)

echo -n "has a id_dsa file been generated? "
if [ ! -f ~/.vnodectrl.d/ssh/id_dsa ]; then
    echo "no"
    
    mkdir -p ~/.vnodectrl.d/ssh > /dev/null

    ssh-keygen -t dsa -N '' -f ~/.vnodectrl.d/ssh/id_dsa
else
    echo "yes"
fi

# Bak folder used with unison
if [ ! -d /bak ]; then
    echo $1 | sudo -S mkdir -p /bak
fi

echo $1 | sudo -S chown -R $(whoami)\: /bak

# Bak folder used with unison
if [ ! -d /srv ]; then
	echo $1 | sudo -S mkdir -p /srv
fi

echo $1 | sudo -S chown -R $(whoami)\: /srv

# Make sure we have a nice file structure
if [ ! -d /srv/mysql ]; then
    mkdir -p /srv/mysql
fi

if [ ! -d /srv/www ]; then
    mkdir -p /srv/www
fi

if [ ! -d /srv/vhosts ]; then
    mkdir -p /srv/vhosts
fi

if [ ! -d /srv/share ]; then
    mkdir -p /srv/share
fi

if [ ! -d /srv/drush ]; then
	mkdir -p /srv/drush
fi

# Move drushrc to /srv/drush
#mv ~/guest/drush/* /srv/drush

#if [ ! -L $HOME/.drush ]; then
#    ln -s /srv/drush $HOME/.drush
#fi

# Remove sites-enabled and use symlink to /srv/vhosts
if [ ! -L /etc/apache2/sites-enabled ]; then
    echo $1 | sudo -S rm -r /etc/apache2/sites-enabled
    echo $1 | sudo -S ln -s /srv/vhosts /etc/apache2/sites-enabled
	
	# Restart apache.
	echo $1 | sudo -S /etc/init.d/apache2 restart
fi


echo $1 | sudo -S apt-get install unison -y
