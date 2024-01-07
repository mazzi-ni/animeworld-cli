from os import system, name
import random as r
import color as c
import time

def ascii_font():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')
	
	# --------------- open font file and get array font -------------------------------

	file = open('/home/mazzi/Documents/project/python-project/animeworld_v2/font.txt', 'r')
	array_row = file.readlines()
	fonts = []
	font = ''
	for row in array_row:
		if row == '\n':
			fonts.append(font)
			font = ''
		else:
			font += row

	fonts.append(font)

	# ---------------------------------------------------------------------------------

	
	index = r.randint(0, len(fonts) - 1)
	color = '\33[' + str(r.randint(31, 37)) + 'm';
	print('\n' + color + fonts[index] + c.RESET + '\n')
	
