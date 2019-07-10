#!/opt/anaconda/envs/bd9/bin/python
import happybase

table_name = 'evgeny.suvitov'

connection = happybase.Connection('master.cluster-lab.com')
connection.open()
tables = connection.tables()
if table_name in tables:
        connection.disable_table(table_name)
        connection.delete_table(table_name)
connection.create_table(table_name, {'data':dict(max_versions=4096)})
