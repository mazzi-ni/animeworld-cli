from os import system, name
import sys
# from alive_progress import alive_bar
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
		'  Sec: ' + "{:.2f}".format(value), 
		end='\r'
	);

def hide_cursor():
  if name == 'nt':
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
  elif name == 'posix':
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
  if name == 'nt':
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = True
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
  elif name == 'posix':
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
