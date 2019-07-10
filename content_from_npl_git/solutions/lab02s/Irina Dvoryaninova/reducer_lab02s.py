#!/opt/anaconda/envs/bd9/bin/python3
import sys

prev_url = None
summ = 0
for line in sys.stdin:
    url, value = line.strip().split('\t')
    if url != prev_url and prev_url is not None:
        print(prev_url + '\t' + str(summ))
        summ = 0
    summ += int(value)
    prev_url = url
if prev_url is not None:
    print(prev_url + '\t' + str(summ))
