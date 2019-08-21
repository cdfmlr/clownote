package mine.java.tour;

import java.io.*;

public class SystemIn {
	// 使用 BufferedReader 在控制台读取字符
	public static void chrRead() throws IOException {
		// 用 System.in 创建 BufferedReader
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("输入字符，到'q'退出：");
		// 读取字符
		for (char character = '\0'; character != 'q'; ) {
			character = (char) br.read();
			System.out.println(character);
		}
	}

	// 使用 BufferedReader 在控制台读取字符串
	public static void strRead() throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("Please enter lines of text, 'end' to quit: ");
		// 读取字符串
		for (String line = "\0"; !line.equals("end"); ) {
			line = (String) br.readLine();
			System.out.println(line);
		}
	}

	public static void main(String[] args) throws IOException {
		chrRead();
		strRead();
	}
}

