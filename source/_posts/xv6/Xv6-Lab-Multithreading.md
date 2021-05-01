---
date: 2021-04-27 16:12:22.007144
title: 6.S081 Xv6 Lab Multithreading
---


![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)




# 6.S081 Xv6 Lab: Multithreading

> Lab: Multithreading of MIT 6.S081 Fall 2020

```sh
$ git fetch
$ git checkout thread
$ make clean
```

## Uthread: switching between threads

这个题有意思的，手写用户线程的实现。做起来不难，大体框架人家都给了，自己只要实现一下上下文切换。

首先在 `notxv6/uthread.c` 里面补充定义一个「线程上下文」：

```c
// saved registers for thread context switches
struct threadcontext {
	uint64 ra;
	uint64 sp;
	// callee-saved
	uint64 s0;
	uint64 s1;
	uint64 s2;
	uint64 s3;
	uint64 s4;
	uint64 s5;
	uint64 s6;
	uint64 s7;
	uint64 s8;
	uint64 s9;
	uint64 s10;
	uint64 s11;
};
```

这个其实和 `kernel/proc.h` 里面的 `struct context` 是一样的，直接导进来用也行。

接下来在 `notxv6/uthread_switch.S` 中实现上下文的切换，直接抄 `kernel/swtch.S`:

```assembly
	.text

	/*   void 
	     thread_switch(struct threadcontext *old, struct threadcontext *new);

         * save the old thread's registers,
         * restore the new thread's registers.
         */

	.globl thread_switch
thread_switch:
	sd ra, 0(a0)
	sd sp, 8(a0)
	sd s0, 16(a0)
	sd s1, 24(a0)
	sd s2, 32(a0)
	sd s3, 40(a0)
	sd s4, 48(a0)
	sd s5, 56(a0)
	sd s6, 64(a0)
	sd s7, 72(a0)
	sd s8, 80(a0)
	sd s9, 88(a0)
	sd s10, 96(a0)
	sd s11, 104(a0)

	ld ra, 0(a1)
	ld sp, 8(a1)
	ld s0, 16(a1)
	ld s1, 24(a1)
	ld s2, 32(a1)
	ld s3, 40(a1)
	ld s4, 48(a1)
	ld s5, 56(a1)
	ld s6, 64(a1)
	ld s7, 72(a1)
	ld s8, 80(a1)
	ld s9, 88(a1)
	ld s10, 96(a1)
	ld s11, 104(a1)

	ret    /* return to ra */
```

接下来就用上下文、上下文切换来完成线程的切换。

在 `struct thread` 的定义里面加上一项 context:

```c
struct thread {
  ...
  struct threadcontext context;  /* switch here to run thread */
};
```

新建线程的时候要设置一下相关的 context：

- `ra` 寄存器指向线程要运行的函数，switch 结束后会返回到 ra 处开始运行；
- `sp` 指向线程自己的栈。要注意：压栈是减小栈指针，所以一开始在最高处。（参考 CSAPP2e 3.4.2 fig 3-5）

```c
void 
thread_create(void (*func)())
{
  struct thread *t;

  for (t = all_thread; t < all_thread + MAX_THREAD; t++) {
    if (t->state == FREE) break;
  }
  t->state = RUNNABLE;
  t->context.ra = (uint64)func;
  t->context.sp = (uint64)&t->stack[STACK_SIZE-1];
}
```

最后一步，在 `thread_schedule()` 里调用刚才汇编写的 `thread_switch`：

```c
void 
thread_schedule(void)
{
  struct thread *t, *next_thread;

  /* Find another runnable thread. */
  ...

  if (current_thread != next_thread) {  /* switch threads?  */
    next_thread->state = RUNNING;
    t = current_thread;
    current_thread = next_thread;
    /* Invoke thread_switch to switch from t to next_thread:
     */
	thread_switch(
        (uint64)&t->context, 
        (uint64)&next_thread->context
    );  // (+) 只需添加这个调用
  } else
    next_thread = 0;
}
```

Done.

## Using threads

这题不是在 Xv6 里写，要在真实的 Unix 系统里面，学用 pthread 的互斥锁：

```c
pthread_mutex_t lock;            // 声明一把锁
pthread_mutex_init(&lock, NULL); // 初始化锁
pthread_mutex_lock(&lock);       // 获取锁
pthread_mutex_unlock(&lock);     // 释放锁
```

具体的题目就是在 `notxv6/ph.c` 里面实现了个简单的哈希表，要把它改成线程安全的。加锁即可。

首先最基本的暴力实现，一把大锁，  `put()` 开始时取锁，返回前释放即可：

```c
pthread_mutex_t lock;

static
void put(int key, int value)
{
    pthread_mutex_lock(&lock);
    ...
    pthread_mutex_unlock(&lock);
}

int main(int argc, char *argv[])
{
    pthread_mutex_init(&lock, NULL);
    ...
}
```

> 注：这里获取锁（pthread_mutex_lock）可以移到找 key 的 for 循环后面，这样就可以快很多。但...

这个实现可以通过 make grade 的 ph_safe 测试，但过不了后面的 ph_fast 测试。

ph_fast 是要让多线程可以比单线程快。大锁的实现肯定是只会更慢，所以要把锁“改小”。这里咱谨遵 hint，每个桶一把锁：

```c
pthread_mutex_t locks[NBUCKET];

static 
void put(int key, int value)
{
  int i = key % NBUCKET;

  // is the key already present?
  struct entry *e = 0;
  for (e = table[i]; e != 0; e = e->next) {
    if (e->key == key) break;
  }
  pthread_mutex_lock(locks + i);  // (+)
  if(e){
    e->value = value;
  } else 
    insert(key, value, &table[i], table[i]);
  }
  pthread_mutex_unlock(locks + i);  // (+)
}

int main(int argc, char *argv[])
{
    for (int i = 0; i < NBUCKET; i++) {
        pthread_mutex_init(locks + i, NULL);
    }

    ...
}
```

## Barrier

这个题也是在真实的 Unix 系统里写，不在 Xv6。这题是学习 pthread 的条件等待：

```c
pthread_cond_wait(&cond, &mutex); // 在cond上睡, 释放mutex锁, 醒来时重新获取锁
pthread_cond_broadcast(&cond); // 唤醒所有在cond上睡着的线程
```

题目让实现一个 `Barrier`，“拦住”执行得快的线程，等所有线程都到了 Barrier 的这个点，再继续。

~~emmm，要去洗澡，没时间写思路了，直接上代码~~：

```c
static void 
barrier()
{
  // Block until all threads have called barrier() and
  // then increment bstate.round.

  pthread_mutex_lock(&bstate.barrier_mutex);
  if (++bstate.nthread < nthread) {
    pthread_cond_wait(&bstate.barrier_cond, &bstate.barrier_mutex);
  } else {
    bstate.nthread = 0;
    bstate.round++;
    pthread_cond_broadcast(&bstate.barrier_cond);
  }
  pthread_mutex_unlock(&bstate.barrier_mutex); 
}
```

## 实验结果

最后，贴上大家希望看到的满分截图：

![实验结果截屏](https://tva1.sinaimg.cn/large/008i3skNly1gq2rl0t012j30ki0d2dih.jpg)

---

2021.05.01  CDFMLR

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。