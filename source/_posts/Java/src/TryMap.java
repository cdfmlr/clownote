import java.util.logging.Logger;
import java.util.Set;
import java.util.Map;
import java.util.HashMap;

public class TryMap {
	public static void main(String[] args) {
		Logger l = Logger.getLogger("Test");

		// 声明
		Map<String, Integer> mapOfIntegers = new HashMap<>();
		// 添加
		mapOfIntegers.put("168", Integer.valueOf(168));
		mapOfIntegers.put("233", Integer.valueOf(233));
		mapOfIntegers.put("666", Integer.valueOf(666));

		l.info("put something: " + mapOfIntegers);
		// 取值
		Integer oneHundered68 = mapOfIntegers.get("168");
		System.out.println(oneHundered68);
		// 删除
		mapOfIntegers.remove("233", Integer.valueOf(666));	// 注意这个key-value对应和 Map 中的不匹配的
		l.info("Try to remove {\"233\": 666}: " + mapOfIntegers.toString());

		mapOfIntegers.remove("233");
		l.info("Try to remove key of \"233\": " + mapOfIntegers.toString());

		// 遍历
		Set<String> keys = mapOfIntegers.keySet();
		for (String key : keys) {
			Integer value = mapOfIntegers.get(key);
			l.info("Value keyed by '" + key + "' is '" + value + "'.");
		}
	}
}
