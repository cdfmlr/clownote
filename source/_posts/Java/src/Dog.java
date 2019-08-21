public class Dog {
	String name;
	int age;

	void eat(String food) {
		System.out.println(name + " is eating " + food + ".");
	}

	public Dog() {
		name = "Dog";
		age = 0;

		System.out.println("构造()：");
		System.out.println(name + "\t" + age);
	}

	public Dog(String dogName, int dogAge) {
		name = dogName;
		age = dogAge;
		System.out.println("构造(name, age)：");
		System.out.println(name + "\t" + age);
	}

	public static void main(String[] args) {
		Dog Dog0 = new Dog();
		Dog Dog1 = new Dog("FooBar", 3);

		// 访问变量
		Dog0.name = "Ana";
		System.out.println(Dog0.name);

		// 访问方法
		Dog1.eat("cat");

	}
}
