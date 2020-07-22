#!/bin/sh
#
#Options:
#  -S	use the `soft' resource limit
#  -H	use the `hard' resource limit
#  -a	all current limits are reported
#  -b	the socket buffer size
#  -c	the maximum size of core files created
#  -d	the maximum size of a process's data segment
#  -e	the maximum scheduling priority (`nice')
#  -f	the maximum size of files written by the shell and its children
#  -i	the maximum number of pending signals
#  -k	the maximum number of kqueues allocated for this process
#  -l	the maximum size a process may lock into memory
#  -m	the maximum resident set size
#  -n	the maximum number of open file descriptors
#  -p	the pipe buffer size
#  -q	the maximum number of bytes in POSIX message queues
#  -r	the maximum real-time scheduling priority
#  -s	the maximum stack size
#  -t	the maximum amount of cpu time in seconds
#  -u	the maximum number of user processes
#  -v	the size of virtual memory
#  -x	the maximum number of file locks
#  -P	the maximum number of pseudoterminals
#  -T	the maximum number of threads


if [ `whoami` != "dbmon" ];then
echo "Must Be Run as dbmon"
exit 9
fi

basedir=$(dirname $(dirname $(readlink -f "$0")))
conf=${basedir}/conf/dbMon.conf
env=${basedir}/conf/dbmon_env
log=${basedir}/dbmon.log
srv=${basedir}/src/WebSrv.py

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
