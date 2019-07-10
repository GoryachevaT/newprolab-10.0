#!/opt/anaconda/envs/bd9/bin/python
import re
import sys
import happybase

table_name = 'evgeny.suvitov'

connection = happybase.Connection('master.cluster-lab.com')
connection.open()
table = connection.table(table_name)
for line in sys.stdin:
	uid, time, url = line.split("\t")
	url = url.strip()
	if (not uid) or (not time) or (not url) or (url=='-') or (uid=='-') or (int(uid) % 256 != 49) or (not url.startswith("http")):
		continue
	table.put(uid, {'data:url':url}, timestamp = int(float(time)*1000))
connection.close()