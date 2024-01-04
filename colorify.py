from os import system, name
import random
import time

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 60, fill = '█', printEnd = "\r"): 
  percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
  filledLength = int(length * iteration // total)
  bar = fill * filledLength + '-' * (length - filledLength)
  print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
  if iteration == total:
    print()

def loading_bar(minute):
  items = list(range(0, minute))
  l = len(items)

  printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
  for i, item in enumerate(items):
    time.sleep(0.15)
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


def init():
  # ->> clear:
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')
  
  # ->> ascii art
  file = open('/home/mazzi/Documents/project/python-project/animeworld/font.txt', 'r')
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

  # ->> random
  index = random.randint(0, len(fonts) - 1)
	color = '\33[' + str(random.randint(31, 37)) + 'm'
	color = '\33[' + str(random.randint(31, 37)) + 'm'
  color = '\33[' + str(random.randint(31, 37)) + 'm'

	print(' ')
  print(color + fonts[index] + RESET)
	print(' ')


# ->> color
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'

RESET = '\033[0m'
BOLD='\033[01m'

