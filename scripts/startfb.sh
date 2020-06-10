#!/bin/sh

rm -rf nohup.out
fbpath=`awk -F'=' '{if($1=="fbpath"){gsub("\r",""); print $NF}}' ../dbMon.conf`
local_ip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ../dbMon.conf`
db_logpath=`awk -F'=' '{if($1=="dblog_path"){gsub("\r",""); print $NF}}' ../dbMon.conf`
cd $fbpath
nohup ./filebeat -E MON_ADDR=${local_ip} -E FILEPATH=${db_logpath} -e -c filebeat.yml -d publish >/dev/null 2>error.log  &

exit 0
