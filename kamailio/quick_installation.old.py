Maintenance
The maintenance process is very simple right now. You have to be user root and execute following commands:

  cd /usr/local/src/kamailio-5.0/kamailio
  git pull origin
  make all
  make install
  /etc/init.d/kamailio restart
  
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ KAMAILIO 5.0 INSTALLATION $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
tail -n50 -f /var/log/syslog
 ngrep -d any -qt -W byline "CSeq: [0-9]+ (INVITE|ACK|CANCEL|BYE)" port 5060
 /etc/init.d/kamailio restart

 
ROUTE_GRAPH page 319
dpkg-reconfigure tzdata
apt-get update
apt-get upgrade
apt-get dist-upgrade   ( server debian OVH)
apt-get install mysql-server  (password)  prodiction (password)  ( kolmisoft  pour replicate)
(faire un par un) apt-get install git-core gcc flex bison libmysqlclient-dev(apt install libmariadbclient-dev mariadb-client-10.1)  make
(faire un par un) apt-get install libssl-dev libcurl4-openssl-dev libxml2-dev libpcre3-dev (facultatif)

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


nano -w /usr/local/etc/kamailio/kamctlrc  (DBENGINE=MYSQL & sip domaine) pass: pw  ( rw & ro)  Uncomment
/usr/local/sbin/kamdbctl create

nano /usr/local/etc/kamailio/kamailio.cfg  {
#!define WITH_MYSQL
#!define WITH_NAT

#!define WITH_AUTH
#!define WITH_USRLOCDB

then DBURL's password change'
}

cp pkg/kamailio/deb/debian/kamailio.init /etc/init.d/kamailio
chmod 755 /etc/init.d/kamailio
nano /etc/init.d/kamailio  {
DAEMON=/usr/local/sbin/kamailio
CFGFILE=/usr/local/etc/kamailio/kamailio.cfg
}

cp pkg/kamailio/deb/debian/kamailio.default /etc/default/kamailio
nano /etc/default/kamailio   (RUN_KAMAILIO=yes & user & group & shm & pkg & CFGFILE(corrigé mauvais adresse par /usr/local/etc/kamailio/kamailio.cfg)) Uncomment

mkdir -p /var/run/kamailio
adduser --quiet --system --group --disabled-password --shell /bin/false --gecos "Kamailio" --home /var/run/kamailio kamailio
chown -R kamailio:kamailio /var/run/kamailio

nano /etc/systemd/system/kamailio.service   {
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
}

/etc/init.d/kamailio restart
/etc/init.d/kamailio stop

kamctl add username password email  (yebe/yebe   & keffa/keffa )

apt-get install ngrep

when creating new password for kamailio, uncomment please 

Big debug =  kamailio -M 8 -E -e -dd
" netstat -altpn "   show port and user   (use kill PID)   ( apt-get install net-tools )
mysqladmin -u root -pkolmisoft flush-hosts

$$$$$$$$$$$$$$$$$$$$ -FIN INSTALLATION KAMAILIO 5.0-  $$$$$$$$$$$$$$$$$$$

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ - RTPPROXY - $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
cd /usr/local/src/
$ git clone -b master https://github.com/sippy/rtpproxy.git
$ git -C rtpproxy submodule update --init --recursive
$ cd rtpproxy
$ ./configure
$ make
$ make install
rtpproxy -l ip -s udp:localhost:7722  ( NOUBLIE PAS DE CHANGER DE IP) # rtpproxy -F -l 176.31.229.216 -s udp:localhost:7722 
# rtpproxy -F -l 94.23.31.19 -s udp:localhost:7722 
# rtpproxy -F -l 145.239.169.63 -s udp:localhost:7722 
rtpproxy -l ip -s udp:*:7722 


delete it
apt-get remove --auto-remove rtpproxy

$$$$$$$$$$$$$$$$$$$$ -FIN INSTALLATION RTPPROXY-  $$$$$$$$$$$$$$$$$$$

$$$$$$$$$$$$$$$$$$$$$ -SIREMIS- $$$$$$$$$$$$$$$$$$$$$$$$$$$

apt-get install apache2
service apache2 restart
a2enmod rewrite

apt-get install php php-mysql php-gd php-curl php-xml libapache2-mod-php
a2enmod php7.0
cd /var/www
wget https://github.com/asipto/siremis/archive/master.zip
unzip master.zip
cd siremis-master
apache2ctl -v  ( debug: see apache version) 
make apache-conf  or make apache24-conf  ( pour apache 2,4, utilese le 24)
nano /etc/apache2/sites-available/000-default.conf
ADD into </VirtualHost>  {# siremis apache 2.4 conf snippet ...

	Alias /siremis "/var/www/siremis-master/siremis"
	<Directory "/var/www/siremis-master/siremis">
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Require all granted
		<FilesMatch "\.xml$">
			Require all denied
		</FilesMatch>
		<FilesMatch "\.inc$">
			Require all denied
		</FilesMatch>
	</Directory>
}
service apache2 restart
http://5.135.177.203/siremis/install/
make prepare24 or make prepare
 make chown  ( will repar session write problem)
 
 mysql -uroot -p
 GRANT ALL PRIVILEGES ON siremis.* TO siremis@localhost IDENTIFIED BY 'siremisrw';
 select * from mysql.user;
 
 GO to http://5.135.177.203/siremis/install/
 coché tous la premiere fois
 cd siremis
 mv install installSaver
 ls
 
$$$$$$$$$$$$$$$$ -FIN INSTALLATION SIREMIS- $$$$$$$$$$$$$$$ 
 

$$$$$$$$$$$$$$$$$$$$$$  ACCOUNTING & CDR-Stats $$$$$$$$$$$$$$$$$$$$$
# -- for siremis CDRs --------------
loadmodule "rtimer.so"
loadmodule "sqlops.so"
 
modparam("rtimer", "timer", "name=cdr;interval=300;mode=1;")
modparam("rtimer", "exec", "timer=cdr;route=CDRS")
modparam("sqlops", "sqlcon", "cb=>mysql://kamailio:kamailiorw@localhost/kamailio")
 
 
 
# ======================================================
# Populate CDRs Table of Siremis
# ======================================================
route[CDRS] {
	sql_query("cb","call kamailio_cdrs()","rb");
	sql_query("cb","call kamailio_rating('default')","rb");
 
}


read
https://github.com/asipto/siremis/blob/master/siremis/modules/sipadmin/mod.install.siremis.sql#L156
http://kb.asipto.com/siremis:install53x:accounting
-------ok

# ----- tm params -----
# auto-discard branches from previous serial forking leg
modparam("tm", "failure_reply_mode", 3)
# default retransmission timeout: 30sec
modparam("tm", "fr_timer", 1000)
# default invite retransmission timeout after 1xx: 120sec
modparam("tm", "fr_inv_timer", 60000)

$$$$$$$$$$$$$$$$$$$$$$ FIN installation ACC et CDR $$$$$$$$




