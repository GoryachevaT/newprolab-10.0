#!/opt/anaconda/envs/bd9/bin/python

import os
import sys
import happybase

# Hostname with Happybase
hbase_endpoint = 'master.cluster-lab.com'
hbase_user = os.environ['USER']

connection = happybase.Connection(hbase_endpoint)

# Table name of your choice
table = connection.table(hbase_user)

for line in sys.stdin:
	row = line.strip().split('\t')
	uid, url, t = row
	table.put(uid, { 'data:url': url }, timestamp=int(t))
	


