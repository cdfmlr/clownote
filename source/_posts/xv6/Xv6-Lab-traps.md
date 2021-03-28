---
date: 2021-03-26 09:51:03.275144
tags: xv6
title: 6.S081 Xv6 Lab 4 traps
---
![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)

# Lab: traps

6.S081 的 Xv6 RISC-V **Lab traps**，实验内容：

- https://pdos.csail.mit.edu/6.S081/2020/labs/traps.html

```sh
$ git fetch
$ git checkout traps
$ make clean
```

## RISC-V assembly

这题没什么具体要做的，就看一看，跟着题目学一下 RISC- V 汇编。

## Backtrace

这题主要是实现打印函数栈。就是 GDB 里面 bt 的这种效果：

```gdb
(gdb) bt
#0  fork () at kernel/proc.c:260
#1  0x0000000080002c3c in sys_fork () at kernel/sysproc.c:29
#2  0x0000000080002bb0 in syscall () at kernel/syscall.c:140
#3  0x000000008000289a in usertrap () at kernel/trap.c:67
#4  0x0000000000000050 in ?? ()
```

### 关键代码

`kernel/riscv.h`: 实现一个获取当前 frame pointer 的方法：

```c
static inline uint64
r_fp()
{
	uint64 x;
	asm volatile("mv %0, s0" : "=r" (x) );
	return x;
}
```

`kernel/printf.c`: 打印 backtrace：

```c
void
backtrace(void)
{
	printf("backtrace:\n");
	uint64 fp = r_fp();
	while (PGROUNDDOWN(fp) < PGROUNDUP(fp)) {
		printf("%p\n", *(uint64*)(fp-8));
		fp = *(uint64*)(fp-16);
	}
}
```

### Diff

```diff
diff --git a/kernel/defs.h b/kernel/defs.h
index 4b9bbc0..137c786 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -80,6 +80,7 @@ int             pipewrite(struct pipe*, uint64, int);
 void            printf(char*, ...);
 void            panic(char*) __attribute__((noreturn));
 void            printfinit(void);
+void            backtrace(void);
 
 // proc.c
 int             cpuid(void);
diff --git a/kernel/printf.c b/kernel/printf.c
index e1347de..fbdeb68 100644
--- a/kernel/printf.c
+++ b/kernel/printf.c
@@ -121,6 +121,9 @@ panic(char *s)
   printf("panic: ");
   printf(s);
   printf("\n");
+
+  backtrace();
+
   panicked = 1; // freeze uart output from other CPUs
   for(;;)
     ;
@@ -132,3 +135,18 @@ printfinit(void)
   initlock(&pr.lock, "pr");
   pr.locking = 1;
 }
+
+// print a backtrace: 
+// a list of the function calls on the stack above 
+// the point at which the error occurred.
+void
+backtrace(void)
+{
+	printf("backtrace:\n");
+	uint64 fp = r_fp();
+	while (PGROUNDDOWN(fp) < PGROUNDUP(fp)) {
+		printf("%p\n", *(uint64*)(fp-8));
+		fp = *(uint64*)(fp-16);
+	}
+}
+
diff --git a/kernel/riscv.h b/kernel/riscv.h
index 0aec003..c95316e 100644
--- a/kernel/riscv.h
+++ b/kernel/riscv.h
@@ -319,6 +319,16 @@ sfence_vma()
   asm volatile("sfence.vma zero, zero");
 }
 
+// compiler stores the frame pointer of the currently
+// executing function in s0.
+// this function reads current frame pointer, namely s0
+static inline uint64
+r_fp()
+{
+	uint64 x;
+	asm volatile("mv %0, s0" : "=r" (x) );
+	return x;
+}
 
 #define PGSIZE 4096 // bytes per page
 #define PGSHIFT 12  // bits of offset within a page
diff --git a/kernel/sysproc.c b/kernel/sysproc.c
index e8bcda9..a520959 100644
--- a/kernel/sysproc.c
+++ b/kernel/sysproc.c
@@ -58,6 +58,8 @@ sys_sleep(void)
   int n;
   uint ticks0;
 
+  backtrace();
+
   if(argint(0, &n) < 0)
     return -1;
   acquire(&tickslock);
```



## Alarm

做一套系统调用，在用户进程每运行指定次数时钟后，调用该进程提供的一个 handler。

