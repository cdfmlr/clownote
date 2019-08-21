public class MultArr {
	public static void main(String[] args) {
		int a[][] = new int[2][3];
		for (int i = 0; i < a.length; i++) {
			for (int j = 0; j < a[i].length; j++) {
				a[i][j] = i*10 + j;
			}
		}
		for(int i[]: a) {
			for (int j: i) {
				System.out.println(j);
			}
		}
	}
}
