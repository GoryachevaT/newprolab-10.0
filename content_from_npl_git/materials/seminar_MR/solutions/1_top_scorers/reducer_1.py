#!/opt/anaconda/envs/bd9/bin/python3

import sys
prev_key = None
marks = []

def print_res(key, values):
    avg = sum(values)/len(values)
    if avg > 4.5:
        print("%s\t%.2f" % (key, avg)) 

values = []
for line in sys.stdin:
    key, value = line.strip().split("\t")
    if key != prev_key and prev_key is not None:
        print_res(prev_key, values)
        values = []
    values.append(float(value))
    prev_key = key

if prev_key is not None:
    print_res(prev_key, values)
