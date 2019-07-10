from pyhive import hive

conn = hive.Connection(host='node1.cluster-lab.com', port=10000, username='USER', password='PASSWORD', auth='LDAP')

with conn.cursor as cur:
	cur.execute("show databases")
	print(cur.fetchall())