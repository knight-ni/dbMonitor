#!/bin/sh
pyenv virtualenv-delete dbMonitor
pyenv virtualenv 3.7.2 dbMonitor
pyenv virtualenv-init -
pyenv init
. ~/.pyenv/versions/dbMonitor/bin/activate
pip install --upgrade pip
pip install -r ../conf/requirements.txt
