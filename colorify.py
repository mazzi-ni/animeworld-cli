from os import system, name
import sys
import random as r
import color as c
import time

# TODO:
# Esempio barra
# ━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━ 11.9/18.3 MB 1.1 MB/s eta 0:00:06'

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
	print('\n' + color + fonts[index] + c.RESET + '\n');

def progress_bar(value, duration_min):
	prefix = c.BOLD + c.CGREEN + '-' + c.RESET;
	non_prefix = c.BOLD + c.CRED + '-' + c.RESET;
	
	length = 60;
	duration_tot = duration_min * 60;
	perc = int((int(value) * length) / duration_tot);
	
	# print(perc, end='\r');
	
	prefix_bar = '';
	empty_bar = '';
	
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

