### 1- Install Docker Ubunter server 18
```
sudo apt update
sudo apt upgrade ( keep all local version / case of OVH VPS)
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo docker version
```

### 2- Install Portainer
```
sudo docker pull portainer/portainer
sudo docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
sudo docker ps
```

Chrome -> ip:9000  then set admin / 2xSxxxxxx3    
choose *Local_Manage the local Docker environment*




### 3- Use case with docker pull kamailio/kamailio:5.2.2-stretch

https://hub.docker.com/r/kamailio/kamailio

https://github.com/ReadyTalk/kamailio-docker/blob/master/README.md

Before first run need to prepare kamailio default config files. If you already have kamailio config files, then you can skip this. To prepare default config files need to execute
```
docker create --name kamailio kamailio/kamailio:5.2.2-stretch
docker cp kamailio:/etc/kamailio /etc
docker rm kamailio

( run docker rm each time before docker run )
docker run --net=host --name kamailio -v /etc/kamailio:/etc/kamailio kamailio/kamailio:5.2.2-stretch -m 64 -M 8
```

RUN in background
```
docker run -d --net=host --name kamailio -v /etc/kamailio:/etc/kamailio kamailio/kamailio:5.2.2-stretch -m 64 -M 8  
```

**Connect MariaDB to Kamailio**

a- image MariaDB + custom docker network with gateway    
b- nano etc/kamailio/kamctlrc  (DBENGINE=MYSQL / DBHOST=192.168.0.2  / DBACCESSHOST=192.168.0.2)    
c- kamctl create   

**Issu**
Go to MariaDB, change kamailio(rw/ro) user to be access from %


d- kamailio.cfg     
```
#!define WITH_MYSQL
#!define WITH_NAT
#!define WITH_AUTH
#!define WITH_USRLOCDB
```
```
DBURL "mysql://kamailio:kamailiorw@192.168.0.2/kamailio"
```
```
kamailio restart
```
## FINISH

usefull command
```
ngrep -d any -qt -W byline "CSeq: [0-9]+ (INVITE|ACK|CANCEL|BYE)" port 5060
kamailio restart
kamailio -M 8 -E -e -dd  (Debug)
netstat -altpn ( to show and kill PID)( apt-get install net-tools -> intall netstat)
mysqladmin -u root -pkolmisoft flush-hosts ( need to it to run Kamailio after rash )

```

INSTALL RTPPROXY ( must be installed on Host, not in the contenair)
*dependencies*
```
sudo apt-get install git-core gcc flex bison libxml2-dev libpcre3-dev
```
```
cd /usr/local/src/
git clone -b master https://github.com/sippy/rtpproxy.git
git -C rtpproxy submodule update --init --recursive
cd rtpproxy
./configure
make
make install
*rtpproxy -F -l 94.23.31.19 -s udp:localhost:7722*
*rtpproxy -F -l 145.239.169.63 -s udp:localhost:7722*
rtpproxy -l ip -s udp:*:7722 ( to match all interface when we have multiple public IP on same Host )
```
