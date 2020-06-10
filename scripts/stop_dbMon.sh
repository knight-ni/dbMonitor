#!/bin/sh
local_ip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ../dbMon.conf`
ps -ef|grep "start_dbMon.sh"|grep -v grep|awk '{print "kill -15 "$2}'|sh
curl -X POST "http://${local_ip}:5000/shutdown"
