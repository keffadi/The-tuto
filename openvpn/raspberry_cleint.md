
## 1- connection d'un raspdebian à un server openvpn
```
sudo -s
apt-get update && apt-get install openvpn
wget https://*****/client.ovpn
openvpn --config client.ovpn  ( then ctrl X, no deomond, test purpose)
mv client.ovpn  /etc/openvpn/client.conf
reboot
```

```
curl ipinfo.io
```
