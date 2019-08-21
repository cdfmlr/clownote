public class Static {
	public static void main(String[] args) {
		Example foo = new Example();
		Example bar = new Example();

		foo.staticVar = foo.normalVar = "foobar";
		/* 其实像上面这样写不好，会被编译器提醒改成：`staticVar = foo.normalVar = "foobar";` */

		System.out.println(foo.staticVar + "\t" + foo.normalVar);
		System.out.println(bar.staticVar + "\t" + bar.normalVar);
	}
}

class Example {
	static String staticVar = "Example";
	String normalVar = "Example";
}
