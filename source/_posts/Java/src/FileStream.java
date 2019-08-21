package mine.java.tour;

import java.io.*;
import java.util.logging.Logger;

public class FileStream {
	private static Logger l = Logger.getLogger("Test");

	// 通过 byte 以二进制的形式读写文件
	public static void ioByByte() throws IOException {
		l.info("通过 byte 以二进制的形式读写文件:");
		try (
				OutputStream ostream = new FileOutputStream("test.txt");
				InputStream istream = new FileInputStream("test.txt");
				) {
			// 写入文件
			byte toBeWritten[] = {0x43, 0x44, 0x46, 0x4d, 0x4c, 0x52};
			for (int i : toBeWritten) {
				ostream.write(i);
			}
			// 从文件中读取
			int fileSize = istream.available();
			for (int i = 0; i < fileSize; i++) {
				System.out.print((char)istream.read());
			}
			System.out.print("\n");
		} catch (IOException e) {
			l.severe("IOException: " + e);
		}
	}
	// 读写中文(Unicode)
	public static void ioUnicode() throws IOException {
		l.info("读写中文(Unicode):");
		File fileForIO = new File("测试.txt");
		if (!fileForIO.exists()) {
			fileForIO.createNewFile();
		}
		// 写
		OutputStream ostream = new FileOutputStream(fileForIO);
		OutputStreamWriter writer = new OutputStreamWriter(ostream, "UTF-8");
		try {
			writer.append("中文");
			writer.append("\n");
			writer.append("English");
		} catch (IOException e) {
			l.severe("Fail to write: " + e);
		} finally {
			if (writer != null) writer.close();
			if (ostream != null) ostream.close();
		}
		// 读
		InputStream istream = new FileInputStream(fileForIO);
		InputStreamReader reader = new InputStreamReader(istream, "UTF-8");
		try {
			StringBuffer sb = new StringBuffer();	
			while (reader.ready()) {
				sb.append((char)reader.read());
			}
			String result = sb.toString();
			System.out.println(result);
		} catch (IOException e) {
			l.severe("Fail to read: " + e);
		} finally {
			if (reader != null) reader.close();
			if (istream != null) istream.close();
		}
	}

	public static void main(String[] args) throws IOException {
		ioByByte();
		ioUnicode();
	}
}

