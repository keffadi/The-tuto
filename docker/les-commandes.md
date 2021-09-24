- docker et VMware font de la virtualisation
- Vmware recrée le OS
- docker s'appuie sur le OS de l'host en créant des contenair isolé
- Docker CE est different selon la distribution Linux


## Docker ROOT installation Debian 9 
```
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common
```
 ```   
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
```
```
apt-key fingerprint 0EBFCD88
```
		.....E2D8 8D81 803C 0EBF CD88
		
```		
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable nightly test"
     
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io
docker run hello-world
docker --version
```

*FIN Installation Completed on Debian Stretch*


.

### Install Docker Compose 
https://docs.docker.com/compose/install/
```
curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
docker-compose --version
```
*Fin  Install Docker Compose*

.

### Utilisation

https://training.play-with-docker.com/    training  ( durée de vie des contenair 4 h)
```
docker run --rm bash echo salut
```
--rm  détruit le container apres avoir monté l'image
bash:3.2  ( la version peut etre specifier)

```
docker images
```
liste des images dans le repository local 
on peut avoir deux version d'une meme image

```
docker run -ti --rm bash 
```
 -ti  ouvre un putty, bash#

```
uname -n 
```
nom de l'hote ou Tag du container
 
 ```
docker ps
```
container en ligne
	
docker images --> docker history "imageID"
 image ID can be c2dhs45dddk  or c2d ( juste les premier lettre)
 
LES MODIFICATION faites dans un fichier dans le Contenair sont TEMPORAIRE (--RM)

```diff
docker ps --help
```
pour voir les options d'une commande

```
docker run
```
il crée toujour un nouveau conteneur

```
docker start -ai gifted_swartz
```
a spécifier le NAME du contenair
i pour interactive bash
gifted-swart est le nom du contenair
	
	
une images est constitué de plusieurs couches, sauf la dernière est READ/WRITE, les autres sont en lecture seule


------ **VOLUME** ----

store contenair data on host 
```
echo >> /test
```
ecrit a la suite de la dernière ligne
```	
docker run -ti --rm -v $(pwd)/fichier:/test:ro bash 
```
ro for read only
$(pwd) is contenair side
	
	
---- RESEAU ----
```
docker run --rm -p 8080:80  nginx
```
mappage de port 80,
8080 is from host side

```
netstat -nate
```
avoir les ports déjà ouvet

```	
docker inspect "name of running contenair"
```
donne plus d'info sur l'image
	
	
--- **CREATION D'IMAGE a partir d'autres IMAGEs** ----

dockerfile
```
 FROM php:7.0.31-cli (source de l'image avec sa version)
 RUN apt-get update
 RUN apt-get install -y libxmls-dev
 
 
docker build -t php_libxmls:7.0.31-keff   .
```
le nom par defaut est Dockerfile, sinon -f mondockerfile .
t pour TAG
 

---- **NetWork** ------

network bridge est utilisé quand on ne précise pas de reseau
```
docker network create --driver=bridge mon_bridge
```
```
docker network ls
```
liste les réseaux existant
```

docker run -ti --rm --network=mon-bridge --name=mon_server bash
```

brigde cloné ont un DNS, donc peuvent etre pingué par leur nom

```
docker network --help
```
```
docker network connect mon_bridge server01
```
connecter un contenair a un autre bridge
  
--network=host
	pour eviter la mappage, les ports des contenairs = port host
	
	
--- **Docker compose** ---
```
docker-compose.yml
	version: "3"
	services:    ( liste des contenair)
		wordpress:
			image:wordpress:4.9
			port:
				- 80:80
			environment:
				- WORDPRESS_DB_HOST=db
				- WORDPRESS_DB_USER=luke 
				- WORDPRESS_DB_PASSWORD=otherpas
				- WORDPRESS_DB_NAME=wordp
			networks:
				- galaxie
			volumes:
				- ./data/wp:/var/www/html
		db:
			image: mysql:5.7
			environment:
				- MYSQL_ROOT_PASSWORD=monpass
				- MYSQL_DATABASE=wordp
				- MYSQL_USER=luke
				- MYSQL_PASSWORD=otherpas
			volumes:
			- ./data/db:/var/lib/mysql
			
	#volumes:
	#restart: no, always .....
	networks:
		- galaxie        ( nom du network bridgé est galaxy )
		
		
docker-compose up -d
	construction de l'environnement
	- d tourner en background

docker-compose logs -f
	Crtl+C  to leave
	
docker-compose stop / start
	permet d'arreter et demarrer les images

docker-compose down
	 supprime tous sauf les volumes
	 -v pour supprimer les volumes avec

```

---- **Portainer** ----
```
docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer   ( see documentation)
```
	


	
	



