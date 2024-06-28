1. Install openvpn and download easyrsa v3.2.0
  wget https://github.com/OpenVPN/easy-rsa/releases/download/v3.2.0/EasyRSA-3.2.0.tgz
OR: git clone https://github.com/OpenVPN/easy-rsa.git
tar xf EasyRSA-3.2.0.tgz
mv EasyRSA-3.2.0 easyrsa
cd easyrsa
cp vars.example vars
vim vars
set_var EASYRSA_REQ_COUNTRY     "CN"
set_var EASYRSA_REQ_PROVINCE    "JIANGSU"
set_var EASYRSA_REQ_CITY        "SUZHOU"
set_var EASYRSA_REQ_ORG         "Better_Qualtity"
set_var EASYRSA_REQ_EMAIL       "nick_niu@hotmail.com"
set_var EASYRSA_REQ_OU          "BQ-LTD"
set_var EASYRSA_NO_PASS 1
set_var EASYRSA_CA_EXPIRE       3650
set_var EASYRSA_CERT_EXPIRE     3650

2. prepare vars and generate files

```commandline
./easyrsa init-pki
./easyrsa build-ca
./easyrsa build-server-full openvpn-udp-tun-1194
./easyrsa gen-dh # get dh.pem
openvpn --genkey secret ta.key

# in configuration dir
mkdir ccd
```

3. Prepare the files

  ```
  # ca.crt
  # ta.key
  # dh.pem
  # server-xxx.key
  # server-xxx.crt
  # pw-file
  # learn-*
  chmod 644 pw-file
  chmod +x learn-address-script-wrapper
  ```

4. Start OpenVPN service and check logs

```
system eanble --now openvpn-udp-tun-1194.service

tail -f /var/log/openvpn/openvpn-udp-tun-1194.log
```
5. Setup client
```
ls -al /etc/systemd/system/multi-user.target.wants/openvpn-client@client-openvpn-udp-tun-1194-test1.service
lrwxrwxrwx 1 root root 43 May 29 13:14 /etc/systemd/system/multi-user.target.wants/openvpn-client@client-openvpn-udp-tun-1194-test1.service -> /lib/systemd/system/openvpn-client@.service

nick@openvpn-test:~$ cat /etc/systemd/system/multi-user.target.wants/openvpn-client@client-openvpn-udp-tun-1194-test1.service
[Unit]
Description=OpenVPN tunnel for %I
After=network-online.target
Wants=network-online.target
Documentation=man:openvpn(8)
Documentation=https://community.openvpn.net/openvpn/wiki/Openvpn24ManPage
Documentation=https://community.openvpn.net/openvpn/wiki/HOWTO

[Service]
Type=notify
PrivateTmp=true
WorkingDirectory=/etc/openvpn/client
ExecStart=/usr/sbin/openvpn --daemon ovpn-%i --status /run/openvpn/%i.status 10 --cd /etc/openvpn/client --script-security 2 --config /etc/openvpn/client/%i.conf --writepid /run/openvpn/%i.pid
CapabilityBoundingSet=CAP_IPC_LOCK CAP_NET_ADMIN CAP_NET_RAW CAP_SETGID CAP_SETUID CAP_SYS_CHROOT CAP_DAC_OVERRIDE
LimitNPROC=10
DeviceAllow=/dev/null rw
DeviceAllow=/dev/net/tun rw
ProtectSystem=true
ProtectHome=true
KillMode=process

[Install]
WantedBy=multi-user.target
nick@openvpn-test:~$

```