10 avril- su
- voir dans source  "Install Kamailio on Debian"
  * creer dossier /var/run/kamailio  et ensuite fichier nano /var/run/kamailio/kamailio.fifo  (don't use touch)
  
  
  
  
exemple of setting: https://blog.voipxswitch.com/2015/03/27/kamailio-basic-sip-proxy-all-requests-setup/
https://wiki.freeswitch.org/wiki/Kamailio_basic_setup_as_proxy_for_FreeSWITCH

Loose routing is new in SIP version 2.
When you use loose routing, the R-URI is never changed and backwards compatibility is maintained with the older method 
             B         C             D
invite D   invite D  invite D     
route B,C  route C


/etc/default/kamailio  
# Set to yes to enable kamailio, once configured properly.
RUN_KAMAILIO=yes
 
# User to run as
USER=kamailio
 
# Group to run as
GROUP=kamailio
 
# Amount of shared and private memory to allocate
# for the running Kamailio server (in Mb)
SHM_MEMORY=64
PKG_MEMORY=4
 
# Config file
CFGFILE=/etc/kamailio/kamailio.cfg

adduser --quiet --system --group --disabled-password --shell /bin/false --gecos "Kamailio" --home /var/run/kamailio kamailio

http://lists.sip-router.org/pipermail/sr-users/2015-August/089446.html  (init )
  
 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$- RTPPROXY -$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$ git clone -b master https://github.com/sippy/rtpproxy.git
$ git -C rtpproxy submodule update --init --recursive
$ cd rtpproxy
$ ./configure
$ make
$ make install
rtpproxy -l 5.135.177.203 -s udp:localhost:7722
rtpproxy -F -l 5.135.177.203 -s udp:localhost:7722


delete it
apt-get remove --auto-remove rtpproxy



----------------------------------------------------------------



------------------------------------------------
tm.so  /D
sl.so  /D
textops.so  /D
sqlops.so

modparam("sqlops","sqlcon","numbering_cn=>mysql://backup:keffa2015@91.121.83.105/numbering")

request_route {
	sql_query("numbering_cn", "call `pro`(\"$fU\", \"$rU\")","resultat");
	xlog("L_ALERT","ALERT: call enclose with paramettre, from $fU to $rU\n");
	$var(ip1)=$dbr(resultat=>[0,3]);
	$var(port1)=$dbr(resultat=>[0,6]);
	$var(port2)=$dbr(resultat=>[0,7]);
	$var(port3)=$dbr(resultat=>[0,8]);
	$var(failgroup_ip)=$dbr(resultat=>[0,9]);
	$var(failgroup)=$dbr(resultat=>[0,12]);
	
	sql_result_free("resultat");
	xlog("L_ALERT","ALERT: $var(ip1) \n");
	xlog("L_ALERT","PORT1: $var(port1) \n");
	xlog("L_ALERT","PORT2: $var(port2) \n");
	xlog("L_ALERT","PORT3: $var(port3) \n");
	xlog("L_ALERT","Failgoup_ip: $var(failgroup_ip) \n");
	xlog("L_ALERT","Failgroup: $var(failgroup) \n");
}

---------------------------------------------------------------------------------------------------------------

request_route {
	if (is_method("INVITE")) {
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: avant exit, route FWD executer \n");	
	}
	exit;
}

route[FWD] {
	t_on_branch("CHECK");
	t_relay();
}
		
		


branch_route[CHECK] {
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
	xlog("L_ALERT","ALERT: call enclose with paramettre, from $fU to $rU  et source ip $si pour $rd =\n");
	$avp(ip1)=$dbr(resultat=>[0,3]);
	$avp(port1)=$dbr(resultat=>[0,6]);
	$avp(port2)=$dbr(resultat=>[0,7]);
	$avp(port3)=$dbr(resultat=>[0,8]);
	$avp(failgroup_ip)=$dbr(resultat=>[0,9]);
	$avp(failgroup)=$dbr(resultat=>[0,12]);
	
	sql_result_free("resultat");
	xlog("L_ALERT","ALERT: $avp(ip1) \n");
	xlog("L_ALERT","PORT1: $avp(port1) \n");
	xlog("L_ALERT","PORT2: $avp(port2) \n");
	xlog("L_ALERT","PORT3: $avp(port3) \n");
	xlog("L_ALERT","Failgoup_ip: $avp(failgroup_ip) \n");
	xlog("L_ALERT","Failgroup: $avp(failgroup) \n");
	$rd=$avp(ip1);
	$rU=$avp(port1)+$rU;
	xlog("L_ALERT","dst rewrited: $rU \n");
}

----------------------------------------------------------
request_route {
	if (is_method("INVITE")) {
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: avant exit, route FWD est executer \n");
		$var(ip1)="51.254.245.58";
		$var(port1)="33";
	}
	exit;
}

route[FWD] {
	t_on_branch("CHECK");
	t_relay();
}
		

branch_route[CHECK] {
	$rd=$var(ip1);
	$rU=$var(port1)+$rU;
	xlog("L_ALERT","dst rewrited: $rU \n");
}

--------------------
request_route {
	if (is_method("INVITE")) {
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: avant exit, route FWD est executer \n");
	}
	exit;
}

route[FWD] {
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
	$var(ip1)=$dbr(resultat=>[0,3]);
	$var(port1)=$dbr(resultat=>[0,6]);
	sql_result_free("resultat");
	t_on_branch("CHECK");
	t_relay();
}
		

branch_route[CHECK] {
	$rd=$var(ip1);
	$rU=$var(port1)+$rU;
	xlog("L_ALERT","dst rewrited: $rU \n");
}
--------------------------  çà Marche -----------------------
request_route {
	if (is_method("INVITE")) {
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: avant exit, route FWD executer \n");	
	}
	exit;
}

route[FWD] {
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
	$avp(ip1)=$dbr(resultat=>[0,3]);
	$avp(port1)=$dbr(resultat=>[0,6]);
	$avp(port2)=$dbr(resultat=>[0,7]);
	$avp(port3)=$dbr(resultat=>[0,8]);
	$avp(failgroup_ip)=$dbr(resultat=>[0,9]);
	$avp(failgroup)=$dbr(resultat=>[0,12]);
	
	sql_result_free("resultat");
	xlog("L_ALERT","ALERT: $avp(ip1) \n");
	xlog("L_ALERT","PORT1: $avp(port1) \n");
	xlog("L_ALERT","PORT2: $avp(port2) \n");
	xlog("L_ALERT","PORT3: $avp(port3) \n");
	xlog("L_ALERT","Failgoup_ip: $avp(failgroup_ip) \n");
	xlog("L_ALERT","Failgroup: $avp(failgroup) \n");
	$rd=$avp(ip1);
	$rU=$avp(port1)+$rU;
	xlog("L_ALERT","dst rewrited: $rU \n");
	t_relay();
	xlog("L_ALERT","Route FWD is executed from ip:$si to ip:$rd \n");
}	
	
--------------------- ça Marche -----------------------
request_route {
	if (is_method("INVITE")) {
		#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$fU\", \"$rU\", NOW())");
		xlog("Affected rows: $sqlrows(numbering_cn)\n");
		
		#event_route[dialog:start] {
			#sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$fU\", \"$rU\", NOW())");
			#xlog("Affected rows for Ended Dialogue: $sqlrows(numbering_cn)\n");
		#} 
			
		
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");	
	}
	exit;
}

route[FWD] {
	# ask numbering system 
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(ip1)=$dbr(resultat=>[0,3]);
			$avp(port1)=$dbr(resultat=>[0,6]);
			$avp(port2)=$dbr(resultat=>[0,7]);
			$avp(port3)=$dbr(resultat=>[0,8]);
			$avp(failgroup_ip)=$dbr(resultat=>[0,9]);
			$avp(failgroup)=$dbr(resultat=>[0,12]);
	
			sql_result_free("resultat");
			xlog("L_ALERT","ALERT: $avp(ip1) \n");
			xlog("L_ALERT","PORT1: $avp(port1) \n");
			xlog("L_ALERT","PORT2: $avp(port2) \n");
			xlog("L_ALERT","PORT3: $avp(port3) \n");
			xlog("L_ALERT","Failgoup_ip: $avp(failgroup_ip) \n");
			xlog("L_ALERT","Failgroup: $avp(failgroup) \n");
			$avp(frep1)="sip:"+$avp(port1)+$rU+"@"+$avp(ip1);
			$avp(frep2)="sip:"+$avp(port2)+$rU+"@"+$avp(ip1);
			$avp(frep3)="sip:"+$avp(port3)+$rU+"@"+$avp(ip1);
			$avp(frep4)="sip:"+$avp(failgroup)+$rU+"@"+$avp(failgroup_ip);
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	
	$ru=$avp(frep1);
	xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
	#t_on_branch("CHECK");
	t_on_failure("REROUTE1");
	t_relay();
}

failure_route[REROUTE1] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep2);
		t_on_failure("REROUTE2");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
		exit; 
	}
}	

failure_route[REROUTE2] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep3);
		t_on_failure("REROUTE3");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep4);
		t_on_failure("REROUTE4");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","dst rewrited dans failure route4: $ru source ip $si pour $rd \n");
	t_reply("500", "Server error");	
}
-------------------------------test ------------------------------------
request_route {

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}
	
	  
	if (is_method("INVITE")) {		
		
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");	
	}
	exit;
}

route[FWD] {
	# ask numbering system 
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(ip1)=$dbr(resultat=>[0,3]);
			$avp(port1)=$dbr(resultat=>[0,6]);
			$avp(port2)=$dbr(resultat=>[0,7]);
			$avp(port3)=$dbr(resultat=>[0,8]);
			$avp(failgroup_ip)=$dbr(resultat=>[0,9]);
			$avp(failgroup)=$dbr(resultat=>[0,12]);
	
			sql_result_free("resultat");
			xlog("L_ALERT","ALERT: $avp(ip1) \n");
			xlog("L_ALERT","PORT1: $avp(port1) \n");
			xlog("L_ALERT","PORT2: $avp(port2) \n");
			xlog("L_ALERT","PORT3: $avp(port3) \n");
			xlog("L_ALERT","Failgoup_ip: $avp(failgroup_ip) \n");
			xlog("L_ALERT","Failgroup: $avp(failgroup) \n");
			$avp(frep1)="sip:"+$avp(port1)+$rU+"@"+$avp(ip1);
			$avp(frep2)="sip:"+$avp(port2)+$rU+"@"+$avp(ip1);
			$avp(frep3)="sip:"+$avp(port3)+$rU+"@"+$avp(ip1);
			$avp(frep4)="sip:"+$avp(failgroup)+$rU+"@"+$avp(failgroup_ip);
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	$ru=$avp(frep4);
	route("INSERT");
	xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
	#t_on_branch("CHECK");
	t_on_failure("REROUTE1");
	t_on_reply("LIMIT");
	t_relay();
}

