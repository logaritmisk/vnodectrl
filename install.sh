#!/bin/bash


APP_FOLDER=/opt/vnodectrl.d
SRC_FOLDER=$(dirname $0)

if [ ! -d $APP_FOLDER ]; then
	sudo mkdir -p $APP_FOLDER
fi

sudo cp -R $SRC_FOLDER/src/bin $APP_FOLDER
sudo cp -R $SRC_FOLDER/src/lib $APP_FOLDER
sudo cp -R $SRC_FOLDER/src/res $APP_FOLDER

sudo cp $SRC_FOLDER/src/default.conf $APP_FOLDER
sudo cp $SRC_FOLDER/src/vnodectrl $APP_FOLDER

sudo chmod +x $APP_FOLDER/vnodectrl

sudo ln -sf $APP_FOLDER/vnodectrl /usr/bin/

if [ ! -d $HOME/.vnodectrl.d ]; then
	mkdir -p $HOME/.vnodectrl.d/conf.d
fi

cp $SRC_FOLDER/src/completion.sh ~/.vnodectrl.d/completion.sh

if ! grep "source ~/.vnodectrl.d/completion.sh" $HOME/.bashrc > /dev/null; then
	echo -e "\nsource ~/.vnodectrl.d/completion.sh" >> $HOME/.bashrc
	. $HOME/.bashrc
fi
