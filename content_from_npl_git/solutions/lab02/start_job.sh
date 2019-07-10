#!/usr/bin/env sh


DIR_IN=/labs/lab02data/facetz_2015_02_13/
DIR_OUT=/user/$USER/facetz

hadoop fs -rm -r -f $DIR_OUT

hadoop jar ~/hadoop-streaming.jar \
	-D mapred.reduce.tasks=1 \
	-input ${DIR_IN} \
	-output ${DIR_OUT} \
	-file "mapper.py" -file "reducer.py" \
	-mapper "mapper.py" -reducer "reducer.py"

