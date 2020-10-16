#!/bin/bash
basedir=$(dirname $(dirname $(readlink -f "$0")))
conf=${basedir}/conf/dbMon.conf

es_addr=`awk -F= '{if($1=="es_url"){gsub(/\r/,"",$NF);print $2}}' $conf`
retention=`awk -F'=' '{if($1=="es_retention") print$2}' $conf`
ts=`date -d "${retention} day ago" +%Y%m%d`

curl -s -XGET http://${es_addr}/_cat/indices?v |sed 1d|sort -k 3|awk '{split($3,b,"-");gsub(/\./,"",b[3]);if (b[3]<'"${ts}"') print $3}' >clean.lst
while read line
do
echo $line
curl -s -XDELETE "http://${es_addr}/$line"
done<clean.lst
rm -rf clean.lst
