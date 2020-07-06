#!/bin/sh

export INFORMIXSERVERDIR=/opt/informix/INST1/informixdir
export INFORMIXDIR=/opt/informix/INST1/informixclientdir
export INFORMIXSQLHOSTS=$INFORMIXSERVERDIR/etc/sqlhosts.INST1
export INFORMIXSERVER=jsvfpredb_tcp
export ONCONFIG=$INFORMIXSERVERDIR/etc/onconfig.INST1
export LD_LIBRARY_PATH=/opt/informix/INST1/informixdir/lib:/opt/informix/INST1/informixclientdir/lib:/opt/informix/INST1/informixclientdir/lib/esql:/opt/informix/INST1/informixclientdir/lib/cli:/opt/informix/INST1/informixclientdir/lib/client:/opt/informix/INST1/informixclientdir/lib/c++:/opt/informix/INST1/informixclientdir:/opt/informix/INST1/informixclientdir/lib/dmi:/home/dbmon/openssl/lib
export ODBCINI=/home/dbmon/dbMonitor/odbc.ini
export PATH=/home/dbmon/Python37/bin:$INFORMIXDIR/bin:$INFORMIXCLIENTDIR/bin:$PATH

basedir=$(dirname $(dirname $(readlink -f "$0")))
scripts=${basedir}/scripts


sh ${scripts}/stopfb.sh >/dev/null
sh ${scripts}/stop_dbMon.sh 
