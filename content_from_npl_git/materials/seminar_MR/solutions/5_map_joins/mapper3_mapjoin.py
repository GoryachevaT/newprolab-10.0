import sys
student_disciplines = {}
for line in open('student_disciplines.txt'):
    student, discipline = line.strip().split("\t")
    student_disciplines[student] = discipline

for line in sys.stdin:
    student, score = line.strip().split('\t')
    print(student_disciplines[student] + "\t" + score)
