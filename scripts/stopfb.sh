#!/bin/sh

conf=`readlink -f $0 |awk -F'/' -v OFS='/' '{NF--NF--}1'`/conf/dbMon.conf

fbpath=`awk -F'=' '{if($1=="fbpath"){gsub("\r",""); print $NF}}' ${conf}`
local_ip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ${conf}`
db_logpath=`awk -F'=' '{if($1=="dblog_path"){gsub("\r",""); print $NF}}' ${conf}`
ps -ef|grep "./filebeat -E MON_ADDR=${local_ip} -E FILEPATH=${db_logpath} -e -c filebeat.yml -d publish"|grep -v grep|awk '{print "kill -15 "$2}'|sh

exit 0
