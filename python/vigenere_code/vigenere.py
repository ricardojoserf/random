import string, sys
from itertools import product
from string import ascii_lowercase

MODULE = len(string.ascii_lowercase) # 26 para el alfabeto ASCII inglés

def shift_by(char, shift):
    if char.isalpha():
        aux = ord(char) + shift
        z = 'z' if char.islower() else 'Z'
        if aux > ord(z):
            aux -= MODULE
        char = chr(aux)
    return char


def vigenere(text, key, decrypt=False):
    shifts = [ord(k) - ord('a') for k in key.lower()]
    i = 0
    def do_shift(char):
        nonlocal i
        if char.isalpha():
            shift = shifts[i] if not decrypt else MODULE - shifts[i]
            i = (i + 1) % len(key)
            return shift_by(char, shift)
        return char
    return ''.join(map(do_shift, text))

#texto="JXCSTWPHTH SGUVCY�D SBH GU JTHQCKD UL SWKLGYD JHFGY XPH FQUIGYHPJLC ZRDYH RYLXHFKKDF F VGNXTPGCK LPMRTT�WKJD FL WCUWC JDNPGCK FQTR NH MCZBR. LVRLUCTRU XXG VV IBVVL HN JWH. SD HSDI LV LHVAW{67F60444544CMDCK319069FFJ78I1735}."
texto = sys.argv[1]
longitud = sys.argv[2]

keywords = [''.join(i) for i in product(ascii_lowercase, repeat = int(longitud))]


for key in keywords:
	result =  vigenere(texto,key,True)
	if "jasyp" in result.lower():
		print (key)
		print (result)
