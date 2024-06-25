#!/bin/sh
shared=$1
if [ "${shared}" = "on" ];then
#enable the share mode on vpn
  /etc/init.d/iptables enable_openvpn_nat
  cp /etc/openvpn/openvpn_shared.conf /etc/openvpn/openvpn.conf
  echo "#shared_mode" >> /etc/openvpn/openvpn.conf
else
  /etc/init.d/iptables disable_openvpn_nat
  cp /etc/openvpn/openvpn_c2c.conf /etc/openvpn/openvpn.conf
fi
#remember server configuration
cp /etc/openvpn/openvpn.conf /etc/openvpn/server_conf/openvpn.conf
#check the open vpn service status
status=`/etc/init.d/openvpn status | grep stopped`
if [ -z "$status" ];then
  /etc/init.d/openvpn restart
fi
