#!/usr/bin/env python3

import json
import sys
import re
from ipaddress import IPv6Address, IPv6Network
from time import time
import argparse

config = {
  'mz': {
    'prefix': 'fd37:b4dc:4b1e::/64',
    'soa': 'spinat.ffmz.org. hostmaster.ffmz.org.',
    'ns': [
      'spinat.ffmz.org.',
      'hinterschinken.ffmz.org.',
      'lotuswurzel.ffmz.org.'
    ]
  },
  'wi': {
    'prefix': 'fd56:b4dc:4b1e::/64',
    'soa': 'spinat.ffwi.org. hostmaster.ffwi.org.',
    'ns': [
      'spinat.ffwi.org.',
      'hinterschinken.ffwi.org.',
      'lotuswurzel.ffwi.org.'
    ]
  }
}

parser = argparse.ArgumentParser()
parser.add_argument('community', action='store', choices=config.keys())
args = parser.parse_args()

HostnameRegex = re.compile(
  "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
)
prefix = IPv6Network(config[args.community]['prefix'])

data = json.load(sys.stdin)

print("""$TTL 300  ; 5 minutes
@     IN SOA   %s (
          %i        ; Serial
          2h        ; Refresh
          1h        ; Retry
          41d       ; Expire
          300       ; Negative Cache TTL
          )
\tNS %s
      """ %(
        config[args.community]['soa'],
        time(),
        '\n\tNS  '.join(config[args.community]['ns'])
      ) )

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
