# File name: UDPClient.py
# Author: Sanskriti Sharma, John Lutz, Justice Graves
# Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 196/197

# import the socket module, the pillow module, the os module, and the tkinter module
import socket
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import os
import signal
import multiprocessing
import random
import datetime

# Creates a new window interface and labels it
rootView = tk.Tk()
rootView.title("Client Package")
rootView.geometry("525x500")

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

# Creates a label and a spinner object to choose the error level in the GUI
spinnerLabel = tk.Label(rootView, text="Choose data error percentage below:")
spinnerLabel.grid(column=0, row=16)
errorSpinner = tk.Spinbox(rootView, from_=0, to=99, width=5)
errorSpinner.grid(column=0, row=18)

# Creates a label and a spinner object to choose the loss level in the GUI
lossLabel = tk.Label(rootView, text="Choose data loss percentage below:")
lossLabel.grid(column=0, row=20)
lossSpinner = tk.Spinbox(rootView, from_=0, to=99, width=5)
lossSpinner.grid(column=0, row=22)

# Creates a state/message log in the GUI
stateLog = scrolledtext.ScrolledText(rootView, width=60, height=10)
stateLog.grid(column=0, row=24)
stateLog.insert(tk.END, "Client State Log:\n")

# Set-up for multiprocessing communication support
queue = multiprocessing.Queue()
process = 0

# Variable to hold the pathway for the image selected to be sent
imagePath = "image.bmp"

# Creates a label that shows the current image pathway selected
imageLabel = tk.Label(rootView, text="Selected Image Pathway: " + imagePath)
imageLabel.grid(column=0, row=10)


# Function serving as the point for the thread that will do the background work behind the GUI
def clientActivity(connection, name, pathWay, errorPercentage, lossPercentage):
    mailBox = connection
    # The UDP socket is created.
    # The UDP socket is created same as the client.
    # AF_INET indicates that the underlying network is using IPv4.
    # SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Server Port chosen arbitrarily
    serverPort = 12000
    # Buffer size set to 6000 bytes
    buf = 6000
    mailBox.put("Beginning to send image data...\n")
    sequenceNumberInt = 0
    # The variable message is set to the pixel values of image.bmp
    with open(pathWay, "rb") as image:
        clientMap = True
        initialTime = datetime.datetime.now()
        while clientMap:
            stateMap = True
            # Parse though the image data to gather a message of only 1024 bytes
            message = image.read(1024)
            # Generate the checksum (int)
            checksumInt = generateChecksum(int.from_bytes(message, byteorder="little"), sequenceNumberInt, True)
            # Change the sequence number into a suitable bytes item for transport (1x2 bytes long)
            sequenceNumber = sequenceNumberInt.to_bytes(1, byteorder="little")
            # Change the integer checksum into a suitable bytes item for transport (4x2 bytes long)
            checksum = checksumInt.to_bytes(4, byteorder="little")
            while stateMap:
                lossMap = True
                try:  # From the moment a new timer is started, make sure it can interrupt the current state
                    # Inject error into the outgoing message to the server
                    messageModed = injectError(message, errorPercentage)
                    # The packet is then prepared and sent via the client socket
                    data = sequenceNumber + checksum + messageModed
                    mailBox.put("State " + str(sequenceNumberInt) + ": Sending\n")
                    clientSocket.sendto(data, (name, serverPort))
                    # Start the timer (45ms callback feature)
                    signal.setitimer(signal.ITIMER_REAL, 0.45)
                    mailBox.put("State " + str(sequenceNumberInt) + ": Waiting for ACK " +
                                str(sequenceNumberInt) + "\n")
                    # Inject potential packet "loss" into the client system
                    while lossMap:
                        output, serverAddress = clientSocket.recvfrom(buf)
                        lossMap = injectLoss(lossPercentage)
                    # Stop the timer/alarm, as an ACK has been received
                    signal.alarm(0)
                    packet = sortData(output)
                    # Inject error into the incoming ACK
                    packet["ACK"] = injectError(packet["ACK"], errorPercentage)
                    packet["ACK_Int"] = int.from_bytes(packet["ACK"], byteorder="little")  # converted ACK into an integer
                    # State Switcher 0->1->0
                    if packet["SN"] == sequenceNumberInt:  # Does this ACK carry the proper SN?
                        ackChecksum = generateChecksum(packet["ACK_Int"], packet["SN"], False)
                        if verifyChecksum(packet["Checksum"], ackChecksum):  # Is the checksum valid?
                            stateMap = False
                            # Break when message ends
                            if message == b'':
                                finalTime = datetime.datetime.now()
                                mailBox.put("... Image finished sending\n")
                                clientMap = False
                            sequenceNumberInt = sequenceSwitch(sequenceNumberInt)
                except TypeError:
                        pass  # Go back, and send the old data again, after the timer is stopped
                        # If all fail, then send the packet of data again, nothing in the sequence advances forward
        finishTime = finalTime - initialTime
        mailBox.put("Finish time: " + str(finishTime) + "\n")
        clientSocket.close()


