#!/bin/bash
export LC_ALL=en_US.UTF-8
cd /home/admin/clones/alfred2zone/
/home/admin/bin/alfred-json -s /var/run/alfred-wi.sock -z -r 158 | /usr/bin/python3 alfred2zone-wi.py wi > /var/lib/bind/ffwi/nodes.ffwi.org.master.db
/home/admin/bin/alfred-json -s /var/run/alfred-mz.sock -z -r 158 | /usr/bin/python3 alfred2zone-mz.py mz > /var/lib/bind/ffmz/nodes.ffmz.org.master.db

sudo /usr/sbin/rndc reload
