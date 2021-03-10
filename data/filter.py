#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#

import sys

def main ():
	if len(sys.argv) == 2:
		y = sys.argv[1]
		while True:
			line = sys.stdin.readline()
			if line == '':
				break
			line = line.strip()
			if ' ' in line:
				tonality, line = line.split()
			else:
				tonality = None
			old = None
			for x in line.split('->'):
				if (old != None) and ((old == y) or (x == y)):
					if tonality != None:
						print("%s %s->%s" % (tonality, old, x))
					else:
						print("%s->%s" % (old, x))
				old = x
	else:
		print("usage: %s stage_interval" % (sys.argv[0],))

if __name__ == '__main__':
	main()
