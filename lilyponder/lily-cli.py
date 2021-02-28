#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.02
#

import sys
import LilyPonder

def main ():
	args = sys.argv[1:]
	err = True
	s = None
	tonality = None
	debug = False
	titles = None

	if len(args) > 0:
		while len(args) > 0:
			arg = args.pop(0)
			if arg == '-d':
				debug = True
			elif arg == '-t':
				if len(args) > 0:
					arg = args.pop(0)
					if arg in ('en', 'ru'):
						titles = arg
					else:
						break
			elif len(args) == 1:
				s = arg
				tonality = args.pop(0)
				err = False
			else:
				break

	if s == '-':
		ss = [ s.rstrip() for s in sys.stdin.readlines() ]
	else:
		ss = (s,)

	if not err:
		print(LilyPonder.LilyPonder(tonality).processStrings(ss, debug=debug, titles=titles))
	else:
		print("usage: %s [ -d ] [ -t ( en | ru ) ] ( str | - ) tonality" % (sys.argv[0],))
		print("	-d: debug output")
		print("	-t: add interval titles")
		print("	str example: III_s3->IV_l3->II_l6->III_s6->I_l3->VIb_l6->V_p8->VII_d5->I_l3")
		print("	tonality:")
		print("		C: c major")
		print("		c: c minor")
		print("		D: d major")
		print("		...")

if __name__ == '__main__':
	main()
