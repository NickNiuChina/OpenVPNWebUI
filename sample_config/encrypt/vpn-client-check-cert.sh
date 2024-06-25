#!/bin/sh
VPN_FOLDER=/opt/vpnclient

cd "$VPN_FOLDER"
((CA_MIN_VALIDITY_SECONDS = 30 * 86400))

if [[ -f $VPN_FOLDER/device_cert ]];then
	openssl x509 -checkend $CA_MIN_VALIDITY_SECONDS -noout -in device_cert
	if [[ $? -ne 0 ]]; then
		/home/webui/pvshell-web/scripts/vpn-client-reset.sh 1
	fi
fi
exit 0