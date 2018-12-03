from scapy.all import *
import config

def send_packet(load_str):
        load=(load_str).decode('hex')
        ip_=IP(dst=config.dst_ip, src=config.src_ip)
        udp_=UDP(dport=config.dport,sport=config.sport)
        packet=ip_/udp_/load
        send(packet, verbose=0, loop = 1)

def main():
	send_packet(sys.argv[1])

main()