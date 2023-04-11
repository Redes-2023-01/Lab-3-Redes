import java.io.*;
import java.net.*;
import java.util.Scanner;

public class UDPClient {
    public static void main(String[] args) throws IOException {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Ingrese la cantidad de clientes que desea crear (hasta 25): ");
            int numClients = scanner.nextInt();

            for (int i = 1; i <= numClients; i++) {
                new Thread(new ClientRunnable(i)).start();
            }
        }
    }

    public static class ClientRunnable implements Runnable {
        private final int clientNumber;

        public ClientRunnable(int clientNumber) {
            this.clientNumber = clientNumber;
        }

        @Override
        public void run() {
            try {
                DatagramSocket clientSocket = new DatagramSocket();
                InetAddress serverIPAddress = InetAddress.getByName("192.168.10.6");

                byte[] sendData = new byte[UDPUtils.MAX_PACKET_SIZE];
                byte[] receiveData = new byte[UDPUtils.MAX_PACKET_SIZE];

                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverIPAddress, 9876);
                clientSocket.send(sendPacket);

                String receivedFileName = "client-" + clientNumber + "-Prueba-" + clientNumber + ".txt";
                File receivedFile = new File(UDPUtils.RECEIVED_FILES_DIR, receivedFileName);
                receivedFile.getParentFile().mkdirs();
                FileOutputStream fos = new FileOutputStream(receivedFile);

                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                while (true) {
                    clientSocket.receive(receivePacket);

                    if (UDPUtils.isFileEndMessage(receivePacket)) {
                        break;
                    }

                    fos.write(receivePacket.getData(), 0, receivePacket.getLength());
                }

                fos.close();
                clientSocket.close();

                System.out.println("Cliente " + clientNumber + " recibió el archivo: " + receivedFile.getAbsolutePath());

                // Registrar el tiempo de inicio de la transferencia
                String logFileName = "client_log_" + LogUtils.getFormattedDate() + ".txt";
                String startTime = LogUtils.getFormattedDate();
                LogUtils.writeLog(logFileName, "Inicio de la transferencia al cliente " + clientNumber + " a las " + startTime);

                // Registrar el nombre del archivo recibido y su tamaño
                LogUtils.writeLog(logFileName, "Archivo recibido: " + receivedFile.getName() + " - Tamaño: " + receivedFile.length() + " bytes");

                // Registrar el tiempo de finalización de la transferencia
                String endTime = LogUtils.getFormattedDate();
                LogUtils.writeLog(logFileName, "Fin de la transferencia al cliente " + clientNumber + " a las " + endTime);

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}