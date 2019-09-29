import socket
import time

print('This is the client.')
print('If you are unsure of server hostname or IP please see info in server window.')
print('The hostname should not be case sensitive.')
serverName = input('Input destination server hostname or IP: ') # requires an ip address or DNS resolvable hostname
print('Server to connect to is set to:', serverName)

serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# AF_INET: address family (IPv4), SOCK_DGRAM: datagram (UDP)
# client socket port # determined by OS


# server is waiting for image data

cont = 'Y'
while cont == 'Y':
    ogFileName = input('Input name of file to send: ') # input original file to open
    ogPyImg = open(ogFileName, 'rb')

    readImg = True # as long as there is image data to read and send
    while readImg == True:

        clientPartImgBytes = ogPyImg.read(4096) # was 1024 reads image files, cant read bytes or PILf image object
        clientSocket.sendto(clientPartImgBytes,(serverName, serverPort)) # send piece of image
        #print(clientPartImgBytes) # usefull to verify splitting of data
        # possibly automatically sends empty b'' as last since thats what prints out, easy built in EOF flag
        time.sleep(0.010) # (x) second delay. trying to reduce from 0.010

        if clientPartImgBytes == (b''): # at EOF, when there is no more image data to read
            readImg = False # exit while loop at end of file (EOF)
            

    cont = input('Continue ? [Y]es : ').upper()