failure_route[REROUTE1] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep2);
		route("INSERT");
		t_on_failure("REROUTE2");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
		exit; 
	}
}	

failure_route[REROUTE2] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep3);
		route("INSERT");
		t_on_failure("REROUTE3");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep4);
		route("INSERT");
		t_on_failure("REROUTE4");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","dst rewrited dans failure route4: $ru source ip $si pour $rd \n");
	t_reply("500", "Server error");	
}

onreply_route[LIMIT] {
	if (t_grep_status("486")){
		sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$rU\", \"$rU\", NOW())");
		xlog("reply route code in Delete stat $T_reply_code \n");
	}
	#if(status==”500”) {
		#sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$rd\", \"$rU\", NOW())");
		#xlog("Affected rowS pour Delete: $sqlrows(numbering_cn)\n");
	#}
	
}

route[INSERT] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$ru\", \"$rU\", NOW())");
		xlog("Affected rows: $sqlrows(numbering_cn)\n");
}
-------------------- ajout de switch et en meme temps authentification--- route par 5550(gw for 55 et gw_port for 50)-------------
request_route {

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}
	
	  
	if (is_method("INVITE")) {		
		
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);
		xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"51.254.245.60":
			$rd="51.254.245.58";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
			
	# ask numbering system 
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(route-1)=$dbr(resultat=>[0,2]);
			$avp(route-2)=$dbr(resultat=>[0,3]);
			$avp(route-3)=$dbr(resultat=>[0,4]);
			$avp(route-fail)=$dbr(resultat=>[0,5]);
			
	
			sql_result_free("resultat");
			xlog("L_ALERT","Numbering1: $avp(route-1) \n");
			xlog("L_ALERT","Numbering2: $avp(route-2) \n");
			xlog("L_ALERT","Numbering3: $avp(route-3) \n");
			xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
			
			
			
			$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd;
			$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd;
			$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd;
			$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd;
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	$ru=$avp(frep1);
	route("INSERT");
	xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
	#t_on_branch("CHECK");
	t_on_failure("REROUTE1");
	t_on_reply("LIMIT");
	t_relay();
}

failure_route[REROUTE1] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep2);
		route("INSERT");
		t_on_failure("REROUTE2");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
		exit; 
	}
}	

failure_route[REROUTE2] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep3);
		route("INSERT");
		t_on_failure("REROUTE3");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep4);
		route("INSERT");
		t_on_failure("REROUTE4");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","dst rewrited dans failure route4: $ru source ip $si pour $rd \n");
	t_reply("500", "Server error");	
}

onreply_route[LIMIT] {
	if (t_grep_status("486")){
		sql_query("numbering_cn", "delete from current where destination LIKE \"%$tU\"");
		xlog("L_ALERT","reply route code in Delete stat $T_reply_code \n");
	}
	if (t_grep_status("500")){
		sql_query("numbering_cn", "delete from current where destination LIKE \"%$tU\"");
		xlog("L_ALERT","reply route code in Delete stat $T_reply_code \n");
	}
	#if(status==”500”) {
		#sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$rd\", \"$rU\", NOW())");
		#xlog("Affected rows pour Delete: $sqlrows(numbering_cn)\n");
	#}
	
}

route[INSERT] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (caller_id, destination, time) values (\"$ru\", \"$rU\", NOW())");
		xlog("L_ALERT","Affected rows: $sqlrows(numbering_cn) valeur de to \n");
}
--------------------------------------------------------------------------------ça marche check port statur 1
request_route {

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}

	if (method=="BYE") {
		xlog("L_ALERT","Check: Bye recu \n");
	} 
	
	if (is_method("INVITE")) {		
				
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"51.254.245.57":
			$rd="51.254.245.58";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
	# last port-history case
	sql_query("numbering_cn", "select * from current_porthistory where destination=\"$tU\"","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
			} 
				
	
	
	# ask numbering system 
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(route-1)=$dbr(resultat=>[0,2]);
			$avp(route-2)=$dbr(resultat=>[0,3]);
			$avp(route-3)=$dbr(resultat=>[0,4]);
			$avp(route-fail)=$dbr(resultat=>[0,5]);
			
	
			sql_result_free("resultat");
			xlog("L_ALERT","Numbering1: $avp(route-1) \n");
			xlog("L_ALERT","Numbering2: $avp(route-2) \n");
			xlog("L_ALERT","Numbering3: $avp(route-3) \n");
			xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
			
			
			
			$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd;
			$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd;
			$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd;
			$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd;
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	# first attemps
	if ($dbr(porthistory=>rows)>0) {
		$ru=$avp(frep0);
	} else {
		$ru=$avp(frep1);
	}
	
	# check if la ligne est active
	sql_query("numbering_cn", "select * from current_porthistory where route=$avp(route-0) or route=$avp(route-1)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 1: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep2);
			route("INSERT");
			t_on_failure("REROUTE2");
			t_relay();
		} else {
			route("INSERT");
			xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
			#t_on_branch("CHECK");
			t_on_failure("REROUTE1");
			t_on_reply("LIMIT");
			t_relay();
		}
	
}

failure_route[REROUTE1] {
	sql_query("numbering_cn", "select * from current_porthistory where route=$avp(route-2)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 2: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep3);
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408")) {
				$ru=$avp(frep2);
				route("INSERT");
				t_on_failure("REROUTE2");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
				exit; 
			}
		}
}	

failure_route[REROUTE2] {
	sql_query("numbering_cn", "select * from current_porthistory where route=$avp(route-3)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 3: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep4);
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408")) {
				$ru=$avp(frep3);
				route("INSERT");
				t_on_failure("REROUTE3");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
				exit; 
			}
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep4);
		route("INSERT");
		t_on_failure("REROUTE4");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","500 de server erreur envoyer");
	xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");
	t_reply("500", "Server error");	
}

onreply_route[LIMIT] {
	# maybe user ivoirien is busy
	#if (t_grep_status("486")){
		#route("INSERT");
	#}  PEUT PAS METTRE ICI CAR rU NA PaS de VALeur
	
	# normal end
	if(t_check_status("(503)|(404)|(480)|(408)|(403)|(486)")){
		route("DELETE");
	}	
	
}

route[INSERT] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (route, destination, time, status) values (substr($rU, 1 , 4 ), $tU, NOW(), \"0\")");
		xlog("L_ALERT","INSERT: $sqlrows(numbering_cn) valeur de to $tU\n");
}
route[DELETE] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "update current set status=1 where destination=\"$tU\"");
		xlog("L_ALERT","UPDATE: $sqlrows(numbering_cn) valeur de to $tU \n");
}




------------------------------------------------------------------------------------------------
	sql_query("numbering_cn", "select * from current_porthistory where route=$avp(route-0) or route=$avp(route-1)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 1: occuper \n");
			# 
			sql_query("numbering_cn", "select * from current_porthistory where route=$avp(route-2)","portstatus");
			if ($dbr(portstatus=>rows)>0) {
				xlog("L_ALERT","status ligne 1: occuper \n");
				
				sql_query("numbering_cn", "select * from current_porthistory where route=$avp(route-3)","portstatus");
					if ($dbr(portstatus=>rows)>0) {
					xlog("L_ALERT","status ligne 1: occuper \n");
			
			
			# 
			$ru=$avp(frep2);
			route("INSERT");
			t_on_failure("REROUTE2");
			t_relay();
		} else {
			route("INSERT");
			xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
			#t_on_branch("CHECK");
			t_on_failure("REROUTE1");
			t_on_reply("LIMIT");
			t_relay();
		}
	
}

