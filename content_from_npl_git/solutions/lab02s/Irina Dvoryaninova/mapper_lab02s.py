#!/opt/anaconda/envs/bd9/bin/python3
import sys

for line in sys.stdin:
    row = line.strip().split('\t')
    if len(row) == 3:
        if row[0] != '-' and row[2] != '-' and row[2] != '-':
            print(row[2] + '\t' + str(1))
