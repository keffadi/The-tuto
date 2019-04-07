# FAILLED, have to update processs with "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock"

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

Uncomment (DBENGINE=MYSQL & sip domaine) and Kamailio user/password ( if you want not use default password)
```
nano -w /usr/local/etc/kamailio/kamctlrc 
/usr/local/sbin/kamdbctl create
```

nano /usr/local/etc/kamailio/kamailio.cfg  
```
#!define WITH_MYSQL
#!define WITH_NAT
#!define WITH_AUTH
#!define WITH_USRLOCDB

then DBURL's password change'
```

```
cp pkg/kamailio/deb/debian/kamailio.init /etc/init.d/kamailio
chmod 755 /etc/init.d/kamailio
nano /etc/init.d/kamailio  {
DAEMON=/usr/local/sbin/kamailio
CFGFILE=/usr/local/etc/kamailio/kamailio.cfg
```
```
cp pkg/kamailio/deb/debian/kamailio.default /etc/default/kamailio
nano /etc/default/kamailio   (RUN_KAMAILIO=yes & user & group & shm & pkg & CFGFILE(corrigé mauvais adresse par /usr/local/etc/kamailio/kamailio.cfg)) Uncomment
```
```
mkdir -p /var/run/kamailio
adduser --quiet --system --group --disabled-password --shell /bin/false --gecos "Kamailio" --home /var/run/kamailio kamailio
chown kamailio:kamailio /var/run/kamailio

nano /etc/systemd/system/kamailio.service   
```
Kamailio.service:
[Unit]
Description=Kamailio SIP Server

[Service]
Type=forking
ExecStart=/usr/local/sbin/kamctl start
ExecRestart=/usr/local/sbin/kamctl restart
ExecStop=/usr/local/sbin/kamctl stop

[Install]
WantedBy=multi-user.target
```
```
/etc/init.d/kamailio restart
/etc/init.d/kamailio stop
```
```
kamctl add username password email  (yebe/yebe   & keffa/keffa )
apt-get install ngrep
```
