#!/opt/anaconda/envs/bd9/bin/python
import sys


prev_url = None
prev_value = 0
for line in sys.stdin:
	url, value = line.split("\t")
	value = int(value.strip())
	if prev_url != url:
		if prev_url:
			print("%s\t%d"%(prev_url, prev_value))
		prev_url = url
		prev_value = value
	else:
		prev_value += value
print("%s\t%d"%(prev_url, prev_value))
