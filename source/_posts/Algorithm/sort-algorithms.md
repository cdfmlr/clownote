---
date: 2021-08-23 12:10:33.418216
title: 各种排序算法，用C语言实现
---
# Sort Algorithms

你心爱的各种排序算法，用 C 语言实现。

我们下面将要实现的算法，全部准循这个接口：

```c
// sort 对数组 A 的前 n 个元素进行原址排序
typedef void (*sort)(int A[], int n);
```

##  直接插入排序

遍历，往前找到合适的位置，逐个元素后移腾出空间，插入进去。

复杂度：
- 时间 $O(n^2)$
- 空间 $O(1)$

```c
void
insert_sort(int A[], int n)
{
    for (int i = 0; i < n; ++i) {
        int curr = A[i];

        int j = i - 1;
        while (j >= 0 && curr < A[j]) {
            A[j + 1] = A[j];
            --j;
        }

        A[j + 1] = curr;
    }
}
```

## 二分插入排序

就是直接插入里往前找合适位置那里用个二分查找。

复杂度：
- 时间：较好 $O(n \log(n))$，较坏 $O(n^2)$，平均 $O(n^2)$
- 空间 $O(1)$

```c
void
binary_insert_sort(int A[], int n)
{
    for (int i = 0; i < n; ++i) {
        int curr = A[i];

        // 二分查找
        int l = 0, r = i - 1;
        while (r >= 0 && l < i && l <= r) {
            int m = (l + r) / 2;
            if (curr < A[m]) {
                r = m - 1;
            } else {
                l = m + 1;
            }
        }
        // 后移
        for (int j = i - 1; j >= l; --j) {
            A[j + 1] = A[j];
        }
        // 插入
        A[l] = curr;
    }
}
```

## Shell 排序

递减增量(gap)的排序算法（非稳定）。就是分好几轮排序，每轮里在隔 gap 个的序列里调整插入。

空间复杂度是 $O(1)$，时间复杂度依赖于步长序列。

```c
void
shell_sort(int A[], int n)
{
    int gap;
    foreach_gaps(gap, n, {
        // 里面就是个插入排序:
        for (int i = gap; i < n; i++) {
            int curr = A[i];
            int j = i - gap;
            for (; j >= 0 && A[j] > curr; j -= gap) {
                A[j + gap] = A[j];
            }
            A[j + gap] = curr;
        }
    });
}
```

`foreach_gaps` 遍历增量序列，将步长值放到 gap 中。可以选用多种步长序列（注意步长最后一步务必为 1）：

- Shell 步长序列: $n/2^i$，最坏情况下时间复杂度 $O(n^2)$

    ```c
    #define for_shell_gap(gap, n, f)                                               \
        for (gap = n >> 1; gap > 0; gap >>= 1)                                     \
            f
    ```

