#!/opt/anaconda/envs/bd9/bin/python3

import sys

prev_key = None
score = 0.0
cnt = 0

for line in sys.stdin:
    k, v = line.strip().split('\t')
    v = float(v)
    if k != prev_key and prev_key is not None:
        avg = score / cnt
        print('{:.1f}\t1'.format(avg))
        cnt = 0
        score = 0
    prev_key = k
    score += v
    cnt += 1

if k != prev_key and prev_key is not None:
    print('{:.1f}\t1'.format(avg))
