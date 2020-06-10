#!/bin/bash
retention=`awk -F'=' '{if($1=="es_retention") print$2}' dbMon.conf`
ts=`date -d "${retention} day ago" +%Y%m%d`
es_addr=`awk -F= '{if($1=="es_url"){gsub(/\r/,"",$NF);print $2}}' dbMon.conf`
curl -s -XGET http://${es_addr}/_cat/indices?v |sort -k 3|awk '{split($3,b,"-");gsub(/\./,"",b[2]);if (b[2]<'"${ts}"') print $3}' >clean.lst
while read line
do
echo $line
curl -s -XDELETE "http://${es_addr}/$line"
done<clean.lst
rm -rf clean.lst
