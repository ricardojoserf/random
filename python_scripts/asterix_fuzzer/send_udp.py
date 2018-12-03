from scapy.all import *
import config

def send_packet(load_str):
	load=(load_str).decode('hex')
	ip_=IP(dst=config.dst_ip, src=config.src_ip)
	udp_=UDP(dport=config.dport,sport=config.sport)
	packet=ip_/udp_/load
	send(packet, verbose=0)


def get_combinations(string_,index1,index2):
	load_str=list(string_)
	permutaciones=[]
	characters=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
	for n in reversed(range(int(index1),int(index2)+1)):
		for k in characters:
			orig_value = load_str[n]
			load_str[n] = str(k)
			perm = "".join(load_str)
			permutaciones.append(perm)
			load_str[n] = orig_value
	return permutaciones


def main():
	texto = sys.argv[1]
	index1 = sys.argv[2]
	index2 = sys.argv[3]
	combinaciones = get_combinations(texto, index1, index2)
	for c in combinaciones:
		print c
		send_packet(c)
	aux_texto = list(texto)
	for i in range(int(index1),int(index2)+1):
		aux_texto[i]="X"
	print "".join(aux_texto)
	print "Cambiamos:", texto[int(index1):(int(index2)+1)]

main()
