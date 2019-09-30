#File name: UDPClient.py
#Author: Sanskriti Sharma
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 199

#import the socket module, the pillow module and the io module
import socket
from PIL import Image
import io
import os

#The server port and buffer are set to the same as the client
serverPort = 12000
buf = 5000

print('This is the server.')
serverHostname = socket.gethostname() # acquires hostname of machine used to run server
print('Server hostname is:', serverHostname)
serverIP = (socket.gethostbyname(serverHostname))
print('Server IP is:', serverIP)
print('Enter one of these in the client interface.')

#The UDP socket is created same as the client. 
#AF_INET indicates that the underlying network is using IPv4. 
#SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#The port number 12000 is bound to the server’s socket.
serverSocket.bind(('',serverPort))
print ('The server is ready to receive')

if os.path.exists("temp.bin"):
	os.remove("temp.bin")
if os.path.exists("final.bmp"):
	os.remove("final.bmp")

message = []

#Enters an indefinite loop
while True:

	receiveFile = True
	while receiveFile:
		#The message is recieved from the client and the client address is saved
		output, clientAddress = serverSocket.recvfrom(buf)

		message.append(output)
		if (output == b''):
			receiveFile = False

	with open ('temp.bin', 'ab+') as file:
		for n in range(len(message)):
			file.write(message[n])

	image = Image.open("temp.bin")
	image.show()	
	#The image is converted to greyscale and saved to modifiedImage
	modifiedImage = image.convert('L')

	#The pixel values of the image are converted into a byte array
	imgByteArr = io.BytesIO()
	#modifiedImage.save(imgByteArr, format='BMP')
	modifiedImage.save('final.bmp')
	#The values of the buffer are returned and saved to "finalMessage"
	#finalMessage = imgByteArr.getvalue()
	#the final message is sent to the client
	with open("final.bmp", "rb") as final:
		while True:
			finalMessage = final.read(4096)
			serverSocket.sendto(finalMessage, clientAddress)
			if (finalMessage == (b'')):
				break





