---------ççç
xlog("L_ALERT","status ligne 2: occuper \n");
			# contenue de fail route 1
			route("REROUTE-2");
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
			
			
			-----------------------------avant d'aller a Kamailio 5.0--------
			request_route {

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}

	if (method=="BYE") {
		xlog("L_ALERT","Check: Bye recu \n");
	} 
	
	if (is_method("INVITE")) {		
				
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"51.254.245.57":
			$rd="51.254.245.58";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
	# last port-history case
	sql_query("numbering_cn", "select * from current_porthistory where destination=\"$tU\"","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
			} 
				
	
	
	# ask numbering system 
	sql_query("numbering_cn", "call `proc`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(route-1)=$dbr(resultat=>[0,2]);
			$avp(route-2)=$dbr(resultat=>[0,3]);
			$avp(route-3)=$dbr(resultat=>[0,4]);
			$avp(route-fail)=$dbr(resultat=>[0,5]);
			
	
			sql_result_free("resultat");
			xlog("L_ALERT","Numbering1: $avp(route-1) \n");
			xlog("L_ALERT","Numbering2: $avp(route-2) \n");
			xlog("L_ALERT","Numbering3: $avp(route-3) \n");
			xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
			
			
			
			$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd;
			$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd;
			$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd;
			$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd;
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	# first attemps
	if ($dbr(porthistory=>rows)>0) {
		$ru=$avp(frep0);
	} else {
		$ru=$avp(frep1);
	}
	
	# check if la ligne est active
	sql_query("numbering_cn", "select * from current where route=substr(\"$tU\", 1 , 4 )","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			route("REROUTEa1");
		} else {
			route("INSERT");
			xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
			#t_on_branch("CHECK");
			t_on_failure("REROUTE1");
			t_on_reply("LIMIT");
			t_relay();
		}
	
}

failure_route[REROUTE1] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-2)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 2: occuper \n");
			# contenue de fail route 1
			route("REROUTEa2");
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408")) {
				$ru=$avp(frep2);
				route("INSERT");
				t_on_failure("REROUTE2");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
				exit; 
			}
		}
}	

failure_route[REROUTE2] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-3)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 3: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep4);
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408")) {
				$ru=$avp(frep3);
				route("INSERT");
				t_on_failure("REROUTE3");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
				exit; 
			}
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep4);
		route("INSERT");
		t_on_failure("REROUTE4");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","500 de server erreur envoyer");
	xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");
	t_reply("500", "Server error");	
}

onreply_route[LIMIT] {
	# maybe user ivoirien is busy
	#if (t_grep_status("486")){
		#route("INSERT");
	#}  PEUT PAS METTRE ICI CAR rU NA PaS de VALeur
	
	# normal end
	if(t_check_status("(503)|(404)|(480)|(408)|(403)|(486)")){
		route("DELETE");
	}	
	
}

route[INSERT] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (route, destination, time, status) values (substr($rU, 1 , 4 ), $tU, NOW(), \"0\")");
		xlog("L_ALERT","INSERT: $sqlrows(numbering_cn) valeur de to $tU\n");
}
route[DELETE] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "update current set status=1 where destination=\"$tU\"");
		xlog("L_ALERT","UPDATE: $sqlrows(numbering_cn) valeur de to $tU \n");
}
route[REROUTEa1] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-2)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			route("REROUTEa2");
		} else {
			xlog("L_ALERT","status ligne 1: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep2);
			route("INSERT");
			t_on_failure("REROUTE2");
			t_relay();
		}
}
route[REROUTEa2] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-3)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			route("REROUTEa3");
		} else {
			xlog("L_ALERT","status ligne 1: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep3);
			route("INSERT");
			t_on_failure("REROUTE2");
			t_relay();
		}
}

route[REROUTEa3] {
	xlog("L_ALERT","status ligne 1: occuper \n");
	# contenue de fail route 1
	$ru=$avp(frep4);
	route("INSERT");
	t_on_failure("REROUTE4");
	t_relay();

}
-------------------------------------------------------------------
# set rtpproxy control socket
modparam("rtpproxy", "rtpproxy_sock", "udp:127.0.0.1:7722")		


*** To enable nat traversal execute:
- define WITH_NAT
- install RTPProxy: http://www.rtpproxy.org - start RTPProxy:
$ git clone -b master https://github.com/sippy/rtpproxy.git
$ git -C rtpproxy submodule update --init --recursive
$ cd rtpproxy
$ ./configure
$ make
$ make install
rtpproxy -l 5.135.177.203 -s udp:localhost:7722



- option for NAT SIP OPTIONS keepalives: WITH_NATSIPPING

#!ifdef WITH_NAT
266. loadmodule "nathelper.so"
267. loadmodule "rtpproxy.so"
268. #!endif


#!ifdef WITH_NAT
408. # ----- rtpproxy params -----
409. modparam("rtpproxy", "rtpproxy_sock", "udp:127.0.0.1:7722")


From Kamailio point of view, handling NAT traversal involves several operations: • detect if the SIP request comes from behind a NAT router
• detect of the SIP requests has to be forwarded behind a NAT router
• save information about natted state of an UA in location record
• update the SIP headers to make NAT traversal possible for SIP sessions
• engage a RTP relay application to proxy the media streams
There are few options offered by Kamailio as solution for NAT traversal:
• nathelper and rtpproxy module used with RTPProxy application • iptrtpproxy module used with kernel based RTP forwarding rules • mediaproxy module used with mediaproxy application
In this book, we focus on the first option, being largely used and provided as NAT traversal solution in Kamailio’s default configuration 

RTPProxy runs on a different machine than Kamailio. For example using 127.0.0.1 and port 7722 to communicate with Kamailio:
rtpproxy -s udp:127.0.0.1:7722 ...
Installation for sources requires the standard operations for any Linux application: download, configure, make and install:
mkdir -p /usr/local/src/rtpproxy
cd /usr/local/src/rtpproxy
wget http://b2bua.org/chrome/site/rtpproxy-1.2.1.tar.gz tar xvfz rtpproxy-1.2.1.tar.gz
cd rtpproxy-1.2.1
./configure
make
make install
Rtpproxy application is deployed at /usr/local/bin/rtpproxy.
One of the next chapters shows how to start it to be used together with the default configuration file of Kamailio.

--------------   error in 5.0 ----
request_route {
	if (method == "INVITE") {
		if (rtpproxy_offer())
			t_on_reply("LIMIT");
	}

	if (method == "BYE" || method == "CANCEL")
		unforce_rtp_proxy();


	if(is_method("OPTIONS")) {
	# send reply for each OPTIONS request 
	sl_send_reply("200", "I got it");
	exit;
	}

 
	
	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}

	if (method=="BYE") {
		xlog("L_ALERT","Check: Bye recu \n");
	} 
	
	if (is_method("INVITE")) {		
				
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"51.254.245.57":
			$rd="51.254.245.34";
			$rp="5070";
			break;
		case"91.121.146.63":
			$rd="91.121.83.122";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
	# last port-history case
	sql_query("numbering_cn", "select * from current_porthistory where destination=\"$tU\"","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
			} 
				
	
	
	# ask numbering system 
	sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(route-1)=$dbr(resultat=>[0,2]);
			$avp(route-2)=$dbr(resultat=>[0,3]);
			$avp(route-3)=$dbr(resultat=>[0,4]);
			$avp(route-fail)=$dbr(resultat=>[0,5]);
			
	
			sql_result_free("resultat");
			xlog("L_ALERT","Numbering1: $avp(route-1) \n");
			xlog("L_ALERT","Numbering2: $avp(route-2) \n");
			xlog("L_ALERT","Numbering3: $avp(route-3) \n");
			xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
			
			
			
			$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd+ ":" +$rp;
			$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd+ ":" +$rp;
			$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd+ ":" +$rp;
			$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd+ ":" +$rp;
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	# first attemps
	if ($dbr(porthistory=>rows)>0) {
		$ru=$avp(frep0);
	} else {
		$ru=$avp(frep1);
	}
	
	# check if la ligne est active
	sql_query("numbering_cn", "select * from current where route=substr(\"$tU\", 1 , 4 )","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			route("REROUTEa1");
		} else {
			route("INSERT");
			xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
			#t_on_branch("CHECK");
			t_on_failure("REROUTE1");
			t_on_reply("LIMIT");
			t_relay();
		}
	
}

failure_route[REROUTE1] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-2)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 2: occuper \n");
			# contenue de fail route 1
			route("REROUTEa2");
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408")) {
				$ru=$avp(frep2);
				route("INSERT");
				t_on_failure("REROUTE2");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
				exit; 
			}
		}
}	

failure_route[REROUTE2] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-3)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 3: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep4);
			route("INSERT");
			t_on_failure("REROUTE3");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408")) {
				$ru=$avp(frep3);
				route("INSERT");
				t_on_failure("REROUTE3");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
				exit; 
			}
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408")) {
		$ru=$avp(frep4);
		route("INSERT");
		t_on_failure("REROUTE4");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","500 de server erreur envoyer");
	xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");
	t_reply("500", "Server error");	
}

