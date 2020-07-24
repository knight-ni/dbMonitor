#!/bin/sh
basedir=$(dirname $(dirname $(readlink -f "$0")))
conf=${basedir}/conf/dbMon.conf

rm -rf nohup.out
username=`awk -F'=' '{if($1=="username"){gsub("\r",""); print $NF}}' ${conf}`
password=`awk -F'=' '{if($1=="password"){gsub("\r",""); print $NF}}' ${conf}`

id ${username} >/dev/null 2>/dev/null
if [ $? -ne 0 ];then
useradd ${username}
echo ${password}|passwd ${username} --stdin
echo ". ${basedir}/conf/dbmon_env" >>~dbmon/.bash_profile
fi
