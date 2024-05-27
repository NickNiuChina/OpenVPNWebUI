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

3. Prepare the files

  ```
  # ca.crt
  # ta.key
  # dh.pem
  # server-xxx.key
  # server-xxx.crt
  
  chmod +x learn-address-script-wrapper
  ```

4. Start OpenVPN service and check logs

```
system eanble --now openvpn-udp-tun-1194.service

tail -f /var/log/openvpn/openvpn-udp-tun-1194.log
```

