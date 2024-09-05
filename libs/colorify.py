from os import system, name, path
import random as r
import libs.color as c
import time
import sys

# TODO:
# Esempio barra
# ━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━ 11.9/18.3 MB 1.1 MB/s eta 0:00:06'

def ascii_font():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')
	
	# --------------- open font file and get array font -------------------------------

	# file = open('/home/mazzi/Documents/project/python-project/animeworld_v2/font.txt', 'r')
	file = open(path.join(path.dirname(__file__), 'fonts/font.txt'), 'r')
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
	print('\n' + color + fonts[index] + c.RESET + '\n');

def progress_bar(value, duration_min):
	color_prefix = c.BOLD + c.CGREEN;
	colot_non_prefix = c.BOLD + c.CRED;
	char = '-'

	length = 60;
	duration_tot = duration_min * 60;
	perc = int((int(value) * length) / duration_tot);
	
	if perc >= length:
		perc = length;
		color_prefix = c.BOLD + c.CGREEN;
	
	prefix = color_prefix + char + c.RESET;
	non_prefix = colot_non_prefix + char + c.RESET;
	
	prefix_bar = '';
	empty_bar = '';
	# middle_bar = color_non_prefix + '╺' + c.RESET;
	
	for i in range(0, perc):
		prefix_bar += prefix;
	
	for i in range(perc, length):
		empty_bar += non_prefix;
	
	print(
		'   ' + prefix_bar + empty_bar + 
		'  Perc: ' + "{:.2f}".format(int(value) * 100 / duration_tot) + "%", 
		end='\r',
		flush = True
	);

