#File name: TCPServer.py
#Author: Sanskriti Sharma, John Lutz, Justice Graves
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 199

#import the socket, pillow, io, os, tkinter, multiprocessing and signal modules
import socket
from PIL import ImageTk, Image
import io
import os
import tkinter as tk
from tkinter import scrolledtext
import multiprocessing
import signal

# Creates a new window interface and labels it
rootView = tk.Tk()
rootView.title("Server Package")
rootView.geometry("675x800")

# Creates a top label giving the hostname and IP address of the server
serverHostname = socket.gethostname()  # acquires hostname of machine used to run server
hostNameLabel = tk.Label(rootView, text="Server hostname is: " + serverHostname)
hostNameLabel.grid(column=0, row=0)

serverIP = (socket.gethostbyname(serverHostname))
IPANameLabel = tk.Label(rootView, text="Server IPA is: " + serverIP)
IPANameLabel.grid(column=0, row=2)

# Additional instructions to tell the user what to put into the Client Package
infoLabel = tk.Label(rootView, text="Please enter the HostName or IPA of the above into the 'Client Package'")
infoLabel.grid(column=0, row=4)

# Creates a state/message log in the GUI
stateLog = scrolledtext.ScrolledText(rootView, width=60, height=10)
stateLog.grid(column=0, row=6)
stateLog.insert(tk.END, "Server State Log:\n")

# Creates an image label in the window to show as the image is loaded in the GUI
imageObject = ImageTk.PhotoImage(Image.open("Mamemon.jpeg"))
imageLabel = tk.Label(rootView, image=imageObject)
imageLabel.grid(column=0, row=8)


