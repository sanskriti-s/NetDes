#File name: UDPClient.py
#Author: Sanskriti Sharma
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 199

#import the socket module, the pillow module and the io module
from socket import *
from PIL import Image
import io

#The server port and buffer are set to the same as the client
serverPort = 12000
buf = 65535

#The UDP socket is created same as the client. 
#AF_INET indicates that the underlying network is using IPv4. 
#SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
serverSocket = socket(AF_INET, SOCK_DGRAM)
#The port number 12000 is bound to the server’s socket.
serverSocket.bind(('',serverPort))
print ('The server is ready to receive')
#Enters an indefinite loop
while True:
	#The message is recieved from the client and the client address is saved
	message, clientAddress = serverSocket.recvfrom(buf)
	#The image is opened
	image = Image.open(io.BytesIO(message), 'r')
	#The image is converted to greyscale and saved to modifiedImage
	modifiedImage = image.convert('L')

	#The pixel values of the image are converted into a byte array
	imgByteArr = io.BytesIO()
	modifiedImage.save(imgByteArr, format='BMP')
	#The values of the buffer are returned and saved to "finalMessage"
	finalMessage = imgByteArr.getvalue()
	#the final message is sent to the client
	serverSocket.sendto(finalMessage, clientAddress)