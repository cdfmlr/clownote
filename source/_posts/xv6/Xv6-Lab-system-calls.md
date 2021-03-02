---
date: 2021-03-02 15:10:33.762005
tags: xv6
title: Xv6 Lab system calls
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)


# Lab: system calls

> From: https://pdos.csail.mit.edu/6.S081/2020/labs/syscall.html


## 【NOTE】Add a new system call

To add a new system call, say, named `xxx`:

1. add a prototype for the system call to `user/user.h`
   ```c
   int xxx(int)
   ```
   
2. add a stub to `user/usys.pl`
   ```perl
   entry("xxx");
   ```
   
3. add a syscall number to `kernel/syscall.h`
   ```c
   #define SYS_xxx  22
   ```
   
4. add the new syscall into `kernel/syscall.c` 
   ```c
   extern uint64 sys_xxx(void);  // 1
   
   static uint64 (*syscalls[])(void) = {
   ...
   [SYS_xxx]   sys_xxx,          // 2
   };
   ```
   
5. add `sys_xxx` (a function takes void as argument and returns uint64) in`kernel/sysproc.c`. This function do fetch arguments about the system call and return values.

   ```c
   uint64 
   sys_xxx(void)
   {
   	// about arguments: the [xv6 book](https://pdos.csail.mit.edu/6.S081/2020/xv6/book-riscv-rev1.pdf) Sections 4.3 and 4.4 of Chapter 4
   }
   ```
   
6. implement the syscall somewhere in the kernel. (e.g. implement a `xxx` function , defines in `kernel/defs.h`, to do hard work)

## System call tracing

In this assignment you will add a system call tracing feature that may help you when debugging later labs. You'll create a new `trace` system call that will control tracing. It should take one argument, an integer "mask", whose bits specify which system calls to trace. For example, to trace the fork system call, a program calls `trace(1 << SYS_fork)`, where `SYS_fork` is a syscall number from `kernel/syscall.h`. You have to modify the xv6 kernel to print out a line when each system call is about to return, if the system call's number is set in the mask. The line should contain the process id, the name of the system call and the return value; you don't need to print the system call arguments. The `trace`system call should enable tracing for the process that calls it and any children that it subsequently forks, but should not affect other processes.

### Main implement

`kernel/sysproc.c`:

```c
...

// *
uint64
sys_trace(void)
{
	if (argint(0, &myproc()->tracemask) < 0)
		return -1;

	return 0;
}
```

`kernel/proc.h`:

```c
struct proc {
  struct spinlock lock;
  ...
  int pid;                     // Process ID
  ...
  int tracemask;               // trace mask  // *
};
```

`kernel/syscall.c`:

```c
...

extern uint64 sys_chdir(void);
extern uint64 sys_close(void);
...
extern uint64 sys_trace(void);  // *

static uint64 (*syscalls[])(void) = {
[SYS_fork]    sys_fork,
[SYS_exit]    sys_exit,
...
[SYS_trace]   sys_trace,  // *
};

char *syscallnames[] = {
[SYS_fork]    "fork",
[SYS_exit]    "exit",
...
[SYS_trace]   "trace",  // *
};

void
syscall(void)
{
  ...
  
  // trace  // *
  if (p->tracemask >> num) {
	  printf("%d: syscall %s -> %d\n", 
			  p->pid, syscallnames[num], p->trapframe->a0);
  }
}
```

### Detailed diff

