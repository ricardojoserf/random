#!/usr/bin/env python

import config
import functions as fn
import sys
import os
import commands
import Image
import pytesseract
import pyexifinfo
import json
import struct
from zlib import crc32
import shutil
import csv
from subprocess import Popen, PIPE


convert_check = config.convert_check
binwalk_extract = config.binwalk_extract
binwalk_recursive_extract = config.binwalk_recursive_extract
strings_check = config.strings_check
cat_check = config.cat_check
metadata_check = config.metadata_check
ocr_check = config.ocr_check
png_8bit = config.png_8bit
list_colors = config.list_colors
file_check = config.file_check
unzip_check = config.unzip_check
signatures_check = config.signatures_check


image_name = sys.argv[1]
filename = os.path.splitext(image_name)[0]
extension = os.path.splitext(image_name)[1]
directory = image_name + "_analysis"
directory_binwalk = directory + "/binwalk"
directory_binwalk_recursive = directory + "/binwalk_recursive"
directory_pallette = directory + "/pallette"


if not os.path.exists(directory):
    os.makedirs(directory)
else:
	shutil.rmtree(directory)

if not os.path.exists(directory_binwalk):
    os.makedirs(directory_binwalk)

if not os.path.exists(directory_binwalk_recursive):
    os.makedirs(directory_binwalk_recursive)

if not os.path.exists(directory_pallette):
    os.makedirs(directory_pallette)


if file_check:
	os.system("file "+image_name)

if convert_check:
	new_image_name = directory+"/"+filename + "_convert" + extension
	os.system("convert "+image_name+" "+new_image_name)
	orig_size = os.path.getsize(image_name)
	new_size  = os.path.getsize(new_image_name)
	diff_size = orig_size - new_size
	prcn_size = 100 * float(diff_size) / float(orig_size)
	print "-------"*7
	print "Size difference: %d bytes (%f" % (diff_size, prcn_size) + "%)"
	if prcn_size > 1:
		print "WARNING- Check size difference, maybe something hidden with steghide?"


if binwalk_extract:
	print "-------"*7
	print "Binwalk extraction. Extracting to %s " % (directory_binwalk)
	os.system("binwalk -q -C "+directory_binwalk+" -e "+image_name)


if binwalk_recursive_extract:
	print "-------"*7
	print "Binwalk recursive extraction. Extracting to %s " % (directory_binwalk_recursive)
	os.system("binwalk -q -C "+directory_binwalk_recursive+" -Me "+image_name)


if strings_check:
	os.system("strings "+image_name+" >> "+directory+"/strings_result.txt")
	word = "flag"
	found_text = commands.getoutput("strings "+image_name+" | grep '"+word+"'")
	print "-------"*7
	print "String analysis - Searching word: %s" %(word)
	print "Results: %s" % (found_text)


if cat_check:
	os.system("cat "+image_name+" >> "+directory+"/cat_result.txt")
	word = "flag"
	found_text = commands.getoutput("cat "+image_name+" | grep '"+word+"'")
	print "-------"*7
	print "Cat analysis - Searching word: %s" %(word)
	print "Results: %s" % (found_text)


if ocr_check:
	jpg_image_name = directory+"/"+filename + "_convert.jpg"
	png_image_name = directory+"/"+filename + "_convert.png"
	os.system("convert "+image_name+" "+jpg_image_name)
	os.system("convert "+image_name+" "+png_image_name)
	bw_image_name = directory+"/"+filename + "_bw"+extension
	Image.open(image_name).convert('1').save(bw_image_name)
	jpg_text  = pytesseract.image_to_string(Image.open(jpg_image_name))
	orig_text = pytesseract.image_to_string(Image.open(image_name))
	png_text  = pytesseract.image_to_string(Image.open(png_image_name))
	bw_text  = pytesseract.image_to_string(Image.open(bw_image_name))
	print "-------"*7
	print "OCR results: \n"
	print " - Original: %s \n - JPG: %s \n - PNG: %s \n - B/W: %s" % (orig_text, jpg_text, png_text, bw_text)


if metadata_check:
	print "-------"*7
	print "Metadata\n"
	info = pyexifinfo.get_json(image_name)
	for i in info[0]:
		print "%s: %s" % (i, info[0].get(i))


if png_8bit and extension == ".png":
	print "-------"*7
	print "8-bit image - Changing pallette. Extracting to %s" % (directory_pallette)
	# for i in {0..255}; do ./change_palette.py doge_stege.png "single-color-${i}.png" "${i}"
	for color_n in range(0,255):
		palette_image = directory_pallette + "/" + filename+"_"+str(color_n)+extension
		fn.palette_func(image_name, palette_image, color_n)


if list_colors:
	csv_images_file = directory + "/" + image_name+"pixels.csv"
	print "-------"*7
	print "Extracting pixels color to %s" % (csv_images_file)
	im = Image.open(image_name)
	from collections import defaultdict
	by_color = defaultdict(int)
	for pixel in im.getdata():
		by_color[pixel] += 1
	with open(csv_images_file, 'wb') as csvfile:
		writer_ = csv.writer(csvfile)
		writer_.writerow(['Color'] + ['Pixels'])
		for color in sorted(by_color, key=by_color.get, reverse=True):
			writer_.writerow([color] + [by_color[color]])

if unzip_check:
	import zipfile, tarfile
	print "-------"*7
	print "Zip/tar extraction check"
	try:
		zip_ref = zipfile.ZipFile(image_name, 'r')
		zip_ref.extractall(directory)
		zip_ref.close()
	except:
		"Failed. Probably not a zip"
	try:
		tar = tarfile.open(image_name)
		tar.extractall()
		tar.close()
	except:
		"Failed. Probably not a tar"

if signatures_check:
	print "-------"*7
	print "Signatures check"
	p = Popen(['xxd', '-p', image_name], stdout=PIPE) 
	dump = p.communicate()[0]           
	res = []
	signatures = config.signatures
	for sig, desc in signatures:
		if sig in dump:
			res.append([sig, desc, dump.find(sig)])
	res.sort(key=lambda x: x[2])
	for sig, desc, offset in res:
            print("[+] %s : %s %s" % (sig, desc, "<- Offset: "+str(offset)))