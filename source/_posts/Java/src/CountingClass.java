public class CountingClass {
	public static void main(String[] args) {
		Counter a = new Counter();
		Counter b = new Counter();
		Counter c = new Counter();

		System.out.println("Total Counters: " + a.total + " == " + b.total + " == " + c.total);
	}
}

class Counter { // 自计数类
	static int total = 0;

	public Counter() {
		total++;
		System.out.println("第 " + total + " 个 Counter 被构造。");
	}
}
