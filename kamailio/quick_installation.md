### 1- Installation de Kamailio 5.X sur Ubuntu 18.04 Bionic

```
sudo dpkg-reconfigure tzdata
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade 

```
** install MariaDB**
```
sudo apt-get install software-properties-common
sudo apt -y install mariadb-server mariadb-client
```

others dependences
```
sudo apt-get install git-core gcc flex bison libmariadbclient-dev make
sudo apt-get install libssl-dev libcurl4-openssl-dev libxml2-dev libpcre3-dev (facultatif)
```
```
mkdir -p /usr/local/src/kamailio-5.0
cd /usr/local/src/kamailio-5.0
git clone --depth 1 --no-single-branch https://github.com/kamailio/kamailio kamailio
cd kamailio
git checkout -b 5.0 origin/5.0
make cfg
nano -w src/modules.lst    (include_modules= db_mysql)
make all
make install
echo $PATH  ( to see if /usr/local/sbin)
```
```
Uncomment (DBENGINE=MYSQL & sip domaine) and Kamailio user/password ( if you want not use default password)
```
nano -w /usr/local/etc/kamailio/kamctlrc 
/usr/local/sbin/kamdbctl create
```
