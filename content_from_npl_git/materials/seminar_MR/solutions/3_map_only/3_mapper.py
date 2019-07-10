import sys

for line in sys.stdin:
    token, _ = line.strip().split()
    if token.startswith('П'):
        print(token + '\t1')
