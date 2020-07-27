#!/bin/sh
v1=7.1.0-1
v2=x86_64

cat <<EOF >/etc/yum.repos.d/Grafana.repo

[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF

if [ ! -f grafana-${v1}.${v2}.rpm ];then
    yum install -y grafana
fi

yum install -y grafana-${v1}.${v2}.rpm
rm /etc/yum.repos.d/Grafana.repo

for p in grafana-clock-panel grafana-piechart-panel michaeldmoore-annunciator-panel
do
if [ ${p} == "grafana-clock-panel" ];then
grafana-cli plugins install $p 1.0.3
else
grafana-cli plugins install $p
fi
done

/etc/rc.d/init.d/grafana-server restart
