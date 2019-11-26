import os
import sys

os.system("cat "+sys.argv[1]+" | awk '{print $2 \" \" $4}' | grep -v start > ips.txt")
array_aux = [{'range': 32, 'val': 1}, {'range': 31, 'val': 2}, {'range': 30, 'val': 4}, {'range': 29, 'val': 8}, {'range': 28, 'val': 16}, {'range': 27, 'val': 32}, {'range': 26, 'val': 64}, {'range': 25, 'val': 128}, {'range': 24, 'val': 256}, {'range': 23, 'val': 512}, {'range': 22, 'val': 1024}, {'range': 21, 'val': 2048}, {'range': 20, 'val': 4096}, {'range': 19, 'val': 8192}, {'range': 18, 'val': 16384}, {'range': 17, 'val': 32768}, {'range': 16, 'val': 65536}, {'range': 15, 'val': 131072}, {'range': 14, 'val': 262144}, {'range': 13, 'val': 524288}, {'range': 12, 'val': 1048576}, {'range': 11, 'val': 2097152}, {'range': 10, 'val': 4194304}, {'range': 9, 'val': 8388608}, {'range': 8, 'val': 16777216}, {'range': 7, 'val': 33554432}, {'range': 6, 'val': 67108864}, {'range': 5, 'val': 134217728}, {'range': 4, 'val': 268435456}, {'range': 3, 'val': 536870912}, {'range': 2, 'val': 1073741824}, {'range': 1, 'val': 2147483648}]

f = open("ips.txt").read().splitlines()
for i in f:
	aux_val = i.split(" ")[1]
	for j in array_aux:
		if (int(aux_val)-int(j['val'])) <=0:
			print i.split(" ")[0]+"/"+str(j['range'])
			break

