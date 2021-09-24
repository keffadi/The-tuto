
## 1- connection d'un raspdebian / ubuntu  à un server openvpn
```
sudo -s
apt-get update && apt-get install openvpn
wget https://*****/client.ovpn
openvpn --config client.ovpn  ( then ctrl X, no deamon, test purpose)
mv client.ovpn  /etc/openvpn/client.conf
reboot
```

```
curl ipinfo.io
```



other way to do
https://www.octanevpn.com/tutorials/setup-guide-for-openvpn-on-ubuntu.html
