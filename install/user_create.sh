#!/bin/sh
basedir=$(dirname $(dirname $(readlink -f "$0")))
conf=${basedir}/conf/dbMon.conf

rm -rf nohup.out
username=`awk -F'=' '{if($1=="username"){gsub("\r",""); print $NF}}' ${conf}`
password=`awk -F'=' '{if($1=="password"){gsub("\r",""); print $NF}}' ${conf}`

id ${username} >/dev/null 2>/dev/null
if [ $? -ne 0 ];then
useradd ${username} -g ${username} -G informix
echo ${password}|passwd ${username} --stdin
echo ". ${basedir}/conf/dbmon_env" >>~dbmon/.bash_profile
fi

echo "Run Command Followed as informix to grant permission to ${username}."

cat <<EOF
echo "grant connect to ${username}"|dbaccess sysadmin
echo "grant resource to ${username}"|dbaccess sysadmin
echo "grant dba to ${username}"|dbaccess sysadmin
echo "grant connect to ${username}"|dbaccess sysmaster
echo "grant resource to ${username}"|dbaccess sysmaster
echo "grant dba to ${username}"|dbaccess sysmaster
EOF
