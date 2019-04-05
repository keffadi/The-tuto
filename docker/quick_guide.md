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
