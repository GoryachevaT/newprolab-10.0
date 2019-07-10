#!/opt/anaconda/envs/bd9/bin/python3

import sys

prev_key = None
cnt = 0

for line in sys.stdin:
    k, v = line.strip().split('\t')
    if k != prev_key and prev_key is not None:
        print('{}\t{}'.format(prev_key, '*' * cnt))
        cnt = 0
    prev_key = k
    cnt += 1

if prev_key is not None:
    print('{}\t{}'.format(prev_key, '*' * cnt))
