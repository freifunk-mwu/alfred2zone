#!/bin/bash
export LC_ALL=en_US.UTF-8
cd /home/admin/clones/alfred2zone/
/home/admin/bin/alfred-json -s /var/run/alfred-wi.sock -z -r 158 > /home/admin/clones/alfred2zone/tmp_alfred158_wi.json
/home/admin/bin/alfred-json -s /var/run/alfred-mz.sock -z -r 158 > /home/admin/clones/alfred2zone/tmp_alfred158_mz.json
cat /home/admin/clones/alfred2zone/tmp_alfred158_wi.json | /usr/bin/python3 alfred2zone-wi.py > /var/lib/bind/ffwi/nodes.ffwi.org.master.db
cat /home/admin/clones/alfred2zone/tmp_alfred158_mz.json | /usr/bin/python3 alfred2zone-mz.py > /var/lib/bind/ffmz/nodes.ffmz.org.master.db
rm /home/admin/clones/alfred2zone/tmp_alfred158_wi.json
rm /home/admin/clones/alfred2zone/tmp_alfred158_mz.json

sudo /usr/sbin/rndc reload
