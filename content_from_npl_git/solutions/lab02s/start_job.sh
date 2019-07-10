#!/usr/bin/env sh

hadoop fs -rm -r -f results

hadoop jar ~/hadoop-streaming.jar \
	-D mapred.reduce.tasks=1 \
	-input /labs/lab02data/facetz_2015_02_12/ \
	-output results \
	-file ./m.py \
	-mapper "python m.py" \
	-file ./r.py \
	-reducer "python r.py"

hadoop fs -cat results/* | sort -nrk2 | head -n350 > top350.txt
