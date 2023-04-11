import java.io.*;
import java.net.*;
import java.util.Scanner;

public class UDPServer {
    public static void main(String[] args) throws IOException {
        try (DatagramSocket serverSocket = new DatagramSocket(9876)) {
            System.out.println("Servidor UDP iniciado en el puerto 9876.");

            File filesDir = new File(UDPUtils.FILES_DIR);
            File[] availableFiles = filesDir.listFiles();
            System.out.println("Archivos disponibles para enviar:");
            for (int i = 0; i < availableFiles.length; i++) {
                System.out.println((i + 1) + ". " + availableFiles[i].getName());
            }

            try (Scanner scanner = new Scanner(System.in)) {
                System.out.print("Ingrese el número del archivo que desea enviar: ");
                int fileIndex = scanner.nextInt() - 1;

                File fileToSend = availableFiles[fileIndex];
                byte[] fileData = new byte[(int) fileToSend.length()];
                FileInputStream fis = new FileInputStream(fileToSend);
                fis.read(fileData);
                fis.close();

                int numPackets = (int) Math.ceil((double) fileData.length / UDPUtils.MAX_PACKET_SIZE);
                System.out.println("Enviando " + fileToSend.getName() + " a los clientes conectados...");

                while (true) {
                    DatagramPacket receivedPacket = new DatagramPacket(new byte[UDPUtils.MAX_PACKET_SIZE], UDPUtils.MAX_PACKET_SIZE);
                    serverSocket.receive(receivedPacket);
                    InetAddress clientIPAddress = receivedPacket.getAddress();
                    int clientPort = receivedPacket.getPort();

                    for (int i = 0; i < numPackets; i++) {
                        int packetSize = Math.min(UDPUtils.MAX_PACKET_SIZE, fileData.length - i * UDPUtils.MAX_PACKET_SIZE);
                        DatagramPacket sendPacket = new DatagramPacket(fileData, i * UDPUtils.MAX_PACKET_SIZE, packetSize, clientIPAddress, clientPort);
                        serverSocket.send(sendPacket);
                    }

                    // Enviar mensaje de fin de archivo
                    byte[] endData = UDPUtils.FILE_END_MESSAGE.getBytes();
                    DatagramPacket endPacket = new DatagramPacket(endData, endData.length, clientIPAddress, clientPort);
                    serverSocket.send(endPacket);

                    // Registrar el tiempo de inicio de la transferencia
                    String logFileName = "server_log_" + LogUtils.getFormattedDate() + ".txt";
                    String startTime = LogUtils.getFormattedDate();
                    LogUtils.writeLog(logFileName, "Inicio de la transferencia a " + clientIPAddress + ":" + clientPort + " a las " + startTime);

                    // Registrar el nombre del archivo enviado y su tamaño
                    LogUtils.writeLog(logFileName, "Archivo enviado: " + fileToSend.getName() + " - Tamaño: " + fileToSend.length() + " bytes");

                    // Registrar el tiempo de finalización de la transferencia
                    String endTime = LogUtils.getFormattedDate();
                    LogUtils.writeLog(logFileName, "Fin de la transferencia a " + clientIPAddress + ":" + clientPort + " a las " + endTime);
                }
            }
        }
    }
}
