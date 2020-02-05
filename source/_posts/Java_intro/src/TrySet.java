import java.util.Set;
import java.util.HashSet;
import java.util.logging.Logger;

public class TrySet {	
	public static void main(String[] arg) {
		Logger l = Logger.getLogger("Tset");

		Set<Integer> setOfIntegers = new HashSet<>();

		setOfIntegers.add(Integer.valueOf(12));
		setOfIntegers.add(Integer.valueOf(20));
		setOfIntegers.add(Integer.valueOf(5));
		
		setOfIntegers.add(Integer.valueOf(5));

		l.info(setOfIntegers.toString());

		setOfIntegers.remove(Integer.valueOf(20));

		l.info("" + setOfIntegers.size());

		for (Integer i : setOfIntegers) {
			i += 100;
			System.out.println(i);
		}
		l.info(setOfIntegers.toString());
	}
}

