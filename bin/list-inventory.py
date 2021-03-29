#!/usr/bin/env python
#
# list dictionary entries from a system inventory file
#
# usage: list-inventory.py filename <section>
#
# where <section> is optional and matches the string in the json
#
import json
import sys

with open(sys.argv[1]) as f:
      data = json.load(f)

sysinfo=sys.argv[2]

try: sysinfo
except NameError: sysinfo = None

if sysinfo is None:
    print(json.dumps(data, indent=4, sort_keys=True))
else:
    print(json.dumps(data["system_info"][sysinfo], indent=4, sort_keys=True))

