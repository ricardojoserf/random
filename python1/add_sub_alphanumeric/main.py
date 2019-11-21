import sys,os

init_hex = sys.argv[1]
list_opc = [init_hex[i:i+2] for i in range(0, len(init_hex), 2)]
list_opc = list_opc[::-1]


def get_vals(num):
	print "NUM: ", num
	if num < 96:
		num += 256 
	arr = []
	print num
	if num >= 96 and num < 159:
		rest = num - 64 
		#print "32 + 32 +", rest
		arr = [hex(32), hex(32), hex(rest)]

	elif num >= 159 and num < 232:
		rest = num - 100
		#print "53 + 53 +", rest
		arr = [hex(50), hex(50), hex(rest)]

	elif num >= 232 and num < 326:
		rest = num - 200
		#print "64 + 64 +", rest
		arr = [hex(100), hex(100), hex(rest)]

	elif num >= 326:
		rest = num - 256
		#print "128 + 128 +", rest
		arr = [hex(128), hex(128), hex(rest)]
	#print arr
	return arr

two_compl_arr = []
final_arr = []

for i in range(0, len(list_opc)):
	dec_val =  int (list_opc[i], 16)
	if i == (len(list_opc)-1):
		dec_cmpl = 255 - dec_val + 1
	else:
		dec_cmpl = 255 - dec_val
	#print "ORIG: ", list_opc[i], " (",dec_val,")\tCMPL: ",hex(dec_cmpl), " (", dec_cmpl, ")"
	two_compl_arr.append(hex(dec_cmpl))
	final_arr.append(get_vals(dec_cmpl))

print "Inverted array =>     ", list_opc
print "Complement 2 array => ", two_compl_arr


text0 = "sub eax,"
text1 = "sub eax,"
text2 = "sub eax,"

for arr in final_arr:
	text0 += arr[0].replace("0x","")
	text1 += arr[1].replace("0x","")
	text2 += arr[2].replace("0x","")

print
print text0
print text1
print text2
print

for arr in final_arr:
	for el in arr:
		el_dec = int(el.replace("0x",""),16)
		if el_dec < 32 or el_dec >= 128:
			print "Problem with ",el
		