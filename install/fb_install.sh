#!/bin/sh

if [ `whoami` != "root" ];then
echo "Must Run As Root";
exit
fi

if [ $# -ne 1 ];then
echo "file or mode needed"
exit 999
fi

v1=7.8.0
v2=x86_64


if [ $1 == "download" ];then
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${v1}-${v2}.rpm -o filebeat-${v1}-${v2}.rpm
else
file=$1
yum install -y $file
fi

cp  ../sample/filebeat/filebeat.yml /etc/filebeat/
mkdir -p /var/lib/filebeat
mkdir -p /var/log/filebeat
chown -R dbmon.dbmon /etc/filebeat
chown -R dbmon.dbmon /var/lib/filebeat
chown -R dbmon.dbmon /var/log/filebeat