- Papernov-Stasevich 步长序列：$2^k-1$，最坏情况下时间复杂度 $O(n^{\frac{3}{2}})$

    ```c
    // papernov_stasevich_start find the max n s.t. (2^k+1) < n
    // return 2^k+1
    static inline int
    ps_start(int n)
    {
        int k = 1, nn = n - 1;
        while (nn > 0 && nn != 1) {
            nn >>= 1;
            k <<= 1;
        }
        return k + 1;
    }
    
    // 2^k+1, ..., 65, 33, 17, 9, 5, 3, 1
    static inline int
    ps_next(int gap)
    {
        switch (gap) {
            case 1:
                return -1; // to stop
            case 3:
                return 1;
            default:
                return ((gap - 1) >> 1) + 1;
        }
    }
    
    #define for_papernov_stasevich_gap(gap, n, f)                                  \
        for (gap = ps_start(n); gap > 0; gap = ps_next(gap))                       \
            f;

还有很多种步长，这个 Papernov-Stasevich 也不是最好的。具体维基百科有介绍。

## 冒泡排序

从后向前形成序列（`i=n-1...1`）：每次从 0 检查至 i-1，后一个比前一个大的就交换一下：冒泡。

- 时间复杂度：最坏 $O(n^2)$，最好 $O(n)$
- 空间复杂度：$O(1)$

```c
void
bubble_sort(int A[], int n)
{
    for (int i = n - 1; i > 0; i--) {
        int swap_flag = 0;

        for (int j = 0; j < i; j++) {
            if (A[j] > A[j + 1]) {
                swap(A, j, j + 1);
                swap_flag = 1;
            }
        }

        if (!swap_flag) { // 这一轮都没交换，已经有序了，提前结束
            return;
        }
    }
}
```

其中的 swap 容易实现：

```c
// swap 原址交换数组 A 中下标 i 与 j 的值
static inline void
swap(int A[], int i, int j)
{
    if (i != j) {
        // 左 iji，右 jij
        A[i] ^= A[j];
        A[j] ^= A[i];
        A[i] ^= A[j];
    }
    
    // 注意一定要 判断 i != j 再执行，
    // 同一个内存地址用 xor swap 就会爆炸（结果全变成 0 ）：
    //   x = x ^ x   ->  x = 0
    //   x = x ^ x   ->  x = 0
    //   x = x ^ x   ->  x = 0
}
```

## 快速排序

对 `A[l...r]` (闭区间) 快速排序:

- 选个轴，序列中比轴小的放轴左边，比轴大的在其右边
- 然后把轴左右分别做两个子序列，递归。

复杂度：

-  时间复杂度：最好 $O(n\log(n))$，最坏 $O(n^2)$，平均 $O(n \log(n))$
- 空间复杂度 $O(log(n))$

```c
void
quick_sort(int A[], int l, int r)
{
    if (l < r) {
        int p = partition(A, l, r);
        quick_sort(A, l, p - 1);
        quick_sort(A, p + 1, r);
    }
}

// quick_sort_all 对整个长度为 n 的序列 A 执行快速排序
void
quick_sort_all(int A[], int n)
{
    return quick_sort(A, 0, n - 1);
}
```

其中，`partition` 做快排的交换工作：

- 以第一个元素 `A[l]` 为轴
- 序列中比轴小的放轴左边，比轴大的在其右边
- 返回轴的索引

这个写了两种实现，一种是 partition_place，一种是 partition_swap，无论是从好理解还是从方便记，我都喜欢后者：

```c
int
partition_place(int A[], int l, int r)
{
    int pv = A[l];
    while (l < r) {
        while (r > l && A[r] > pv)
            --r;
        if (l < r)
            A[l++] = A[r];
        while (l < r && A[l] < pv)
            ++l;
        if (l < r)
            A[r--] = A[l];
    }
    A[l] = pv;

    return l;
}
```

```c
int
partition_swap(int A[], int l, int r)
{
    int p = l;

    for (int i = l; i < r; i++) {
        if (A[i] <= A[r]) {
            swap(A, p, i);
            p++;
        }
    }
    swap(A, p, r);

    return p;
}
```

## 选择排序

从下标 0 到 n，每个位置 `i` 选择 `A[i...n]` （闭区间）里最小的一个放上去。

- 时间复杂度 $O(n^2)$
- 空间复杂度 $O(1)$

```c
void
select_sort(int A[], int n)
{
    for (int i = 0; i < n; i++) {
        int smallest = i;
        for (int j = i + 1; j < n; j++) {
            if (A[j] < A[smallest]) {
                smallest = j;
            }
        }
        swap(A, i, smallest);
    }
}

```

## 堆排序

把序列搞成个大根堆（根结点比页大的那种），然后依次出根节点，重新调整堆。

- 时间复杂度 $O(n \log(n))$
- 空间复杂度 $O(1)$

```c
void
heap_sort(int A[], int n)
{
    // 建立堆
    int heap_size = n;
    for (int i = n / 2 - 1; i >= 0; i--) {
        sift(A, i, n - 1);
    }
    // 调整堆，依次出根节点
    for (int i = n - 1; i >= 0; i--) {
        swap(A, 0, i);
        sift(A, 0, i - 1);
    }
}

