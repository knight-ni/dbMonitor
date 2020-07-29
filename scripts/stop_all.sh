#!/bin/sh
basedir=$(dirname $(dirname $(readlink -f "$0")))
scripts=${basedir}/scripts

sh ${scripts}/stopfb.sh >/dev/null
sh ${scripts}/stop_dbMon.sh 
