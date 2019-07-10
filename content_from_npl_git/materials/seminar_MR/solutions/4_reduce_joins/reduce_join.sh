cat data/student_scores.txt | python mapper_3_1.py > data/tmp
cat  data/student_disciplines.txt | python mapper_3_2.py  >> data/tmp
sort -k1,1 data/tmp |python reducer3_1.py > data/reducer3_1_output
sort -k1,1 data/reducer3_1_output | python reducer3_2.py 
