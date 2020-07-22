#!/bin/sh

if [ $# -ne 1 ];then
echo "file or mode needed"
exit 999
fi

v1=2.19.2
v2=linux-amd64

if [ $1 == "download" ];then
wget https://github.com/prometheus/prometheus/releases/download/v2.19.2/prometheus-${v1}.${v2}.tar.gz -O prometheus-${v1}.${v2}.tar.gz
tar -xvzf prometheus-${v1}.${v2}.tar.gz -C /etc
else
file=$1
dir=`echo $file|sed -e 's/\.tar\.gz//'`
tar -xvzf $file -C /etc
fi

cp -rp prometheus/prometheus.yml /etc/prometheus-${v1}.${v2}/
cat <<EOF >/etc/prometheus-${v1}.${v2}/start.sh
cd /etc/prometheus-${v1}.${v2}
#/bin/sh
nohup ./prometheus --config.file=./prometheus.yml --storage.tsdb.retention.time=15d &
EOF

cat <<EOF >/etc/prometheus-${v1}.${v2}/stop.sh
#/bin/sh
ps -ef|grep prometheus|grep -v grep|grep storage.tsdb.retention.time|awk '{print "kill -15 "\$2}'|sh
EOF
