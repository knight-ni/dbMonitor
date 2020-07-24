#!/bin/sh

v1=2.19.2
v2=linux-amd64

if [ ! -f prometheus-${v1}.${v2}.tar.gz ];then
wget https://github.com/prometheus/prometheus/releases/download/v2.19.2/prometheus-${v1}.${v2}.tar.gz -O prometheus-${v1}.${v2}.tar.gz
tar -xvzf prometheus-${v1}.${v2}.tar.gz -C /etc
else
file=prometheus-${v1}.${v2}.tar.gz
dir=`echo $file|sed -e 's/\.tar\.gz//'`
tar -xvzf $file -C /etc
fi

basedir=$(dirname $(dirname $(dirname $(readlink -f "$0"))))
conf=${basedir}/conf/dbMon.conf

hostname=`awk -F'=' '{if($1=="dsn"){gsub("\r",""); print $NF}}' ${conf}`
localip=`awk -F'=' '{if($1=="local_ip"){gsub("\r",""); print $NF}}' ${conf}`

grep -q ${localip} ${basedir}/sample/prometheus/prometheus.yml

if [ $? -ne 0 ];then
cat <<EOF >>${basedir}/sample/prometheus/prometheus.yml

  - job_name: 'dbMonitor-${hostname}'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    metrics_path: /metrics/${hostname}

    static_configs:
    - targets: ['${localip}:5000']
EOF
fi

/bin/cp -rp ${basedir}/sample/prometheus/prometheus.yml /etc/prometheus-${v1}.${v2}/
cat <<EOF >/etc/prometheus-${v1}.${v2}/start.sh
#/bin/sh
cd /etc/prometheus-${v1}.${v2}
nohup ./prometheus --config.file=./prometheus.yml --storage.tsdb.retention.time=15d &
EOF

cat <<EOF >/etc/prometheus-${v1}.${v2}/stop.sh
#/bin/sh
ps -ef|grep prometheus|grep -v grep|grep storage.tsdb.retention.time|awk '{print "kill -15 "\$2}'|sh
EOF
