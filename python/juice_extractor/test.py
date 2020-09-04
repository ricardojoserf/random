import socket
import subprocess
from tabulate import tabulate
import sys
import argparse
from termcolor import colored
from collections import Counter 
import os


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_file', required=False, action='store', help='Domains file (without protocol)')
  parser.add_argument('-o', '--output_file', required=False, default ='output_file.txt', action='store', help='Output file')
  parser.add_argument('-d', '--dictionary', required=False, default ='juicy.txt', action='store', help='Dictionary')
  my_args = parser.parse_args()
  return my_args


args = get_args()
dict_ = args.dictionary
output_file = args.output_file
input_file = args.input_file
gowitness_directory = "gow/"


def check_open(ip_, port_):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(2)
	location = (ip_, port_)
	return (sock.connect_ex(location) == 0)


def print_write(text):
	print(text)
	with open(output_file, 'a') as o_f:
		o_f.write(text+"\n")


def fuzz_hname(url_, index, length, port):
	try:
		print_write("\n(%s/%s) %s [%s]" % (index,length, url_, port))
		out = subprocess.Popen(['./ffuf', '-u', url_+'/FUZZ', '-w', dict_], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout,stderr = out.communicate()
		paths = []
		sizes = []
		codes = []
		for i in stdout.decode("utf-8").split("\n"):
			if "Size" in i:
				a = i.split("[2K")[2]
				b = (" ".join(a.split()).split(" "))
				paths.append({"path":b[0], "code": b[2].replace(",",""), "size":b[4].replace(",","")})
				codes.append(b[2].replace(",",""))
				sizes.append(b[4].replace(",",""))
		res = tabulate(paths, tablefmt="plain")
		'''
		for r in res.split("\n"):
			if "20" in r:
				print(colored(r, 'green'))
			elif "302" in r:
				print('\033[95m'+r+'\033[0m')
			elif "401" in r: 
				print(colored(r, 'magenta'))
			elif "301" in r:
				print(colored(r, 'grey'))
			elif "403" in r:
				print(colored(r, 'yellow'))
			else:
				print(r)
		'''
		most_common_size = str(Counter(sizes).most_common(1)[0][0])
		most_common_code = str(Counter(codes).most_common(1)[0][0])
		for r in res.split("\n"):
			if "200" in r:
				print_write(r+" --- 200")
			elif most_common_code not in r:
				print_write(r+" --- Code")
			elif most_common_size not in r:
				print_write(r+" --- Size")
			else:
				print_write(r)

	except Exception as e:
		pass


def screenshot(url_):
	command_ = "./gowitness single -u "+url_+" -d "+gowitness_directory+" 2>/dev/null"
	os.system(command_)
	print("Screenshot taken")


def check_ports(hname_, index, length):
	if (check_open(hname_, 80)):
		url_ = "http://"+hname_
		fuzz_hname(url_, index, length, 80)
		screenshot(url_)

	if (check_open(hname_, 443)):
		url_ = "https://"+hname_
		fuzz_hname(url_, index, length, 443)
		screenshot(url_)

	if (check_open(hname_, 8080)):
		url_ = "http://"+hname_+":8080"
		fuzz_hname(url_, index, length, 8080)
		screenshot(url_)

	if (check_open(hname_, 8443)):
		url_ = "https://"+hname_+":8443"
		fuzz_hname(url_, index, length, 8443)
		screenshot(url_)


def main():
	args = get_args()
	index = 0
	for hname_ in open(input_file).read().splitlines():
		index+=1
		try:
			check_ports(hname_, index, len(open(input_file).read().splitlines()))
		except:
			print("Fallo: %s"%(hname_))
			pass

main()

