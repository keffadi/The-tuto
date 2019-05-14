### Ubuntu 18 Debain 9 use case

update
```
sudo -s
apt-get update
```

set time zone 
```
dpkg-reconfigure tzdata
apt-get install ntp
/etc/init.d/ntp restart
```

add user and group
```
adduser asteriskpbx    ( after password prompt: asteriskpbx)
```

install dependancies
```
apt-get install build-essential subversion  libncurses5-dev libssl-dev libxml2-dev libsqlite3-dev uuid-dev vim-nox
```


Create your directory structure & download source
```
mkdir -p ~/src/asterisk-complete/asterisk 
cd ~/src/asterisk-complete/asterisk
svn co http://svn.asterisk.org/svn/asterisk/branches/11
```

installation
```
cd ~/src/asterisk-complete/asterisk/11
 ./configure
 make
 make install 
 make config

 ```
  ```
 cd ~/src/asterisk-complete/asterisk/11/ 
 sudo apt-get install libnewt-dev
 sudo apt-get install libbluetooth-dev
 cd menuselect
 get out from menu select folder
 make clean
 ./configure --with-bluetooth
 ( on raspberry cd ~/src/asterisk-complete/asterisk/11/ )
 make menuselect   (core sound package EN-WAV, EN-ULAW,EN-ALAW) & (Extra Sound Packages EN-WAV, EN-ULAW,EN-ALAW)
 make install
 chown -R asteriskpbx:asteriskpbx /var/lib/asterisk/sounds/
  ```
  
   ```
chown -R asteriskpbx:asteriskpbx /var/lib/asterisk/
chown -R asteriskpbx:asteriskpbx /var/spool/asterisk/ 
chown -R asteriskpbx:asteriskpbx /var/log/asterisk/
chown -R asteriskpbx:asteriskpbx /var/run/asterisk/

 mkdir -p /etc/asterisk
 chown asteriskpbx:asteriskpbx /etc/asterisk
 cd /etc/asterisk/
 
 cp ~/src/asterisk-complete/asterisk/11/configs/indications.conf.sample  ./indications.conf
 cp ~/src/asterisk-complete/asterisk/11/configs/asterisk.conf.sample  /etc/asterisk/asterisk.conf

vim /etc/asterisk/asterisk.conf   (uncommenting and add pbx)   / esc then :wq
test =>  /usr/sbin/asterisk -cvvv   then "module show"  then "core stop now"
 ```
 
 Create the modules.conf file
  ```
cat >> /etc/asterisk/modules.conf 
 ```
 ```
; The modules.conf file, used to define which modules Asterisk should load (or
; not load).
;
[modules]
autoload=yes
; Resource modules currently not needed
noload => res_speech.so
noload => res_phoneprov.so
noload => res_ael_share.so
noload => res_ael_share.so
noload => res_clialiases.so
noload => res_adsi.so
; PBX modules currently not needed
noload => pbx_ael.so
noload => pbx_dundi.so
; Channel modules currently not needed
noload => chan_oss.so
noload => chan_mgcp.so
noload => chan_skinny.so
noload => chan_phone.so
noload => chan_agent.so
noload => chan_unistim.so
noload => chan_alsa.so
; Application modules currently not needed
noload => app_nbscat.so
noload => app_amd.so
noload => app_minivm.so
noload => app_zapateller.so
noload => app_ices.so
noload => app_sendtext.so
noload => app_speech_utils.so
noload => app_mp3.so
noload => app_flash.so
noload => app_getcpeid.so
noload => app_setcallerid.so
noload => app_adsiprog.so
noload => app_forkcdr.so
noload => app_sms.so
noload => app_morsecode.so
noload => app_followme.so
noload => app_url.so
noload => app_alarmreceiver.so
noload => app_disa.so
noload => app_dahdiras.so
noload => app_senddtmf.so
noload => app_sayunixtime.so
noload => app_test.so
noload => app_externalivr.so
noload => app_image.so
noload => app_dictate.so
noload => app_festival.so
load => chan_mobile.so
  ```
   save 
```
Ctrl+D
```

Configuremusiconhold.conf

```
cat > musiconhold.conf
```
```
; musiconhold.conf
[general]
[default]
mode=files
directory=moh
 ```   
save
```
Ctrl+D
```

create /etc/asterisk/sip.conf
```
nano sip.conf
```
```
[general]
context=unauthenticated           ; default context for incoming calls
allowguest=no                     ; disable unauthenticated calls
srvlookup=no                      ; disable DNS SRV record lookup on outbound calls
                                 ;   (unless you have a reliable DNS connection,
                                            ;   in which case yes)
udpbindaddr=0.0.0.0               ; listen for UDP requests on all interfaces
tcpenable=no                      ; disable TCP support
[office-phone](!)                 ; create a template for our devices
type=friend                       ;   the channel driver will match on username first,
                                 ;   IP second
context=LocalSets                 ;   this is where calls from the device will enter
                                 ;   the dialplan
host=dynamic                      ; the device will register with asterisk
nat=force_rport,comedia           ; assume device is behind NAT
                                 ;   *** NAT stands for Network Address Translation,
                                 ;   which allows multiple internal devices to share an
                                 ;   external IP address.
dtmfmode=auto                     ;   accept touch-tones from the devices, negotiated
                                 ;   automatically
disallow=all                      ; reset which voice codecs this device will accept or offer
allow=g722                        ; audio codecs to accept from, and request to, the device
allow=ulaw                        ; in the order we prefer
allow=alaw
                                 ; define a device name and use the office-phone template
[test01](office-phone)
secret=keffa2015                 ; a unique password for this device --
                                ; DON'T USE THE PASSWORD WE'VE USED IN THIS EXAMPLE!
                                ; define another device name using the same template
[test02](office-phone)
secret=keffa2015                ; a unique password for this device --
                               ; DON'T USE THE PASSWORD WE'VE USED IN THIS EXAMPLE!
```

create /etc/asterisk/extensions.conf  for dialplan
```
nano /etc/asterisk/extensions.conf
[LocalSets] ; this is the context name
exten => 100,1,Dial(SIP/test01) ; Replace 0000FFFF0001 with your device name
exten => 101,1,Dial(SIP/test02) ; Replace 0000FFFF0002 with your device name
exten => 200,1,Answer()
same => n,Playback(hello-world)
same => n,Hangup()
```