```diff
diff --git a/Makefile b/Makefile
index f0beb51..1c07efd 100644
--- a/Makefile
+++ b/Makefile
@@ -149,6 +149,7 @@ UPROGS=\
 	$U/_grind\
 	$U/_wc\
 	$U/_zombie\
+	$U/_trace\
 
 
 
diff --git a/gradelib.pyc b/gradelib.pyc
new file mode 100644
index 0000000..d118849
Binary files /dev/null and b/gradelib.pyc differ
diff --git a/kernel/proc.c b/kernel/proc.c
index 6afafa1..73845e4 100644
--- a/kernel/proc.c
+++ b/kernel/proc.c
@@ -280,6 +280,9 @@ fork(void)
   // copy saved user registers.
   *(np->trapframe) = *(p->trapframe);
 
+  // copy trace mask
+  np->tracemask = p->tracemask;
+
   // Cause fork to return 0 in the child.
   np->trapframe->a0 = 0;
 
diff --git a/kernel/proc.h b/kernel/proc.h
index 9c16ea7..cf18b9b 100644
--- a/kernel/proc.h
+++ b/kernel/proc.h
@@ -103,4 +103,6 @@ struct proc {
   struct file *ofile[NOFILE];  // Open files
   struct inode *cwd;           // Current directory
   char name[16];               // Process name (debugging)
+
+  int tracemask;               // trace mask
 };
diff --git a/kernel/syscall.c b/kernel/syscall.c
index c1b3670..182ca99 100644
--- a/kernel/syscall.c
+++ b/kernel/syscall.c
@@ -104,6 +104,7 @@ extern uint64 sys_unlink(void);
 extern uint64 sys_wait(void);
 extern uint64 sys_write(void);
 extern uint64 sys_uptime(void);
+extern uint64 sys_trace(void);
 
 static uint64 (*syscalls[])(void) = {
 [SYS_fork]    sys_fork,
@@ -127,6 +128,32 @@ static uint64 (*syscalls[])(void) = {
 [SYS_link]    sys_link,
 [SYS_mkdir]   sys_mkdir,
 [SYS_close]   sys_close,
+[SYS_trace]   sys_trace,
+};
+
+char *syscallnames[] = {
+[SYS_fork]    "fork",
+[SYS_exit]    "exit",
+[SYS_wait]    "wait",
+[SYS_pipe]    "pipe",
+[SYS_read]    "read",
+[SYS_kill]    "kill",
+[SYS_exec]    "exec",
+[SYS_fstat]   "fstat",
+[SYS_chdir]   "chdir",
+[SYS_dup]     "dup",
+[SYS_getpid]  "getpid",
+[SYS_sbrk]    "sbrk",
+[SYS_sleep]   "sleep",
+[SYS_uptime]  "uptime",
+[SYS_open]    "open",
+[SYS_write]   "write",
+[SYS_mknod]   "mknod",
+[SYS_unlink]  "unlink",
+[SYS_link]    "link",
+[SYS_mkdir]   "mkdir",
+[SYS_close]   "close",
+[SYS_trace]   "trace",
 };
 
 void
@@ -143,4 +170,10 @@ syscall(void)
             p->pid, p->name, num);
     p->trapframe->a0 = -1;
   }
+  
+  // trace
+  if (p->tracemask >> num) {
+	  printf("%d: syscall %s -> %d\n", 
+			  p->pid, syscallnames[num], p->trapframe->a0);
+  }
 }
diff --git a/kernel/syscall.h b/kernel/syscall.h
index bc5f356..01004db 100644
--- a/kernel/syscall.h
+++ b/kernel/syscall.h
@@ -20,3 +20,5 @@
 #define SYS_link   19
 #define SYS_mkdir  20
 #define SYS_close  21
+
+#define SYS_trace  22
diff --git a/kernel/sysproc.c b/kernel/sysproc.c
index e8bcda9..7a078c0 100644
--- a/kernel/sysproc.c
+++ b/kernel/sysproc.c
@@ -95,3 +95,12 @@ sys_uptime(void)
   release(&tickslock);
   return xticks;
 }
+
+uint64
+sys_trace(void)
+{
+	if (argint(0, &myproc()->tracemask) < 0)
+		return -1;
+
+	return 0;
+}
diff --git a/user/user.h b/user/user.h
index b71ecda..774bb03 100644
--- a/user/user.h
+++ b/user/user.h
@@ -24,6 +24,8 @@ char* sbrk(int);
 int sleep(int);
 int uptime(void);
 
+int trace(int);
+
 // ulib.c
 int stat(const char*, struct stat*);
 char* strcpy(char*, const char*);
diff --git a/user/usys.pl b/user/usys.pl
index 01e426e..2e51985 100755
--- a/user/usys.pl
+++ b/user/usys.pl
@@ -36,3 +36,5 @@ entry("getpid");
 entry("sbrk");
 entry("sleep");
 entry("uptime");
+
+entry("trace");
```

## Sysinfo

In this assignment you will add a system call, `sysinfo`, that collects information about the running system. The system call takes one argument: a pointer to a `struct sysinfo` (see `kernel/sysinfo.h`). The kernel should fill out the fields of this struct: the `freemem` field should be set to the number of bytes of free memory, and the `nproc` field should be set to the number of processes whose `state` is not `UNUSED`. We provide a test program `sysinfotest`; you pass this assignment if it prints "sysinfotest: OK".

