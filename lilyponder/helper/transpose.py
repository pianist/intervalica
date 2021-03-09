#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#
# based on:
#	https://music.stackexchange.com/a/40047
#

noteToStep0 = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
noteToStep = lambda x: noteToStep0[x[0]] + x[1:].count('is') - x[1:].count('es') + (x.count("'") - x.count(",")) * 12

noteToNum0 = {'c': 1, 'd': 3, 'e': 5, 'f': 0, 'g': 2, 'a': 4, 'b': 6}
numToNote0 = {0: 'f', 1: 'c', 2: 'g', 3: 'd', 4: 'a', 5: 'e', 6: 'b'}

noteToNum = lambda x: noteToNum0[x[0]] + (x[1:].count('is') - x[1:].count('es')) * 7

def numToNote (x):
	sharps, noteNum = divmod(x, 7)
	y = numToNote0[noteNum]
	if sharps > 0:
		y += "is"*sharps
	elif sharps < 0:
		y += "es"*(-sharps)
	return y

def stepNumToNote (step, num):
	note = numToNote(num)
	dStep = step - noteToStep(note)
	assert dStep % 12 == 0
	octaves = dStep // 12
	if octaves > 0:
		note += "'"*octaves
	elif octaves < 0:
		note += ","*(-octaves)
	return note

def transpose (f, t, noteF):
	num = noteToNum(noteF) + noteToNum(t) - noteToNum(f)
	step = noteToStep(noteF) + noteToStep(t) - noteToStep(f)
	return stepNumToNote(step, num)

if __name__ == '__main__':
	FROM = 'c'
	TO = 'des'

	print("TRANSPOSE %s -> %s" % (FROM, TO))
	for note in ('c', 'cis', 'des', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'aes' , 'a', 'bes', 'b'):
		print("	%5s -> %-5s" % (note, transpose(FROM, TO, note)))
