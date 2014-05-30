#! /usr/bin/python

# (C) 2014 by folkert@vanheusden.com

import random
import subprocess
import sys

def gen_board():
	b = [[0 for x in xrange(8)] for x in xrange(8)] 

	# uppercase is white

	for y in xrange(2, 6):
		for x in range(8):
			b[y][x] = ' '

	for p in xrange(8):
		b[1][p] = 'P'

	b[0][0] = b[0][7] = 'R'
	b[0][1] = b[0][6] = 'N'
	b[0][2] = b[0][5] = 'B'
	b[0][3] = 'Q'
	b[0][4] = 'K'

	for y in xrange(2):
		for x in xrange(8):
			b[7 - y][x] = b[y][x].lower()

	return b

def shuffel_board(b, n_swap, n_erase):
	for it in xrange(n_swap):

		while True:
			x1 = random.randint(0, 7)
			y1 = random.randint(0, 7)
			x2 = random.randint(0, 7)
			y2 = random.randint(0, 7)

			if b[y1][x1] != ' ' or b[y2][x2] != ' ':
				break

		temp = b[y1][x1]
		b[y1][x1] = b[y2][x2]
		b[y2][x2] = temp

	for it in xrange(n_erase):
		while True:
			x3 = random.randint(0, 7)
			y3 = random.randint(0, 7)

			if b[y3][x3] != ' ' and b[y3][x3] != 'k' and b[y3][x3] != 'K':
				break

def gen_epd(b):
	fs = ''

	for y in range(7, -1, -1):
		empty = 0

		for x in range(0, 8):
			if b[y][x] == ' ':
				empty += 1

			else:
				if empty > 0:
					fs += '%d' % empty
					empty = 0

				fs += b[y][x]

		if empty > 0:
			fs += '%d' % empty

		if y > 0:
			fs += "/"

	# FIXME random
	fs += " w"

	fs += " ";

	canCastle = False
	if b[0][7] == 'R' and b[0][4] == 'K':
		fs += "K"
		canCastle = True
	if b[0][0] == 'R' and b[0][4] == 'K':
		fs += "Q"
		canCastle = True
	if b[7][7] == 'r' and b[7][4] == 'k':
		fs += "k"
		canCastle = True
	if b[7][0] == 'r' and b[7][4] == 'k':
		fs += "q"
		canCastle = True

	if not canCastle:
		fs += '-'

	fs += ' -' # last move FIXME

	fs += ' 10' # FIXME

	return fs

def try_epd(engine, epd):
        p = subprocess.Popen([engine, epd], stdout = subprocess.PIPE)

        if p.wait() == 0:
                return p.communicate()[0].rstrip('\n')

	return None


if len(sys.argv) != 3:
	print 'Required parameters: engine_1 engine_2'
	print 'Engine_x should be a chess program that emits the number of moves it can do (as a string to stdout) for a given EPD/FEN string.'
	print 'It receives the FEN/EPD string as 1 argument (all in argv[1] so to say).'
	print ''
	print '-- mail@vanheusden.com'
	sys.exit(1)
		
engine1 = sys.argv[1]
engine2 = sys.argv[2]

it = 1

while True:
	b = gen_board()

	while True:
		n_swap = random.randint(0, 64)
		n_erase = random.randint(0, 32)

		if n_swap > 0 or n_erase > 0:
			break

	shuffel_board(b, n_swap, n_erase)

	epd = gen_epd(b)

	print '%d] %s' % (it, epd)

	result1 = try_epd(engine1, epd)
	if result1 == None:
		print 'Failed geting result from %s' % engine1

	else:
		result2 = try_epd(engine2, epd)
		if result2 == None:
			print 'Failed geting result from %s' % engine2

		else:
			it += 1

			if result1 != result2:
				print 'Results differ: %s %s' % (result1, result2)