### Main implement

`kernel/sysproc.c`:

```c
uint64
sys_sysinfo(void)
{
  uint64 info; // user pointer to struct stat

  if(argaddr(0, &info) < 0)
    return -1;
  return systeminfo(info);
}
```

`kernel/sysinfo.c`:

```c
#include "types.h"
#include "riscv.h"
#include "param.h"
#include "spinlock.h"
#include "defs.h"
#include "sysinfo.h"
#include "proc.h"

// Get current system info
// addr is a user virtual address, pointing to a struct sysinfo.
int
systeminfo(uint64 addr) {
  struct proc *p = myproc();
  struct sysinfo info;

  info.freemem = freemem();
  info.nproc = nproc();

  if(copyout(p->pagetable, addr, (char *)&info, sizeof(info)) < 0)
    return -1;
  return 0;
}
```

`kernel/proc.c`:

```c
// Get the number of processes whose state is not UNUSED. 
int
nproc(void)
{
  int n = 0;
  struct proc *p;

  for(p = proc; p < &proc[NPROC]; p++) {
    acquire(&p->lock);
    if(p->state != UNUSED)
      ++n;
    release(&p->lock);
  }

  return n;
}
```

`kernel/kalloc.c`:

```c
// Get the number of bytes of free memory
int
freemem(void)
{
  int n = 0;
  struct run *r;
  acquire(&kmem.lock);
  
  for (r = kmem.freelist; r; r = r->next)
    ++n;

  release(&kmem.lock);

  return n * 4096;
}
```

### Detailed diff