onreply_route[LIMIT] {
	if (!(status=~"183" || status=~"200"))
		break;
	rtpproxy_answer("FA");
	# maybe user ivoirien is busy
	#if (t_grep_status("486")){
		#route("INSERT");
	#}  PEUT PAS METTRE ICI CAR rU NA PaS de VALeu
	
	# normal end
	if(t_check_status("(503)|(404)|(480)|(408)|(403)|(486)")){
		route("DELETE");
	}	
	
}

route[INSERT] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (route, destination, time, status) values (substr($rU, 1 , 4 ), $tU, NOW(), \"0\")");
		xlog("L_ALERT","INSERT: $sqlrows(numbering_cn) valeur de to $tU\n");
}
route[DELETE] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "update current set status=1 where destination=\"$tU\"");
		xlog("L_ALERT","UPDATE: $sqlrows(numbering_cn) valeur de to $tU \n");
}
route[REROUTEa1] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-2)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			route("REROUTEa2");
		} else {
			xlog("L_ALERT","status ligne 1: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep2);
			route("INSERT");
			t_on_failure("REROUTE2");
			t_relay();
		}
}
route[REROUTEa2] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-3)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			route("REROUTEa3");
		} else {
			xlog("L_ALERT","status ligne 1: occuper \n");
			# contenue de fail route 1
			$ru=$avp(frep3);
			route("INSERT");
			t_on_failure("REROUTE2");
			t_relay();
		}
}

route[REROUTEa3] {
	xlog("L_ALERT","status ligne 1: occuper \n");
	# contenue de fail route 1
	$ru=$avp(frep4);
	route("INSERT");
	t_on_failure("REROUTE4");
	t_relay();

}
-----------------------------------------------------------# if
check if PSTN GW IP is defined (strempty($sel(cfg_get.pstn.gw_ip))) {
xlog("SCRIPT: PSTN rotuing enabled but pstn.gw_ip not defined\n");
return; }
#
#
# if(!($rU=~"^(\+|00)[1-9][0-9]{3,20}$"))
route to PSTN dialed numbers starting with '+' or '00' (international format)
- updat


-------------EXIT leave ----------------
####### Routing Logic ########

request_route {
# Kamailio
	# per request initial checks
	route(REQINIT);

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}

	# handle requests within SIP dialogs
	route(WITHINDLG);

	### only initial requests (no To tag)

	# handle retransmissions
	if(t_precheck_trans()) {
		t_check_trans();
		exit;
	}
	t_check_trans();


# keffa
	if (method == "INVITE") {
		record_route();
		setflag(FLT_ACC); # do accounting
		if (rtpproxy_offer())
			t_on_reply("LIMIT");
	}
	
	#handle RTP proxy
	if (method == "BYE" || method == "CANCEL")
		unforce_rtp_proxy();
 
	
	
	if (is_method("INVITE")) {		
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"51.254.245.57":
			$rd="46.105.112.67";
			#$rp="5070";
			break;
		case"91.121.146.63":
			$rd="91.121.83.122";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
	# last port-history case
	sql_query("numbering_cn", "select * from current_porthistory where destination=\"$tU\" ORDER BY id DESC LIMIT 1","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
			} 
				
	
	
	# ask numbering system 
	sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
		if ($dbr(resultat=>rows)>0) {
			$avp(route-1)=$dbr(resultat=>[0,2]);
			$avp(route-2)=$dbr(resultat=>[0,3]);
			$avp(route-3)=$dbr(resultat=>[0,4]);
			$avp(route-fail)=$dbr(resultat=>[0,5]);
			
	
			sql_result_free("resultat");
			xlog("L_ALERT","Numbering1: $avp(route-1) \n");
			xlog("L_ALERT","Numbering2: $avp(route-2) \n");
			xlog("L_ALERT","Numbering3: $avp(route-3) \n");
			xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
			
			
			
			$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd+ ":" +$rp;
			$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd+ ":" +$rp;
			$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd+ ":" +$rp;
			$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd+ ":" +$rp;
			
			# blocked l'appel a ce niveau
			if ($avp(route-1)=="9999") {
			sl_send_reply("404"," Not found9");
			xlog("L_ALERT","CALL END: by $avp(route-1) \n");
			exit;
			}
		}
		else {
			sl_send_reply("404"," Not found");
			exit;
		}
	# first attemps
	if ($dbr(porthistory=>rows)>0) {
		$ru=$avp(frep0);
	} else {
		$ru=$avp(frep1);
	}
	
	# check if la ligne est active
	sql_query("numbering_cn", "select * from current where route=substr(\"$rU\", 1 , 4 )","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligne 1: occuper \n");
			$ru="sip:alice@51.254.245.41:5060";
			t_on_failure("REROUTE1");
			t_on_reply("LIMIT");
			t_relay();
		} else {
			route("INSERT");
			xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
	
			#t_on_branch("CHECK");
			t_on_failure("REROUTE1");
			t_on_reply("LIMIT");
			t_relay();
		}
	
}

failure_route[REROUTE1] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-2)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligneF1 2: occuper \n");
			# contenue de fail route 1
			$ru="sip:alice@51.254.245.41:5060";
			t_on_failure("REROUTE2");
			t_on_reply("LIMIT");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408|503")) {
				$ru=$avp(frep2);
				route("INSERT");
				t_on_failure("REROUTE2");
				t_on_reply("LIMIT");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
				exit; 
			}
		}
}	

failure_route[REROUTE2] {
	sql_query("numbering_cn", "select * from current where route=$avp(route-3)","portstatus");
		if ($dbr(portstatus=>rows)>0) {
			xlog("L_ALERT","status ligneF2 3: occuper \n");
			# contenue de fail route 1
			$ru="sip:alice@51.254.245.41:5060";
			t_on_failure("REROUTE3");
			t_on_reply("LIMIT");
			t_relay();
		} else {
			# si la reponse est canceled, transmettre
			if(t_is_canceled()) {
				exit;
			}
			if(t_check_status("486|408|503")) {
				$ru=$avp(frep3);
				route("INSERT");
				t_on_failure("REROUTE3");
				t_on_reply("LIMIT");
				t_relay();
				xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
				exit; 
			}
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503")) {
		$ru=$avp(frep4);
		route("INSERT");
		t_on_failure("REROUTE4");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
		exit; 
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","500 de server erreur envoyer Mais a ete  recrit en 404");
	xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");
	t_reply("404", "Not foundS");	
}

onreply_route[LIMIT] {
	if(status==”403”)
		t_reply("404", "Not foundd");
	if (!(status=~"183" || status=~"200"))
		break;
	rtpproxy_answer("FA");
	# maybe user ivoirien is busy
	#if (t_grep_status("486")){
		#route("INSERT");
	#}  PEUT PAS METTRE ICI CAR rU NA PaS de VALeu
	
	# normal end
	if(t_check_status("(503)|(404)|(480)|(408)|(403)|(486)")){
		route("DELETE");
	}	
	
}

route[INSERT] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "insert into current (route, destination, time, status) values (substr($rU, 1 , 4 ), $tU, NOW(), \"0\")");
		xlog("L_ALERT","INSERT: $sqlrows(numbering_cn) valeur de to $tU\n");
}
route[DELETE] {
	#  inserer l'appel dans la table current, eviter que beaucoup d'appel tape le gateway
		sql_query("numbering_cn", "update current set status=1 where destination=\"$tU\"");
		xlog("L_ALERT","UPDATE: $sqlrows(numbering_cn) valeur de to $tU \n");
}

 
# ======================================================
# Populate CDRs Table of Siremis
# ======================================================
route[CDRS] {
	sql_query("cb","call kamailio_cdrs()","rb");
	sql_query("cb","call kamailio_rating('default')","rb");
 
}

# ======================================================
# From Kamailio exemple file
# ======================================================

# Per SIP request initial checks
route[REQINIT] {
#!ifdef WITH_ANTIFLOOD
	# flood dection from same IP and traffic ban for a while
	# be sure you exclude checking trusted peers, such as pstn gateways
	# - local host excluded (e.g., loop to self)
	if(src_ip!=myself) {
		if($sht(ipban=>$si)!=$null) {
			# ip is already blocked
			xdbg("request from blocked IP - $rm from $fu (IP:$si:$sp)\n");
			exit;
		}
		if (!pike_check_req()) {
			xlog("L_ALERT","ALERT: pike blocking $rm from $fu (IP:$si:$sp)\n");
			$sht(ipban=>$si) = 1;
			exit;
		}
	}
	if($ua =~ "friendly-scanner") {
		sl_send_reply("200", "OK");
		exit;
	}
#!endif

	if (!mf_process_maxfwd_header("10")) {
		sl_send_reply("483","Too Many Hops");
		exit;
	}

	if(is_method("OPTIONS") && uri==myself && $rU==$null) {
		sl_send_reply("200","Keepalive");
		exit;
	}

	if(!sanity_check("1511", "7")) {
		xlog("Malformed SIP message from $si:$sp\n");
		exit;
	}
}


