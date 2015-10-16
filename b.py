#encoding=utf-8
import socket
import sys

HOST, PORT = "10.1.2.62", 1234
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
	# Connect to server and send data
	sock.connect((HOST, PORT))
	sock.sendall(data + "\n")
	i = 0
	while (i < 30000000):
		i+=1
	# Receive data from the server and shut down
	received = sock.recv(1024)
finally:
	sock.close()

print "Sent:	 {}".format(data)
print "Received: {}".format(received)