#!/bin/bash


SRC_FOLDER=$(dirname $0)
APP_FOLDER=/opt/vnodectrl.d


if [ ! -d $APP_FOLDER ]; then
	sudo mkdir -p $APP_FOLDER
fi

sudo cp -R $SRC_FOLDER/src/* $APP_FOLDER

sudo chmod +x $APP_FOLDER/vnodectrl

sudo ln -sf $APP_FOLDER/vnodectrl /usr/bin/

if [ ! -d $HOME/.vnodectrl.d ]; then
	mkdir -p $HOME/.vnodectrl.d/identifier
fi

if ! grep "source $APP_FOLDER/completion.sh" $HOME/.bashrc > /dev/null; then
	echo -e "\nsource $APP_FOLDER/completion.sh" >> $HOME/.bashrc
	. $HOME/.bashrc
fi
