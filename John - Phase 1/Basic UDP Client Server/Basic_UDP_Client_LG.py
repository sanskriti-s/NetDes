# Course Name:		Network Design
# Course #:		    EECE 4830-5830 - 201
# Instructor:		Dr. Vinod Vokkarane
# Student:		    John Lutz
# Semester:		    Fall 2019
# Project:		    Phase 1 - UDP Client
# Date Created:		11 Sep 2019
# Language:         Python 3.7 x64
# References:       Located at end of code

import time
from PIL import Image # for pillow image handling

import socket #replaces # from socket import *    # allows creation of sockets
# incompatible with import socket which is required for gethostname

print('This is the client.')
print('If you are unsure of server hostname or IP please see info in server window.')
print('The hostname should not be case sensitive.')
serverName = input('Input destination server hostname or IP: ') # requires an ip address or DNS resolvable hostname
print('Server to connect to is set to:', serverName)

serverPort = 12000 # what port will the socket operate on / talk to
# set this to the same in the server code
# print('Server port is automatically set to',serverPort)

# clientSocket = socket(AF_INET, SOCK_DGRAM) # creates the clients socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # replaces above
# AF_INET: address family (IPv4), SOCK_DGRAM: datagram (UDP)
# client socket port # determined by OS

cont = 'Y'
while cont == 'Y':

    cmd = input('Send a [M]essage or a [F]ile ? ').upper()

    if cmd == 'M': # Message Mode

        clientSocket.sendto(cmd.encode(),(serverName, serverPort))
# convert cmd from string to bytes, include destination, send out of client socket to server

        message = input('Input a message to send: ') # was raw_input; request message to send
        print('You entered: ', message) # confirm input message
        
        clientSocket.sendto(message.encode(),(serverName, serverPort))
# convert message from string to bytes, include destination, send out of client socket to server

        # client awaits server response

        modifiedMessage, serverAddress = clientSocket.recvfrom(4096) # num is buffer size in bytes
# store server response in "modifiedMessage", store server address and port # in serverAddress

        print('The server capitalized your message & sent it back to you.', modifiedMessage.decode())
        # decodes message from bytes to string & displays it
  
    elif cmd == 'F': # File Mode

        clientSocket.sendto(cmd.encode(),(serverName, serverPort))
# convert cmd from string to bytes, include destination, send out of client socket to server   

        ogFileName = input('Input name of file to send: ') # input original file to open
        ogImg = Image.open(ogFileName) # PILf creates image object
        #ogBmp.show() # PILf display original image for verification if desired
        # print(ogBmp) # PY output original image info

        ogImgSizeString = (str(ogImg.size)) # converts image size 2 tuple into string
        clientSocket.sendto(ogImgSizeString.encode(),(serverName, serverPort)) # encode & send binary image size
        clientImgBytes = ogImg.tobytes() # convert image to bytes for TX, encoder_name = 'raw'
        
        # server is waiting for image data
        ogPyImg = open(ogFileName, 'rb')
        ogPyImg.read(1024) # cant read bytes or PILf image object


        # !! MAX file size is currently ~ 41 k

        clientSocket.sendto(clientImgBytes,(serverName, serverPort)) # send the binary image file

        # client awaits server response
        needModImg = 'true'
        while needModImg == 'true':
            print('Client awating modified image.')
            binModImg, serverAddress = clientSocket.recvfrom(96000) # num is buffer size in bytes
    # store server response in "binModImg", store server address and port # in serverAddress
            clientModImg = Image.frombytes('RGB', (ogImg.size), binModImg) # creates image from bitstream
    # (mode, size, data, decoder_name = 'raw', *args) size must be at least a 2 dimension tuple
            clientModImg.show()
            needModImg = 'false'

    else:
        print('Invalid command.')
    
    cont = input('Continue ? [Y]es : ').upper()


print('\nThe client is closing in: ')
for i in range(3, 0, -1): # decrements from 3 to 0
  print(i)
  time.sleep(1) # for 1 second countdown delay

clientSocket.close()    # close socket & terminate process
