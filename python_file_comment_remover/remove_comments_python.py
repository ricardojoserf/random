import sys

f = open(sys.argv[1])
content = [x.strip() for x in f.readlines()]
good_lines = []

for i in content:
	if not i.startswith("#"):
		good_lines.append(i)

file = open("new_"+sys.argv[1],"w") 
for j in good_lines:
	file.write(j + "\n")
file.close()
