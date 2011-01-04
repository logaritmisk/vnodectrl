#!/bin/bash

# Script to dump all databases one by one from MySQL
# @author Anders Olsson (logaritmisk)


BACKUP_DIR=/srv/mysql


# Remove old backup files
echo "Removing old backup files..."
find $BACKUP_DIR/ -mtime +20 -exec rm {} \;

echo "Dumping databases..."

# Backing up local database
for DATABASE in $(mysql -u root -e "SHOW DATABASES;" --xml | egrep -o 'Database\">(.*?)<' | sed -e "s/^Database\">//" -e "s/<$//"); do
	BACKUP_NAME=$DATABASE.`date +%Y%m%d_%H.%M.%S`.sql.gz
	
	echo " * dumping '$DATABASE' to '$BACKUP_DIR/$BACKUP_NAME'"
	
	mysqldump -u root --databases $DATABASE | gzip > $BACKUP_DIR/$BACKUP_NAME;
	
	ln -f $BACKUP_DIR/$BACKUP_NAME $BACKUP_DIR/$DATABASE.last.sql.gz
done
