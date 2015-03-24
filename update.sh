#!/bin/sh
export LC_ALL=en_US.UTF-8
WORKDIR="/home/admin/clones/alfred2zone"
BINDDIR="/var/lib/bind"

cd $WORKDIR

/usr/bin/python3 $WORKDIR/alfred2zone.py mz > $BINDDIR/ffmz/nodes.ffmz.org.master.db
/usr/bin/python3 $WORKDIR/alfred2zone.py wi > $BINDDIR/ffwi/nodes.ffwi.org.master.db

sudo /usr/sbin/rndc reload
