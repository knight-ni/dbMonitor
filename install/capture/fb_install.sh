#!/bin/sh

if [ `whoami` != "root" ];then
echo "Must Run As Root";
exit
fi

v1=7.8.0
v2=x86_64

if [  ! -f filebeat-${v1}-${v2}.rpm ];then
    wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${v1}-${v2}.rpm -o filebeat-${v1}-${v2}.rpm
fi

yum localinstall -y filebeat-${v1}-${v2}.rpm

basedir=$(dirname $(dirname $(dirname $(readlink -f "$0"))))
conf=${basedir}/conf/dbMon.conf

es_addr=`awk -F'=' '{if($1=="es_url"){gsub("\r",""); print $NF}}' ${conf}`

/bin/cp ${basedir}/sample/filebeat/filebeat.yml /etc/filebeat/
sed -i 's! hosts: .*! hosts: ['"${es_addr}"']!' /etc/filebeat/filebeat.yml

mkdir -p /var/lib/filebeat
mkdir -p /var/log/filebeat
chown -R dbmon.dbmon /etc/filebeat
chown -R dbmon.dbmon /var/lib/filebeat
chown -R dbmon.dbmon /var/log/filebeat
