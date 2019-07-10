#!/usr/bin/python
import sys

for line in sys.stdin:
	line = line.split(",")
	country = line[2].strip()
	value = float(line[4].strip())
	print ("%s,%f" % (country, value))