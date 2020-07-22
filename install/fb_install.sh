#!/bin/sh

if [ `whoami` != "root" ];then
echo "Must Run As Root";
exit
fi

rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch

cat <<EOF >/etc/yum.repos.d/elastic.repo
[elastic-7.x]
name=Elastic repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

yum install -y filebeat
cp  ../sample/filebeat/filebeat.yml /etc/filebeat/
chown -R dbmon.dbmon /etc/filebeat
chown -R dbmon.dbmon /var/lib/filebeat
chown -R dbmon.dbmon /var/log/filebeat
