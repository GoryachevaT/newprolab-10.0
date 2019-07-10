import sys
for line in sys.stdin:
    user, score = line.strip().split()
    print (user + "\t" + "score" + "\t" + score)
