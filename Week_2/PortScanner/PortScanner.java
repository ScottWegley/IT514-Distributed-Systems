package Week_2.PortScanner;

import java.net.*;

class PortScanner {

    /**
     * Scans all ports on a given host and prints the open ports to the console.
     * 
     * @author Scott Wegley
     * @param args The hostname to scan.
     */
    public static void main(String[] args) {
        String hostname = args[0];
        System.out.println("Scanning ports on host: " + hostname);
        for (int port = 1; port <= 65535; port++) {
            try {
                Socket socket = new Socket();
                socket.connect(new InetSocketAddress(hostname, port), 1000);
                socket.close();
                System.out.println("Port " + port + " is open");
            } catch (Exception e) {
            }
        }
    }
}