// sift 调整，建堆
void
sift(int A[], int l, int r)
{
    int i = l, j = 2 * i + 1;
    int root = A[l];

    while (j <= r) {
        if (j + 1 <= r && A[j] < A[j + 1])
            ++j;
        if (A[j] > root) {
            A[i] = A[j];
            i = j;
            j = 2 * i + 1;
        } else {
            break;
        }
    }

    A[i] = root;
}
```

用 CLRS 里面的 maxHeapify，更容易理解：

```c
void
heap_sort(int A[], int n)
{
    // 建立堆
    for (int i = n / 2 - 1; i >= 0; i--) {
        max_heapify(A, i, n - 1);
    }

    // 依次出根节点，调整堆
    for (int i = n - 1; i >= 0; i--) {
        swap(A, 0, i);
        max_heapify(A, 0, i - 1);
    }
}

// max_heapify 建立大根堆的调整函数
void
max_heapify(int A[], int i, int n)
{
    // l, r are the children of root i
    int l = (i << 1) + 1;
    int r = l + 1;

    // max = max_idx(A[root], A[l], A[r])
    int max = i;
    if (l <= n && A[l] > A[max])
        max = l;
    if (r <= n && A[r] > A[max])
        max = r;

    // 更改根，继续向后调整
    if (max != i) {
        swap(A, i, max);
        max_heapify(A, max, n);
    }
}
```

## 归并排序

递归完成左右两半的排序，然后归并

- 时间复杂度 $O(n \log(n))$
- 空间复杂度 $O(n)$

```c
void
merge_sort(int A[], int l, int r)
{
    if (l >= r)
        return;

    int m = (l + r) / 2;
    merge_sort(A, l, m);
    merge_sort(A, m + 1, r);
    merge(A, l, m, r);
}

// merge_sort_all 对整个长度为 n 的序列 A 执行归并排序
void
merge_sort_all(int A[], int n)
{
    merge_sort(A, 0, n - 1);
}
```

归并：把数组的 `A[l: m+1]` 和 `A[m: r+1]` 两个已排序部分按升序合并：

- 先备份数组
- 顺序从左右两半中选出较小者，放入原数组
- 完成归并

需要辅助数组，空间复杂度 $O(n)$

```c
void
merge(int A[], int l, int m, int r)
{
    const int INF = 1 << 30;

    // 先备份左右两半切片：

    // b = A[l: m+1] + [INF]
    int n1 = (m - l + 1) + 1;
    int* b = malloc(sizeof(int) * n1);
    for (int i = 0, j = l; j <= m; i++, j++) {
        b[i] = A[j];
    }
    b[n1 - 1] = INF;

    // c = A[m: r+1] + [INF]
    int n2 = (r - m) + 1;
    int* c = malloc(sizeof(int) * n2);
    for (int i = 0, j = m + 1; j <= r; i++, j++) {
        c[i] = A[j];
    }
    c[n2 - 1] = INF;

    // 从左右切片里逐个取小的出来，凑成排序数组：
    int i = 0, j = 0;
    for (int k = l; k <= r; k++) {
        if (b[i] <= c[j]) {
            A[k] = b[i++];
        } else { // c[i] < b[i]
            A[k] = c[j++];
        }
    }
}
```

## 完整代码

完整代码整合在这个 gist 中：

- https://gist.github.com/cdfmlr/07b9b4880de4f3a457f1aa90eacb55ad

<script src="https://gist.github.com/cdfmlr/07b9b4880de4f3a457f1aa90eacb55ad.js"></script>

# 参考

- CLRS, 3e
- https://juejin.cn/post/6997172275787071518
- 天勤
- 王道
- 还有其他好多，忘了。。

---

大概就这样吧，我对排序算法什么的，没有多少热情，并不想写这篇文章的。算法测试用例写的也单一，所以并不保证正确，如有谬误，还望海涵。