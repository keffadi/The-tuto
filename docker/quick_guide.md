### 1- OVH VPS with Docker
### 2- Install portenair

```
docker volume create portainer_data
docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

### First setup
 Chrome -> ip:9000  then set admin / 2*S****23
 
 choose **Local_Manage the local Docker environment**
