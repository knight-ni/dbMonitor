#!/bin/sh
basedir=$(dirname $(dirname $(readlink -f "$0")))
conf=${basedir}/conf/dbMon.conf
env=${basedir}/conf/dbmon_env
log=${basedir}/logs/dbmon.log
srv=${basedir}/src/WebSrv.py

username=`awk -F'=' '{if($1=="username"){gsub("\r",""); print $NF}}' ${conf}`

if [ `whoami` != "${username}" ];then
echo "Must Be Run as ${username}"
exit 9
fi

source ${env}
. ~/.pyenv/versions/dbMonitor/bin/activate
nohup python -B ${srv} >/dev/null 2>${log} &

while true
do
if [ -f ${log} ] && [ `du -sm ${log}|awk '{print $1}'` -ge 10 ];then
cp -f ${log} ${log}.`date +%Y%m%d`
cat /dev/null >${log}
else
find ${basedir} -name "$log.*" -mtime +3 -exec rm -rf {} \;
sleep 60
fi
done >/dev/null 2>/dev/null &
