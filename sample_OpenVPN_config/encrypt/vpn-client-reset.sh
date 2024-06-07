#!/bin/sh
DEPTH=${1:-"2"}
VPN_FOLDER=/opt/vpnclient
CONF_FOLDER=/etc/openvpn
#DEPTH 0: complete clean up of /opt/vpnclient: remove device_uuid too. Useful to get to a starting condition.
#DEPTH 1: re-generate certificate, key and password. Useful when certificate is about to expire.
#DEPTH 2: delete imported .conf files (udp and tcp) and returns to server configuration. Useful when there are overwrite issues (default).

cd "$VPN_FOLDER"
if [ "$DEPTH" -eq 0 ]; then
	rm -rf device_uuid

	#NEW_UUID
	[[ -r device_uuid ]] || uuidgen --time > device_uuid
fi
if [ "$DEPTH" -le 1 ]; then
	rm -rf device_password
	rm -rf device_cert
	rm -rf device_key

	#NEW_PASSWORD
	[[ -r device_password ]] || (</dev/urandom tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' | head -c 20 ; echo) > device_password
	#NEW_CERT
	openssl req -x509 -newkey rsa:4096 -nodes -keyout device_key -out device_cert -days 366 -subj "/CN=$(<device_uuid)"
fi
if [ "$DEPTH" -eq 2 ]; then
	rm -rf $CONF_FOLDER/client_conf/*
	cp $CONF_FOLDER/server_conf/openvpn.conf $CONF_FOLDER/openvpn.conf
	echo "" > /var/log/openvpn.log
	sed -i 's/client/server/g' $CONF_FOLDER/config.json
fi

exit 0
