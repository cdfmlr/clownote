import java.util.Arrays;

public class UseArrays {
	public static void main(String[] args) {
		int[] a = new int[5];
		int[] b = {9, 2, 1, 3, 7};

		// toString
		System.out.println(Arrays.toString(a));
		System.out.println(Arrays.toString(b));

		// fill
		Arrays.fill(a, 6);
		System.out.println(Arrays.toString(a));
		
		Arrays.fill(a, 2, 4, 8);
		System.out.println(Arrays.toString(a));

		// sort
		Arrays.sort(b, 1, 4);
		System.out.println(Arrays.toString(b));

		Arrays.sort(b);
		System.out.println(Arrays.toString(b));

		// equals
		System.out.println(
				Arrays.equals(a, a)
				);
		System.out.println(
				Arrays.equals(a, b)
				);

		// binarySearch
		System.out.println(
				Arrays.binarySearch(b, 3)
				);
		System.out.println(
				Arrays.binarySearch(b, 99)
				);
	}
}