# "sendButton" click handler
def onClick():
    global sendButton
    global process
    sendButton.configure(state=tk.DISABLED)
    # Server name is set to localhost as we are working on one system
    serverName = hostNameView.get()
    if serverName == "":
        stateLog.insert(tk.END, "Error: Cannot Send, Invalid Server IPA/Name\n")
        stateLog.yview(tk.END)
        sendButton.configure(state=tk.ACTIVE)
    else:
        # Start multiprocessing the background activity of the server application
        signal.signal(signal.SIGALRM, clientActivity)  # child activity handles the alarm signal call
        process = multiprocessing.Process(target=clientActivity, args=(queue, serverName, imagePath,
                                                                       int(errorSpinner.get()), int(lossSpinner.get())))
        process.start()


# "selectButton" click handler (handles only BMP, PNG, JPG, or JPEG extensions for images
def onSelect():
    global selectButton
    global imagePath
    selectButton.configure(state=tk.DISABLED)
    try:
        filePath = filedialog.askopenfile(mode="r", initialdir=os.path.dirname(imagePath), filetypes=[("Image files",
                                                                                    "*.bmp *.png *.jpg *.jpeg")]).name
        if filePath is not None:
            imagePath = filePath
    except AttributeError:
        pass
    imageLabel.configure(text="Selected Image Pathway: " + imagePath)
    selectButton.configure(state=tk.ACTIVE)


# Generate the checksum for the given 1kB chunk of data and SN
def generateChecksum(data, sn, flag):
    a = sn
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
    dictionary["SN"] = data[0]  # sequence number leads the data received (1x2 bytes long)
    dictionary["Checksum"] = int.from_bytes(data[1:4], byteorder="little")  # the checksum is before the message data
    # received (4x2 bytes long)
    dictionary["ACK"] = data[5:]  # message data received (1024 bytes long)
    return dictionary


# Simple function call to switch the value of the SN
def sequenceSwitch(value):
    # Swap the sequence number between each case
    if value == 1:
        value = 0
    else:
        value = 1
    return value


# A simple function call that injects data bit error and Ack error into the system intentionally
# returns either the ack with error, or no error.
def injectError(information, error):
    if error > 99:
        error = 99
    randomInt = random.randrange(1, 100)
    if randomInt < error:
        injection = int.from_bytes(information, byteorder="little")
        injection = bin(injection)
        injection = int(injection.translate(str.maketrans("10", "01"))[2:], 2)
        information = injection.to_bytes(1024, byteorder="little")
    return information


# A simple function call that, using probability, determines if a received ack "exists" or not
# returns True, if the data is to be ignored, and False if the data is to be accepted
def injectLoss(loss):
    if loss > 99:
        loss = 99
    randomLoss = random.randrange(1, 100)
    if randomLoss < loss:
        return True
    return False

# Checks if there is a message in the queue to update the GUI with for the action log or picture updater
def collectUpdate():
    global process
    while not queue.empty():
        info = queue.get()
        stateLog.insert(tk.END, info)
        stateLog.yview(tk.END)
        if info == "... Image finished sending\n":
            sendButton.configure(state=tk.ACTIVE)
            process = 0
    rootView.after(100, collectUpdate)


# Creates a button to initiate the send and to show sending info
sendButton = tk.Button(rootView, text="Transfer Image", command=onClick)
sendButton.grid(column=0, row=12)

# Creates a button to open a filedialog from Tkinter to select a different image than the default
selectButton = tk.Button(rootView, text="Select Image", command=onSelect)
selectButton.grid(column=0, row=8)

rootView.after(100, collectUpdate())
# Show the window GUI in the OS of the user
rootView.mainloop()

if not process == 0:
    os.kill(process.pid, signal.SIGABRT)
