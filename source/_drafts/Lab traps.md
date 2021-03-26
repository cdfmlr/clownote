---
date: 2021-03-26 09:51:03.275144
title: Lab traps
---
# Lab: traps

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