其实也不难，（我觉得比页表简单），跟着 hint 一步步做就行了。

###  关键实现

1. `kernel/proc.h`: 在 proc 结构体里添加需要的字段（间隔时长、已运行时长计数、处理函数地址(vm)、保存 alarm 前的寄存器）：

```c
struct proc {
  ...
  int alarm_interval;     // the alarm interval (ticks)
  int alarm_passed;       // how many ticks have passed since the last call
  uint64 alarm_handler;   // pointer to the alarm handler function
  struct trapframe etpfm; // trapframe to resume
}
```

2. 添加 `sys_sigalarm` 系统调用：接收参数，为进程设置 alarm 的间隔时长和处理函数。最终的实现在 `kernel/sysproc.c` （添加新系统调用的完整步骤见：[6.S081 Xv6 Lab 2: system calls](https://blog.csdn.net/u012419550/article/details/114286013)）:

```c
uint64
sys_sigalarm(void)
{
	int interval;
	uint64 handler;

	if(argint(0, &interval) < 0)
		return -1;

	if(argaddr(1, &handler) < 0)
		return -1;

	struct proc *p = myproc();

	p->alarm_interval = interval;
	p->alarm_handler = handler;

	return 0;
}
```

3. 在 `usertrap` （`kernel/trap.c`）中处理时钟中断时，如果进程需要 alarm 就保存当前 trapframe 到 etpfm，调用 handler （把 handler 地址放到 trapframe->epc，回到用户空间之后就会运行该函数）：

```c
void
usertrap(void)
{
  ...
  if(which_dev == 2) {
	// alarm
	if (p->alarm_interval) {
	  if (++p->alarm_passed == p->alarm_interval) {
		memmove(&(p->etpfm), p->trapframe, sizeof(struct trapframe));
		// return to alarm handler: call p->alarm_handler();
		p->trapframe->epc = p->alarm_handler;
	  }
	}
    yield();
  }
  ...
}
```

4. 实现  `sys_sigalarm` 系统调用，恢复 alarm 前的 trapframe（回到用户空间就会接着 alarm 之前的 PC 开始运行），把 alarm_passed 计数器置为零（允许下一次 alarm）：

```c
uint64
sys_sigreturn(void)
{
	struct proc *p = myproc();
	memmove(p->trapframe, &(p->etpfm), sizeof(struct trapframe));
	p->alarm_passed = 0;
	return 0;
}
```

### 某bug的sizeof

我做的时候不小心写了个 sizeof 的语法错误，找了半个小时呢。。。（这个问题超初学者的，，我对8起 K&R）

我一开始是这么写的：

```c
struct trapframe {...}

struct proc {
    ...
    struct trapframe *trapframe;
    struct trapframe etpfm;
}

void 
usertrap(void)
{
	...
    memmove(&(p->etpfm), p->trapframe, sizeof(p->trapframe));
    ...
}

uint64
sys_sigreturn(void)
{
	...
	memmove(p->trapframe, &(p->etpfm), sizeof(p->trapframe));
	...
}
```

解决：把 `sizeof(p->trapframe)` 改成 `sizeof(struct trapframe)`。


### Diff

emmm，上一题做完忘记 commit 了，所以下面这个 diff 也包含了上一题（backtrace）的：

```diff
diff --git a/Makefile b/Makefile
index 1fa367e..a74296b 100644
--- a/Makefile
+++ b/Makefile
@@ -175,6 +175,7 @@ UPROGS=\
 	$U/_grind\
 	$U/_wc\
 	$U/_zombie\
+	$U/_alarmtest\
 
 
 
diff --git a/grade-lab-traps b/grade-lab-traps
index 058e77b..8619bbe 100755
--- a/grade-lab-traps
+++ b/grade-lab-traps
@@ -60,7 +60,7 @@ def test_alarmtest_test2():
 def test_usertests():
     r.run_qemu(shell_script([
         'usertests'
-    ]), timeout=300)
+    ]), timeout=500)
     r.match('^ALL TESTS PASSED$')
 
 @test(1, "time")
diff --git a/kernel/defs.h b/kernel/defs.h
index 4b9bbc0..137c786 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -80,6 +80,7 @@ int             pipewrite(struct pipe*, uint64, int);
 void            printf(char*, ...);
 void            panic(char*) __attribute__((noreturn));
 void            printfinit(void);
+void            backtrace(void);
 
 // proc.c
 int             cpuid(void);
diff --git a/kernel/printf.c b/kernel/printf.c
index e1347de..fbdeb68 100644
--- a/kernel/printf.c
+++ b/kernel/printf.c
@@ -121,6 +121,9 @@ panic(char *s)
   printf("panic: ");
   printf(s);
   printf("\n");
+
+  backtrace();
+
   panicked = 1; // freeze uart output from other CPUs
   for(;;)
     ;
@@ -132,3 +135,18 @@ printfinit(void)
   initlock(&pr.lock, "pr");
   pr.locking = 1;
 }
+
+// print a backtrace: 
+// a list of the function calls on the stack above 
+// the point at which the error occurred.
+void
+backtrace(void)
+{
+	printf("backtrace:\n");
+	uint64 fp = r_fp();
+	while (PGROUNDDOWN(fp) < PGROUNDUP(fp)) {
+		printf("%p\n", *(uint64*)(fp-8));
+		fp = *(uint64*)(fp-16);
+	}
+}
+
diff --git a/kernel/proc.c b/kernel/proc.c
index dab1e1d..237fecb 100644
--- a/kernel/proc.c
+++ b/kernel/proc.c
@@ -127,6 +127,11 @@ found:
   p->context.ra = (uint64)forkret;
   p->context.sp = p->kstack + PGSIZE;
 
+  // Initialize alarm
+  p->alarm_interval = 0;
+  p->alarm_passed = 0;
+  p->alarm_handler = 0;
+
   return p;
 }
 
diff --git a/kernel/proc.h b/kernel/proc.h
index 9c16ea7..2dac44f 100644
--- a/kernel/proc.h
+++ b/kernel/proc.h
@@ -103,4 +103,9 @@ struct proc {
   struct file *ofile[NOFILE];  // Open files
   struct inode *cwd;           // Current directory
   char name[16];               // Process name (debugging)
+
+  int alarm_interval;          // the alarm interval (ticks)
+  int alarm_passed;            // how many ticks have passed since the last call
+  uint64 alarm_handler;        // pointer to the alarm handler function
+  struct trapframe etpfm;      // trapframe to resume, 啊, 不会xv6的动态内存分配，所以这里直接 hardcode 一个对象了。
 };
diff --git a/kernel/riscv.h b/kernel/riscv.h
index 0aec003..c95316e 100644
--- a/kernel/riscv.h
+++ b/kernel/riscv.h
@@ -319,6 +319,16 @@ sfence_vma()
   asm volatile("sfence.vma zero, zero");
 }
 
+// compiler stores the frame pointer of the currently
+// executing function in s0.
+// this function reads current frame pointer, namely s0
+static inline uint64
+r_fp()
+{
+	uint64 x;
+	asm volatile("mv %0, s0" : "=r" (x) );
+	return x;
+}
 
 #define PGSIZE 4096 // bytes per page
 #define PGSHIFT 12  // bits of offset within a page
diff --git a/kernel/syscall.c b/kernel/syscall.c
index c1b3670..eb079af 100644
--- a/kernel/syscall.c
+++ b/kernel/syscall.c
@@ -104,6 +104,8 @@ extern uint64 sys_unlink(void);
 extern uint64 sys_wait(void);
 extern uint64 sys_write(void);
 extern uint64 sys_uptime(void);
+extern uint64 sys_sigalarm(void);
+extern uint64 sys_sigreturn(void);
 
 static uint64 (*syscalls[])(void) = {
 [SYS_fork]    sys_fork,
@@ -127,6 +129,8 @@ static uint64 (*syscalls[])(void) = {
 [SYS_link]    sys_link,
 [SYS_mkdir]   sys_mkdir,
 [SYS_close]   sys_close,
+[SYS_sigalarm]  sys_sigalarm,
+[SYS_sigreturn] sys_sigreturn,
 };
 
 void
diff --git a/kernel/syscall.h b/kernel/syscall.h
index bc5f356..382d781 100644
--- a/kernel/syscall.h
+++ b/kernel/syscall.h
@@ -20,3 +20,5 @@
 #define SYS_link   19
 #define SYS_mkdir  20
 #define SYS_close  21
+#define SYS_sigalarm  22
+#define SYS_sigreturn 23
diff --git a/kernel/sysproc.c b/kernel/sysproc.c
index e8bcda9..5b64016 100644
--- a/kernel/sysproc.c
+++ b/kernel/sysproc.c
@@ -58,6 +58,8 @@ sys_sleep(void)
   int n;
   uint ticks0;
 
+  backtrace();
+
   if(argint(0, &n) < 0)
     return -1;
   acquire(&tickslock);
@@ -95,3 +97,32 @@ sys_uptime(void)
   release(&tickslock);
   return xticks;
 }
+
+uint64
+sys_sigalarm(void)
+{
+	int interval;
+	uint64 handler;
+
+	if(argint(0, &interval) < 0)
+		return -1;
+
+	if(argaddr(1, &handler) < 0)
+		return -1;
+
+	struct proc *p = myproc();
+
+	p->alarm_interval = interval;
+	p->alarm_handler = handler;
+
+	return 0;
+}
+
+uint64
+sys_sigreturn(void)
+{
+	struct proc *p = myproc();
+	memmove(p->trapframe, &(p->etpfm), sizeof(struct trapframe));
+	p->alarm_passed = 0;
+	return 0;
+}
diff --git a/kernel/trap.c b/kernel/trap.c
index a63249e..9f2a64b 100644
--- a/kernel/trap.c
+++ b/kernel/trap.c
@@ -77,8 +77,20 @@ usertrap(void)
     exit(-1);
 
   // give up the CPU if this is a timer interrupt.
-  if(which_dev == 2)
+  if(which_dev == 2) {
+	// alarm
+	if (p->alarm_interval /*&& p->alarm_handler*/) {  // handler addr might be 0
+	  if (++p->alarm_passed == p->alarm_interval) {
+		memmove(&(p->etpfm), p->trapframe, sizeof(struct trapframe));
+		// return to alarm handler: call p->alarm_handler();
+		p->trapframe->epc = p->alarm_handler;
+		// printf("[DEBUG] alarm: %s(%d), handler=%x\n", 
+		// 		p->name, p->pid, p->alarm_handler);
+		// p->alarm_passed = 0;  // sigreturn 时再恢复: prevent re-entrant calls to the handler
+	  }
+	}
     yield();
+  }
 
   usertrapret();
 }
diff --git a/user/alarmtest.c b/user/alarmtest.c
index 38f09ff..427c460 100644
--- a/user/alarmtest.c
+++ b/user/alarmtest.c
@@ -101,6 +101,7 @@ test1()
     // restored correctly, causing i or j or the address ofj
     // to get an incorrect value.
     printf("\ntest1 failed: foo() executed fewer times than it was called\n");
+	printf("\ti=%d, j=%d\n", i, j);
   } else {
     printf("test1 passed\n");
   }
diff --git a/user/user.h b/user/user.h
index b71ecda..57404e0 100644
--- a/user/user.h
+++ b/user/user.h
@@ -23,6 +23,8 @@ int getpid(void);
 char* sbrk(int);
 int sleep(int);
 int uptime(void);
+int sigalarm(int ticks, void (*handler)());
+int sigreturn(void);
 
 // ulib.c
 int stat(const char*, struct stat*);
diff --git a/user/usys.pl b/user/usys.pl
index 01e426e..fa548b0 100755
--- a/user/usys.pl
+++ b/user/usys.pl
@@ -36,3 +36,5 @@ entry("getpid");
 entry("sbrk");
 entry("sleep");
 entry("uptime");
+entry("sigalarm");
+entry("sigreturn");
```

## 实验结果

最后，`make grade` (我的机器上跑 usertests 巨慢，要改一下 timeout 才能通过。。):

```sh
== Test answers-traps.txt == answers-traps.txt: OK 
== Test backtrace test == 
$ make qemu-gdb
backtrace test: OK (4.7s) 
== Test running alarmtest == 
$ make qemu-gdb
(3.9s) 
== Test   alarmtest: test0 == 
  alarmtest: test0: OK 
== Test   alarmtest: test1 == 
  alarmtest: test1: OK 
== Test   alarmtest: test2 == 
  alarmtest: test2: OK 
== Test usertests == 
$ make qemu-gdb
usertests: OK (448.3s) 
    (Old xv6.out.usertests failure log removed)
== Test time == 
time: OK 
Score: 85/85
```


---

EOF

---

By CDFMLR 2020-03-28

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。