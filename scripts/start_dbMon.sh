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

rm -f nohup.out
pypath=`awk -F'=' '{if($1=="pypath"){gsub("\r",""); print $NF}}' ../dbMon.conf`
python=${pypath}/bin/python3
#echo " "|nice -n 18 nohup ${python} WebSrv.py &
cd ..
nohup ${python} WebSrv.py >/dev/null 2>dbmon.log &

while true
do
if [ -f nohup.out ] && [ `du -sm ${PWD}/nohup.out |awk '{print $1}'` -ge 10 ];then
cp -f ${PWD}/nohup.out ${PWD}/nohup.out.`date +%Y%m%d`
cat /dev/null >nohup.out
else
find ${PWD} -name "nohup.out.*" -mtime +3 -exec rm -rf {} \;
sleep 60
fi
done >/dev/null 2>/dev/null &