# Function serving as the point for the thread that will do the background work behind the GUI
def serverActivity(connection, relay):
    mailBox = connection
    pictureBox = relay
    buf = 1039
    # The server port is set to the same as what's within the client
    serverPort = 12000
    # The UDP socket is created same as the client.
    # AF_INET indicates that the underlying network is using IPv4.
    # SOCK_DGRAM means it is a UDP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # The port number 12000 is bound to the servers socket.
    serverSocket.bind(('', serverPort))
    ack = "ACK".encode("UTF-8")
    ackValue = int.from_bytes(ack, byteorder="little")
    connectionMap = True
    # Enters an indefinite loop
    while True:
        sequenceNumber = 0
        completeMap = False
        # Unset the FIN flag for the beginning of this process
        FIN = (0).to_bytes(2, byteorder="little")
        # Manually establish "TCP" connection
        while connectionMap:
            # Wait for a connection request
            output, clientAddress = serverSocket.recvfrom(buf)
            packet = sortData(output)
            # Check if the data is valid for the request
            ackChecksum = generateChecksum(packet["Message_Int"], packet["SN"], packet["Total_Collection"],
                                           packet["SYN"], packet["FIN"], False)
            if verifyChecksum(packet["Checksum"], ackChecksum):
                if packet["SYN"] == 1:
                    if packet["FIN"] == 0:
                        sequenceNumber = packet["SN"]
                        # Send the acknowledgement back
                        SYN = (1).to_bytes(2, byteorder="little")
                        sequenceValue = (sequenceNumber).to_bytes(3, byteorder="little")
                        checksum = generateChecksum(1, sequenceNumber, packet["Total_Collection"], 1, 0, True)\
                            .to_bytes(4, byteorder="little")
                        data = SYN + FIN + sequenceValue + checksum + (1).to_bytes(2, byteorder="little")
                        serverSocket.sendto(data, clientAddress)
                        connectionMap = False

        message = {}
        # Set the value the SYN value for the rest of the transmission
        SYN = (0).to_bytes(2, byteorder="little")
        # Complete the hand-shake, and take the first data being sent to the server
        output, clientAddress = serverSocket.recvfrom(buf)
        packet = sortData(output)
        checksum = generateChecksum(packet["Message_Int"], packet["SN"], packet["Total_Collection"],
                                        packet["SYN"], packet["FIN"], False)
        if verifyChecksum(packet["Checksum"], checksum):  # Does the checksum match up?
            if packet["SYN"] == 0:
                if packet["FIN"] == 0:
                    message[str(packet["SN"])] = packet["Message"]  # Send the data up to the application level
                    # Send an ACK that indicates that data was properly received
                    ackCheckInt = generateChecksum(int.from_bytes(ack, byteorder="little"), packet["SN"],
                                                   packet["Total_Collection"], 0, 0, True)
                    ackChecksum = ackCheckInt.to_bytes(4, byteorder="little")
                    switchback = SYN + FIN + packet["SN"].to_bytes(3, byteorder="little") + ackChecksum + ack
                    serverSocket.sendto(switchback, clientAddress)
                    mailBox.put("Connection Established\n")
                    mailBox.put("Prepared to receive image data...\n")
                    mailBox.put("State " + str(packet["SN"]) + ": Received\n")
            elif packet["SYN"] == 1:
                if packet["FIN"] == 0:
                    connectionMap = True    # The connection wasn't established, so go back and try again

        receiveFile = True
        while receiveFile:
            # The message is received from the client and the client address is saved
            output, clientAddress = serverSocket.recvfrom(buf)
            packet = sortData(output)
            # State Jumper
            # Check the output's checksum
            checksum = generateChecksum(packet["Message_Int"], packet["SN"], packet["Total_Collection"],
                                        packet["SYN"], packet["FIN"], False)
            if verifyChecksum(packet["Checksum"], checksum):  # Does the checksum match up?
                if packet["SYN"] == 0:
                    if packet["FIN"] == 0:
                        message[str(packet["SN"])] = packet["Message"]  # Send the data up to the application level
                        mailBox.put("State " + str(packet["SN"]) + ": Received\n")
                        # Send an ACK that indicates that data was properly received
                        ackCheckInt = generateChecksum(int.from_bytes(ack, byteorder="little"), packet["SN"],
                                                       packet["Total_Collection"], 0, 0, True)
                        ackChecksum = ackCheckInt.to_bytes(4, byteorder="little")
                        switchback = SYN + FIN + packet["SN"].to_bytes(3, byteorder="little") + ackChecksum + ack
                        serverSocket.sendto(switchback, clientAddress)
                        if len(message) >= packet["Total_Collection"]:
                            receiveFile = False
                            completeMap = True
                elif packet["SYN"] == 1:
                    if packet["FIN"] == 0:
                        receiveFile = False
                        connectionMap = True  # The connection wasn't established, so go back and try again

        if completeMap:
            # Order the message into a single variable
            try:
                orderedMessage = b""
                for x in range(sequenceNumber + 1, packet["Total_Collection"]):
                    orderedMessage += message[str(x)]
            except KeyError:
                pass  # In call cases, let this pass so the error message can be invoked

            pictureBox.put(orderedMessage)

            # Show the image file
            image = Image.open(io.BytesIO(orderedMessage))
            format = image.format

            # Deleting end-of-transfer saved files, if they exist
            if os.path.exists("final.BMP"):
                os.remove("final.BMP")
            if os.path.exists("final.PNG"):
                os.remove("final.PNG")
            if os.path.exists("final.JPG"):
                os.remove("final.JPG")
            if os.path.exists("final.JPEG"):
                os.remove("final.JPEG")

            try:
                mailBox.put("... Finished image transfer successfully\n")
                # The image is converted to greyscale and saved to modifiedImage
                modifiedImage = image.convert('L')
                # The pixel values of the image are converted into a byte array
                modifiedImage.save("final." + format)
            except OSError:
                mailBox.put("Error: Image transfer corrupted (Server Side)\n")

        # Connection Teardown
        FIN = (1).to_bytes(2, byteorder="little")
        sequenceNumber = 0
        teardownMapping = True
        while teardownMapping:
            # Send an ACK for a FIN request to the client
            output, clientAddress = serverSocket.recvfrom(buf)
            packet = sortData(output)
            checksum = generateChecksum(packet["Message_Int"], packet["SN"], packet["Total_Collection"],
                                        packet["SYN"], packet["FIN"], False)
            if verifyChecksum(packet["Checksum"], checksum):  # Does the checksum match up?
                if packet["SYN"] == 0:
                    if packet["FIN"] == 1:
                        # Send an acknowledgement back
                        sequenceValue = (sequenceNumber).to_bytes(3, byteorder="little")
                        checksum = generateChecksum(ackValue, sequenceNumber, packet["Total_Collection"], 0, 1, True) \
                            .to_bytes(4, byteorder="little")
                        data = SYN + FIN + sequenceValue + checksum + ack
                        serverSocket.sendto(data, clientAddress)
            mapping = True
            while mapping:
                # Send a FIN request to the client for an ACK
                sequenceValue = (0).to_bytes(3, byteorder="little")
                checksum = generateChecksum(ackValue, 0, packet["Total_Collection"], 0, 1, True) \
                    .to_bytes(4, byteorder="little")
                data = SYN + FIN + sequenceValue + checksum + ack
                serverSocket.sendto(data, clientAddress)
                output, clientAddress = serverSocket.recvfrom(buf)
                packet = sortData(output)
                checksum = generateChecksum(packet["Message_Int"], packet["SN"], packet["Total_Collection"],
                                            packet["SYN"], packet["FIN"], False)
                if verifyChecksum(packet["Checksum"], checksum):  # Does the checksum match up?
                    if packet["SYN"] == 0:
                        if packet["FIN"] == 1:
                                mapping = False
                                teardownMapping = False
        mailBox.put("Connection Closed\n")
        mailBox.put("----------------------------------------\n")


