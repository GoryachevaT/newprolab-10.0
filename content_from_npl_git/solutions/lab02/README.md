**Lab02 Solution:**

* Login via ssh to master

* Create your table in HBase: `sh create_table.sh`.

* Run a MapReduce Job (modify the contents of `mapper.py`, `reducer.py`, `start_job.sh` if needed): `sh start_job.sh`.

* If you are going to run the job multiple times, clean up your table after each job: `sh drop_table.sh`.
