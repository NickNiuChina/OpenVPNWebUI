#!/bin/sh
SRCPATH="$1"
VPN_FOLDER=/opt/vpnclient
CONF_FOLDER=/etc/openvpn/client_conf/

cp $SRCPATH $VPN_FOLDER

FILENAME=`basename $(ls $VPN_FOLDER/*.p7mb64)`
if [ -z "$FILENAME" ]; then
	exit 1
fi

#base64
base64 --decode $VPN_FOLDER/$FILENAME > $VPN_FOLDER/"${FILENAME%%.*}".p7m
if [ "$?" -ne "0" ]; then
	rm -rf $SRCPATH $VPN_FOLDER/$FILENAME 
	exit 1
fi

#decrypt .p7m
openssl smime -decrypt -binary -in $VPN_FOLDER/"${FILENAME%%.*}".p7m -out $VPN_FOLDER/"${FILENAME%%.*}".enc -inkey $VPN_FOLDER/device_key
if [ "$?" -ne "0" ]; then
	rm -rf $SRCPATH $VPN_FOLDER/$FILENAME $VPN_FOLDER/"${FILENAME%%.*}".p7m $VPN_FOLDER/"${FILENAME%%.*}".enc
	exit 1
fi

#decrypt .enc
DEVICE_UUID=$(<$VPN_FOLDER/device_uuid)
DEVICE_PASSWORD=$(<$VPN_FOLDER/device_password)
PEPPER=`cat /opt/.key`
PASSWORD=${PEPPER}${DEVICE_PASSWORD}${DEVICE_UUID}

openssl enc -aes-256-cbc -md sha512 -pbkdf2 -d -a -out $VPN_FOLDER/ovpn-profiles.tar.gz -in $VPN_FOLDER/"${FILENAME%%.*}".enc -k "$PASSWORD"
if [ "$?" -ne "0" ]; then
	rm -rf $SRCPATH $VPN_FOLDER/$FILENAME $VPN_FOLDER/"${FILENAME%%.*}".p7m $VPN_FOLDER/"${FILENAME%%.*}".enc $VPN_FOLDER/ovpn-profiles.tar.gz
	exit 1
fi

tar xf $VPN_FOLDER/ovpn-profiles.tar.gz -C $VPN_FOLDER
if [ "$?" -ne "0" ]; then
	rm -rf $SRCPATH $VPN_FOLDER/$FILENAME $VPN_FOLDER/"${FILENAME%%.*}".p7m $VPN_FOLDER/"${FILENAME%%.*}".enc $VPN_FOLDER/ovpn-profiles.tar.gz $VPN_FOLDER/ovpn-profiles/
	exit 1
fi

if [ ! -d "$CONF_FOLDER" ]; then
	mkdir $CONF_FOLDER
fi
cp $VPN_FOLDER/ovpn-profiles/* $CONF_FOLDER

#clean temp files
rm -rf $SRCPATH $VPN_FOLDER/"${FILENAME%%.*}".* $VPN_FOLDER/ovpn-profiles.tar.gz $VPN_FOLDER/ovpn-profiles/
exit 0