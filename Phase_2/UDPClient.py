# File name: UDPClient.py
# Author: Sanskriti Sharma, John Lutz, Justice Graves
# Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 196/197

# import the socket module, the pillow module, the os module, and the tkinter module
import socket
import tkinter as tk
from tkinter import scrolledtext

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
hostNameView.focus()

# Creates labels and a spin object to choose the error level in the GUI
spinnerLabel = tk.Label(rootView, text="Choose error percentage below:")
spinnerLabel.grid(column=0, row=14)
errorSpinner = tk.Spinbox(rootView, from_=0, to=100, width = 5)
errorSpinner.grid(column=0, row=16)

# Creates a state/message log in the GUI
stateLog = scrolledtext.ScrolledText(rootView, width=60, height=10)
stateLog.grid(column=0, row=20)
stateLog.insert(tk.END, "Client State Log:\n")

# The UDP socket is created.
# The UDP socket is created same as the client.
# AF_INET indicates that the underlying network is using IPv4.
# SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server Port chosen arbitrarily
serverPort = 12000
clientPort = 13000
# Buffer size set to 6000 bytes
buf = 6000
# The port number 13000 is bound to the client socket.
clientSocket.bind(('', clientPort))

# "sendButton" click handler
def onClick():
    # Server name is set to localhost as we are working on one system
    serverName = hostNameView.get()
    if serverName == "":
        stateLog.insert(tk.END, "Error: Cannot Send, Invalid Server IPA/Name\n")
    else:
        stateLog.insert(tk.END, "Sending image data...\n")
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
                checksumInt = generateChecksum(int.from_bytes(message, byteorder="little"), sequenceNumberInt, True)
                # Change the sequence number into a suitable bytes item for transport (1x2 bytes long)
                sequenceNumber = sequenceNumberInt.to_bytes(1, byteorder="little")
                # Change the integer checksum into a suitable bytes item for transport (4x2 bytes long)
                checksum = checksumInt.to_bytes(4, byteorder="little")
                # The packet is then prepared and sent via the client socket
                data = sequenceNumber + checksum + message
                clientSocket.sendto(data, (serverName, serverPort))
                # Break when message ends
                if message == b'':
                    stateLog.insert(tk.END, "... Image sent completely\n")
                    break

# Generate the checksum for the given 1kB chunk of data and SN
def generateChecksum(data, sn, flag):
    a = sn
    d = bin(data)[2:]
    for x in range(0, 511):
        temp = a
        try:
            a += int(d[(16 * x): (15 + (16 * x))], 2)
            if a > 65536:
                a -= 65536
                a += 1
        except ValueError:
                a = temp
    if flag:
        return int(bin(a).translate(str.maketrans("10", "01"))[2:], 2)
    else:
        return a

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
clientSocket.close()
