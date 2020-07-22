#!/bin/sh
if [ $# -ne 1 ];then
echo "file or mode needed"
exit 999
fi


v1=7.1.0-1
v2=x86_64

if [ $1 == "download" ];then
wget https://dl.grafana.com/oss/release/grafana-${v1}.${v2}.rpm -o grafana-${v1}.${v2}.rpm
else
file=$1
fi

yum install -y $file

for p in grafana-clock-panel grafana-piechart-panel michaeldmoore-annunciator-panel
do
grafana-cli plugins install $p
done

/etc/rc.d/init.d/grafana-server restart
