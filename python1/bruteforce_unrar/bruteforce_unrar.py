import os,sys
from itertools import product
from string import ascii_lowercase

longitud = sys.argv[1]

keywords = [''.join(i) for i in product(ascii_lowercase, repeat = int(longitud))]

for key in keywords:
	os.system("unrar e $1 p "+key)
