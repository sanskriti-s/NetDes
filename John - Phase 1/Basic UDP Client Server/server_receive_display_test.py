from PIL import Image # for pillow image handling
import os
import socket #replaces: from socket import *, required for gethostname, allows creation of sockets

print('This is the server.')
serverHostname = socket.gethostname() # acquires hostname of machine used to run server
print('Server hostname is:', serverHostname)
serverIP = (socket.gethostbyname(serverHostname))
print('Server IP is:', serverIP)
print('Enter one of these in the client interface.')

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))     # binds / assigns the port to the socket
# the server is now listening on a socket at an ip and port

while True:
    print('Server is awaiting image data.')
    
    if os.path.exists("temp.bin"):
        os.remove("temp.bin") 

    receiveFile = True
    while receiveFile:

        serverImgBytes, clientAddress = serverSocket.recvfrom(5000) # was 2048 num is a non-persistent buffer size in bytes
        # incoming data stored in "serverImgBytes". Can only RX a single TX.
        # Size is limited by network maximum packet size of ~ 41k
        # stores client address and port # in clientAddress, used to send response
        # print(serverImgBytes)
        with open ('temp.bin', 'ab+') as file: # append, binary, create if nonexistent
            file.write(serverImgBytes) # write data from serverImgBytes to temBin object
       
        if serverImgBytes == (b''):
            #print(serverImgBytes)
            imgFile = Image.open('temp.bin')
            imgFile.show()
            receiveFile = False
