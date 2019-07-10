#!/opt/anaconda/envs/bd9/bin/python3
import sys
import happybase

from collections import Counter

def main():
    connection = happybase.Connection('master.cluster-lab.com')
    connection.open()
    connection.create_table('svetlana.alekseeva',{'data:url': dict(max_versions=4096)})
    table = connection.table('svetlana.alekseeva')

    for line in sys.stdin:
        splitted = line.strip().split("\t")
        table.put(splitted[0], {'data:url': splitted[2]}, timestamp=int(splitted[1]))
    connection.close()    
main()
