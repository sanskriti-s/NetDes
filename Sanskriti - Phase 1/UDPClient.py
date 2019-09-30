#File name: UDPClient.py
#Author: Sanskriti Sharma
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 196/197

#import the socket module, the pillow module and the io module
import socket
from PIL import Image
import io
import os

#Server name is set to localhost as we are working on one system
serverName = 'localhost'
#Server Port chosen arbitrairily 
serverPort = 12000
#Buffer size set to 64kB
buf = 5000

print('This is the client.')
print('If you are unsure of server hostname or IP please see info in server window.')
print('The hostname is not case sensitive and works on machines with multiple IPs.')
serverName = input('Input destination server IP or hostname: ') # requires an ip address or DNS resolvable hostname
print('Server to connect to is set to:', serverName)

#The UDP socket is created. 
#AF_INET indicates that the underlying network is using IPv4. 
#SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if os.path.exists("temp1.bin"):
	os.remove("temp1.bin")

#The variable message is set to the pixel values of image.bmp
with open("image1.bmp", "rb") as image:
	while True:
		message = image.read(4096)
		#The packet is then sent via the client socket
		clientSocket.sendto(message,(serverName, serverPort))
		if (message == (b'')):
			break

final = []
recieveFile = True
while recieveFile:
	#A new message "modifiedMessage" is received from the server and the server address is saved
	modifiedMessage, serverAddress = clientSocket.recvfrom(buf)
	#print(modifiedMessage)
	final.append(modifiedMessage)
	if (modifiedMessage == b''):
		recieveFile = False

print(modifiedMessage)

with open ('temp1.bin', 'ab+') as file:
	for n in range(len(final)):
		file.write(final[n])

image = Image.open('temp1.bin')
image.show()

clientSocket.close()