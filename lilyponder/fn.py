#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03, 2022.09
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
		if f is None:
			if x == ('IV', 'l3'):
				# если можно, ставим S. Если нельзя (до этого была доминанта) — D
				if prevF == 'D':
					f = 'D'
				else:
					f = 'S'
			elif x in (('IV', 's3'), ('VIb', 'l6')):
				# IV_s3 и VIb_l6 после T (или S) считаем S
				if prevF in ('T', 'S'):
					f = 'S'
			elif x == ('II', 's3'):
				# терция II_s3 — или D, или S, или Sh. По возможности D скорее ставим
				f = 'D' # 'D' | 'S' | 'Sh'
			elif x == ('VI', 's6'):
				if prevF is None:
					# секста из субдоминанты, до неё ничего нет, можно сразу считать S
					f = 'S'
				elif prevF == 'T':
					# V_l6->VI_s6->IV_l6->V_l3->III_s6->IV_l2->III_s3->II_l6->I_p8
					# тут VI_s6 явно S, так как идёт после Т и из трезвучия S
					f = 'S'
			elif x == ('I', 's6'):
				# I_s6 считаем D, так как до того было D
				if prevF == 'D':
					f = 'D'
			elif x == ('I', 'l6'):
				if prevF == 'T':
					# I_l6 — секста из S, до неё T идёт, потому сразу S
					# I_l6 — типичная секста из S, особенно после T
					f = 'S'
			elif x == ('IV', 'l6'):
				if (i > 0) and (seq[i-1] == ('V', 'l3')) and (prevF == 'D'):
					# IV_l6 после D в виде V_l3 точно будет D
					f = 'D'
				elif prevF == 'T':
					# V_l6 сразу D после T
					f = 'D'
			elif x == ('VI', 'p4'):
				# VI_p4 после тоники точно S
				if prevF == 'T':
					f = 'S'
			elif x in (('I', 'l2'), ('II', 's7')):
				# Для I_l2 придумал правило:
				# * Если после S, то S
				# * Иначе D
				# II_s7 — малая септима как секунда, правила те же что и для I_l2, т. е. чаще всего доминанта будет
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
				if f is None:
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
		elif x == ('IV', 'l6'):
			if f is None:
				if (i > 0) and (ff[i-1] == 'S') and (i + 1 < len(seq)) and (ff[i+1] == 'D'):
					# IV_l6 — D, между S и D уже можно на D
					f = 'D'
		ff[i] = f
		i += 1

	# pass 3
	for i in range(len(seq)):
		f = ff[i]
		if (f is None) and (i > 0) and (i + 1 < len(seq)) and (ff[i-1] == ff[i+1]):
			# Можно сделать простой конечный проход, что всё не раскрашенное между двумя одинаковыми функциями — той же функции
			f = ff[i-1]
		ff[i] = f
		i += 1

	return ff

def encodeSeq (ff):
	rr = []
	for f in ff:
		if f is not None:
			rr.append(f)
		else:
			rr.append('?')
	return '->'.join(rr)

__all__ = ['seq2fn_major', 'encodeSeq']
