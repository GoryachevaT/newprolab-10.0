Загружаем данные с сервера NPL:
wget http://data.cluster-lab.com/public-newprolab-com/advert.log.lzma -O /tmp/advert.log.lzma

**Mapper.py**

``` import sys

for line in sys.stdin:
    tokens = line.strip().split(',')
    print(tokens[2], '\t', tokens[4]) 
 ``` 




**Reducer.py**

 ``` 
import sys

prev_key = None
sum = 0
for line in sys.stdin:
    tokens = line.strip().split('\t')
    key = tokens[0]
    value = int(tokens[1])
    if key != prev_key and prev_key is not None:
        print('%s\t%.2f' % (prev_key, sum))
        sum = 0
    prev_key = key
    sum += value
if prev_key is not None:
    print('%s\t%.2f' % (prev_key, sum))
 ``` 
***MAPREDUCE JOB*
(какая-то из джоб ниже, не помню точно, какая)
 ``` 
hadoop jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming.jar 
    -D mapred.reduce.tasks=1 
    -input /users/adv 
    -output /users/adverts 
    -file /data/home/antonina.goryacheva/mapreduce/mapper.py 
    -mapper "python3 mapper.py" 
    -file /data/home/antonina.goryacheva/mapreduce/reducer.py 
    -reducer "python3 reducer.py"
 ``` 
 ``` 
hadoop jar /data/home/antonina.goryacheva/mapreduce/hadoop-streaming.jar 
    -D mapred.reduce.tasks=1 
    -input /user/antonina.goryacheva/task1/students_scores.txt 
    -output  /user/antonina.goryacheva/task1/students_fin.txt 
    -file mapper.py 
    -mapper "python3 mapper.py" 
    -file reducer.py 
    -reducer "python3 reducer.py"
 ``` 

