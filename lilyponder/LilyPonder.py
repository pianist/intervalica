#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#
# https://music.stackexchange.com/a/40047
#

import hashlib, subprocess, tempfile, os

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

transpose = lambda f, t, noteF: stepNumToNote(noteToStep(noteF) + noteToStep(t) - noteToStep(f), noteToNum(noteF) + noteToNum(t) - noteToNum(f))

intervalToStep = {
	'major': {
		'p1': 0,
		's2': 1, 'l2': 2, 'e2': 3,
		's3': 3, 'l3': 4,
		'd4': 4, 'p4': 5, 'e4': 6,
		'd5': 6, 'p5': 7, 'e5': 8,
		's6': 8, 'l6': 9,
		'd7': 9, 's7': 10, 'l7': 11,
		'p8': 12
	}
}

intervalToNum = {
	'major': {
		'p1': 0,
		's2': -5, 'l2': 2, 'e2': 2 + 7,
		's3': -3, 'l3': 4,
		'd4': None, 'p4': -1, 'e4': None, # TODO
		'd5': None, 'p5': 1, 'e5': None, # TODO
		's6': -4, 'l6': 3,
		'd7': -2 - 7, 's7': -2, 'l7': 5,
		'p8': 0
	}
}

stageToStep = {
	'major': {
		'I': 0,
		'I#': 1,
		'IIb': 1,
		'II': 2,
		'II#': 3,
		'III': 4,
		'IV': 5,
		'IV#': 6,
		'V': 7,
		'V#': 8,
		'VIb': 8,
		'VI': 9,
		'VIIb': 10,
		'VII': 11
	}
}

stageToNum = {
	'major': {
		'I': 1 - 1,
		'I#': 8 - 1,
		'IIb': -4 - 1,
		'II': 3 - 1,
		'II#': 10 - 1,
		'III': 5 - 1,
		'IV': 0 - 1,
		'IV#': 7 - 1,
		'V': 2 - 1,
		'V#': 9 - 1,
		'VIb': -3 - 1,
		'VI': 4 - 1,
		'VIIb': -1 - 1,
		'VII': 6 - 1
	}
}

tonalityToMode = {
	'C': 'major', 'C#': 'major',
	'Db': 'major', 'D': 'major',
	'Eb': 'major', 'E': 'major',
	'F': 'major', 'F#': 'major',
	'Gb': 'major', 'G': 'major',
	'Ab': 'major', 'A': 'major',
	'Bb': 'major', 'B': 'major',

	'c': 'minor',
	'd': 'minor',
	'e': 'minor',
	'f': 'minor',
	'g': 'minor',
	'a': 'minor',
	'b': 'minor'
}

tonalityToNote = {
	'C': 'c', 'C#': 'cis',
	'Db': 'des', 'D': 'd',
	'Eb': 'ees', 'E': 'e',
	'F': 'f', 'F#': 'fis',
	'Gb': 'ges', 'G': 'g',
	'Ab': 'aes', 'A': 'a',
	'Bb': 'bes', 'B': 'b',

	'c': 'c',
	'd': 'd',
	'e': 'e',
	'f': 'f',
	'g': 'g',
	'a': 'a',
	'b': 'b'
}

stageToNote = lambda tNote, mode, stage: stepNumToNote(stageToStep[mode][stage] + noteToStep(tNote), stageToNum[mode][stage] + noteToNum(tNote))

enToRu = {
	'p1': 'ч1',
	's2': 'м2', 'l2': 'б2', 'e2': 'ув2',
	's3': 'м3', 'l3': 'б3',
	'd4': 'ум4', 'p4': 'ч4', 'e4': 'ув4',
	'd5': 'ум5', 'p5': 'ч5', 'e5': 'ув5',
	's6': 'м6', 'l6': 'б6',
	'd7': 'ум7', 's7': 'м7', 'l7': 'б7',
	'p8': 'ч8'
}

def lilyPondNormalizeOctaves (x):
	n = x.count("'") - x.count(",")
	x = x.replace("'", '').replace(",", '')
	if n > 0:
		x += "'"*n
	elif n < 0:
		x += ","*(-n)
	return x

def addInterval (mode, n0, interval):
	n0s = noteToStep(n0)
	n0n = noteToNum(n0)

	n1s = n0s + intervalToStep[mode][interval]
	n1n = n0n + intervalToNum[mode][interval]

	return stepNumToNote(n1s, n1n)

def strToLilyPond0 (s, tonality, titles=None, debug=False, octave=None):
	mode = tonalityToMode[tonality]
	tonalityNote = tonalityToNote[tonality]

	seq = [ (stage, interval) for stage, interval in [ xy.split('_') for xy in s.split('->') ] ]

	oldLow = None
	oldHigh = None
	low = []
	high = []
	minLow = None
	maxLow = None
	maxHigh = None
	for stage, interval in seq:
		n0 = stageToNote(tonalityNote, mode, stage)
		n0s = noteToStep(n0)

		# low voice: relative
		if oldLow != None:
			while n0s - oldLow < -6:
				n0s += 12
				n0 += "'"
			while n0s - oldLow >= 6:
				n0s -= 12
				n0 += ","

		# prevent high voice jumps through low
		if (oldHigh != None) and (oldLow != None):
			# example: III_s6->VII_s3
			while n0s + intervalToStep[mode][interval] < oldLow:
				n0s += 12
				n0 += "'"

			# example: III_s3->VI_s7
			while n0s > oldHigh:
				n0s -= 12
				n0 += ","

		n1s = n0s + intervalToStep[mode][interval]
		oldLow = n0s
		oldHigh = n1s
		low.append(n0)
		n1 = addInterval(mode, n0, interval)
		high.append(n1)

		if (minLow == None) or (minLow > n0s):
			minLow = n0s
		if (maxLow == None) or (maxLow < n0s):
			maxLow = n0s
		if (maxHigh == None) or (maxHigh < n1s):
			maxHigh = n1s

	if octave == None:
		m = (minLow + maxLow + 1) // 2
		octave = (12 + 11 - m) // 12

