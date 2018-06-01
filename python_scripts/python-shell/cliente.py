import sys, readline, socket

max_caracteres = 1000
server_ip = sys.argv[1] if len(sys.argv) >= 3  else raw_input("Server IP: ")
server_port = int(sys.argv[2]) if len(sys.argv) >= 3 else int(raw_input("Server Port: "))

while 1:
	client_socket 	= socket.socket()
	client_socket.connect((server_ip, server_port))

	command = sys.argv[3] if len(sys.argv) >= 4 else raw_input("Command: ")
	client_socket.send(command)

	print client_socket.recv(max_caracteres)