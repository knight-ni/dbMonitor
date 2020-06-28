#!/bin/sh

conf=`readlink -f $0 |awk -F'/' -v OFS='/' '{NF--NF--}1'`/conf/dbMon.conf

rm -rf nohup.out
fbpath=`awk -F'=' '{if($1=="fbpath"){gsub("\r",""); print $NF}}' ${conf}`
local_ip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ${conf}`
db_logpath=`awk -F'=' '{if($1=="dblog_path"){gsub("\r",""); print $NF}}' ${conf}`
cd $fbpath
nohup ./filebeat -E MON_ADDR=${local_ip} -E FILEPATH=${db_logpath} -e -c filebeat.yml -d publish >/dev/null 2>error.log  &

exit 0
