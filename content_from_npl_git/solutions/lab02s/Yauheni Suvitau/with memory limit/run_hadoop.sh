for val in $(seq 0 7)
do
    hadoop jar /usr/hdp/3.0.0.0-1634/hadoop-mapreduce/hadoop-streaming.jar -file /data/home/evgeny.suvitov/lab2s/mapper.py -mapper "/data/home/evgeny.suvitov/lab2s/mapper.py $val" -file /data/home/evgeny.suvitov/lab2s/reducer.py -reducer /data/home/evgeny.suvitov/lab2s/reducer.py -input /labs/lab02data/facetz_2015_02_12/ -output /user/evgeny.suvitov/lab2s/part$val
done
