import socket
 
def Main():
	CONSTANT=1024*8
	host = "127.0.0.1"
	port = 5000
	 
	mySocket = socket.socket()
	mySocket.bind((host,port))
	
	mySocket.listen(1)
	conn, addr = mySocket.accept()
	print ("Connection from: " + str(addr))
	f = open("server.mp4","wb")
	while True:
		data = conn.recv(CONSTANT)
		if not data:
			break
		f.write(data)

	conn.close()
	 
if __name__ == '__main__':
	Main()