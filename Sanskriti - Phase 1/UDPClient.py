#File name: UDPClient.py
#Author: Sanskriti Sharma
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 196/197

#import the socket module, the pillow module and the io module
from socket import *
from PIL import Image
import io

#Server name is set to localhost as we are working on one system
serverName = 'localhost'
#Server Port chosen arbitrairily 
serverPort = 12000
#Buffer size set to 64kB
buf = 65535

#The UDP socket is created. 
#AF_INET indicates that the underlying network is using IPv4. 
#SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
clientSocket = socket(AF_INET, SOCK_DGRAM)
#The variable message is set to the pixel values of image.bmp
with open("image.bmp", "rb") as image:
	message = image.read()
#The message is then sent via the client socket
clientSocket.sendto(message,(serverName, serverPort))
#A new message "modifiedMessage" is received from the server and the server address is saved
modifiedMessage, serverAddress = clientSocket.recvfrom(buf)
#An empty file is opened
f = open('grayscale.bmp', 'wb')
#The new message is written to the file 
f.write(modifiedMessage)
#THe image is displayed and the client socket is closed
finalImage = Image.open(io.BytesIO(modifiedMessage))
finalImage.show()
clientSocket.close()