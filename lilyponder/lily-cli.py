#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
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
	outputFormat = None

	outputFormatsImage = ('pdf', 'svg', 'png')
	outputFormatsSound = ('midi', 'wav', 'opus')

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
			elif arg == '-of':
				if len(args) > 0:
					arg = args.pop(0)
					if arg in outputFormatsImage + outputFormatsSound:
						outputFormat = arg
					else:
						break
			elif len(args) == 1:
				tonality = arg
				s = args.pop(0)
				err = False
			else:
				break

	if s == '-':
		ss = [ s.rstrip() for s in sys.stdin.readlines() ]
	else:
		ss = (s,)

	if not err:
		lilyPonder = LilyPonder.LilyPonder(tonality)
		r = lilyPonder.strs2LilyPond(ss, debug=debug, titles=titles)
		if outputFormat == None:
			print('\n\n'.join(r))
		else:
			header = r[0]
			for s0 in r[1:]:
				s = header + '\n\n' + s0
				s = s.encode('utf-8')
				if outputFormat in outputFormatsImage:
					fName = lilyPonder.getImage(s, outputFormat)
				elif outputFormat in outputFormatsSound:
					fName = lilyPonder.getSound(s, outputFormat)
				else:
					assert False
				assert fName != None
				print(fName)
	else:
		print("usage: %s { -d | -t lang | -of format } tonality ( str | - )" % (sys.argv[0],))
		print("	-d: debug output")
		print("	-t lang: add interval titles")
		print("		lang: language")
		print("			en: English")
		print("			ru: Russian")
		print("	-of format: specify output format (if not specified: LilyPond)")
		print("		format: pdf | svg | png | midi | wav | opus")
		print("	str example: III_s3->IV_l3->II_l6->III_s6->I_l3->VIb_l6->V_p8->VII_d5->I_l3")
		print("	tonality:")
		print("		C: c major")
		print("		C#: c# major")
		print("		Db: db major")
		print("		c: c minor")
		print("		...")
		print("		*dur: all major")
		print("		*moll: all minor")

if __name__ == '__main__':
	main()
