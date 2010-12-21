#!/bin/bash


readonly APP_FOLDER=/usr/vnodectrl


/usr/bin/sudo /bin/mkdir -p $APP_FOLDER
/usr/bin/sudo /bin/chmod g+w $APP_FOLDER

/bin/bash -o pipefail -c "/usr/bin/curl -sSfL https://github.com/Logaritmisk/vnodectrl/tarball/2.x-dev | sudo /usr/bin/tar xvz -C$APP_FOLDER --strip 1"

/usr/bin/sudo /bin/ln -sf $APP_FOLDER/bin /usr/bin/vnodectrl













#SRC_FOLDER=$(dirname $0)
#APP_FOLDER=/opt/vnodectrl.d


#if [ ! -d $APP_FOLDER ]; then
#	sudo mkdir -p $APP_FOLDER
#fi

#sudo cp -R $SRC_FOLDER/src/* $APP_FOLDER

#sudo chmod +x $APP_FOLDER/vnodectrl

#sudo ln -sf $APP_FOLDER/vnodectrl /usr/bin/

#if [ ! -d $HOME/.vnodectrl.d ]; then
#	mkdir -p $HOME/.vnodectrl.d/conf.d
#fi

#if ! grep "source $APP_FOLDER/completion.sh" $HOME/.bashrc > /dev/null; then
#	echo -e "\nsource $APP_FOLDER/completion.sh" >> $HOME/.bashrc
#	. $HOME/.bashrc
#fi
