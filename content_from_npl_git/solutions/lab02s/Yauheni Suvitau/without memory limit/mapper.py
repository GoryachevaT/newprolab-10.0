#!/opt/anaconda/envs/bd9/bin/python
import sys
import hashlib

arr = {}

for line in sys.stdin:
        uid, time, url = line.split("\t")
        url = url.strip()
        if (not uid) or (not url) or (uid=='-'):
                continue
        if url in arr:
        	arr[url] += 1
        else:
        	arr[url] = 1

for key, value in arr.items():
	print("%s\t%d"%(key, value))