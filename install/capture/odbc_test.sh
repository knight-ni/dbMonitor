#!/bin/sh

odbcinst -j >/dev/null 2>/dev/null
if [ $? -ne 0 ];then
   echo "Please Make Sure Your ODBC Can Work!"
   exit 999
fi

basedir=$(dirname $(dirname $(dirname $(readlink -f "$0"))))
conf=${basedir}/conf/dbMon.conf

dsn=`awk -F'=' '{if($1=="dsn"){gsub("\r",""); print $NF}}' ${conf}`
isql -b ${dsn} -v<<EOF
quit
EOF
if [ $? -eq 0 ];then
echo "Success"
else
echo "Failed"
fi

