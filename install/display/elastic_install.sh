#!/usr/bin/env bash
v1=7.8.0
v2=linux-x86_64

basedir=$(dirname $(dirname $(dirname $(readlink -f "$0"))))
conf=${basedir}/conf/dbMon.conf

rm -rf nohup.out
es_addr=`awk -F'=' '{if($1=="es_url"){gsub("\r",""); print $NF}}' ${conf}`
read ip port <<<`echo ${es_addr}|awk -F":" '{print $1" "$2}'`

if [ ! -f elasticsearch-${v1}-${v2}.tar.gz ];then
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${v1}-${v2}.tar.gz -o elasticsearch-${v1}-${v2}.tar.gz
else 
file=elasticsearch-${v1}-${v2}.tar.gz
dir=`echo $file|sed -e 's/\.tar\.gz//'`
tar -xvzf $file -C /etc
fi

/bin/cp -rp ${basedir}/sample/elasticsearch/elasticsearch.yml /etc/elasticsearch-${v1}/config/

sed -i 's!cluster.initial_master_nodes.*!cluster.initial_master_nodes: ["'"${ip}"'"]!' /etc/elasticsearch-${v1}/config/elasticsearch.yml
sed -i 's!http.port.*!http.port: '"${port}"'!' /etc/elasticsearch-${v1}/config/elasticsearch.yml


chown -R dbmon.dbmon /etc/elasticsearch-${v1}

nofile=`su - dbmon -c "ulimit -n"`

if [ $nofile -lt 65536 ];then
cat <<EOF >>/etc/security/limits.conf
############add for dbmon
dbmon soft nofile 65536
dbmon hard nofile 65536

EOF
fi

max_count=`sysctl -a 2>/dev/null|grep vm.max_map_count|awk -F"=" '{print $NF}'`
if [ ${max_count} -lt 262144 ];then
cat <<EOF >>/etc/sysctl.conf
vm.max_map_count=655360
EOF
sysctl -p
fi


cat <<EOF >/etc/elasticsearch-${v1}/start.sh
#/bin/sh
su - dbmon -c "cd /etc/elasticsearch-${v1}/bin;nohup ./elasticsearch >/etc/elasticsearch-${v1}/logs/elasticsearch.log &"

curl http://${ip}:${port}
while [ \$? -ne 0 ];
do
sleep 1
curl http://${ip}:${port}
done

curl -XPUT -H "Content-Type: application/json" -d '{"transient":{"cluster":{"max_shards_per_node":100000}}}' 'http://${ip}:${port}/_cluster/settings'
EOF

cat <<EOF >/etc/elasticsearch-${v1}/stop.sh
#/bin/sh
ps -ef|grep elasticsearch|grep -v grep|awk '{print "kill -15 "\$2}'|sh
EOF

