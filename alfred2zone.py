#!/usr/bin/env python3

import json
import sys
import re
from ipaddress import IPv6Address, IPv6Network
from time import time
import argparse
import subprocess

config = {
  'mz': {
    'prefix': 'fd37:b4dc:4b1e::/64',
    'soa': 'aubergine.ffmz.org. hostmaster.ffmz.org.',
    'ns': [
      'spinat.ffmz.org.',
      'wasserfloh.ffmz.org.',
      'lotuswurzel.ffmz.org.',
      'ingwer.ffmz.org.'
    ],
    'socket': '/var/run/alfred-mz.sock'
  },
  'wi': {
    'prefix': 'fd56:b4dc:4b1e::/64',
    'soa': 'aubergine.ffwi.org. hostmaster.ffwi.org.',
    'ns': [
      'spinat.ffwi.org.',
      'wasserfloh.ffwi.org.',
      'lotuswurzel.ffwi.org.',
      'ingwer.ffwi.org.'
    ],
    'socket': '/var/run/alfred-wi.sock'
  }
}

parser = argparse.ArgumentParser()
parser.add_argument('community', action='store', choices=config.keys())
args = parser.parse_args()

HostnameRegex = re.compile(
  "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
)
prefix = IPv6Network(config[args.community]['prefix'])

data = json.loads(subprocess.check_output(["alfred-json","-z","-f","json","-r","158","-s",str(config[args.community]['socket'])]).decode("utf-8"))

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
