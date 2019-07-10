#!/opt/anaconda/envs/bd9/bin/python

import sys

# Enter you mod number from the assignment
my_mod = N

for line in sys.stdin:
    row = line.strip().split('\t')
    if len(row) == 3 and row[0] != '-' and row[2].startswith('http'):
        try:
            uid = int(row[0])
            timestamp = int(float(row[1]) * 1000)
            url = row[2]
            if uid % 256 == my_mod: print("{}\t{}\t{}".format(uid, url, timestamp))
        except Exception:
        	pass

