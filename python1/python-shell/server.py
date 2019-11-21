import sys, socket, threading
import subprocess
import time

def getTime():
    return time.strftime("%H:%M:%S")

max_caracteres = 1000
server_ip = sys.argv[1] if len(sys.argv) >= 3  else raw_input("Server IP: ")
server_port = int(sys.argv[2]) if len(sys.argv) >= 3  else raw_input("Server Port: ")

server_socket = socket.socket()
server_socket.bind((server_ip, server_port))
server_socket.listen(10)

while 1:
    client_socket, address = server_socket.accept()
    address = ':'.join(map(str, address))
    timestamp = getTime()
    print ("["+timestamp+"]   "+address+" connected. Waiting for command...")
    
    command = client_socket.recv(max_caracteres)
    timestamp = getTime()
    print ("["+timestamp+"]   " +"Command \""+command+"\" received from "+address+".")
    
    client_socket.send(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read())
    client_socket.close()