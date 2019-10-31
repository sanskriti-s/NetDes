﻿#File name: UDPClient.py
#Author: Sanskriti Sharma, John Lutz, Justice Graves
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 199

#import the socket, pillow, io, os, tkinter, multiprocessing and signal modules
import socket
from PIL import Image
import io
import os
import tkinter as tk
from tkinter import scrolledtext
import multiprocessing
import signal

# Creates a new window interface and labels it
rootView = tk.Tk()
rootView.title("Server Package")
rootView.geometry("525x400")

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


# Function serving as the point for the thread that will do the background work behind the GUI
def serverActivity(connection):
    QUEUE = connection
    # The server port and buffer are set to the same as the client
    serverPort = 12000
    buf = 6000
    # The UDP socket is created same as the client.
    # AF_INET indicates that the underlying network is using IPv4.
    # SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # The port number 12000 is bound to the servers socket.
    serverSocket.bind(('', serverPort))

    # Deleting temporary files if they exists
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
    if os.path.exists("final.bmp"):
        os.remove("final.bmp")

    message = []
    # Enters an indefinite loop
    while True:
        QUEUE.put("Prepared to receive image data...\n")
        receiveFile = True
        while receiveFile:
            # The message is received from the client and the client address is saved
            output, clientAddress = serverSocket.recvfrom(buf)
            packet = sortData(output)
            # Check the output's checksum
            checksum = generateChecksum(packet["Message_Int"], packet["SN"], False)
            if verifyChecksum(packet["Checksum"], checksum):
                message.append(packet["Message"])
                if packet["Message"] == b'':
                    receiveFile = False

        # Write message to a file
        with open('temp.bin', 'ab+') as file:
            for n in range(len(message)):
                file.write(message[n])

        image = Image.open("temp.bin")
        try:
            image.show()
            QUEUE.put("... Finished image transfer successfully\n")
            # The image is converted to greyscale and saved to modifiedImage
            modifiedImage = image.convert('L')
            # The pixel values of the image are converted into a byte array
            imgByteArr = io.BytesIO()
            # modifiedImage.save(imgByteArr, format='BMP')
            modifiedImage.save('final.bmp')
        except OSError:
            QUEUE.put("Error: Image transfer corrupted\n")


# Generate the checksum for the given 1kB chunk of data, and the given IPA, PORT, and SN
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
    dictionary["Message"] = data[5:]  # message data received (1024 bytes long)
    dictionary["Message_Int"] = int.from_bytes(data[5:], byteorder="little")  # converted message data into an integer
    return dictionary


def collectUpdate():
    while not queue.empty():
        stateLog.insert(tk.END, queue.get())
        stateLog.yview(tk.END)
    # Look for updates continuously from the other process (after 100ms) [prevents recursion]
    rootView.after(100, collectUpdate)


# Start multiprocessing the background activity of the server application
queue = multiprocessing.Queue()
process = multiprocessing.Process(target=serverActivity, args=(queue,))
if __name__ == '__main__':
    process.start()


# Look for updates continuously from the other process (after 100ms)
rootView.after(100, collectUpdate())
# Show the window GUI in the OS of the user
rootView.mainloop()

# Kill the additional process running in the background
os.kill(process.pid, signal.SIGABRT)
