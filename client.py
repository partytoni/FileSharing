import socket
import os
import math

def Main():
	CONSTANT=1024*8
	FILE="cose.mp4"
	host = '127.0.0.1'
	port = 5000
	
	#variables used to compute percentage
	percentage=1
	times=0
		
	#open connection with server
	mySocket = socket.socket()
	mySocket.connect((host,port))
	
	#open file to send and save its size in bytes
	f = open(FILE, "rb")
	size = os.path.getsize(FILE)
	
	#byte contains each read of CONSTANT bytes
	byte = f.read(CONSTANT)

	while byte:
		mySocket.send(byte)
		times+=1
		current_percentage=math.floor(((times*CONSTANT)/size)*100)
		if current_percentage>percentage:
			print(current_percentage)
			percentage+=1

		#reads next sequence of bytes	
		byte = f.read(CONSTANT)
			
	#close the socket when you are done
	mySocket.close()

if __name__ == '__main__':
	Main()