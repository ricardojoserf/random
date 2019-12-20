import sys
import os
import argparse
from APIs.utils import *


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-r', '--ranges_file', required=False, action='store', help='File with ranges to analyze')
  parser.add_argument('-c', '--companies_file', required=False, action='store', help='File with ranges to analyze')
  parser.add_argument('-o', '--output_file', default="results", required=False, action='store', help='Output file')
  my_args = parser.parse_args()
  return my_args


def analyze_range(arr_points, length_, output_file, counter, len_ranges):
	if length_ < 8:
		aux1 = 8 - length_
		first_ = get_base(int(arr_points[0]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = str(first_) + ".0.0.0"
		last_ip  = str(last_) + ".255.255.255"
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			for i in range(0,255):
				for h in range(0,255):
					for g in range(0,255):
						resolve_ip(str(j) + "." + str(i) + "." + str(h) + "." + str(g), output_file)
	elif length_ < 16:
		aux1 = 16 - length_
		first_ = get_base(int(arr_points[1]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + str(first_) + ".0.0"
		last_ip  = arr_points[0] + "." + str(last_) + ".255.255"
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			for i in range(0,255):
				for h in range(0,255):
					resolve_ip(arr_points[0]+"."+ str(j) + "." + str(i) + "." + str(h), output_file)
	elif length_ < 24:
		aux1 = 24 - length_
		first_ = get_base(int(arr_points[2]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + arr_points[1] + "." + str(first_) + ".0"
		last_ip  = arr_points[0] + "." + arr_points[1] + "." + str(last_) + ".255"
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			for i in range(0,255):
				resolve_ip(arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i), output_file)
	elif length_ < 32:
		aux1 = 32 - length_
		first_ = get_base(int(arr_points[3]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(first_)
		last_ip  = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(last_)
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + str(j), output_file)
	elif length_ == 32:
		resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + arr_points[3], output_file)
	else:
		print("Wrong IP format")
		sys.exit(1)


def range_extractor(ranges_file, companies_file, output_file):
	ranges = []
	ranges_info = None
	if ranges_file is not None:
		ranges = open(ranges_file).read().splitlines()
	if companies_file is not None:
		companies = open(companies_file).read().splitlines()
		for c in companies:
			calc_ranges, ranges_info = get_ranges(c)
			print("\nCompany: "+c+"\n")
			for r in calc_ranges:
				print("- Range: %s   \tName: %s "%(r['range'], r['name']))
				ranges.append(r['range'])
			if len(calc_ranges) == 0:
				print(" - No data found")
	counter = 0
	len_ranges = len(ranges)
	for r in ranges:
		counter += 1
		try:
			length_ = int(r.split("/")[1])
			arr_points = r.split("/")[0].split(".")
			analyze_range(arr_points, length_, output_file, counter, len_ranges)
		except:
			pass
	if os.path.isfile(output_file):
		order_subdomains(output_file)
	return output_file, ranges, ranges_info


def main():
	args= get_args()
	ranges_file = args.ranges_file
	companies_file = args.companies_file
	if ranges_file is None and companies_file is None:
		print("Error: Ranges or company file is necessary")
		print("usage: range_domains.py [-h] [-r RANGES_FILE] [-c COMPANIES_FILE] [-o OUTPUT_FILE]")
		sys.exit(1)
	output_file = args.output_file
	range_extractor(ranges_file, companies_file, output_file)
	

if __name__== "__main__":
	main()
