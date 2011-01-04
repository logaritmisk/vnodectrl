#!/bin/bash

# Script to restore all databases one by one from /srv/mysql
# @author Anders Olsson (logaritmisk)

for DATABASE in $(ls /srv/mysql/*.last.sql.gz); do
	gunzip -c $DATABASE | mysql -u root
done
