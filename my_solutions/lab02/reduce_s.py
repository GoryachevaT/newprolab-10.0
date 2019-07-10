#!/opt/anaconda/envs/bd9/bin/python3
import sys

prev_key = None
sum = 0
for line in sys.stdin:
    tokens = line.strip().split('\t')
    key = tokens[0]
    value = int(tokens[1])
    if key != prev_key and prev_key is not None:
        print(prev_key+'\t'+str(sum))
        sum = 0
    prev_key = key
    sum += value
if prev_key is not None:
    print(prev_key+'\t'+str(sum))