#	if octave == None:
#		m = (minLow + maxHigh + 1) // 2
#		# octave = (12 + 11 + 6 - m) // 12
#		octave = (12 + 11 + 5 - m) // 12

	voices = [('voiceOne', []), ('voiceTwo', [])]
	for i in range(len(seq)):
		n0 = low[i]
		n1 = high[i]

		if octave > 0:
			n0 += "'"*octave
			n1 += "'"*octave
		elif octave < 0:
			n0 += ","*(-octave)
			n1 += ","*(-octave)

		intervalRepr = seq[i][1]
		if titles == None:
			title = None
		elif titles == 'en':
			title = intervalRepr
		elif titles == 'ru':
			title = enToRu[intervalRepr]
		else:
			assert False

		assert noteToStep(n0) <= noteToStep(n1)
		voices[0][1].append((n1, title))
		voices[1][1].append((n0, None))

	r = ['\\score {\n\t\\new Staff <<']
	for voice in voices:
		notes = [lilyPondNormalizeOctaves(x[0]) for x in voice[1]]
		if len(notes) > 1:
			notes[0] = notes[0] + "2"
		if len(notes) % 2 == 1:
			notes[-1] = notes[-1] + '1'
		for i in range(len(notes)):
			if voice[1][i][1] != None:
				notes[i] += '^"%s"' % (voice[1][i][1],)
		r.append("""		\\new Voice
			{
				\\key %s \\%s
				\\%s
				%s
			}""" % (tonalityNote, mode, voice[0], ' '.join(notes)))
	r.append("	>>")
	if debug:
		debugStr = tonality + ' ' + s.replace('->', ' → ')
		r.append("""	\\header {
		piece = "%s"
	}""" % (debugStr,))
	r.append("""	\\layout { }
	\\midi { }
}""")
	return '\n'.join(r)

def strToLilyPond (s, tonality, titles=None, debug=False, octave=None):
	if ' ' in s:
		tonality, s = s.split()

	if tonality == '*dur':
		r = [ strToLilyPond0(s, tonality, titles=titles, debug=debug, octave=octave) for tonality, mode in tonalityToMode.items() if mode == 'major' ]
	elif tonality == '*moll':
		r = [ strToLilyPond0(s, tonality, titles=titles, debug=debug, octave=octave) for tonality, mode in tonalityToMode.items() if mode == 'minor' ]
	else:
		r = ( strToLilyPond0(s, tonality, titles=titles, debug=debug, octave=octave), )

	return r

# ss: list of strings
# returns: [ header, score0, score1, ... ]
def strs2LilyPond (ss, tonality, debug=False, titles=None):
	r = [ '\\version "2.8.0"' ]
	r.append("""\\header {
	tagline = ""
}""")
	r = [ '\n\n'.join(r) ]

	r.extend(['\n\n'.join(strToLilyPond(s, tonality, titles=titles, debug=debug)) for s in ss])

	return r

def getBaseFileName (s):
	cacheDir = os.path.join(tempfile.gettempdir(), 'LilyPonder-cache')
	os.makedirs(cacheDir, exist_ok=True)
	name = hashlib.blake2s(s).hexdigest()
	return os.path.join(cacheDir, name)

def getImage (s, format):
	assert format in ('pdf', 'svg', 'png', 'ps', 'eps')

	baseFName = getBaseFileName(s)
	fName = baseFName + '.' + format
	if not os.path.exists(fName):
		srcFName = baseFName + '.lp'
		with open(srcFName, 'wb') as fh:
			fh.write(s)

		ret = subprocess.run(["lilypond", "--%s" % (format,), "-s", "-o", baseFName, srcFName], stdout=subprocess.DEVNULL)
		assert ret.returncode == 0

	if os.path.exists(fName):
		return fName

def getMIDI (s):
	fName = getBaseFileName(s) + '.midi'
	if not os.path.exists(fName):
		r = getImage(s, 'pdf')
		assert r != None
	if os.path.exists(fName):
		return fName

def getWAV (s):
	fName = getBaseFileName(s) + '.wav'
	if not os.path.exists(fName):
		srcFName = getMIDI(s)
		if os.path.exists(srcFName):
			ret = subprocess.run(["timidity", "-s", "48000", "-OwS1", "-o", fName, srcFName], stdout=subprocess.DEVNULL)
			assert ret.returncode == 0
	if os.path.exists(fName):
		return fName

def getOpus (s):
	fName = getBaseFileName(s) + '.opus'
	if not os.path.exists(fName):
		wavFName = getWAV(s)
		if wavFName != None:
			ret = subprocess.run(["ffmpeg", "-n", "-hide_banner", "-loglevel", "error", "-i", wavFName, fName], stdout=subprocess.DEVNULL)
			assert ret.returncode == 0
	if os.path.exists(fName):
		return fName

def getSound (s, format):
	if format == 'opus':
		return getOpus(s)
	elif format == 'midi':
		return getMIDI(s)
	elif format == 'wav':
		return getWAV(s)
	else:
		assert False

class LilyPonder:

	def __init__ (self, tonality):
		self.tonality = tonality

	def strs2LilyPond (self, ss, debug=False, titles=None):
		return strs2LilyPond(ss, self.tonality, debug=debug, titles=titles)

	def getImage (self, s, format):
		return getImage(s, format)

	def getSound (self, s, format):
		return getSound(s, format)

__all__ = ["LilyPonder"]
