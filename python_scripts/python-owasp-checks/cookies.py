import requests

def get_info(site):
	r = requests.get(site)
	cookies = r.cookies
	cookie_values = []
	for c in cookies:
		try:
			httponly_ = c._rest['HttpOnly']
		except:
			httponly_ = 'Not set'
			pass
		cookie_values.append({'name': c.name, 'value': c.value, 'path': c.path, 'domain': c.domain, 'secure': c.secure, 'httponly': httponly_})
	return cookie_values


site = 'https://www.google.com'
cookie_info = get_cookies(site)
print  cookie_info