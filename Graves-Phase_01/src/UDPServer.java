/******************************** UDPSERVER.JAVA ***********************
 * Programmer: Justice J.H. Graves (ID# 01645187)
 * Date Finished: September 17th, 2019
 * References: Utilized the method for coding a UDP client as outlined in the document labeled "Sockets.pdf"
 * provided by Professor V. Vokkarane for EECE.4830 Network Design
 * Purpose: This program acts a server in a local network, expecting to take and save an image file in bmp format, and
 * then send the exact same data back to the client the original data packet came from.
 * NOTICE: It will not receive a packet of information from a client if it is starting to execute AFTER the client is
 * already executing. As this server runs in a loop, just restart the client program while keeping any iteration of
 * this server program in execution.
 */
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.*;

public class UDPServer
{
    public static void main(String args[]) throws Exception
    {
        // Create a new socket at port 2001
        DatagramSocket sSocket = new DatagramSocket(2001);

        // Initialize data variables
        byte[] rData = new byte[100000];
        byte[] sData;
        // Infinite While Loop
        // Continuously waits for data to be received from a client program
        while(true)
        {
            // Data Reception
            DatagramPacket rPacket = new DatagramPacket(rData, rData.length);
            sSocket.receive(rPacket);
                // Grab the IP and PORT of the sender
            InetAddress IPAddress = rPacket.getAddress();
            int PORT = rPacket.getPort();

            // Image Saving and Processing from reception (rPacket)
            ByteArrayInputStream iStream = new ByteArrayInputStream(rPacket.getData());
            BufferedImage image = ImageIO.read(iStream);
            ImageIO.write(image, "bmp", new File("example_s.bmp"));

            // Data Transfer -> Back to Client
                // Read back the saved file and prepare it's contents for transfer
            BufferedImage saved_image = ImageIO.read(new File("example_s.bmp"));
            ByteArrayOutputStream oStream = new ByteArrayOutputStream();
            ImageIO.write(saved_image, "bmp", oStream);
            oStream.flush();
            sData = oStream.toByteArray();
                // Send the data of the bmp file
            DatagramPacket sPacket = new DatagramPacket(sData, sData.length, IPAddress, PORT);
            sSocket.send(sPacket);
        }
    }
}