```diff
diff --git a/Makefile b/Makefile
index 1c07efd..b626677 100644
--- a/Makefile
+++ b/Makefile
@@ -36,6 +36,7 @@ OBJS = \
   $K/kernelvec.o \
   $K/plic.o \
   $K/virtio_disk.o \
+  $K/sysinfo.o \
 
 ifeq ($(LAB),pgtbl)
 OBJS += $K/vmcopyin.o
@@ -150,6 +151,7 @@ UPROGS=\
 	$U/_wc\
 	$U/_zombie\
 	$U/_trace\
+	$U/_sysinfotest\
 
 
 
diff --git a/kernel/defs.h b/kernel/defs.h
index 4b9bbc0..7ebebb8 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -8,6 +8,7 @@ struct spinlock;
 struct sleeplock;
 struct stat;
 struct superblock;
+struct sysinfo;
 
 // bio.c
 void            binit(void);
@@ -63,6 +64,7 @@ void            ramdiskrw(struct buf*);
 void*           kalloc(void);
 void            kfree(void *);
 void            kinit(void);
+int             freemem(void);
 
 // log.c
 void            initlog(int, struct superblock*);
@@ -104,6 +106,7 @@ void            yield(void);
 int             either_copyout(int user_dst, uint64 dst, void *src, uint64 len);
 int             either_copyin(void *dst, int user_src, uint64 src, uint64 len);
 void            procdump(void);
+int             nproc(void);
 
 // swtch.S
 void            swtch(struct context*, struct context*);
@@ -183,5 +186,8 @@ void            virtio_disk_init(void);
 void            virtio_disk_rw(struct buf *, int);
 void            virtio_disk_intr(void);
 
+// sysinfo.c
+int             systeminfo(uint64);
+
 // number of elements in fixed-size array
 #define NELEM(x) (sizeof(x)/sizeof((x)[0]))
diff --git a/kernel/kalloc.c b/kernel/kalloc.c
index fa6a0ac..5051a1d 100644
--- a/kernel/kalloc.c
+++ b/kernel/kalloc.c
@@ -80,3 +80,19 @@ kalloc(void)
     memset((char*)r, 5, PGSIZE); // fill with junk
   return (void*)r;
 }
+
+// Get the number of bytes of free memory
+int
+freemem(void)
+{
+  int n = 0;
+  struct run *r;
+  acquire(&kmem.lock);
+  
+  for (r = kmem.freelist; r; r = r->next)
+    ++n;
+
+  release(&kmem.lock);
+
+  return n * 4096;
+}
diff --git a/kernel/proc.c b/kernel/proc.c
index 73845e4..73d2745 100644
--- a/kernel/proc.c
+++ b/kernel/proc.c
@@ -696,3 +696,20 @@ procdump(void)
     printf("\n");
   }
 }
+
+// Get the number of processes whose state is not UNUSED. 
+int
+nproc(void)
+{
+  int n = 0;
+  struct proc *p;
+
+  for(p = proc; p < &proc[NPROC]; p++) {
+    acquire(&p->lock);
+    if(p->state != UNUSED)
+      ++n;
+    release(&p->lock);
+  }
+
+  return n;
+}
diff --git a/kernel/syscall.c b/kernel/syscall.c
index 182ca99..fdf996d 100644
--- a/kernel/syscall.c
+++ b/kernel/syscall.c
@@ -105,6 +105,7 @@ extern uint64 sys_wait(void);
 extern uint64 sys_write(void);
 extern uint64 sys_uptime(void);
 extern uint64 sys_trace(void);
+extern uint64 sys_sysinfo(void);
 
 static uint64 (*syscalls[])(void) = {
 [SYS_fork]    sys_fork,
@@ -129,6 +130,7 @@ static uint64 (*syscalls[])(void) = {
 [SYS_mkdir]   sys_mkdir,
 [SYS_close]   sys_close,
 [SYS_trace]   sys_trace,
+[SYS_sysinfo] sys_sysinfo,
 };
 
 char *syscallnames[] = {
@@ -154,6 +156,7 @@ char *syscallnames[] = {
 [SYS_mkdir]   "mkdir",
 [SYS_close]   "close",
 [SYS_trace]   "trace",
+[SYS_sysinfo] "sysinfo",
 };
 
 void
diff --git a/kernel/syscall.h b/kernel/syscall.h
index 01004db..6716e88 100644
--- a/kernel/syscall.h
+++ b/kernel/syscall.h
@@ -22,3 +22,4 @@
 #define SYS_close  21
 
 #define SYS_trace  22
+#define SYS_sysinfo 23
diff --git a/kernel/sysinfo.c b/kernel/sysinfo.c
new file mode 100644
index 0000000..40bd08a
--- /dev/null
+++ b/kernel/sysinfo.c
@@ -0,0 +1,22 @@
+#include "types.h"
+#include "riscv.h"
+#include "param.h"
+#include "spinlock.h"
+#include "defs.h"
+#include "sysinfo.h"
+#include "proc.h"
+
+// Get current system info
+// addr is a user virtual address, pointing to a struct sysinfo.
+int
+systeminfo(uint64 addr) {
+  struct proc *p = myproc();
+  struct sysinfo info;
+
+  info.freemem = freemem();
+  info.nproc = nproc();
+
+  if(copyout(p->pagetable, addr, (char *)&info, sizeof(info)) < 0)
+    return -1;
+  return 0;
+}
diff --git a/kernel/sysproc.c b/kernel/sysproc.c
index 7a078c0..a1231d0 100644
--- a/kernel/sysproc.c
+++ b/kernel/sysproc.c
@@ -104,3 +104,13 @@ sys_trace(void)
 
 	return 0;
 }
+
+uint64
+sys_sysinfo(void)
+{
+  uint64 info; // user pointer to struct stat
+
+  if(argaddr(0, &info) < 0)
+    return -1;
+  return systeminfo(info);
+}
diff --git a/time.txt b/time.txt
new file mode 100644
index 0000000..0cfbf08
--- /dev/null
+++ b/time.txt
@@ -0,0 +1 @@
+2
diff --git a/user/user.h b/user/user.h
index 774bb03..708496d 100644
--- a/user/user.h
+++ b/user/user.h
@@ -1,5 +1,6 @@
 struct stat;
 struct rtcdate;
+struct sysinfo;
 
 // system calls
 int fork(void);
@@ -25,6 +26,7 @@ int sleep(int);
 int uptime(void);
 
 int trace(int);
+int sysinfo(struct sysinfo *);
 
 // ulib.c
 int stat(const char*, struct stat*);
diff --git a/user/usys.pl b/user/usys.pl
index 2e51985..fce5771 100755
--- a/user/usys.pl
+++ b/user/usys.pl
@@ -38,3 +38,4 @@ entry("sleep");
 entry("uptime");
 
 entry("trace");
+entry("sysinfo");
```

---
EOF

---

By CDFMLR 2020-03-02

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。