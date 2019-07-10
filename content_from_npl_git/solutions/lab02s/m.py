#!/usr/bin/env python3

import sys

for l in sys.stdin:
	try:
	   uid, ts, url = l.strip().split('\t')
	except ValueError:
 		#logging.warn("Could not split line: %s", line)
 		continue
	if not uid.isdigit():
		continue
	if url == '-' or url is None:
		continue
	print( '%s\t1' % (url.strip()))
