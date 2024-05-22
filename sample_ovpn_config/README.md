1. Install openvpn and download easyrsa v3.2.0
2. prepare vars and generate files
```commandline
./easyrsa init-pki
./easyrsa build-ca
./easyrsa build-server-full openvpn-udp-tun-1194
./easyrsa gen-dh # get dh.pem
openvpn --genkey secret ta.key
```

3. system start openvpn-udp-tun-1194.service