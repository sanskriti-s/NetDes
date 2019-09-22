Name: Sanskriti Sharma

Files submitted:

1.ReadMe.txt: Name of the team member, list the names of files submitted and their purpose, and steps required to set up and execute your program.

2.Design.docx: Describes purpose of each data type and provides a step-by-step execution of the code.

3.UDPClient.py: Source file with UDP Socket programming for Client with ability to convert image into bytes and transfer it over UDP network to server and later receive the altered image and convert the bytes back into a .bmp image.

4.UDPServer.py: Source file with UDP Socket programming for Server with ability to receive bytes, convert it into a.bmp image, convert it to greyscale and then convert image into back into bytes and send it to Client.

5.image.bmp: File to be transferred

Steps to execute program:

1.Have python3 working on system

2.Open two terminals

3.Change directory to the directory containing UDPServer.py, UDPClient.py and image.bmp in both terminals

4.In one terminal type 'python UDPServer.py'
The following text should appear: The server is ready to receive

5.In the second terminal type 'python UDPClient'
The image should appear in greyscale format in the same directory