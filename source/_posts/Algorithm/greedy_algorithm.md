---
title: 贪心算法
tags: Algorithm
---



# 贪心算法

> 这是篇很老的博客了，是我刚学贪心的时候写的笔记。今天无意间翻到，就分享一下。
>
> 内容没写多少，主要是看例子，这几个题都比较经典，都是当时我参考大佬的博客自己研究了写的（都是运行了测试过的，但时间长了，我不保证都对）。

### 算法描述
贪心选择是采用从顶向下（问题拆分）、以迭代的方法做出相继选择（循环处理拆分出的部分），每做一次贪心选择就将所求问题简化为一个规模更小的子问题（找出这个部分的贪心最优解）。

贪心算法追求的不是问题整体上的最优解，只是迭代找到各部分贪心较优解（最关注的那一项），并将循环结果作为较为满意的解（贪心算法的每一次操作都对结果产生直接影响）。

找到最优解要穷举所有可能，因此会消耗大量时间。而贪心算法常以每一个迭代的情况为基础做最优选择，而不考虑整体情况（贪心算法不需要回溯），因此可以快速找到较优解。

### 算法过程

* 建立数学模型来描述问题；
* 把求解的问题分成若干个子问题；
* 对每一子问题求解，得到子问题的局部最优解；
* 把子问题的解局部最优解合成原来解问题的一个解。

```python
fat = 问题
sub = 拆分(fat)
for a_part in sub:
    res.append(贪心最优解(a_part))
    
print("问题的较优解", res)
```

### 算法实例

1. 背包问题
*有一个背包，背包容量是M=150kg。有几个物品，。要求尽可能让装入背包中的物品总价值最大，但不能超过总容量。*

    （1）物品**不可以**分割成任意大小
这里以物体的价值与质量比作为标准，每次迭代都找比值较优的。
```cpp
//coding : c++ 11

#include <iostream>
#include <vector>
#include <algorithm>

#define MAX 7
#define WEIGHT_OF_BAG 150

using namespace std;

struct Node {
	char id;
	double weight;
	double value;
	double value_pre_weight;
	bool chosen;
};

int main()
{
	Node arr[MAX];

	double weights[MAX] = {35, 30, 60, 50, 40, 15, 20};
	double values[MAX]  = {10, 40, 30, 50, 35, 40, 30};
        /*拆分问题*/
	for (int i = 0; i < MAX; ++i) {
		arr[i].id = i;
		arr[i].weight = weights[i];
		arr[i].value = values[i];
		arr[i].value_pre_weight = values[i]/weights[i];
		arr[i].chosen = false;
	}

        /*寻求部分贪心最优解*/
	double total_weight = 0, total_value = 0;
	vector<Node> chosen_list;

	while (total_weight < WEIGHT_OF_BAG) {
		double greatest = 0.0;
		int choice = 0;

		for (int i = 0; i < MAX; ++i) {
			if (arr[i].chosen == false && total_weight + arr[i].weight <= 150 && arr[i].value_pre_weight >= greatest) {
				greatest = arr[i].value_pre_weight;
				choice = i;
			}
		}

		arr[choice].chosen = true;
		chosen_list.push_back(arr[choice]);
		total_weight += arr[choice].weight;
		total_value += arr[choice].value;
		greatest = arr[choice].value_pre_weight;
	}
        /*将结果循环作为问题的较优解*/
	cout << "Chosen:\n";
	for (auto item : chosen_list)
		cout << "\tThe " << int(item.id) << endl;

	cout	<< "Total weight:\t" << total_weight
		<< "\nTotal value:\t" << total_value
		<< endl;

	return 0;
}
```
   (2)物品**可以**分割成任意大小
   这里以物体质量为标准
   ```cpp
   #include <iostream>
#include <cstdio>

using namespace std;

const int N = 4;

void bag(double m, double *v, double *w, double *x);

int main()
{
	double maxWeight = 50;
	double wts[] = { 10,  30,  20,  5};
	double vls[] = {200, 400, 100, 10};
	double res[N] = {0};		// 记录装物品的比例

	bag(maxWeight, vls, wts, res);
	for (int i=0; i<N; ++i)
		printf("--[%d]: %lf\n", i, res[i]);

	return 0;
}

/* 寻找贪心最优解*/
void bag(double m, double *v, double *w, double *x)
{
	int i;
	for (i=0; i < N; ++i) {
		if (m - w[i] < 0)
			break;
		x[i] = 1.0;
		m -= w[i];
	}

	if (i < N)
		x[i] = m/w[i];
}

   ```

2. 换零钱问题
假设1元、2元、5元、10元、20元、50元、100元的纸币分别有c0, c1, c2, c3, c4, c5, c6张。现在要用这些钱来支付K元，至少要用多少张纸币？用贪心算法的思想，很显然，每一步尽可能用面值大的纸币即可。在日常生活中我们自然而然也是这么做的。在程序中已经事先将Value按照从小到大的顺序排好。

