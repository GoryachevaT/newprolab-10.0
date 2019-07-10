hadoop jar hadoop-streaming.jar 
    -D mapred.reduce.tasks=1
    -input /labs/lab02data/facetz_2015_02_12/ 
    -output  /user/antonina.goryacheva/res_s 
    -file mapper_s.py 
    -mapper "mapper_s.py" 
    -file reduce_s.py 
    -reducer "reduce_s.py"