import sys, scapy
send((IP(dst=sys.argv[1],src=sys.argv[2])/ICMP())*int(sys.argv[3]), iface=sys.argv[4])
