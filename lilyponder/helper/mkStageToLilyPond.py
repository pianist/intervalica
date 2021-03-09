#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#

import transpose

tonalityLilyPond = {
	'C': 'c',
	'C#': 'cis',
	'Db': 'des',
	'D': 'd',
	'Eb': 'ees',
	'E': 'e',
	'F': 'f',
	'F#': 'fis',
	'Gb': 'ges',
	'G': 'g',
	'Ab': 'aes',
	'A': 'a',
	'Bb': 'bes',
	'B': 'b'
}

C = {
	'I'   : 'c',
	'I#'  : 'cis',
	'IIb' : 'des',
	'II'  : 'd',
	'II#' : 'dis',
	'III' : 'e',
	'IV'  : 'f',
	'IV#' : 'fis',
	'V'   : 'g',
	'V#'  : 'gis',
	'VIb' : 'aes',
	'VI'  : 'a',
	'VIIb': 'bes',
	'VII' : 'b'
}

def gen ():
	#r = {'C': C}
	r = {}

	stages = []
	notes = []
	for stage, note in C.items():
		stages.append(stage)
		notes.append(note)

	input = '{' + ' '.join(notes) + '}'
	input = input.encode('ascii')

	for tonality in tonalityLilyPond.keys():
		d = {}
		i = 0
		for i in range(len(stages)):
			stage = stages[i]
			note = notes[i]
			noteTransposed = transpose.transpose('c', tonalityLilyPond[tonality], note)
			d[stage] = noteTransposed
			i += 1
		r[tonality] = d

	q = ["stageToLilyPond = {"]
	i = 0
	for k, v in r.items():
		q.append("	'%s': {" % (k,))
		j = 0
		for k0, v0 in v.items():
			if j == len(v.keys()) - 1:
				q.append("""		'%s': \"%s\"""" % (k0, v0))
			else:
				q.append("""		'%s': \"%s\",""" % (k0, v0))
			j += 1
		if i == len(r.keys()) - 1:
			q.append("	}")
		else:
			q.append("	},")
		i += 1
	q.append("}")

	return q

def main ():
	print('\n'.join(gen()))

if __name__ == '__main__':
	main()
