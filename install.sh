#!/bin/bash


readonly APP_FOLDER=/usr/vnodectrl


/usr/bin/sudo /bin/mkdir -p $APP_FOLDER
/usr/bin/sudo /bin/chmod g+w $APP_FOLDER

/bin/bash -o pipefail -c "/usr/bin/curl -sSfL https://github.com/Logaritmisk/vnodectrl/tarball/2.x-dev | sudo /usr/bin/tar xvz -C$APP_FOLDER --strip 1"

/usr/bin/sudo /bin/ln -sfn $APP_FOLDER/bin /usr/bin/vnodectrl
