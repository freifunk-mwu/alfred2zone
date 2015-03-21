#!/usr/bin/env python3

import json
import sys
import re
from ipaddress import *
from time import time

ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
prefix = IPv6Network('fd56:b4dc:4b1e::/64')

data = json.load(sys.stdin)

print("""$TTL 300  ; 5 minutes
@     IN SOA   spinat.ffwi.org. hostmaster.ffwi.org. (
          %i ; serial
          600        ; refresh (10min)
          30         ; retry (30s)
          3600       ; expire (1 hour)
          60         ; minimum (1 minute)
          )
      NS  spinat.ffwi.org.
      NS  hinterschinken.ffwi.org.
      NS  lotuswurzel.ffwi.org.
      """ % time())

HostnameRegex = re.compile(ValidHostnameRegex)

for i in data:
  node = data[i]
  try:
    hostname = node['hostname']
    if HostnameRegex.match(hostname) == None:
      continue

    address = None

    for a in node['network']['addresses']:
      a = IPv6Address(a)
      if a in prefix:
        address = a
        break

    if address:
      print("%s\tAAAA\t%s" % (hostname, address))
  except:
    pass
