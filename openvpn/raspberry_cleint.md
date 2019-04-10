
## 1- connection d'un raspdebian à un server openvpn
'''
sudo -s
apt-get update && apt-get install openvpn
wget https://*****/client.ovpn
openvpn --config client.ovpn
mv client.ovpn  /etc/openvpn/client.conf
rebbot

curl ipinfo.io
'''
