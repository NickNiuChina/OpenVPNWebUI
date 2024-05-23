1. Install openvpn and download easyrsa v3.2.0

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

3. Prepare the files and start service

  ```
  # ca.crt
  # ta.key
  # dh.pem
  # server-xxx.key
  # server-xxx.crt
  system eanble --now openvpn-udp-tun-1194.service
  ```

4. tail -f /var/log/openvpn/openvpn-udp-tun-1194.log