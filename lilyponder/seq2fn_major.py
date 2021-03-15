#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#

import sys

import fn

def main ():
	args = sys.argv[1:]
	err = True
	s = None

	while len(args) > 0:
		arg = args.pop(0)
		if len(args) == 0:
			s = arg
			err = False
		else:
			break

	if not err:
		if s == '-':
			ss = [ s.strip() for s in sys.stdin.readlines() if s.strip() != '' ]
		else:
			ss = (s,)
		for s in ss:
			print(fn.encodeSeq(fn.str2fn_major(s)))
	else:
		print("usage: %s ( str | - )" % (sys.argv[0],))

if __name__ == '__main__':
	main()
