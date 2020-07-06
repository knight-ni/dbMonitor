#!/bin/sh


basedir=$(dirname $(dirname $(readlink -f "$0")))
scripts=${basedir}/scripts

sh ${scripts}/stopfb.sh >/dev/null 2>/dev/null
sh ${scripts}/startfb.sh

sh ${scripts}/stop_dbMon.sh >/dev/null 2>/dev/null
sh ${scripts}/start_dbMon.sh
