#!/bin/sh
#pyenv install --list to get all version supported

pwd=${PWD}

if [ `whoami` != "root" ];then
echo "Must Run As Root";
exit
fi

mode=openssl
sslv1=1.1.1
sslv2=f
libresslv=3.2.0
osv=`uname -r|awk -F"." '{print $4}'|sed -e 's/el//g'`

check(){
    if [ $? -eq 0 ];then
       echo success
    else 
       echo failed
       exit
    fi
}

rcheck(){
    if [ $? -eq 0 ];then
       echo failed
       exit
    else
       echo success
    fi
}

pack_setup() {
cat <<EOF >/etc/yum.repos.d/CentOS${osv}.repo
[dbMonitor]
name=CentOS-$releasever - Base - 163.com
baseurl=http://mirrors.163.com/centos/${osv}/os/x86_64/
mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
gpgcheck=0
EOF
    mis_pack=`rpm -q zlib-devel bzip2-devel ncurses-devel readline-devel tk-devel gcc make readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs libffi-devel xz-devel unixODBC-devel unzip wget gcc-c++|grep installed|awk '{print $2}'|sed -e ':a;N;s/\n/ /;ta'`
    if [ "$mis_pack" != "" ];then
        yum install -y deltarpm --enablerepo=dbMonitor
        yum install -y ${mis_pack} --enablerepo=dbMonitor
    fi
    rpm -q zlib-devel bzip2-devel ncurses-devel readline-devel tk-devel gcc make readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs libffi-devel xz-devel |grep "not installed"
    rcheck
    rm /etc/yum.repos.d/CentOS${osv}.repo
}

openssl_setup() {
    if [  ! -f openssl-${sslv1}${sslv2}.tar.gz ];then
        wget https://www.openssl.org/source/old/${sslv1}/openssl-${sslv1}${sslv2}.tar.gz -O openssl-${sslv1}${sslv2}.tar.gz
    fi
    gzip -dc openssl-${sslv1}${sslv2}.tar.gz|tar xvf -;
    cd openssl-${sslv1}${sslv2};
    ./config --prefix=/usr/local/openssl shared;
    make;
    make install;
    ln -sf /usr/local/openssl/lib/libssl.so.1.1 /usr/lib64/libssl.so.1.1;
    ln -sf /usr/local/openssl/lib/libcrypto.so.1.1 /usr/lib64/libcrypto.so.1.1;
    /bin/cp -rp /usr/local/openssl/bin/openssl /usr/bin/openssl
    openssl version
    check
}

libressl_setup(){
    if [ ! -f libressl-${libresslv}.tar.gz ];then
        wget https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-${libresslv}.tar.gz -O libressl-${libresslv}.tar.gz
    fi
    gzip -dc libressl-${libresslv}.tar.gz|tar xvf -
    cd libressl-${libresslv}
    ./config
    make
    make install
    ln -sf /usr/local/openssl/lib/libssl.so.48 /usr/lib64/libssl.so.48
    openssl version
    check
}

clean(){
    rm -rf ${pwd}/openssl-${sslv1}${sslv2}
    rm -rf ${pwd}/libressl-${libresslv}
}

pack_setup

x1=`openssl version|grep -c ${sslv1}${sslv2}`
x2=`openssl version|grep -c ${libresslv}`

if [ ${x1} == ${x2} ];then
   case $mode in 
   openssl)
      openssl_setup
   ;;
   libressl)
      libressl_setup
   ;;
   *)
      echo "Invalid"
      exit 999
   ;;
   esac
fi
clean

exit 0
