#!/bin/sh
. ~/.bash_profile
pyenv virtualenv-delete dbMonitor
pyenv virtualenv 3.7.2 dbMonitor
pyenv virtualenv-init -
pyenv init
. ~/.pyenv/versions/dbMonitor/bin/activate
pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
pip install -r ../../conf/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
