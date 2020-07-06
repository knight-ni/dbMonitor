# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

export PATH

export INFORMIXSERVERDIR=/opt/informix/INST1/informixdir
export INFORMIXDIR=/opt/informix/INST1/informixclientdir
export INFORMIXSQLHOSTS=$INFORMIXSERVERDIR/etc/sqlhosts.INST1
export INFORMIXSERVER=jsvfpredb_tcp
export ONCONFIG=$INFORMIXSERVERDIR/etc/onconfig.INST1
export LD_LIBRARY_PATH=/home/dbmon/openssl/lib:/opt/informix/INST1/informixdir/lib:/opt/informix/INST1/informixclientdir/lib:/opt/informix/INST1/informixclientdir/lib/esql:/opt/informix/INST1/informixclientdir/lib/cli:/opt/informix/INST1/informixclientdir/lib/client:/opt/informix/INST1/informixclientdir/lib/c++:/opt/informix/INST1/informixclientdir:/opt/informix/INST1/informixclientdir/lib/dmi:/home/dbmon/openssl/lib
export python=/home/dbmon/Python37/bin/python3.7
export pip=/home/dbmon/Python37/bin/pip3.7
export PYTHONPATH=/home/dbmon/Python37/lib/python3.7/site-packages/
export ODBCINI=/home/dbmon/dbMonitor/odbc.ini
export PATH=/home/dbmon/Python37/bin:$INFORMIXDIR/bin:$INFORMIXCLIENTDIR/bin:$PATH
