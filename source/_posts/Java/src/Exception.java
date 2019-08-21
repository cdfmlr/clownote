package mine.java.tour;

import java.util.logging.Logger;

public class Exception {
	public static void main(String[] args) {
		Logger l = Logger.getLogger("Try-Catch-Finally");

		try {
			// Try to execute
			Integer foo = null;
			System.out.println("foo: " + foo.toString());
		} catch (RuntimeException e) {
			// Catch exception
			l.severe("Caught exception: " + e);
			System.out.println("catch");
		} finally {
			// Always executes
			System.out.println("finally");
		}
	}
}
