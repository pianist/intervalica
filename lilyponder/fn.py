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

	ff = [ None ] * len(seq)

	# pass 1
	prevF = None
	for i in range(len(seq)):
		x = seq[i]
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
			elif x == ('VI', 's6'):
				if prevF == None:
					# секста из субдоминанты, до неё ничего нет, можно сразу считать S
					f = 'S'
			elif x == ('I', 'l6'):
				if prevF == 'T':
					# I_l6 — секста из S, до неё T идёт, потому сразу S
					# I_l6 — типичная секста из S, особенно после T
					f = 'S'
			elif x == ('I', 'l2'):
				# Для I_l2 придумал правило:
				# * Если после S, то S
				# * Иначе D
				if prevF == 'S':
					f = 'S'
				else:
					f = 'D'
			elif x == ('VIb', 'e5'):
				# VIb_e5 это симметричный случай III_d4, пока считаем задержанием "в стиле Чайковского"
				f = prevF
			elif x[1] in ('s2', 'l2', 'e2', 'd7', 's7', 'l7'):
				if x == ('VIb', 'e2'):
					if (i + 1 < len(seq)) and (seq[i+1] == ('V', 'p4')):
						# VIb_e2 — это всегда D. По определению прямо, характерный интервал доминанты с пониженной ноной, так как разрешается в кварту V_p4. Прямо такое правило, если разрешается в V_p4, то D
						f = 'D'
				if f == None:
					# секунды и септимы чаще всего повторяют предыдущую функцию
					f = prevF
		ff[i] = f
		prevF = f
		i += 1

	# pass 2
	for i in range(len(seq)):
		x = seq[i]
		f = ff[i]
		if x == ('IV', 'l2'):
			if (i + 1 < len(seq)) and (ff[i+1] in ('T', 'D')):
				# IV_l2 — это всегда доминанта, если дальше тоника или доминанта. Даже сложно представить там не доминанту
				f = 'D'
		elif x == ('VII', 'd7'):
			if (i + 1 < len(seq)) and (ff[i+1] in ('T',)):
				# VII_d7 — D вполне тут в тему, так как дальше T типичная
				# VII_d7->I_p5 — типичная D
				f = 'D'
		ff[i] = f
		i += 1

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
