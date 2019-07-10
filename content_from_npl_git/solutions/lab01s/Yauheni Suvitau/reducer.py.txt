#!/usr/bin/python
import sys

current_country = None
current_sum = 0

for line in sys.stdin:
	line = line.split(",")
	country = line[0].strip()
	val = float(line[1].strip())
	if country != current_country:
		if current_country:
			print ("%s\t%f" % (current_country, current_sum))
		current_country = country
		current_sum = val
	else:
		current_sum += val
print ("%s\t%f" % (current_country, current_sum))