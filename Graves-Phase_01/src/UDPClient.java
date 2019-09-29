/******************************** UDPCLIENT.JAVA ***********************
 * Programmer: Justice J.H. Graves (ID# 01645187)
 * Date Finished: September 17th, 2019
 * References: Utilized the method for coding a UDP client as outlined in the document labeled "Sockets.pdf"
 * provided by Professor V. Vokkarane for EECE.4830 Network Design
 * Purpose: This program is the client that sends an image out to a server on a local network, and expects to receive
 * the same form of image information back from the server, and save that as a new file in the local project directory.
 * NOTICE: If it is not run AFTER the server begins execution, then the packet it transmits originally may be lost, and
 * it will need to be run again while the server operates continuously.
 */
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.*;

public class UDPClient
{
    public static void main(String args[]) throws Exception
    {
        // Write out a prompt to the user
        System.out.println("CLIENT SENDING IMAGE");

        // Retrieve a BMP file from the default directory of the system
        BufferedImage image = ImageIO.read(new File( "example.bmp"));
        ByteArrayOutputStream oStream = new ByteArrayOutputStream();
        ImageIO.write(image, "bmp", oStream);
        oStream.flush();

        // Set-up the client socket
        DatagramSocket cSocket = new DatagramSocket();

        // DNS translation of IP
        InetAddress IPAddress = InetAddress.getLocalHost();

        // Data Collection
            // BMP Collection
        byte[] sData = oStream.toByteArray();
        byte[] rData = new byte[sData.length];

        // Sending Image
        DatagramPacket sPacket = new DatagramPacket(sData, sData.length, IPAddress, 2001);
        cSocket.send(sPacket);

        // Receiving Image
        DatagramPacket rPacket = new DatagramPacket(rData, rData.length);
        cSocket.receive(rPacket);   // Client stalls at this point until a packet with its IP address is being sent
                                    // on the local network

        // Save return results
        System.out.println("SERVER IMAGE RECEIVED");
            // Render the data as a new image file to be saved
        ByteArrayInputStream iStream = new ByteArrayInputStream(rPacket.getData());
        BufferedImage new_image = ImageIO.read(iStream);
        ImageIO.write(new_image, "bmp", new File("example_c.bmp"));

        // Close the connection, and terminate the program, as it's single-use or single-run
        cSocket.close();
    }
}
