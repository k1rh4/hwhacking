[root@FriendlyARM /opt]# tftp 192.168.0.11 BusyBox v1.13.3 (2010-07-24 19:11:35 CST) multi-call binaryUsage: tftp [OPTION]... HOST [PORT]Transfer a file from/to tftp serverOptions: -l FILE Local FILE -r FILE Remote FILE -g Get file -p Put file -b SIZE Transfer blocks of SIZE octets

PUT : 
$tftp -l {local file name} -p {server ip} 

GET :
$tftp -r {remote fiel name} -g {server ip}

간단한 예제로 보자면,

PUT : 
$tftp -l local_file.txt -p 192.168.0.10
GET : # tftp -r remote_file.txt -g 192.168.0.10
