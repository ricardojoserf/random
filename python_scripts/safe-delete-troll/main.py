import os
import sys
import shutil
import psutil
import multiprocessing
import threading
import time
import argparse

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file', required=True, action='store', help='File to replicate')
  parser.add_argument('-d', '--directory', required=False, default = 'result/', action='store', help='File to replicate')
  parser.add_argument('-t', '--threads', required=False, default = 3, action='store', help='Number of threads')
  parser.add_argument('-n', '--number', required=False, action='store', help='Number of copies')
  my_args = parser.parse_args()
  return my_args

def copy_file((orig_file, copied_file)):
	#print ("Copying %s to %s"%(orig_file,copied_file))
	shutil.copyfile(orig_file, copied_file) 


# Un poco fumada, algoritmo que hice sobre 2016 para otro proyecto
def recursive_copies(orig_file, n_files, directory):
	name_base = orig_file.split(".")[0]+"_"
	name_extn = "."+orig_file.split(".")[1]
	counter_files = 0
	flag = 0
	all_files = [orig_file]
	new_names = []
	count = 0
	flag = 0
	countClones = 1
	while(flag == 0):
	    for i in all_files:
	        clone_name = directory + name_base+str(countClones)+name_extn
	        copy_file( (i, clone_name) )
	        count += 1
	        countClones += 1
	        new_names.append(clone_name)
	        if(count==int(n_files)):
	            flag = 1
	            break
	    for j in new_names:
	        all_files.append(j)
	    new_names=[]


def multiprocessing_copies(orig_file, n_files, directory, threads):
	name_base = orig_file.split(".")[0]+"_"
	name_extn = "."+orig_file.split(".")[1]
	clone_names = []
	for i in range(1, n_files+1):
		clone_names.append( ( orig_file, directory + name_base+str(i)+name_extn ) )
	p = multiprocessing.Pool(threads)
	p.map(copy_file,clone_names)

	'''
	processes = []
	for i in range(1, n_files+1):
		tuple_ = (orig_file, directory+name_base+str(i)+name_extn)
		p = multiprocessing.Process(target=copy_file,args=((tuple_),) )
		processes.append(p)
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	'''

def multithreaded_copies(orig_file, n_files, directory):
	name_base = orig_file.split(".")[0]+"_"
	name_extn = "."+orig_file.split(".")[1]
	jobs = []
	for i in range(1, n_files+1):
		tuple_ = (orig_file, directory+name_base+str(i)+name_extn)
		thread = threading.Thread( target=copy_file,args=((tuple_),) )
		jobs.append(thread)
	for j in jobs:
		j.start() 
	for j in jobs:
		j.join()

def size_info(file_size, total_space, free_space):
	print("\nStorage Info:")
	print("File:\t%s bytes"%file_size)
	print ("Info:\t%s/%s GB" %(free_space / (1024.0 ** 3), total_space / (1024.0 ** 3)))
	print ("Free:\t%s B" %(free_space))
	
def total_files(orig_file, file_size):
	obj_Disk = psutil.disk_usage('/')
	free_space = obj_Disk.free
	total_space = obj_Disk.total
	size_info(file_size, total_space, free_space)
	n_files = free_space / file_size
	resto = free_space % file_size
	return n_files, resto

def createDir(directory):
	time.sleep(1)
	if os.path.exists(directory):
			shutil.rmtree(directory)
	if not os.path.exists(directory):
			os.makedirs(directory)

if __name__ ==  '__main__':
	args = get_args()

	directory = 'result/'
	orig_file = args.file
	threads = int(args.threads)
	file_size = os.path.getsize(orig_file)
	n_files, resto = total_files(orig_file, file_size)
	print ("\nTotal of files to be created:\t%s files\nSpace left after execution:\t%s bytes\n"%(n_files, resto))
	if args.number is None:
		n_files = raw_input("Number of copies to create: ")
	else:
		n_files = args.number
	try:
		n_files = int(n_files)
	except:
		print("Please use an integer")
	resp = raw_input("Creating %s copies. Continue? [y/N] "%(n_files))
	if resp == "y" or resp =="Y":
		
		# print ("\n\nn_files = %s\nthreads = %s"%(n_files, threads))

		'''
		createDir(directory)
		t0 = time.time()
		recursive_copies(orig_file, n_files, directory)
		total_time = time.time()-t0
		print("Total time (Custom algorithm): %s seconds\n"%( (total_time) ))

		createDir(directory)
		t0 = time.time()
		multithreaded_copies(orig_file, n_files, directory)
		total_time = time.time()-t0
		print("Total time (Multithreaded): %s seconds\n"%( (total_time) ))
		
		'''
		createDir(directory)
		t0 = time.time()
		multiprocessing_copies(orig_file, n_files, directory, threads)
		total_time = time.time()-t0
		print("Total time (Multiprocessing): %s seconds\n"%( (total_time) ))

		total_files(orig_file, file_size)
	else:
		print("\nNot executed. Use 'y' or 'Y' to execute.")