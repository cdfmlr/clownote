import java.util.logging.Logger;
import java.util.List;
import java.util.ArrayList;

class UsrList {	
	public static void main(String[] args) {
		Logger l = Logger.getLogger("Test");
		// 声明 List
		List<Integer> listOfIntegers = new ArrayList<>();
		l.info(listOfIntegers.toString());
		// 插入数据
		listOfIntegers.add(Integer.valueOf(238));
		l.info(listOfIntegers.toString());
		listOfIntegers.add(0, Integer.valueOf(987));
		l.info(listOfIntegers.toString());
		// 查看大小
		l.info("Current List size: " + listOfIntegers.size());
		// 获取元素
		l.info("Item at index 0 is: " + listOfIntegers.get(0));
		// 删除元素
		listOfIntegers.remove(0);
		l.info(listOfIntegers.toString());
	}
}

