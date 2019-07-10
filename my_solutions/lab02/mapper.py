#!/opt/anaconda/envs/bd9/bin/python3
import sys
for line in sys.stdin:
    tmp = line.strip().split('\t')
    if len(tmp) == 3:
        try:
            uid = float(tmp[0])
        except ValueError:
            uid = None
        ts  = int(float(tmp[1])*1000)
        url = tmp[2]
        if uid is not None and ts is not None and url is not None:
            if url != '-':
                if url.startswith('http'):
                    if uid % 256 == 170:
                        print(str(uid)+'\t'+url+'\t'+str(ts))
