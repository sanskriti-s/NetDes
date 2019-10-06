#File name: UDPClient.py
#Author: Sanskriti Sharma, John Lutz, Justice Graves
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 199

#import the socket module, the pillow module, io module, os module the tkinter module, multiprocessing module,
# and the signal module
import socket
from PIL import Image
import io
import os
import tkinter as tk
import multiprocessing
import signal

# Class serving as the point for the thread that will do the background work behind the GUI
class ServerThread(multiprocessing.Process):
	def __init__(self):							# function to initiate the class
		multiprocessing.Process.__init__(self)

	def run(self):								# the actual run of the background process
		# The server port and buffer are set to the same as the client
		serverPort = 12000
		buf = 5000
		# The UDP socket is created same as the client.
		# AF_INET indicates that the underlying network is using IPv4.
		# SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# The port number 12000 is bound to the server’s socket.
		serverSocket.bind(('', serverPort))

		# Deleting temporary files if they exists
		if os.path.exists("temp.bin"):
			os.remove("temp.bin")
		if os.path.exists("final.bmp"):
			os.remove("final.bmp")

		message = []
		# Enters an indefinite loop
		while True:
			receiveFile = True
			while receiveFile:
				# The message is recieved from the client and the client address is saved
				output, clientAddress = serverSocket.recvfrom(buf)
				message.append(output)
				if (output == b''):
					receiveFile = False

			# Write message to a file
			with open('temp.bin', 'ab+') as file:
				for n in range(len(message)):
					file.write(message[n])

			image = Image.open("temp.bin")
			image.show()
			# The image is converted to greyscale and saved to modifiedImage
			modifiedImage = image.convert('L')

			# The pixel values of the image are converted into a byte array
			imgByteArr = io.BytesIO()
			# modifiedImage.save(imgByteArr, format='BMP')
			modifiedImage.save('final.bmp')
			# the final message is sent to the client
			with open("final.bmp", "rb") as final:
				while True:
					finalMessage = final.read(4096)
					serverSocket.sendto(finalMessage, clientAddress)
					if (finalMessage == (b'')):
						break

	def kill(self):		# Function definition to kill the running process in a multiprocessing situation
		os.kill(self.pid, signal.SIGKILL)

# Creates a new window interface and labels it
rootView = tk.Tk()
rootView.title("Server Package")
rootView.geometry("400x400")

# Creates a top label giving the hostname and IP address of the server
serverHostname = socket.gethostname()  # acquires hostname of machine used to run server
hostNameLabel = tk.Label(rootView, text="Server hostname is: " + serverHostname)
hostNameLabel.grid(column=0, row=0)

serverIP = (socket.gethostbyname(serverHostname))
IPANameLabel = tk.Label(rootView, text="Server IPA is: " + serverIP)
IPANameLabel.grid(column=0, row=2)

# Additional instructions to tell the user what to put into the Client Package
infoLabel = tk.Label(rootView, text="Please enter the IPA of the above into the 'Client Package'")
infoLabel.grid(column=0, row=4)

# Start multiprocessing the background activity of the server application
process = ServerThread()
process.start()

# Show the window GUI in the OS of the user
rootView.mainloop()

# Kill the additional process running in the background
process.kill()
