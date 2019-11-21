import OpenSSL
import ssl
import sys


port = "443"
cert = ssl.get_server_certificate((sys.argv[1], port))

c = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).get_subject().get_components()
for i in c:
    print(str(i[0].decode('UTF-8')), ":", str(i[1].decode('UTF-8')))
