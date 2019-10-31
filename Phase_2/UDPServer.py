#File name: UDPClient.py
#Author: Sanskriti Sharma, John Lutz, Justice Graves
#Based on code snippet from "Computer Networking: A Top-Down Approach by Kurose, Ross" pg 199

#import the socket, pillow, io, os, tkinter, multiprocessing and signal modules
import socket
from PIL import Image
import io
import os
import tkinter as tk
import multiprocessing
import signal
import math

# Class serving as the point for the thread that will do the background work behind the GUI
class ServerThread(multiprocessing.Process):
	def __init__(self): # function to initiate the class
		multiprocessing.Process.__init__(self)

	def run(self): # the actual run of the background process
		# The server port and buffer are set to the same as the client
		serverPort = 12000
		buf = 5000
		# The UDP socket is created same as the client.
		# AF_INET indicates that the underlying network is using IPv4.
		# SOCK_DGRAM means it is a UDP socket (rather than a TCP socket.)
		#serverSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
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
			receiveFile = True
			while receiveFile:
				# The message is received from the client and the client address is saved
				output, clientAddress = serverSocket.recvfrom(buf)
				serverIPA = self.intIP(serverHostname)
				# Check the output's checksum
				seq = int.from_bytes(output[0:1], byteorder="little")
				test = int.from_bytes(output[2:9], byteorder="little")
				checksum = self.generateChecksum(int.from_bytes(output[10:], byteorder="little"), serverIPA, serverPort,
												int.from_bytes(output[0:1], byteorder="little"), False)
				if self.verifyChecksum(int.from_bytes(output[2:9], byteorder="little"), checksum):
					message.append(output[10:])
					if output[10:] == b'':
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

	# Turn an IPv4 value into a integer value
	def intIP(self, address):
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
	def generateChecksum(self, data, ipa, port, sn, flag):
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
	def verifyChecksum(self, value, checksum):
		verify = bin(value ^ checksum)
		checker = (2 ** (len(verify) - 2)) - 1
		if int(verify, 2) == checker:
			return True
		return False

	def kill(self): # Function definition to kill the running process in a multiprocessing situation
		os.kill(self.pid, signal.SIGABRT)

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
infoLabel = tk.Label(rootView, text="Please enter the HostName or IPA of the above into the 'Client Package'")
infoLabel.grid(column=0, row=4)

# Start multiprocessing the background activity of the server application
process = ServerThread()
if __name__ == '__main__':
	process.start()

# Show the window GUI in the OS of the user
rootView.mainloop()

# Kill the additional process running in the background
process.kill()
