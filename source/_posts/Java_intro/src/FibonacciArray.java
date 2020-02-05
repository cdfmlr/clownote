public class FibonacciArray {
	public static void main(String[] args) {
		// 创建数组
		int size = 10;
		int[] fib = new int[10];

		// 填装数列
		fib[0] = 0;
		fib[1] = 1;
		for (int i = 2; i < size; i++) {
			fib[i] = fib[i-1] + fib[i-2];
		}

		// 输出
		for (int i = 1; i < size; i++) {
			System.out.println(fib[i]);
		}
	}
}
