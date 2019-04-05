### 1- Install Docker Ubunter server 18
```
sudo apt update
sudo apt upgrade ( keep all local version / case of OVH VPS)
sudo apt install docker.io -y
systemctl start docker
systemctl enable docker
docker version
```

### 2- Install Portainer
```
docker pull portainer/portainer
docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
docker ps
```

Chrome -> ip:9000  then set admin / 2xSxxxxxx3    
choose *Local_Manage the local Docker environment*




### 3- Use case with docker pull kamailio/kamailio-ci

https://hub.docker.com/r/kamailio/kamailio-ci

https://github.com/ReadyTalk/kamailio-docker/blob/master/README.md

Before first run need to prepare kamailio default config files. If you already have kamailio config files, then you can skip this. To prepare default config files need to execute
```
docker create --name kamailio kamailio/kamailio:5.2.2-bionic
docker cp kamailio:/etc/kamailio /etc
docker rm kamailio

( run docker rm each time before docker run )
docker run --net=host --name kamailio -v /etc/kamailio:/etc/kamailio kamailio/kamailio:5.2.2-bionic -m 64 -M 8
```

RUN in background
```
docker run -d --net=host --name kamailio -v /etc/kamailio:/etc/kamailio kamailio/kamailio:5.2.2-bionic -m 64 -M 8  
```

**Connect MariaDB to Kamailio**

a- image MariaDB + custom docker network with gateway    
b- nano etc/kamailio/kamctlrc  (DBENGINE=MYSQL / DBHOST=192.168.0.2)    
c- kamctl create   

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
