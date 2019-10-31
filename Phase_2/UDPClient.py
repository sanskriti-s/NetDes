# File name: UDPClient.py
# Author: Sanskriti Sharma, John Lutz, Justice Graves
# Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 196/197

# import the socket module, the pillow module, the os module, and the tkinter module
import socket
from PIL import Image
import os
import tkinter as tk
import math

# Creates a new window interface and labels it
rootView = tk.Tk()
rootView.title("Client Package")
rootView.geometry("525x400")

# Creates a top label explaining instructions
topLabel = tk.Label(rootView, text="If you are unsure of server hostname or IP please see info in server window.")
topLabel.grid(column=0, row=0)
topNextLabel = tk.Label(rootView, text="The hostname is not case sensitive and works on machines with multiple IPs.")
topNextLabel.grid(column=0, row=2)
IPLabel = tk.Label(rootView, text="Input destination Server IPA (or hostname): ")
IPLabel.grid(column=0, row=4)
hintLabel = tk.Label(rootView, text="(Hint: The 'Server Package' must be open BEFORE sending to prevent crashing)")
hintLabel.grid(column=0, row=8)

# Creates a textbox to input information
# The 'Entry' view that will contain the information given by the user
hostNameView = tk.Entry(rootView, width=20)
hostNameView.grid(column=0, row=6)


# "sendButton" click handler
def onClick():
    # Server name is set to localhost as we are working on one system
    serverName = hostNameView.get()
    infoNextLable = tk.Label(rootView, text="                    ")
    infoNextLable.grid(column=0, row=14)
    if serverName == "":
        infoLabel = tk.Label(rootView, text="Please input a server address before trying to send!!!")
        infoLabel.grid(column=0, row=12)
    else:
        infoLabel = tk.Label(rootView, text="Image sent to specified server!")
        infoLabel.grid(column=0, row=12)
        infoNextLable = tk.Label(rootView, text="Waiting on server...")
        infoNextLable.grid(column=0, row=14)
        # Server Port chosen arbitrarily
        serverPort = 12000
        # Buffer size set to 64kB
        buf = 5000

        # The UDP socket is created.
        # AF_INET indicates that the underlying network is using IPv4.
        # SOCK_RAW indicates we are utilizing a custom packet format (to include additional header information)
        # SOCK_IPPROTO_UPD means it is a UDP socket (rather than a TCP socket.)
        #clientSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Deleting temporary file if it exists
        if os.path.exists("temp1.bin"):
            os.remove("temp1.bin")

        sequenceNumberInt = 1
        # The variable message is set to the pixel values of image.bmp
        with open("image1.bmp", "rb") as image:
            while True:
                # Swap the sequence number between each case
                if sequenceNumberInt == 1:
                    sequenceNumberInt = 0
                else:
                    sequenceNumberInt = 1

                # Convert image into packets of bytes
                message = image.read(1024)
                # Generate the checksum (int)

                serverIPA = intIP(serverName)
                checksumInt = generateChecksum(int.from_bytes(message, byteorder="little"),
                                               serverIPA, serverPort, sequenceNumberInt, True)
                value = generateChecksum(int.from_bytes(message, byteorder="little"),
                                               serverIPA, serverPort, sequenceNumberInt, False)
                # Change the sequence number into a suitable bytes item for transport
                sequenceNumber = sequenceNumberInt.to_bytes(2, byteorder="little")
                # Change the integer checksum into a suitable bytes item for transport
                checksum = checksumInt.to_bytes(8, byteorder="little")
                truth = verifyChecksum(value, checksumInt)
                # print(int.from_bytes(checksum, byteorder="big"))
                # The packet is then prepared and sent via the client socket
                data = sequenceNumber + checksum + message
                clientSocket.sendto(data, (serverName, serverPort))
                # Break when message ends
                if message == b'':
                    break

        final = []
        # Set flag
        recieveFile = True
        while recieveFile:
            # A new message "modifiedMessage" is received from the server and the server address is saved
            modifiedMessage, serverAddress = clientSocket.recvfrom(buf)
            final.append(modifiedMessage)
            # Check for end of file
            if (modifiedMessage == b''):
                recieveFile = False

        # Deleting temporary file if it exists
        with open('temp1.bin', 'ab+') as file:
            for n in range(len(final)):
                file.write(final[n])

        infoNextLable = tk.Label(rootView, text="Server Response Complete!")
        infoNextLable.grid(column=0, row=14)

        image = Image.open('temp1.bin')
        image.show()

        clientSocket.close()

# Turn an IPv4 value into a integer value
def intIP(address):
    if address == "localhost":
        address = socket.gethostbyname(socket.gethostname())
    elif address == socket.gethostname():
        address = socket.gethostbyname(socket.gethostname())
    ipa_int = 0
    for v in range(0, math.ceil(len(address) / 2)):
        temp = ''.join(format(ord(i), 'b') for i in address[(2 * v): (2 * (v + 1))])
        ipa_int += int(temp, 2)
    return ipa_int

# Generate the checksum for the given 1kB chunk of data, and the given IPA, PORT, and SN
def generateChecksum(data, ipa, port, sn, flag):
    a = ipa + sn
    b = port
    a += b
    if a > 65536:
        a -= 65536
        a += 1
    a_1 = a
    d = bin(data)[2:]
    for x in range(0, 511):
        temp = a_1
        try:
            a_1 += int(d[(16 * x): (15 + (16 * x))], 2)
            if a_1 > 65536:
                a_1 -= 65536
                a_1 += 1
        except ValueError:
                a_1 = temp
    if flag:
        return int(bin(a_1).translate(str.maketrans("10", "01"))[2:], 2)
    else:
        return a_1

# Check if two checksums are valid for the given received data
def verifyChecksum(value, checksum):
    verify = bin(value^checksum)
    checker = (2 ** (len(verify) - 2)) - 1
    if int(verify, 2) == checker:
        return True
    return False

# Creates a button to initiate the send and to show sending info
sendButton = tk.Button(rootView, text="Send Image", command=onClick)
sendButton.grid(column=0, row=10)

# Show the window GUI in the OS of the user
rootView.mainloop()
