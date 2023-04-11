import java.net.DatagramPacket;

public class UDPUtils {
    public static final int MAX_PACKET_SIZE = 8 * 1024;
    public static final int MAX_CONNECTIONS = 25;
    public static final String FILES_DIR = "Files";
    public static final String RECEIVED_FILES_DIR = "ArchivosRecibidos";
    public static final String LOGS_DIR = "Logs";
    public static final String FILE_END_MESSAGE = "FILE_END";

    public static boolean isFileEndMessage(DatagramPacket packet) {
        String message = new String(packet.getData(), 0, packet.getLength());
        return message.equals(FILE_END_MESSAGE);
    }
}
