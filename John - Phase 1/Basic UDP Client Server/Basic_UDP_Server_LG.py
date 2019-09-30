# Course Name:		Network Design
# Course #:		    EECE 4830-5830 - 201
# Instructor:		Dr. Vinod Vokkarane
# Student:		    John Lutz
# Semester:		    Fall 2019
# Project:		    Phase 1 - UDP Server
# Date Created:		11 Sep 2019
# Language:         Python 3.7 x64
# References:       Located at end of code

from PIL import Image # for pillow image handling
import ast
import socket #replaces: from socket import *, required for gethostname, allows creation of sockets

print('This is the server.')
serverHostname = socket.gethostname() # acquires hostname of machine used to run server
print('Server hostname is:', serverHostname)
serverIP = (socket.gethostbyname(serverHostname))
print('Server IP is:', serverIP)
print('Enter one of these in the client interface.')

serverPort = 12000      # what port will the socket operate on / talk to
# set this to the same in the client code
# print('Server port is automatically set to:', serverPort)

# serverSocket = socket(AF_INET, SOCK_DGRAM)  # creates the servers socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # replaces above
# AF_INET: address family (IPv4), SOCK_DGRAM: datagram (UDP)

serverSocket.bind(('', serverPort))     # binds / assigns the port to the socket
# the server is now listening on a socket at an ip and port

while True:
    print("Server is awaiting your selection.")

    cmd, clientAddress = serverSocket.recvfrom(2048) # num is a buffer size in bytes
    # incoming data packet stored in "cmd"
    # stores client address and port # in clientAddress, used to send response

    if cmd.decode() == 'M':
        status = 'waiting'
        print('Server is awaiting your message.')

        while status == 'waiting':

            message, clientAddress = serverSocket.recvfrom(4096) # num is a buffer size in bytes
        # incoming data packet stored in "message"
        # stores client address and port # in clientAddress, used to send response

            print("Server received this message from the client:", message.decode())
            # converts incoming message from binary to text and displays it to the user
    
            modMessage = message.decode().upper()
            # decodes incoming message from binary to text, modifies it to upper case
   
            serverSocket.sendto(modMessage.encode(), clientAddress)
            # encodes & sends modified (capitalized) message to client

            status = 'done'


    elif cmd.decode() == 'F':
        status = 'waiting'
        while status == 'waiting':

            needSize = 'true'
            while needSize == 'true':
                print('Server is awaiting image dimensions.')
                binImgSize, clientAddress = serverSocket.recvfrom(4096)
                # print(binImgSize)
                sizeStringDecoded = binImgSize.decode() # decode it after RX for use
                # print(sizeStringDecoded)
                newSizeTuple = ast.literal_eval(sizeStringDecoded) # turn sizeStringDecoded back into a sizeTuple ??
                print('Image Dimensions are:', newSizeTuple)
                needSize = 'false'

            needImage = 'true'
            while needImage == 'true':
                print('Server is awaiting image data.')

                binRxImg, clientAddress = serverSocket.recvfrom(96000) # num is a buffer size in bytes
# incoming data stored in "binRxImg"; stores client address and port # in clientAddress, used to send response
                # print(binRxImg) # shows binary stream
  
                RxImg = Image.frombytes('RGB', (newSizeTuple), binRxImg) # creates image from bitstream
                # (mode, size, data, decoder_name = 'raw', *args) size must be at least a 2 dimension tuple

                #clientImg.save('temp.bmp') # save image if desired
                print('Server received this image from the client.')
                RxImg.show()
                modImg = RxImg.rotate(45) # rotate image before sending it back
                #print('modImg', modImg)
                modImgBytes = modImg.tobytes() # convert image to bytes for TX, encoder_name = 'raw'
                serverSocket.sendto(modImgBytes,clientAddress) # send the binary image file
                needImage = 'false'

            status = 'done'

    else:
        print('Invalid command.')

