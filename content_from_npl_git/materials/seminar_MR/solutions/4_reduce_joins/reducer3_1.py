import sys
prev_key = None
values = []

def print_res(key,  values):
    scores = [float(score[1]) for score in filter(lambda value: value[0] == 'score', values)]
    avg = sum(scores)/len(scores)
    discipline = list(filter(lambda value: value[0] == 'discipline', values))[0][1]
    print("%s\t%.2f" % (discipline, avg))

for line in sys.stdin:
    key, record_type, value = line.strip().split("\t")
    if key != prev_key and prev_key is not None:
        print_res(prev_key, values)
        values = []
    values.append((record_type, value))
    prev_key = key

if prev_key is not None:
    print_res(prev_key, values)
