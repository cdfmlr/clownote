package mine.java.tour;

import java.util.Scanner;

public class TryScanner {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		/*
		System.out.println("Please enter something:");
		for (String read = "\0"; scan.hasNext(); ) {
			read = scan.next();
			System.out.println(read);
		}
		*/
		System.out.println("Please enter some lines:");
		for (String read = "\0"; scan.hasNextLine(); ) {
			read = scan.nextLine();
			System.out.println(read);
		}
		scan.close();
	}
}
