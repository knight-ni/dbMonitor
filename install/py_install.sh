#!/bin/sh
#pyenv install --list to get all version supported

v=3.7.2

pwd=${PWD}

py_setup(){
    if [ $? -eq 0 ];then
       export LDFLAGS="-L/usr/local/openssl/lib";
       export CPPFLAGS="-I/usr/local/openssl/include";
       export PKG_CONFIG_PATH="/usr/local/openssl/lib/pkgconfig";
       wget https://npm.taobao.org/mirrors/python//$v/Python-$v.tar.xz -P ~/.pyenv/cache;
       pyenv install $v
    else
       echo "ERROR";exit 999
    fi

}

clean(){
    rm -rf ~/.pyenv/cache/*
}

py_setup
clean

exit 0
