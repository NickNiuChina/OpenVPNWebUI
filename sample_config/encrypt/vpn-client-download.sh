#!/bin/sh
DESTPATH="$1"
VPN_FOLDER=/opt/vpnclient

#if uuid was not generated yet, generate all files
if [[ ! -f $VPN_FOLDER/device_uuid ]]
then
	/home/webui/pvshell-web/scripts/vpn-client-reset.sh 0
#if cert, password or key are missing, re-generate them
elif [[ ! -f $VPN_FOLDER/device_password ]] || [[ ! -f $VPN_FOLDER/device_cert ]] || [[ ! -f $VPN_FOLDER/device_key ]]
then
	/home/webui/pvshell-web/scripts/vpn-client-reset.sh 1
fi

#if cert is about to expire (less than 30 days), re-generate it
/home/webui/pvshell-web/scripts/vpn-client-check-cert.sh > /dev/null 2>&1

cat $VPN_FOLDER/device_uuid $VPN_FOLDER/device_password $VPN_FOLDER/device_cert > $VPN_FOLDER/$(<$VPN_FOLDER/device_uuid).req

#PATH=??? used to generate a blob
if [[ $DESTPATH = "???" ]];then
	cat $VPN_FOLDER/*.req
	rm $VPN_FOLDER/*.req > /dev/null 2>&1
else
	FILENAME=`basename $(ls $VPN_FOLDER/*.req)`
	mv $VPN_FOLDER/*.req $DESTPATH
	echo -n $FILENAME
fi
sync
exit 0
