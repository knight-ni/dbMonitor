#!/usr/bin/env bash
v1=7.8.0
v2=linux-x86_64

if [ $1 == "download" ];then
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${v1}-${v2}.tar.gz -o elasticsearch-${v1}-${v2}.tar.gz
else 
file=$1
dir=`echo $file|sed -e 's/\.tar\.gz//'`
tar -xvzf $file -C /etc
fi

cp -rp elasticsearch/elasticsearch.yml /etc/elasticsearch-${v1}/config/

chown -R dbmon.dbmon /etc/elasticsearch-${v1}

cat <<EOF
add these to /etc/security/limits.conf if not exists
dbmon soft nofile 65536
dbmon hard nofile 65536
EOF

cat <<EOF >/etc/elasticsearch-${v1}/start.sh
#/bin/sh
su - dbmon -c "cd /etc/elasticsearch-${v1}/bin;nohup ./elasticsearch &"
EOF

cat <<EOF >/etc/elasticsearch-${v1}/stop.sh
#/bin/sh
ps -ef|grep elasticsearch|grep -v grep|awk '{print "kill -15 "\$2}'|sh
EOF

