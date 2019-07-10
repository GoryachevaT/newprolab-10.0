#!/opt/anaconda/envs/bd9/bin/python3
import sys
for line in sys.stdin:
    tmp = line.strip().split('\t')
    if len(tmp) == 3:
        uid = tmp[0]
        ts  = int(float(tmp[1])*1000)
        url = tmp[2]
        if uid != '-' and len(url) >= 1:
            print(url+'\t'+str(1))
