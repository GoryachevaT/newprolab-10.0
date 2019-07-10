#!/opt/anaconda/envs/bd9/bin/python3
import happybase
import sys

connection = happybase.Connection('master.cluster-lab.com')
table = connection.table('irina.dvoryaninova')

for line in sys.stdin:
    row = line.strip().split('\t')
    if len(row) == 3:
        if row[0].isdigit() and row[1].replace('.', '').isdigit() and row[2].startswith('http'):
            if int(row[0]) % 256 == 170:
                table.put(row[0].encode('utf8'), {b'data:url': row[2].encode('utf8')}, timestamp=int(float(row[1])*1000))
