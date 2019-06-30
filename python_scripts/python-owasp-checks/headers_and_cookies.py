import requests


def get_headers(site):
	site = site.replace("https://","")
	site = site.replace("http://","")
	try:
		req = requests.get('https://' + site)
	except requests.exceptions.SSLError as error:
		print ("doesn't have SSL working properly (%s)" % (error, ))
		return False
	return  req.headers

	
def get_hsts(headers):
	if 'strict-transport-security' in headers:
		return True
	else:
		return False


def get_security_headers(headers):
	fields = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options', 'Content-Type']
	vals = []
	for f in fields:
		try:
			vals.append("%s: %s"%(f, headers[f]))
		except:
			vals.append("%s: %s"%(f, 'Not ser'))
			pass
	# yo devolveria vals y a bailar, pero es mas facil como lo estamos haciendo asi...
	string_to_print = "HTTP Security Headers \n"
	for v in vals:
		string_to_print += ("%s\n"%(v))
	return string_to_print


def get_cookies(site):
	r = requests.get(site)
	cookies = r.cookies
	cookie_values = []
	for c in cookies:
		try:
			httponly_ = c._rest['HttpOnly']
		except:
			httponly_ = 'Not set'
			pass
		cookie_values.append({'secure': c.secure, 'httponly': httponly_, 'path': c.path, 'domain': c.domain, 'name': c.name, 'value': c.value})
	# yo devolveria cookie_values pero como lo estamos haciendo asi es mas facil... :(
	string_to_print = ""
	counter = 0
	for i in cookie_values:
		counter +=1
		string_to_print += ("\nCookie %s\n" %(counter) )
		for key, value in i.items():
			string_to_print += ( ("%s: %s\n"%(key, value)))
	return string_to_print


def main():
	site = 'https://www.google.com'
	headers = get_headers(site)

	hsts = get_hsts(headers)
	print("HSTS is set: %s\n" % hsts)

	security_headers  = get_security_headers(headers)
	print (security_headers)

	cookie_info = get_cookies(site)
	print  (cookie_info)

main()