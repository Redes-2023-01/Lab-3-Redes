import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class LogUtils {
    private static final String DATE_FORMAT = "yyyy-MM-dd-HH-mm-ss";

    public static String getFormattedDate() {
        SimpleDateFormat sdf = new SimpleDateFormat(DATE_FORMAT);
        return sdf.format(new Date());
    }

    public static synchronized void writeLog(String fileName, String logMessage) {
        File logFile = new File(UDPUtils.LOGS_DIR, fileName);
        logFile.getParentFile().mkdirs();

        try (BufferedWriter bw = new BufferedWriter(new FileWriter(logFile, true))) {
            bw.write(logMessage);
            bw.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}