#!/bin/sh

CWD=`readlink -f $0 |awk -F'/' -v OFS='/' '{NF--NF--}1'`

sh ${PWD}/scripts/stopfb.sh >/dev/null 2>/dev/null
sh ${PWD}/scripts/startfb.sh

sh ${PWD}/scripts/stop_dbMon.sh >/dev/null 2>/dev/null
sh ${PWD}/scripts/start_dbMon.sh
