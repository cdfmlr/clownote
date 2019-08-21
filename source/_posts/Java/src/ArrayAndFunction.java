public class ArrayAndFunction {
	public static int[] returnArray(int base) {
		int[] result = new int[10];
		for (int i = 0; i < result.length; i++) {
		   result[i] = base << i;
		}
		return result;
	}

	public static void printArray(int [] arr) {
		for (int i: arr) {
			System.out.print(i + ", ");
		}
		System.out.print("\n");
	}

	public static void main(String[] args) {
		for (String arg: args) {
			int base = Integer.parseInt(arg);
			int[] array = returnArray(base);
			printArray(array);
		}
	}
}
