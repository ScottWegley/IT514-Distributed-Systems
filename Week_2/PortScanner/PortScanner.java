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
        int portsSinceLastPrint = 0;
        for (int port = 1; port <= 65535; port++) {
            try {
                portsSinceLastPrint++;
                if (portsSinceLastPrint == 1000) {
                    System.out.println("Scanned ports 1-" + port);
                    portsSinceLastPrint = 0;
                }
                Socket socket = new Socket();
                socket.connect(new InetSocketAddress(hostname, port), 500);
                socket.close();
                System.out.println("Port " + port + " is open");
            } catch (Exception e) {
            }
        }
    }
}