```cpp
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

struct Chosen {
	int value;
	int count;
};

const int N = 7;
int Count[N] = {3, 0, 2, 1, 0, 3, 5};
int Value[N] = {1, 2, 5, 10, 20, 50, 100};
vector<Chosen> got;

int solve(int money)
{
	int num = 0;
	for (int i = N - 1; i >= 0; i--) {
		int c = min(money/Value[i], Count[i]);
		money = money - c * Value[i];
		num += c;

		Chosen temp;
		temp.value = Value[i];
		temp.count = c;
		got.push_back(temp);
	}
	if (money > 0)
		num = -1;
	return num;
}

int main()
{
	int money;
	cout << "Enter money: ";
	cin >> money;

	int res = solve(money);
	if (res != -1) {
		cout << "\n共"<< res << " 张。"<< endl;
		for (auto i : got)
			printf("%2d个%2d元\t", i.count, i.value);
		cout << endl;
	}
	else
		cout << "\nCan't solve!" << endl;

	return 0;
}

```

3. 活动安排
有n个需要在同一天使用同一个教室的活动a1,a2,…,an，教室同一时刻只能由一个活动使用。每个活动ai都有一个开始时间si和结束时间fi 。一旦被选择后，活动ai就占据半开时间区间[si,fi)。如果[si,fi]和[sj,fj]互不重叠，ai和aj两个活动就可以被安排在这一天。该问题就是要安排这些活动使得尽量多的活动能不冲突的举行。例如下图所示的活动集合S，其中各项活动按照结束时间单调递增排序。

![屏幕快照 2020-03-25 16.02.45](https://tva1.sinaimg.cn/large/00831rSTgy1gd68gim7rwj30x808w0z0.jpg)

贪心策略应该是每次选取结束时间最早的活动。直观上也很好理解，按这种方法选择相容活动为未安排活动留下尽可能多的时间。这也是把各项活动按照结束时间单调递增排序的原因。
```cpp
#include <cstdio>
#include <iostream>
#include <algorithm>

using namespace std;

int N;

struct Action {
	int start;
	int end;
} act[100];

bool cmp(struct Action a, struct Action b)
{
	return a.end < b.end;
}

int greedy()
{
	int num = 0, i = 0;
	for (int j = 1; j <= N; j++) {
		if (act[j].start >= act[i].end) {
			i = j;
			printf("\t%2d : From %2d To %2d\n", i, act[i].start, act[i].end);
			num++;
		}
	}
	return num;
}

int main()
{
	int t;
	cout << "几组测试数据: ";
	scanf("%d", &t);
	while (t--) {
		cout << " 共几个活动: ";
		scanf("%d", &N);
		for (int i = 1; i <= N; i++) {
			cout << "活动" << i <<"的始末：";
			scanf("%d%d", &act[i].start, &act[i].end);
		}

		act[0].start = act[0].end = -1;
		sort(act + 1, act + N + 1, cmp);
		int res = greedy();
		cout << "共可安排："<< res << endl;
	}

	return 0;
}
```

4. 机器安排
n个作业组成的作业集，可由m台相同机器加工处理。要求给出一种作业调度方案，使所给的n个作业在尽可能短的时间内由m台机器加工处理完成。作业不能拆分成更小的子作业；每个作业均可在任何一台机器上加工处理。

首先将n个作业从大到小排序，然后依此顺序将作业分配给空闲的处理机。也就是说从剩下的作业中，选择需要处理时间最长的，然后依次选择处理时间次长的，直到所有的作业全部处理完毕，或者机器不能再处理其他作业为止。
```cpp
#include <iostream>
#include <algorithm>
#include <vector>

using Work = int;
using namespace std;

int main()
{
	int m=0, n=0;
	vector<Work> arr;

	cout << "machines: ";
	cin >> m;
	cout << "Works: ";
	cin >> n;

	vector<Work> mch(m, 0);

	for (int i = 0; i < n; ++i) {
		Work temp;
		printf("[%d].length: ", i);
		cin >> temp;
		arr.push_back(temp);
	}
	cout << "-----\n";
	sort(arr.begin(), arr.end(), [](auto x,auto y){return x > y;});

	for (int i = 0; i < n; ) {
		int flag = 1;
		while(flag) {
			for (int j = 0; j < m; ++j) {		// Check each machine
				if (mch[j] <= 0) {
					printf("Use (%d) to process [length_%d];\n", j, arr[i]);
					mch[j] = arr[i];
					i++;
					flag = 0;
				} 
				
			}
			int cnt = 0;
			for (auto &p : mch)
				p--;
		}
	}

	return 0;
}
```