# sip dialogue handle
route[WITHINDLG] {
	if (!has_totag()) return;

	# sequential request withing a dialog should
	# take the path determined by record-routing
	if (loose_route()) {
		if (is_method("BYE")) {
			setflag(FLT_ACC); # do accounting ...
			setflag(FLT_ACCFAILED); # ... even if the transaction fails
			xlog("L_ALERT","Check: Bye recu \n");
		}
		else if ( is_method("NOTIFY") ) {
			# Add Record-Route for in-dialog NOTIFY as per RFC 6665.
			record_route();
		}
		route(FWD);
		exit;
	}

	if ( is_method("ACK") ) {
		if ( t_check_trans() ) {
			# no loose-route, but stateful ACK;
			# must be an ACK after a 487
			# or e.g. 404 from upstream server
			t_relay();
			exit;
		} else {
			# ACK without matching transaction ... ignore and discard
			exit;
		}
	}
	sl_send_reply("404", "Not here");
	exit;
}
--------------------------------- progress -----
####### Routing Logic ########

request_route {
# Kamailio
	# per request initial checks
	route(REQINIT);

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}

	# handle requests within SIP dialogs
	route(WITHINDLG);

	### only initial requests (no To tag)

	# handle retransmissions
	if(t_precheck_trans()) {
		t_check_trans();
		exit;
	}
	t_check_trans();


# keffa
	if (method == "INVITE") {
		record_route();
		setflag(FLT_ACC); # do accounting
		if (rtpproxy_offer())
			t_on_reply("LIMIT");
	}
	
	#handle RTP proxy
	if (method == "BYE" || method == "CANCEL")
		unforce_rtp_proxy();
 
	
	
	if (is_method("INVITE")) {		
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"ip":
			$rd="ip";
			#$rp="5070";
			break;
		case"ip":
			$rd="ip";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
		
	#

	# ask numbering system 
	if(rU{s.len}) <= 12) {
		# use wholesale script et permet au ghana, togo, guinee de passer aussi
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
			
	} else if( $rU =~ "^901" || $rU =~ "^902" || $rU =~ "^903" ) {
		#use good retail script
		$rU = $(rU{s.strip,3});
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat"); # procedure stocke des retail sur
			
	} else if( $rU =~ "^904" || $rU =~ "^905" || $rU =~ "^905" ) {
		#use very infected bad retail script
		$rU = $(rU{s.strip,3});
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat"); # procedure stocke des bad retail
				
	} else {
		sl_send_reply("484"," Address Incomplete");
			exit;
	}
	
			if ($dbr(resultat=>rows)>0) {
						$avp(route-1)=$dbr(resultat=>[0,2]);
						$avp(route-2)=$dbr(resultat=>[0,3]);
						$avp(route-3)=$dbr(resultat=>[0,4]);
						$avp(route-fail)=$dbr(resultat=>[0,5]);
		

						sql_result_free("resultat");
						xlog("L_ALERT","Numbering1: $avp(route-1) \n");
						xlog("L_ALERT","Numbering2: $avp(route-2) \n");
						xlog("L_ALERT","Numbering3: $avp(route-3) \n");
						xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
		
		
		
						$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd+ ":" +$rp;
						$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd+ ":" +$rp;
						$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd+ ":" +$rp;
						$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd+ ":" +$rp;
					}
	# block blacklisted callerid, destination and unlisted traffic
	if ($avp(route-1)=="9999") {
		sl_send_reply("404"," Not found9");
		xlog("L_ALERT","CALL END: by $avp(route-1) \n");
		exit;
	}		
	# last port-history case
	sql_query("numbering_cn", "select * from current_porthistory where destination=\"$tU\" ORDER BY id DESC LIMIT 1","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
				
				# first attemps
				$ru=$avp(frep0);
				t_on_failure("REROUTE1");
				t_on_reply("LIMIT");
				t_relay();
				xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
			} else {
				$ru=$avp(frep1);
				t_on_failure("REROUTE1");
				t_on_reply("LIMIT");
				t_relay();
				xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
			}
	
}

failure_route[REROUTE1] {
# si la reponse est canceled, transmettr
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503")) {
		$ru=$avp(frep2);
		t_on_failure("REROUTE2");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
	}
}	

failure_route[REROUTE2] {	
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503")) {
		$ru=$avp(frep3);
		t_on_failure("REROUTE3");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503")) {
		$ru=$avp(frep4);
		t_on_failure("REROUTE4");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","500 de server erreur envoyer Mais a ete  recrit en 404");
	xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");
	t_reply("404", "Not foundS");	
}

onreply_route[LIMIT] {
	if(status==”403”)
		t_reply("404", "Not foundd");
	if (!(status=~"183" || status=~"200"))
		break;
	rtpproxy_answer("FA");
}

 
# ======================================================
# Populate CDRs Table of Siremis
# ======================================================
route[CDRS] {
	sql_query("cb","call kamailio_cdrs()","rb");
	sql_query("cb","call kamailio_rating('default')","rb");
 
}

# ======================================================
# From Kamailio exemple file
# ======================================================

# Per SIP request initial checks
route[REQINIT] {
#!ifdef WITH_ANTIFLOOD
	# flood dection from same IP and traffic ban for a while
	# be sure you exclude checking trusted peers, such as pstn gateways
	# - local host excluded (e.g., loop to self)
	if(src_ip!=myself) {
		if($sht(ipban=>$si)!=$null) {
			# ip is already blocked
			xdbg("request from blocked IP - $rm from $fu (IP:$si:$sp)\n");
			exit;
		}
		if (!pike_check_req()) {
			xlog("L_ALERT","ALERT: pike blocking $rm from $fu (IP:$si:$sp)\n");
			$sht(ipban=>$si) = 1;
			exit;
		}
	}
	if($ua =~ "friendly-scanner") {
		sl_send_reply("200", "OK");
		exit;
	}
#!endif

	if (!mf_process_maxfwd_header("10")) {
		sl_send_reply("483","Too Many Hops");
		exit;
	}

	if(is_method("OPTIONS") && uri==myself && $rU==$null) {
		sl_send_reply("200","Keepalive");
		exit;
	}

	if(!sanity_check("1511", "7")) {
		xlog("Malformed SIP message from $si:$sp\n");
		exit;
	}
}


# sip dialogue handle
route[WITHINDLG] {
	if (!has_totag()) return;

	# sequential request withing a dialog should
	# take the path determined by record-routing
	if (loose_route()) {
		if (is_method("BYE")) {
			setflag(FLT_ACC); # do accounting ...
			setflag(FLT_ACCFAILED); # ... even if the transaction fails
			xlog("L_ALERT","Check: Bye recu \n");
		}
		else if ( is_method("NOTIFY") ) {
			# Add Record-Route for in-dialog NOTIFY as per RFC 6665.
			record_route();
		}
		#route(FWD);
		exit;
	}

	if ( is_method("ACK") ) {
		if ( t_check_trans() ) {
			# no loose-route, but stateful ACK;
			# must be an ACK after a 487
			# or e.g. 404 from upstream server
			t_relay();
			exit;
		} else {
			# ACK without matching transaction ... ignore and discard
			exit;
		}
	}
	sl_send_reply("404", "Not here");
	exit;
}-----------  avant d'enlever 4 essay pour 3 essay ----------
request_route {
# Kamailio
	# per request initial checks
	route(REQINIT);

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans())
			t_relay();
		exit;
	}

	# handle requests within SIP dialogs
	route(WITHINDLG);

	### only initial requests (no To tag)

	# handle retransmissions
	if(t_precheck_trans()) {
		t_check_trans();
		exit;
	}
	t_check_trans();


# keffa
	if (method == "INVITE") {
		record_route();
		setflag(FLT_ACC); # do accounting
		if (rtpproxy_offer())
			t_on_reply("LIMIT");
	}
	
	#handle RTP proxy
	if (method == "BYE" || method == "CANCEL")
		unforce_rtp_proxy();
 
	
	
	if (is_method("INVITE")) {		
		# check if le invite a une transaction active
		if(!t_is_set("branch_route")) route(FWD);	
	}
	exit;
}

