#!/usr/bin/env python3

import sys

prev_key = None
values = []

def print_res(key, values):
	total = sum(values)
	print( '%s\t%d' % (key.strip(), total))

for l in sys.stdin:
	key, value = l.strip().split('\t')
	if key != prev_key and prev_key is not None:
		print_res(prev_key, values)
		values = []
	values.append(int(value))
	prev_key = key

if prev_key is not None:
	print_res(prev_key, values)
