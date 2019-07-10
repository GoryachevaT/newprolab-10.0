#!/opt/anaconda/envs/bd9/bin/python
import sys
import hashlib

arr = {}

mod = int(sys.argv[1])

for line in sys.stdin:
        uid, time, url = line.split("\t")
        url = url.strip()
        if (not uid) or (not url) or (uid=='-') or (int(hashlib.md5(bytearray(url, encoding='utf-8')).hexdigest(), 16) % 8 != mod):
                continue
        if url in arr:
        	arr[url] += 1
        else:
        	arr[url] = 1

for key, value in arr.items():
	print("%s\t%d"%(key, value))