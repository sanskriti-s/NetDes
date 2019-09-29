Course Name:		Network Design
Course #:		EECE 4830-5830 - 201
Instructor:		Dr. Vinod Vokkarane
Student:		John Lutz
Semester:		Fall 2019
Project:		Phase 1 - UDP client server
Date Created:		10 Sep 2019
Date Due:		20 Sep 2019
Date Submitted:		20 Sep 2019

###   Readme Requirements   ###
	Name of the team member. List the names of files submitted and their purpose, and explain steps required to set up and execute your program.


@@@ NOTE: My name graphic below indicates the correct width to view this text file in. If the information below appears jumbled please resize your window.


*****************************************************************************
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
          __            __                    __                __        
         / /  ____     / /_     ____         / /      __  __   / /_   ____
    __  / /  / __ \   / __ \   / __ \       / /      / / / /  / __/  /_  /
   / /_/ /  / /_/ /  / / / /  / / / /      / /___   / /_/ /  / /_     / /_
   \____/   \____/  /_/ /_/  /_/ /_/      /_____/   \____/   \__/    /___/
                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*****************************************************************************


###   Overview   ###

	The server and client were written in Python 3.7 x64 using Microsoft (MS) Visual Studio (VS) 2019. They were tested using MS Windows 7 x64 and a virtual machine of the same OS.

	The host systems must have python installed to run the .py files. Pillow image handling was also used so you might need to install that as well.

	The Server and Client programs allow for the client to send a message or file to the server where the message will be capitalized, sent back and displayed or the image will be rotated, sent back and displayed.

	It was stated in class that the image file does not need to be as large as originally implied because the professor expected us to run into size transfer issues that will be solved in phase two of the project. As such the largest image file included for transfer is only 41 kB.


###   Included Program Files ###
	Basic_UDP_Server.py   Basic_UDP_Client.py


	A variety of file sizes are included. The programs will transfer all of these, but the smaller images are included in case the largest file will not transfer on your system possibly due to your network configuration being different than mine.

###   Included Transfer Test Image Files ###

      Name        Size   Purpose

     42.png       3 kB   To show capability to process a non .bmp format.
     42.bmp       3 kB	 File transfer test image.
   image32.bmp   21 kB   File transfer test image.
   image16.bmp   41 kB   File transfer test image.
 

###   Instructions ###

@@@ NOTE: These programs are NOT fault tolerant. If incorrect commands or typos are input then it is likely that they will crash. It is beyond the scope of this assignment to have full fault tolerance in this interface. This version will only send messages and small image files. It has only been tested with .png and .bmp images.


  ##  Bottom Line up Front  ##
		Run the files and follow the prompts.


  ##  Details  ##

	Ensure that the client and image files are in the same directory or you will have to enter the full path to the image in the client interface.

	The server can be run from the same folder or placed on a separate physical machine or virtual machine (VM) as long as they are on the same local network. In the case of a VM you may have to add a secondary host only network adapter in the VM settings. It is beyond the scope of this project to provide a detailed explanation on how to configure your VM.

	If the proper dependencies are installed on your system then all you need to do to run the client and server is to double click their respective files or whatever you normally do to run .py files.

	The windows will identify themselves as client and server. The server window will display the hostname and IP address of the machine or VM that it is running on. This information is necessary and will have to be entered into the client window at the prompt that requests that information.	Both the IP address method and the hostname method have been tested and work but you may find it easier to use the hostname. So far it works even on machines that have multiple IPs, alternatively you can use the IP option to force communication on a specific address.

	Once the server host information has been input into the client window the client will ask if you want to send a [M]essage or a [F]ile. Type m or f at the prompt, it is NOT case sensitive.

	Once you have chosen, if you are connected to the server, then it will indicate that it is waiting for your message or file. If you do not see a response from the server after you make your selection then you are NOTconnected to it and must remedy that situation.

	If you select [M]essage then the client will prompt you to input a message. After you input the message and press enter the server will display the message that you sent it. Internally it will capitalize the message and send it back. Then the client will display the original message that was capitalized by the server and the server will await your next choice.

	If you select [F]ile then the client will prompt you to input the name of a file to send. If you saved the images in the same folder as the client as you were instructed to do then type the name of the file followed by the extension, e.g. 42.bmp or image16.bmp etc.

	The server will indicate that it is waiting on image dimensions, display them once received, then indicate it is waiting on image data and then tell you that it will show you the image it received. It will then display the image that it received. Internally it will rotate the image and send it back to the client. The client interface will indicate that it is waiting for the modified (rotated) image. Once the client receives the new image it will display it.

	Regardless of which option you select first, upon completion of the cycle the client will ask you if you would like to continue. Enter y to continue (not case sensitive) if you want to send another message or image.

	If you input anything other than y the client will indicate that it is closing and the program will exit.

	The server must be closed manually.
