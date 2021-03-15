#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#

# первые признаки
d0_major = {
	('I', 'l3'): 'T',
	('III', 's3'): 'T',
	('I', 'p5'): 'T',
	('I', 'p8'): 'T',
	('III', 's6'): 'T',
	('V', 'p4'): 'T',
	('V', 'l6'): 'T',

	('V', 'l3'): 'D',
	('VII', 's3'): 'D',
	('V', 'p5'): 'D',
	('VII', 'd5'): 'D',
	('IV', 'e4'): 'D',
	('V', 's7'): 'D',
	('VII', 's6'): 'D',
	('II', 'l6'): 'D',
	('II', 'p4'): 'D'
}

def str2fn_major (s):
	seq = [ (degree, interval) for degree, interval in [ xy.split('_') for xy in s.split('->') ] ]

	ff = []

	prevF = None
	for x in seq:
		f = d0_major.get(x)
		if f == None:
			if x == ('IV', 'l3'):
				# если можно, ставим S. Если нельзя (до этого была доминанта) — D
				if prevF == 'D':
					f = 'D'
				else:
					f = 'S'
			elif x == ('II', 's3'):
				# терция II_s3 — или D, или S, или Sh. По возможности D скорее ставим
				f = 'D' # 'D' | 'S' | 'Sh'
			elif x[1] in ('s2', 'l2', 'e2', 'd7', 's7', 'l7'):
				# секунды и септимы чаще всего повторяют предыдущую функцию
				f = prevF
		ff.append(f)
		prevF = f

	return ff

def encodeSeq (ff):
	rr = []
	for f in ff:
		if f != None:
			rr.append(f)
		else:
			rr.append('?')
	return '->'.join(rr)

__all__ = ['seq2fn_major', 'encodeSeq']
