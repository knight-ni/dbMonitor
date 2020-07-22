#!/bin/sh
#pyenv install --list to get all version supported

pwd=${PWD}

if [ `whoami` != "root" ];then
echo "Must Run As Root";
exit
fi

v=3.7.2
mode=openssl
sslv1=1.1.1
sslv2=f
libresslv=3.2.0

check(){
    if [ $? -eq 0 ];then
       echo success
    else 
       echo failed
       exit
    fi
}

pack_setup() {
    mis_pack=`rpm -q readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs libffi-devel|grep installed|awk '{print $2}'|sed -e ':a;N;s/\n/ /;ta'`
    if [ $mis_pack ];then
        "yum install -y ${mis_pack}"
    fi
    check
}

openssl_setup() {
    wget https://www.openssl.org/source/old/${sslv1}/openssl-${sslv1}${sslv2}.tar.gz -O openssl-${sslv1}${sslv2}.tar.gz
    tar -xvzf openssl-${sslv1}${sslv2}.tar.gz;
    cd openssl-${sslv1}${sslv2};
    ./config --prefix=/usr/local/openssl shared;
    make;
    make install;
    ln -s /usr/local/openssl/lib/libssl.so.1.1 /usr/lib64/libssl.so.1.1;
    ln -s /usr/local/openssl/lib/libcrypto.so.1.1 /usr/lib64/libcrypto.so.1.1;
    openssl version
    check
}

libressl_setup(){
    wget https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-${libresslv}.tar.gz -O libressl-${libresslv}.tar.gz
    tar -xvzf libressl-${libresslv}.tar.gz
    cd libressl-${libresslv}
    ./config
    make
    make install
    ln -s /usr/local/openssl/lib/libssl.so.48 /usr/lib64/libssl.so.48
    openssl version
    check
}

py_setup(){
    if [ $? -eq 0 ];then
       su - dbmon -c "export LDFLAGS=\"-L/usr/local/openssl/lib\";\
                      export CPPFLAGS=\"-I/usr/local/openssl/include\";\
                      export PKG_CONFIG_PATH=\"/usr/local/openssl/lib/pkgconfig\";\
                      wget https://npm.taobao.org/mirrors/python//$v/Python-$v.tar.xz -P ~/.pyenv/cache;\
                      pyenv install $v"
    else
       echo "ERROR";exit 999
    fi

}

clean(){
    rm -rf ./openssl-${sslv1}${sslv2} 
    rm -rf ./libressl-${libresslv}
    rm -rf ~/.pyenv/cache/*
    rm -rf ./openssl-${sslv1}${sslv2}.tar.gz
    rm -rf ./libressl-${libresslv}.tar.gz
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
py_setup
clean

exit 0
