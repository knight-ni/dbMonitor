#!/bin/sh

basedir=$(dirname $(dirname $(readlink -f "$0")))
conf=${basedir}/conf/dbMon.conf
log=${basedir}/logs/filebeat.log

rm -rf nohup.out
fbpath=`awk -F'=' '{if($1=="fbpath"){gsub("\r",""); print $NF}}' ${conf}`
fbconf=`awk -F'=' '{if($1=="fbconf"){gsub("\r",""); print $NF}}' ${conf}`
local_ip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ${conf}`
db_logpath=`awk -F'=' '{if($1=="dblog_path"){gsub("\r",""); print $NF}}' ${conf}`
nohup ${fbpath} -E MON_ADDR=${local_ip} -E FILEPATH=${db_logpath} -e -c ${fbconf} -d publish -path.home /usr/share/filebeat -path.config /etc/filebeat -path.data /var/lib/filebeat >${log} 2>&1 &

exit 0