route[FWD] {

	#allow recognized ip only
	switch($si) {
		# Al call test from start trinity
		case"51.254.245.57":
			$rd="46.105.112.67";
			#$rp="5070";
			break;
		case"91.121.146.63":
			$rd="46.105.112.67";
			break;
		default:
			sl_send_reply("401"," Unauthorized");
			exit;
	}
		
	# 

	# ask numbering system 
	if($(rU{s.len}) <= 12) {
		# use wholesale script et permet au ghana, togo, guinee de passer aussi
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
			
	} else if( $rU =~ "^901" || $rU =~ "^902" || $rU =~ "^903" ) {
		#use good retail script
		$rU = $(rU{s.strip,3});
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat"); # procedure stocke des retail sur
			
	} else if( $rU =~ "^904" || $rU =~ "^905" || $rU =~ "^905" ) {
		#use very infected bad retail script
		$rU = $(rU{s.strip,3});
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat"); # procedure stocke des bad retail
				
	} else {
		sl_send_reply("484"," Address Incomplete");
			exit;
	}
	
			if ($dbr(resultat=>rows)>0) {
						$avp(route-1)=$dbr(resultat=>[0,2]);
						$avp(route-2)=$dbr(resultat=>[0,3]);
						$avp(route-3)=$dbr(resultat=>[0,4]);
						$avp(route-fail)=$dbr(resultat=>[0,5]);
		

						sql_result_free("resultat");
						xlog("L_ALERT","Numbering1: $avp(route-1) \n");
						xlog("L_ALERT","Numbering2: $avp(route-2) \n");
						xlog("L_ALERT","Numbering3: $avp(route-3) \n");
						xlog("L_ALERT","NumberingFail: $avp(route-fail) \n");
		
		
		
						$avp(frep1)="sip:"+$avp(route-1)+$rU+"@"+$rd+ ":" +$rp;
						$avp(frep2)="sip:"+$avp(route-2)+$rU+"@"+$rd+ ":" +$rp;
						$avp(frep3)="sip:"+$avp(route-3)+$rU+"@"+$rd+ ":" +$rp;
						$avp(frep4)="sip:"+$avp(route-fail)+$rU+"@"+$rd+ ":" +$rp;
					}
	# block blacklisted callerid, destination and unlisted traffic
	if ($avp(route-1)=="9999") {
		sl_send_reply("404"," Not found9");
		xlog("L_ALERT","CALL END: by $avp(route-1) \n");
		exit;
	}
	# last port-history case
	sql_query("numbering_cn", "select * from current_porthistory where destination=\"$tU\" ORDER BY id DESC LIMIT 1","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
				
				# first attemps
				$ru=$avp(frep0);
				t_on_failure("REROUTE1");
				t_on_reply("LIMIT");
				t_relay();
				xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
			} else {
				$ru=$avp(frep1);
				t_on_failure("REROUTE1");
				t_on_reply("LIMIT");
				t_relay();
				xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd \n");
			}
	
}

failure_route[REROUTE1] {
# si la reponse est canceled, transmettr
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503|403")) {
		$ru=$avp(frep2);
		t_on_failure("REROUTE2");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route1: $ru source ip $si pour $rd \n");
	}
}	

failure_route[REROUTE2] {	
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503|403")) {
		$ru=$avp(frep3);
		t_on_failure("REROUTE3");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route2: $ru source ip $si pour $rd \n");
	}
}

failure_route[REROUTE3] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	if(t_check_status("486|408|503|403")) {
		$ru=$avp(frep4);
		t_on_failure("REROUTE4");
		t_on_reply("LIMIT");
		t_relay();
		xlog("L_ALERT","dst rewrited dans failure route3: $ru source ip $si pour $rd \n");
	}
}

failure_route[REROUTE4] {
	# si la reponse est canceled, transmettre
	if(t_is_canceled()) {
		exit;
	}
	xlog("L_ALERT","500 de server erreur envoyer Mais a ete  recrit en 404");
	xlog("L_ALERT","ALERT: FIN -- FIN -- FIN -- FIN -- FIN \n");
	t_reply("404", "Not foundS");	
}

onreply_route[LIMIT] {
	#if(status==”403”)
		#t_reply("404", "Not foundd");
	if (!(status=~"183" || status=~"200"))
		break;
	rtpproxy_answer("FA");
}

 
# ======================================================
# Populate CDRs Table of Siremis
# ======================================================
route[CDRS] {
	sql_query("cb","call kamailio_cdrs()","rb");
	sql_query("cb","call kamailio_rating('default')","rb");
 
}

# ======================================================
# From Kamailio exemple file
# ======================================================

# Per SIP request initial checks
route[REQINIT] {
#!ifdef WITH_ANTIFLOOD
	# flood dection from same IP and traffic ban for a while
	# be sure you exclude checking trusted peers, such as pstn gateways
	# - local host excluded (e.g., loop to self)
	if(src_ip!=myself) {
		if($sht(ipban=>$si)!=$null) {
			# ip is already blocked
			xdbg("request from blocked IP - $rm from $fu (IP:$si:$sp)\n");
			exit;
		}
		if (!pike_check_req()) {
			xlog("L_ALERT","ALERT: pike blocking $rm from $fu (IP:$si:$sp)\n");
			$sht(ipban=>$si) = 1;
			exit;
		}
	}
	if($ua =~ "friendly-scanner") {
		sl_send_reply("200", "OK");
		exit;
	}
#!endif

	if (!mf_process_maxfwd_header("10")) {
		sl_send_reply("483","Too Many Hops");
		exit;
	}

	if(is_method("OPTIONS") && uri==myself && $rU==$null) {
		sl_send_reply("200","Keepalive");
		exit;
	}

	if(!sanity_check("1511", "7")) {
		xlog("Malformed SIP message from $si:$sp\n");
		exit;
	}
}


# sip dialogue handle
route[WITHINDLG] {
	if (!has_totag()) return;

	# sequential request withing a dialog should
	# take the path determined by record-routing
	if (loose_route()) {
		if (is_method("BYE")) {
			setflag(FLT_ACC); # do accounting ...
			setflag(FLT_ACCFAILED); # ... even if the transaction fails
			xlog("L_ALERT","Check: loose Bye recu \n");
		}
		else if ( is_method("NOTIFY") ) {
			# Add Record-Route for in-dialog NOTIFY as per RFC 6665.
			record_route();
		}
		t_relay();
		exit;
	}

	if ( is_method("ACK") ) {
		if ( t_check_trans() ) {
			# no loose-route, but stateful ACK;
			# must be an ACK after a 487
			# or e.g. 404 from upstream server
			xlog("L_ALERT","Check: Noloose\n");
			t_relay();
			exit;
		} else {
			# ACK without matching transaction ... ignore and discard
			exit;
		}
	}
	sl_send_reply("404", "Not here");
	exit;
}
------------------------------------------

	if(($time(hour)>= 0) and ($time(hour)<= 6)) {
			# send reply for each OPTIONS request 
			sl_send_reply("404", "Not found");
			xlog("request blocked"); 
			exit;
	}
	
	----------- dialog
	
loadmodule "dialog.so"
	
	#keffa
modparam("dialog", "default_timeout", 43200 )
modparam("dialog", "db_mode", 0 ) # no database writes
modparam("dialog", "dlg_flag", 3 )
modparam("dialog", "hash_size",  4096 )

dlg_manage();

event_route[dialog:start]
	xlog("L_ALERT","START:CI:$dlg(callid):u_id:$dlg_var(uniqueid):U_id:$dlg_var(userid)");
event_route[dialog:end]
	xlog("L_ALERT","END:CI:$dlg(callid):u_id:$dlg_var(uniqueid):U_id:$dlg_var(userid)");
event_route[dialog:failed]
	xlog("L_ALERT","FAILED:CI:$dlg(callid):u_id:$dlg_var(uniqueid):U_id:$dlg_var(userid)");
	
	
	BEGIN
IF EXISTS (SELECT * FROM orange WHERE prefix=substr(desti, 1 , 5 )) THEN
BEGIN
IF EXISTS (SELECT destination FROM `porthistory` WHERE destination=desti AND duration BETWEEN 3 AND 60 group by destination having count(*) > 2) THEN (SELECT * FROM block);
ELSEIF EXISTS (SELECT * FROM blackdest where destination=desti) THEN (SELECT * FROM block_c);
ELSEIF EXISTS (SELECT * FROM blackclid where callerid=caller) THEN (SELECT * FROM block);
ELSEIF EXISTS (SELECT * FROM blackclid3 where callerid=caller) THEN (SELECT * FROM block_c);
ELSEIF EXISTS (SELECT * FROM solid_lien_ok where destination=desti and callerid=caller) THEN (SELECT * FROM allow_solid WHERE destination=substr(desti, 9 , 2 ));
ELSEIF EXISTS (SELECT * FROM blockcountry where cli_prefix=substr(caller, 1 , 3 )) THEN (SELECT * FROM block);
ELSEIF EXISTS (SELECT * FROM kalimatec where callerid=caller) THEN (SELECT * FROM allow_verifier_callerid WHERE destination=substr(desti, 9 , 2 ));
ELSEIF EXISTS (SELECT * FROM t1_1_distin_dest where callerid=caller and distinct_dest < 5) THEN (SELECT * FROM allow_verifier_callerid WHERE destination=substr(desti, 9 , 2 ));
ELSEIF EXISTS (SELECT * FROM destination_ic_x where destination=desti) THEN (SELECT * FROM allow_verifier_callerid WHERE destination=substr(desti, 9 , 2 ));
ELSE (SELECT * FROM block_c);
END IF;
END;


