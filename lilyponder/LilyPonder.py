#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Alexander Shiryaev, 2021.03
#

import hashlib, subprocess, tempfile, os

intervalToPitch = { # halftones
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
intervalToPitch['minor'] = intervalToPitch['major'] # FIXME

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

pitchToLilyPond0 = { # halftones
	'C': {
		0: 'c',
		1: 'des',
		2: 'd',
		3: 'dis',
		4: 'e',
		5: 'f',
		6: 'fis',
		7: 'g',
		8: 'as',
		9: 'a',
		10: 'bes',
		11: 'b'
	},
	'C#': {
		0: 'bis,',
		1: 'cis',
		2: 'd',
		3: 'dis',
		4: 'disis',
		5: 'eis',
		6: 'fis',
		7: 'fisis',
		8: 'gis',
		9: 'a',
		10: 'ais',
		11: 'b'
	},
	'Db': {
		0: 'c',
		1: 'des',
		2: 'eses',
		3: 'es',
		4: 'e',
		5: 'f',
		6: 'ges',
		7: 'g',
		8: 'as',
		9: 'beses',
		10: 'bes',
		11: "ces'"
	},
	'D': {
		0: 'c',
		1: 'cis',
		2: 'd',
		3: 'es',
		4: 'e',
		5: 'eis',
		6: 'fis',
		7: 'g',
		8: 'gis',
		9: 'a',
		10: 'bes',
		11: 'b'
	},
	'Eb': {
		0: 'c',
		1: 'des',
		2: 'd',
		3: 'es',
		4: 'fes',
		5: 'f',
		6: 'fis',
		7: 'g',
		8: 'as',
		9: 'a',
		10: 'bes',
		11: "ces'"
	},
	'E': {
		0: 'c',
		1: 'cis',
		2: 'd',
		3: 'dis',
		4: 'e',
		5: 'f',
		6: 'fis',
		7: 'fisis',
		8: 'gis',
		9: 'a',
		10: 'ais',
		11: 'b'
	},
	'F': {
		0: 'c',
		1: 'des',
		2: 'd',
		3: 'es',
		4: 'e',
		5: 'f',
		6: 'ges',
		7: 'g',
		8: 'gis',
		9: 'a',
		10: 'bes',
		11: 'b'
	},
	'F#': {
		0: 'bis,',
		1: 'cis',
		2: 'd',
		3: 'dis',
		4: 'e',
		5: 'eis',
		6: 'fis',
		7: 'g',
		8: 'gis',
		9: 'gisis',
		10: 'ais',
		11: 'b'
	},
	'Gb': {
		0: 'c',
		1: 'des',
		2: 'eses',
		3: 'es',
		4: 'fes',
		5: 'f',
		6: 'ges',
		7: 'ases',
		8: 'as',
		9: 'a',
		10: 'bes',
		11: "ces'"
	},
	'G': {
		0: 'c',
		1: 'cis',
		2: 'd',
		3: 'es',
		4: 'e',
		5: 'f',
		6: 'fis',
		7: 'g',
		8: 'as',
		9: 'a',
		10: 'ais',
		11: 'b'
	},
	'Ab': {
		0: 'c',
		1: 'des',
		2: 'd',
		3: 'es',
		4: 'fes',
		5: 'f',
		6: 'ges',
		7: 'g',
		8: 'as',
		9: 'beses',
		10: 'bes',
		11: 'b'
	},
	'A': {
		0: 'bis,',
		1: 'cis',
		2: 'd',
		3: 'dis',
		4: 'e',
		5: 'f',
		6: 'fis',
		7: 'g',
		8: 'gis',
		9: 'a',
		10: 'bes',
		11: 'b'
	},
	'Bb': {
		0: 'c',
		1: 'cis',
		2: 'd',
		3: 'es',
		4: 'e',
		5: 'f',
		6: 'ges',
		7: 'g',
		8: 'as',
		9: 'a',
		10: 'bes',
		11: "ces'"
	},
	'B': {
		0: 'c',
		1: 'cis',
		2: 'cisis',
		3: 'dis',
		4: 'e',
		5: 'eis',
		6: 'fis',
		7: 'g',
		8: 'gis',
		9: 'a',
		10: 'ais',
		11: 'b'
	}
}

# tonality -> pitch, mode
decodeTonality = {
	'C': (0, 'major'), 'C#': (1, 'major'),
	'Db': (1, 'major'), 'D': (2, 'major'),
	'Eb': (3, 'major'), 'E': (4, 'major'),
	'F': (5, 'major'), 'F#': (6, 'major'),
	'Gb': (6, 'major'), 'G': (7, 'major'),
	'Ab': (8, 'major'), 'A': (9, 'major'),
	'Bb': (10, 'major'), 'B': (11, 'major'),

	'c': (0, 'minor'),
	'd': (2, 'minor'),
	'e': (4, 'minor'),
	'f': (5, 'minor'),
	'g': (7, 'minor'),
	'a': (9, 'minor'),
	'b': (11, 'minor')
}

# tonality -> LilyPond key
tonalityToLilyPondKey = {
	'C': 'c \\major', 'C#': 'cis \\major',
	'Db': 'des \\major', 'D': 'd \\major',
	'Eb': 'es \\major', 'E': 'e \\major',
	'F': 'f \\major', 'F#': 'fis \\major',
	'Gb': 'ges \\major', 'G': 'g \\major',
	'Ab': 'as \\major', 'A': 'a \\major',
	'Bb': 'bes \\major', 'B': 'b \\major',

	'c': 'c \\minor',
	'd': 'd \\minor',
	'e': 'e \\minor',
	'f': 'f \\minor',
	'g': 'g \\minor',
	'a': 'a \\minor',
	'b': 'b \\minor'
}

stageToLilyPond = {
	'C': {
		'I': "c",
		'I#': "cis",
		'IIb': "des",
		'II': "d",
		'II#': "dis",
		'III': "e",
		'IV': "f",
		'IV#': "fis",
		'V': "g",
		'V#': "gis",
		'VIb': "as",
		'VI': "a",
		'VIIb': "bes",
		'VII': "b"
	},
	'C#': {
		'I': "cis",
		'I#': "cisis",
		'IIb': "d",
		'II': "dis",
		'II#': "disis",
		'III': "eis",
		'IV': "fis",
		'IV#': "fisis",
		'V': "gis",
		'V#': "gisis",
		'VIb': "a",
		'VI': "ais",
		'VIIb': "b",
		'VII': "bis"
	},
	'Db': {
		'I': "des",
		'I#': "d",
		'IIb': "eses",
		'II': "es",
		'II#': "e",
		'III': "f",
		'IV': "ges",
		'IV#': "g",
		'V': "as",
		'V#': "a",
		'VIb': "beses",
		'VI': "bes",
		'VIIb': "ces'",
		'VII': "c'"
	},
	'D': {
		'I': "d",
		'I#': "dis",
		'IIb': "es",
		'II': "e",
		'II#': "eis",
		'III': "fis",
		'IV': "g",
		'IV#': "gis",
		'V': "a",
		'V#': "ais",
		'VIb': "bes",
		'VI': "b",
		'VIIb': "c'",
		'VII': "cis'"
	},
	'Eb': {
		'I': "es",
		'I#': "e",
		'IIb': "fes",
		'II': "f",
		'II#': "fis",
		'III': "g",
		'IV': "as",
		'IV#': "a",
		'V': "bes",
		'V#': "b",
		'VIb': "ces'",
		'VI': "c'",
		'VIIb': "des'",
		'VII': "d'"
	},
	'E': {
		'I': "e",
		'I#': "eis",
		'IIb': "f",
		'II': "fis",
		'II#': "fisis",
		'III': "gis",
		'IV': "a",
		'IV#': "ais",
		'V': "b",
		'V#': "bis",
		'VIb': "c'",
		'VI': "cis'",
		'VIIb': "d'",
		'VII': "dis'"
	},
	'F': {
		'I': "f",
		'I#': "fis",
		'IIb': "ges",
		'II': "g",
		'II#': "gis",
		'III': "a",
		'IV': "bes",
		'IV#': "b",
		'V': "c'",
		'V#': "cis'",
		'VIb': "des'",
		'VI': "d'",
		'VIIb': "es'",
		'VII': "e'"
	},
	'F#': {
		'I': "fis",
		'I#': "fisis",
		'IIb': "g",
		'II': "gis",
		'II#': "gisis",
		'III': "ais",
		'IV': "b",
		'IV#': "bis",
		'V': "cis'",
		'V#': "cisis'",
		'VIb': "d'",
		'VI': "dis'",
		'VIIb': "e'",
		'VII': "eis'"
	},
	'Gb': {
		'I': "ges",
		'I#': "g",
		'IIb': "ases",
		'II': "as",
		'II#': "a",
		'III': "bes",
		'IV': "ces'",
		'IV#': "c'",
		'V': "des'",
		'V#': "d'",
		'VIb': "eses'",
		'VI': "es'",
		'VIIb': "fes'",
		'VII': "f'"
	},
	'G': {
		'I': "g",
		'I#': "gis",
		'IIb': "as",
		'II': "a",
		'II#': "ais",
		'III': "b",
		'IV': "c'",
		'IV#': "cis'",
		'V': "d'",
		'V#': "dis'",
		'VIb': "es'",
		'VI': "e'",
		'VIIb': "f'",
		'VII': "fis'"
	},
	'Ab': {
		'I': "as",
		'I#': "a",
		'IIb': "beses",
		'II': "bes",
		'II#': "b",
		'III': "c'",
		'IV': "des'",
		'IV#': "d'",
		'V': "es'",
		'V#': "e'",
		'VIb': "fes'",
		'VI': "f'",
		'VIIb': "ges'",
		'VII': "g'"
	},
	'A': {
		'I': "a",
		'I#': "ais",
		'IIb': "bes",
		'II': "b",
		'II#': "bis",
		'III': "cis'",
		'IV': "d'",
		'IV#': "dis'",
		'V': "e'",
		'V#': "eis'",
		'VIb': "f'",
		'VI': "fis'",
		'VIIb': "g'",
		'VII': "gis'"
	},
	'Bb': {
		'I': "bes",
		'I#': "b",
		'IIb': "ces'",
		'II': "c'",
		'II#': "cis'",
		'III': "d'",
		'IV': "es'",
		'IV#': "e'",
		'V': "f'",
		'V#': "fis'",
		'VIb': "ges'",
		'VI': "g'",
		'VIIb': "as'",
		'VII': "a'"
	},
	'B': {
		'I': "b",
		'I#': "bis",
		'IIb': "c'",
		'II': "cis'",
		'II#': "cisis'",
		'III': "dis'",
		'IV': "e'",
		'IV#': "eis'",
		'V': "fis'",
		'V#': "fisis'",
		'VIb': "g'",
		'VI': "gis'",
		'VIIb': "a'",
		'VII': "ais'"
	}
}

def lilyPondToPitch (x):
	n = x.count("'") - x.count(",")
	x = x.replace("'", '').replace(",", '')
	return n * 12 + {
		'ces': -1,
		'c': 0,
		'cis': 1,
		'des': 1,
		'cisis': 2,
		'd': 2,
		'eses': 2,
		'dis': 3,
		'es': 3,
		'disis': 4,
		'e': 4,
		'fes': 4,
		'eis': 5,
		'f': 5,
		'fis': 6,
		'ges': 6,
		'fisis': 7,
		'g': 7,
		'ases': 7,
		'gis': 8,
		'as': 8,
		'gisis': 9,
		'a': 9,
		'beses': 9,
		'ais': 10,
		'bes': 10,
		'b': 11,
		'bis': 12
	}[x]

def lilyPondNormalize (x):
	n = x.count("'") - x.count(",")
	x = x.replace("'", '').replace(",", '')
	if n > 0:
		x += "'"*n
	elif n < 0:
		x += ","*(-n)
	return x

def pitchToLilyPond (tonality, x):
	res = pitchToLilyPond0[tonality][x % 12]
	n = x // 12
	if n > 0:
		res += "'"*n
	elif n < 0:
		res += ","*(-n)
	return lilyPondNormalize(res)

def strToLilyPond0 (s, tonality, titles=None, debug=False, octave=None):
	mode = decodeTonality[tonality][1]

	seq = [ (stage, interval) for stage, interval in [ xy.split('_') for xy in s.split('->') ] ]

	oldLow = None
	oldHigh = None
	low = []
	high = []
	minLow = None
	maxLow = None
	maxHigh = None
	for stage, interval in seq:
		n0 = stageToLilyPond[tonality][stage]
		n0p = lilyPondToPitch(n0)

		# low voice: relative
		if oldLow != None:
			while n0p - oldLow < -6:
				n0p += 12
				n0 += "'"
			while n0p - oldLow >= 6:
				n0p -= 12
				n0 += ","

		# prevent high voice jumps through low
		if (oldHigh != None) and (oldLow != None):
			# example: III_s6->VII_s3
			while n0p + intervalToPitch[mode][interval] < oldLow:
				n0p += 12
				n0 += "'"

			# example: III_s3->VI_s7
			while n0p > oldHigh:
				n0p -= 12
				n0 += ","

		n1p = n0p + intervalToPitch[mode][interval]
		oldLow = n0p
		oldHigh = n1p
		low.append(n0)
		n1 = pitchToLilyPond(tonality, n1p) # TODO
		high.append(n1)

		if (minLow == None) or (minLow > n0p):
			minLow = n0p
		if (maxLow == None) or (maxLow < n0p):
			maxLow = n0p
		if (maxHigh == None) or (maxHigh < n1p):
			maxHigh = n1p

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

		assert lilyPondToPitch(n0) <= lilyPondToPitch(n1)
		voices[0][1].append((n1, title))
		voices[1][1].append((n0, None))

	r = ['\\score {\n\t\\new Staff <<']
	for voice in voices:
		notes = [lilyPondNormalize(x[0]) for x in voice[1]]
		if len(notes) > 1:
			notes[0] = notes[0] + "2"
		if len(notes) % 2 == 1:
			notes[-1] = notes[-1] + '1'
		for i in range(len(notes)):
			if voice[1][i][1] != None:
				notes[i] += '^"%s"' % (voice[1][i][1],)
		r.append("""		\\new Voice
			{
				\\key %s
				\\%s
				%s
			}""" % (tonalityToLilyPondKey[tonality], voice[0], ' '.join(notes)))
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
		r = [ strToLilyPond0(s, tonality, titles=titles, debug=debug, octave=octave) for tonality, v in decodeTonality.items() if v[1] == 'major' ]
	elif tonality == '*moll':
		r = [ strToLilyPond0(s, tonality, titles=titles, debug=debug, octave=octave) for tonality, v in decodeTonality.items() if v[1] == 'minor' ]
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
