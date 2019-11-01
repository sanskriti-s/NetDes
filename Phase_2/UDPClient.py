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

# Creates a textbox to input information
# The 'Entry' view that will contain the information given by the user
hostNameView = tk.Entry(rootView, width=20)
hostNameView.grid(column=0, row=6)
hostNameView.focus()

# Creates labels and a spin object to choose the error level in the GUI
spinnerLabel = tk.Label(rootView, text="Choose error percentage below:")
spinnerLabel.grid(column=0, row=12)
errorSpinner = tk.Spinbox(rootView, from_=0, to=100, width=5)
errorSpinner.grid(column=0, row=14)

# Creates a hint label that helps out the user
hintLabel = tk.Label(rootView, text="(Hint: The 'Server Package' must be open BEFORE sending to prevent crashing)")
hintLabel.grid(column=0, row=16)

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
# Buffer size set to 6000 bytes
buf = 6000

# "sendButton" click handler
def onClick():
    global sendButton
    sendButton.configure(state=tk.DISABLED)
    # Server name is set to localhost as we are working on one system
    serverName = hostNameView.get()
    if serverName == "":
        stateLog.insert(tk.END, "Error: Cannot Send, Invalid Server IPA/Name\n")
        stateLog.yview(tk.END)
    else:
        stateLog.insert(tk.END, "Beginning to send image data...\n")
        stateLog.yview(tk.END)
        sequenceNumberInt = 0
        # The variable message is set to the pixel values of image.bmp
        with open("image1.bmp", "rb") as image:
            currentPacket = 0
            sendingMap = True
            while sendingMap:
                stateLog.insert(tk.END, "State " + str(sequenceNumberInt) + ": Waiting for call above\n")
                stateLog.yview(tk.END)
                stateMap = True
                # Parse though the image data to gather a message of only 1024 bytes
                message = image.read(1024)
                # Generate the checksum (int)
                checksumInt = generateChecksum(int.from_bytes(message, byteorder="little"), sequenceNumberInt, True)
                # Change the sequence number into a suitable bytes item for transport (1x2 bytes long)
                sequenceNumber = sequenceNumberInt.to_bytes(1, byteorder="little")
                # Change the integer checksum into a suitable bytes item for transport (4x2 bytes long)
                checksum = checksumInt.to_bytes(4, byteorder="little")
                # The packet is then prepared and sent via the client socket
                data = sequenceNumber + checksum + message
                while stateMap:
                    clientSocket.sendto(data, (serverName, serverPort))
                    stateLog.insert(tk.END, "State " + str(sequenceNumberInt) + ": Waiting for ACK " +
                                    str(sequenceNumberInt) + "\n")
                    stateLog.yview(tk.END)
                    output, serverAddress = clientSocket.recvfrom(buf)
                    packet = sortData(output)
                    # State Switcher 0->1->0
                    if packet["SN"] == sequenceNumberInt:  # Does this ACK carry the proper SN?
                        ackChecksum = generateChecksum(packet["ACK_Int"], packet["SN"], False)
                        if verifyChecksum(packet["Checksum"], ackChecksum):  # Is the checksum valid?
                            # Go on an send the next packet of data
                            stateMap = False
                            currentPacket += 1
                            # Break when message ends
                            if message == b'':
                                stateLog.insert(tk.END, "... Image finished sending\n")
                                stateLog.yview(tk.END)
                                sendingMap = False
                            sequenceNumberInt = sequenceSwitch(sequenceNumberInt)
                            # If all fail, then send the packet of data again, nothing in the sequence advances forward
    sendButton.configure(state=tk.ACTIVE)


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
    verify = bin(value ^ checksum)
    checker = (2 ** (len(verify) - 2)) - 1
    if int(verify, 2) == checker:
        return True
    return False


# Sort the incoming data into its component forms, and return a dictionary of this information
def sortData(data):
    dictionary = {}
    dictionary["SN"] = data[0]  # sequence number leads the data received (1x2 bytes long)
    dictionary["Checksum"] = int.from_bytes(data[1:4], byteorder="little")  # the checksum is before the message data
    # received (4x2 bytes long)
    dictionary["ACK"] = data[5:]  # message data received (1024 bytes long)
    dictionary["ACK_Int"] = int.from_bytes(data[5:], byteorder="little")  # converted ACK into an integer
    return dictionary


# Simple function call to switch the value of the SN
def sequenceSwitch(value):
    # Swap the sequence number between each case
    if value == 1:
        value = 0
    else:
        value = 1
    return value


# Creates a button to initiate the send and to show sending info
sendButton = tk.Button(rootView, text="Send Image", command=onClick)
sendButton.grid(column=0, row=8)

# Show the window GUI in the OS of the user
rootView.mainloop()
clientSocket.close()