---------------------- prefix identification --------------------
if($(rU{s.len}) <= 12) {
		# use wholesale script et permet au ghana, togo, guinee de passer aussi
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
			
	} else if( $rU =~ "^901" || $rU =~ "^902" || $rU =~ "^903" ) {
		#use good retail script
		$rU = $(rU{s.strip,3});
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat"); # procedure stocke des retail sur
			
	} else if( $rU =~ "^904" || $rU =~ "^905" || $rU =~ "^905" ) {
		#use very infected bad retail script
		$rU = $(rU{s.strip,3});
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat"); # procedure stocke des bad retail
				
	} else {
		sl_send_reply("484"," Address Incomplete");
			exit;
	}
	
	
	-------------------------------
	
	
		
if($rU =~ "^225") {	# Cote d'ivoire
	if(($si=="ip") or ($si=="ip") or ($si=="ip")) {
		# Premium
		sql_query("numbering_cn", "call `prok21`(\"$fU\", \"$rU\")","resultat");
	} else {
		# wholesale
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
	}
} else if( $rU =~ "^224") {	# Guinea
	if(($fU=="callshop_france") or ($fU=="taxi_phone_UK")) {
		# Retail
		sql_query("numbering_cn", "call `prok21`(\"$fU\", \"$rU\")","resultat");
	} else {
		# Wholesale
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
	}
} else if( $rU =~ "^233") {	# Ghana
	if(($fU=="callshop_france") or ($fU=="taxi_phone_UK")) {
		# O,21 usd route
		sql_query("numbering_cn", "call `prok21`(\"$fU\", \"$rU\")","resultat");
	} else {
		# 0,15 route
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
	}
} else if( $rU =~ "^228") {	# Togo
	if(($fU=="callshop_france") or ($fU=="taxi_phone_UK")) {
		# O,21 usd route
		sql_query("numbering_cn", "call `prok21`(\"$fU\", \"$rU\")","resultat");
	} else {
		# 0,15 route
		sql_query("numbering_cn", "call `prok`(\"$fU\", \"$rU\")","resultat");
	}
} else {
	sl_send_reply("403","forbidden");
	exit;
}

GRANT ALL ON numbering.* TO cheap@'94.23.31.19' IDENTIFIED BY 'pw';

update db set Host='94.23.31.19' where Db='numbering';
update user set Host='94.23.31.19' where user='cheap';


CREATE USER 'copy'@'94.23.31.19' IDENTIFIED BY 'copier';
GRANT ALL ON *.* TO 'copy'@'94.23.31.19' IDENTIFIED BY 'copier';
GRANT ALL ON *.* TO 'copy'@'%' IDENTIFIED BY 'copier';
::1

---------------------------------------
 
			
		case"ip":      #USER3  
			$rU="490" + $rU;
			break;
		case"ip":      #USER3
			$rU="490" + $rU;
			break;
		case"ip":      #USER3
			$rU="490" + $rU;
			break;
		case"ip5":      #K
			$rU="486" + $rU;
		
		



case"91.200.204.100":      #USER3
			$rd="46.105.112.67";
			break;
		case"ip":      #USER3
			$rd="ip";
			break;
		case"ip":      #USER3
			$rd="ip";
			break;
			
			
			and substr(mor.calls.localized_dst, -11, 3)=225
			
			and substr(mor.calls.localized_dst, -12, 3)=224
			
			
			
			
			
----------------------- CUT ---------------------------------------------
	sql_query("numbering_cn", "select * from routing_current_porthistory where destination=\"$tU\" ORDER BY id DESC LIMIT 1","porthistory");
			if ($dbr(porthistory=>rows)>0) {
				#Quand il ya une historique
				$avp(route-0)=$dbr(porthistory=>[0,1]);
				sql_result_free("porthistory");
				xlog("L_ALERT","Numbering0: $avp(route-0) \n");
				$avp(frep0)="sip:"+$avp(route-0)+$rU+"@"+$rd;
				
				# first attemps
				$ru=$avp(frep0);
				t_on_failure("REROUTE1");
				t_on_reply("LIMIT");
				route(BILLING);
				t_relay();
				xlog("L_ALERT","dst rewrited dans FWD route: $ru source ip $si pour $rd And from user $fU \n");
			} else {---
			
			
				
			---------
-- ASR for all			
select round((sum(case when `duration`> 0 then 1 else 0 end) / count(`src_username`))*100)  ASR
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() and `src_domain`='ip'

-- Duration for all, and USER01
select SEC_TO_TIME(sum(`duration`))   Duration
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE()

select SEC_TO_TIME(sum(`duration`))   Duration
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() and `src_domain`='ip'
 

---ACD
select SEC_TO_TIME(sum(duration)/ sum(case when `duration` > 0 then 1 else 0 end))  ACD
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE()

---USER1 ACD
select SEC_TO_TIME(sum(duration)/ sum(case when `duration` > 0 then 1 else 0 end))  ACD
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() and `src_domain`='ip'
 
-- ANSWERED
select sum(case when `duration`> 0 then 1 else 0 end) answerd
from `collection_cdrs` where DATE(`call_start_time`)<= CURDATE()- INTERVAL 1 DAY 


 _____ JOUR AVANT 
 select SEC_TO_TIME(sum(`duration`))   Duration
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() - INTERVAL 1 DAY and `src_domain`='ip'

---- hier simberry duration
select SEC_TO_TIME(sum(`duration`))   Duration
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() - INTERVAL 1 DAY and `dst_username` LIKE '6288%'

asr simberry
select round((sum(case when `duration`> 0 then 1 else 0 end) / count(`src_username`))*100)  ASR
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() - INTERVAL 1 DAY and `dst_username` LIKE '6288%'

acd simberry
select SEC_TO_TIME(sum(duration)/ sum(case when `duration` > 0 then 1 else 0 end))  ACD
from `collection_cdrs` where DATE(`call_start_time`)= CURDATE() - INTERVAL 1 DAY and `dst_username` LIKE '6288%'

--------------------------------- BILLING USER01-------------------------------------

select sum(case when `duration`> 0 then 1 else 0 end) answerd
from `collection_cdrs` where DATE(`call_start_time`)<= CURDATE()- INTERVAL 1 DAY and `src_domain`='ip'

select round((sum(case when `duration`> 0 then 1 else 0 end) / count(`src_username`))*100)  ASR
from `collection_cdrs` where DATE(`call_start_time`)<= CURDATE()- INTERVAL 1 DAY and `src_domain`='ip'

select SEC_TO_TIME(sum(duration)/ sum(case when `duration` > 0 then 1 else 0 end))  ACD
from `collection_cdrs` where DATE(`call_start_time`)<= CURDATE()- INTERVAL 1 DAY and `src_domain`='ip'

select SEC_TO_TIME(sum(`duration`))   Duration
from `collection_cdrs` where DATE(`call_start_time`)<= CURDATE()- INTERVAL 1 DAY and `src_domain`='ip'


--------------------------------- BILLING USER02-------------------------------------
select sum(`duration`)/60   Duration
from `collection_cdrs` where DATE(`call_start_time`) > "2018-04-01" and `src_domain`='ip'

select sum(case when `duration`> 0 then 1 else 0 end) answerd
from `collection_cdrs` where DATE(`call_start_time`) > "2018-04-01" and `src_domain`='ip'

select round((sum(case when `duration`> 0 then 1 else 0 end) / count(`src_username`))*100)  ASR
from `collection_cdrs` where DATE(`call_start_time`) > "2018-04-01" and `src_domain`='ip'


select SEC_TO_TIME(sum(duration)/ sum(case when `duration` > 0 then 1 else 0 end))  ACD
from `collection_cdrs` where DATE(`call_start_time`) > "2018-04-01" and `src_domain`='ip'

				------------------
				
update allow set status=0
				
				----------------

