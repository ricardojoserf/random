#!/usr/bin/env python
import sys

fname = sys.argv[1]

def create_new_file():
	lines = open(fname).read().splitlines()
	new_file_lines = []
	count_table = 0
	
	#  while read p; do   echo 'new_file_lines.append('\'"$p"\'')'; done < a
	new_file_lines.append('<br><div id="particles-js-background" class="container" ng-controller="mainController"> </div><div id="overlay" class="container" ng-controller="mainController"><br><br>')

	for l in lines:
		bold_counter = 0
		italic_counter = 0
		chars = []
		for i in range(0,len(l)):
			if l[i] == "*":
				if (i+1) < len(l): 
					if bold_counter % 2 ==0:
							if l[i+1] == "*":
								chars.append("<b>")
								bold_counter += 1	
							elif l[i-1] != "*":
								chars.append("<i>")
								bold_counter += 1	
					else:
							if l[i+1] == "*":
								chars.append("</b>")
								bold_counter += 1	
							elif l[i-1] != "*":
								chars.append("</i>")
								bold_counter += 1	
			else:
				chars.append(l[i])
		l = ''.join(chars)


		if l.startswith("#"):
			h_n = str(l.count('#'))
			l = l.replace("#","")
			new_line = "<h"+h_n+">"+l+"</h"+h_n+">"
		elif l.startswith("`"):
			if count_table % 2 == 0:
				new_line = '<input class="form-control input-lg text-center" rows="2" cols="20" style="border: none;" value="'
			else:
				new_line = '"></input><br>'
			count_table += 1
		elif l.startswith("![Screenshot]"):
			l = l.replace("![Screenshot](","")
			l = l.replace(")","")
			new_line = '<img src="'+l+'">'
		elif l.startswith("----"):
			new_line = ""
		else:
			new_line = l
	
		
		if count_table % 2 == 0:
			new_line += "<br>"
	

		new_file_lines.append(new_line)
	
	new_file_lines.append('<br><br><br><br><script src="visual/particles/particles.js"></script><script src="visual/particles/particles_style_2.js"></script>')
	

	#print '\n'.join(new_file_lines)
	open(sys.argv[2],'w').write('\n'.join(new_file_lines))

create_new_file()