# Generate the checksum for the given 1kB chunk of data and the SN
def generateChecksum(data, sn, fSN, syn, fin, flag):
    a = sn + fSN + syn + fin
    d = bin(data)[2:]
    for x in range(0, 511):
        temp = a
        try:
            a += int(d[(16 * x): (15 + (16 * x))], 2)
            if a > 65535:
                a -= 65535
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
    dictionary["SYN"] = int.from_bytes(data[0:1], byteorder="little")  # SYN value for the connection process
    dictionary["FIN"] = int.from_bytes(data[2:3], byteorder="little")  # FIN value for connection teardown
    dictionary["SN"] = int.from_bytes(data[4:6], byteorder="little")
    dictionary["Total_Collection"] = int.from_bytes(data[7:10], byteorder="little")  # the total amount of packets
    # that are in the image collection (4x2 bytes long)
    dictionary["Checksum"] = int.from_bytes(data[11:14], byteorder="little")  # the checksum is before the message data
    # received (4x2 bytes long)
    dictionary["Message"] = data[15:]  # message data received (1024 bytes long)
    dictionary["Message_Int"] = int.from_bytes(data[15:], byteorder="little")  # converted message data into an integer
    return dictionary


# Checks if there is a message in the queue to update the GUI with for the action log or picture updater
def collectUpdate():
    global imageObject
    while (not queue.empty()) or (not imageQueue.empty()):
        if not queue.empty():
            stateLog.insert(tk.END, queue.get())
            stateLog.yview(tk.END)
        if not imageQueue.empty():
            try:
                imageObject = ImageTk.PhotoImage(Image.open(io.BytesIO(imageQueue.get())))
                imageLabel.config(image=imageObject)
            except OSError:
                pass
    # Look for updates continuously from the other process (after 100ms) [this type of callback prevents recursion]
    rootView.after(100, collectUpdate)


# Start multiprocessing the background activity of the server application
queue = multiprocessing.Queue()
imageQueue = multiprocessing.Queue()
process = multiprocessing.Process(target=serverActivity, args=(queue, imageQueue,))
if __name__ == '__main__':
    process.start()


# Look for updates continuously from the other process (after 100ms)
rootView.after(100, collectUpdate())
# Show the window GUI in the OS of the user
rootView.mainloop()

# Kill the additional processes running in the background
os.kill(process.pid, signal.SIGABRT)
