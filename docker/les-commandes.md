docker et VMware font de la virtualisation
- Vmware recrée le OS
- docker s'appuie sur le OS de l'host en créant des contenair isolé

Docker CE est different selon la distribution Linux


-----------------------------Docker ROOT installation Debian 9--------------------------------------
apt-get update

apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common
    
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

apt-key fingerprint 0EBFCD88
		.....E2D8 8D81 803C 0EBF CD88
		
		
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable nightly test"
   
   
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

docker run hello-world

docker --version

------------------------------- FIN Installation Completed on Debian Stretch--------------------------




-----------------------------Install Docker Compose---------------------------
https://docs.docker.com/compose/install/

curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

docker-compose --version




-----------------------------Utilisation ------------------

https://training.play-with-docker.com/    training  ( durée de vie des contenair 4 h)

docker run --rm bash echo salut
--rm  détruit le container apres avoir monté l'image
bash:3.2  ( la version peut etre specifier)


docker images
 liste des images dans le repository local 
 on peut avoir deux version d'une meme image


docker run -ti --rm bash 
 -ti  ouvre un putty, bash#
 
uname -n 
   nom de l'hote ou Tag du container
   
docker ps
	container en ligne