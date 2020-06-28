#!/bin/sh

conf=`readlink -f $0 |awk -F'/' -v OFS='/' '{NF--NF--}1'`/conf/dbMon.conf

local_ip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ${conf}`
ps -ef|grep "start_dbMon.sh"|grep -v grep|awk '{print "kill -15 "$2}'|sh
curl -X POST "http://${local_ip}:5000/shutdown"
