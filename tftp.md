[root@FriendlyARM /opt]# tftp 192.168.0.11 BusyBox v1.13.3 (2010-07-24 19:11:35 CST) multi-call binaryUsage: tftp [OPTION]... HOST [PORT]Transfer a file from/to tftp serverOptions: -l FILE Local FILE -r FILE Remote FILE -g Get file -p Put file -b SIZE Transfer blocks of SIZE octets

### usage 
PUT : 
$tftp -l {local file name} -p {server ip} 
GET :
$tftp -r {remote fiel name} -g {server ip}

### example

PUT : 
$tftp -l localfile.txt -p 192.168.0.10
GET :
$tftp -r remotefile.txt -g 192.168.0.10


### tftpd setting 
sudo apt-get install xinetd tftp tftpd
sudo vi /etc/xinetd.d/tftp
```
service tftp
{
    socket_type     = dgram
    protocol        = udp
    wait            = yes
    user            = root
    server          = /usr/sbin/in.tftpd
    server_args     = -s /tftpboot
    disable         = no
    per_source      = 11
    cps             = 100 2
    flags           = IPv4
}
```
sudo mkdir /tftpboot
sudo chmod 777 /tftpboot
sudo /etc/init.d/xinetd restart


### tftpd testing 
cd /tftpboot
touch test.txt
cd /tmp
tftp localhost  
get test.txt  
