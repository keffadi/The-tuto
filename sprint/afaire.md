

### Aller dans le cloud N1.18—>TOOL  & télécharger:

imagemagento  
imagemysql   
imagephpmyadmin  
   
containermagento  
containerphpmyadmin  
containermysql  


*Taper les commandes suivantes*:
```
docker load -i imagemagento
docker load -i imagemysql
docker load -i imagephpmyadmin
```
```
docker run -i -t docker-magento2_web_1 /bin/bash
docker run -i -t docker-magento2_phpmyadmin_1 /bin/bash
docker run -i -t docker-magento2_db_1 /bin/bash
```
Sur portainer localhost:9000 —> sélectionnés les 3 containers et clicker sur « Start »

Pour activer le domaine, local.magento:
```
sudo nano /private/etc/hosts
```
naviger et coller 
```
127.0.0.1       local.magento
```
avant
```
127.0.0.1       localhost
```
Control+X  —> appuyer sur entrer pour enregistrer   
appliquer les changement avec: 
```
dscacheutil -flushcache
```

http://localhost
http://localhost/admin

ADMIN_USERNAME=admin
ADMIN_PASSWORD=magentorocks1


