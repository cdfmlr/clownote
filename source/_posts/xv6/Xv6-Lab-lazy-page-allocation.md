---
date: 2021-04-03 13:15:52.722759
tags: xv6
title: Xv6 Lab lazy page allocation
---


![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)



# Lab: xv6 lazy page allocation

> https://pdos.csail.mit.edu/6.S081/2020/labs/lazy.html
>
> 新的 2020 版哦。

```sh
$ git fetch
$ git checkout lazy
$ make clean
```

## Eliminate allocation from sbrk()

就是把 sys_sbrk 里的 growproc 调用删了，等用到的时候再去分配内存。如果是空间减小，要取消分配。

```c
uint64
sys_sbrk(void)
{
  int addr;
  int n;
  struct proc *p = myproc();  //(+)

  if(argint(0, &n) < 0)
    return -1;
  addr = p->sz;  // old sz
  p->sz += n;
  if (n < 0) {  // 空间减小: 取消分配
    uvmdealloc(p->pagetable, addr, p->sz);
  }
  return addr;
}
```

## Lazy allocation

在 `vm.c` 里面实现惰性分配（莫忘在 defs.h 中声明函数）：

```c
#include "spinlock.h" //(+)
#include "proc.h"     //(+)

// lazy allocation memory va for proc p: handle page-fault.
// return allocated memory (pa), 0 for failed 
uint64 lazyalloc(struct proc * p, uint64 va){
  if(va >= p->sz || va < PGROUNDUP(p->trapframe->sp)){
    return 0;
  }
  char * mem;
  uint64 a = PGROUNDDOWN(va);
  mem = kalloc();
  if(mem == 0){
    return 0;
  }
  memset(mem, 0, PGSIZE);  
    if(mappages(p->pagetable, a, PGSIZE, (uint64)mem, PTE_W|PTE_X|PTE_R|PTE_U) != 0){
      kfree(mem);
      return 0;
    }

  return (uint64)mem;
}
```

在 usertrap (`trap.c`) 里处理缺页错误，尝试惰性分配（掉上面写的那个函数，失败就杀掉进程）：

```c
void
usertrap(void)
{
  ...
  if(r_scause() == 8){
    // system call
    ...
  } else if((which_dev = devintr()) != 0){
    // ok
  } else if((r_scause() == 13) || (r_scause() == 15)){  // page fault: (+)
  if (lazyalloc(myproc(), r_stval()) <= 0) {
    p->killed = 1;
  }
  } else {
    ...
  }
  ...
}
```

最后改一点点细节，把各种缺页会爆出的 panic 干掉（vm.c里）。以前这些情况正常是不会发生的，但现在惰性分配会带来缺页，所以要告诉操作系统遇到这些事情时 don't panic，继续往下跑就行了：

```c
// vm.c
...

//(+)这个我懒得改结构就goto了，但你应该去改if结构，而不是goto
uint64
walkaddr(pagetable_t pagetable, uint64 va)
{
  ...

  if(pte == 0)
    goto lzac;
  if((*pte & PTE_V) == 0)
    goto lzac;
  if((*pte & PTE_U) == 0)
    goto lzac;
  pa = PTE2PA(*pte);
 
  if (0) {
lzac:
    if ((pa = lazyalloc(myproc(), va)) <= 0)
      pa = 0;
  }
  
  return pa;
}

int
mappages(pagetable_t pagetable, uint64 va, uint64 size, uint64 pa, int perm)
{
  ...
  for(;;){
    ...
    if(*pte & PTE_V)
      // panic("remap");
      ;
    ...
}

void
uvmunmap(pagetable_t pagetable, uint64 va, uint64 npages, int do_free)
{
  ...
  for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
    if((pte = walk(pagetable, a, 0)) == 0) {
      // panic("uvmunmap: walk");
      continue;
    }
    if((*pte & PTE_V) == 0) {
      // panic("uvmunmap: not mapped");
      continue;
    }
    ...
  }
}
    
int
uvmcopy(pagetable_t old, pagetable_t new, uint64 sz)
{
  ...
  for(i = 0; i < sz; i += PGSIZE){
    if((pte = walk(old, i, 0)) == 0){
      // panic("uvmcopy: pte should exist");
      continue;
    }
    if((*pte & PTE_V) == 0){
      // panic("uvmcopy: page not present");
      continue;
    }
    ...
  }
  ...
}
```

## 测试

写的时候可以按题目跑这些测试：

```sh
xv6-labs-2020 $ make qemu
$ echo hi
$ lazytests
$ usertests
```

## diff

详细的 git diff (可以用来做 patch 喔):

```diff
diff --git a/kernel/defs.h b/kernel/defs.h
index 4b9bbc0..7ff16c4 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -171,6 +171,7 @@ uint64          walkaddr(pagetable_t, uint64);
 int             copyout(pagetable_t, uint64, char *, uint64);
 int             copyin(pagetable_t, char *, uint64, uint64);
 int             copyinstr(pagetable_t, char *, uint64, uint64);
+uint64          lazyalloc(struct proc * p, uint64 va);
 
 // plic.c
 void            plicinit(void);
diff --git a/kernel/sysproc.c b/kernel/sysproc.c
index e8bcda9..b799722 100644
--- a/kernel/sysproc.c
+++ b/kernel/sysproc.c
@@ -43,12 +43,15 @@ sys_sbrk(void)
 {
   int addr;
   int n;
+  struct proc *p = myproc();
 
   if(argint(0, &n) < 0)
     return -1;
-  addr = myproc()->sz;
-  if(growproc(n) < 0)
-    return -1;
+  addr = p->sz;  // old sz
+  p->sz += n;
+  if (n < 0) {
+    uvmdealloc(p->pagetable, addr, p->sz);
+  }
   return addr;
 }
 
diff --git a/kernel/trap.c b/kernel/trap.c
index a63249e..fc08231 100644
--- a/kernel/trap.c
+++ b/kernel/trap.c
@@ -67,6 +67,11 @@ usertrap(void)
     syscall();
   } else if((which_dev = devintr()) != 0){
     // ok
+  } else if((r_scause() == 13) || (r_scause() == 15)){  // page fault
+	// lazy allocation
+	if (lazyalloc(myproc(), r_stval()) <= 0) {
+	  p->killed = 1;
+	}
   } else {
     printf("usertrap(): unexpected scause %p pid=%d\n", r_scause(), p->pid);
     printf("            sepc=%p stval=%p\n", r_sepc(), r_stval());
diff --git a/kernel/vm.c b/kernel/vm.c
index bccb405..f3235c3 100644
--- a/kernel/vm.c
+++ b/kernel/vm.c
@@ -5,6 +5,8 @@
 #include "riscv.h"
 #include "defs.h"
 #include "fs.h"
+#include "spinlock.h"
+#include "proc.h"
 
 /*
  * the kernel's page table.
@@ -102,12 +104,19 @@ walkaddr(pagetable_t pagetable, uint64 va)
 
   pte = walk(pagetable, va, 0);
   if(pte == 0)
-    return 0;
+	goto lzac;
   if((*pte & PTE_V) == 0)
-    return 0;
+    goto lzac;
   if((*pte & PTE_U) == 0)
-    return 0;
+    goto lzac;
   pa = PTE2PA(*pte);
+ 
+  if (0) {
+lzac:
+	  if ((pa = lazyalloc(myproc(), va)) <= 0)
+		pa = 0;
+  }
+  
   return pa;
 }
 
@@ -157,7 +166,8 @@ mappages(pagetable_t pagetable, uint64 va, uint64 size, uint64 pa, int perm)
     if((pte = walk(pagetable, a, 1)) == 0)
       return -1;
     if(*pte & PTE_V)
-      panic("remap");
+      // panic("remap");
+	  ;
     *pte = PA2PTE(pa) | perm | PTE_V;
     if(a == last)
       break;
@@ -180,10 +190,14 @@ uvmunmap(pagetable_t pagetable, uint64 va, uint64 npages, int do_free)
     panic("uvmunmap: not aligned");
 
   for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
-    if((pte = walk(pagetable, a, 0)) == 0)
-      panic("uvmunmap: walk");
-    if((*pte & PTE_V) == 0)
-      panic("uvmunmap: not mapped");
+    if((pte = walk(pagetable, a, 0)) == 0) {
+      // panic("uvmunmap: walk");
+	  continue;
+	}
+    if((*pte & PTE_V) == 0) {
+      // panic("uvmunmap: not mapped");
+	  continue;
+	}
     if(PTE_FLAGS(*pte) == PTE_V)
       panic("uvmunmap: not a leaf");
     if(do_free){
@@ -314,10 +328,14 @@ uvmcopy(pagetable_t old, pagetable_t new, uint64 sz)
   char *mem;
 
   for(i = 0; i < sz; i += PGSIZE){
-    if((pte = walk(old, i, 0)) == 0)
-      panic("uvmcopy: pte should exist");
-    if((*pte & PTE_V) == 0)
-      panic("uvmcopy: page not present");
+    if((pte = walk(old, i, 0)) == 0){
+      // panic("uvmcopy: pte should exist");
+	  continue;
+	}
+    if((*pte & PTE_V) == 0){
+      // panic("uvmcopy: page not present");
+	  continue;
+	}
     pa = PTE2PA(*pte);
     flags = PTE_FLAGS(*pte);
     if((mem = kalloc()) == 0)
@@ -440,3 +458,40 @@ copyinstr(pagetable_t pagetable, char *dst, uint64 srcva, uint64 max)
     return -1;
   }
 }
+
+
+// lazy allocation memory va for proc p: handle page-fault.
+// return allocated memory (pa), 0 for failed 
+uint64 lazyalloc(struct proc * p, uint64 va){
+#define lazyalloc_debug 0
+#define lazyalloc_warn(info) { \
+	  printf("lazyalloc(): %s", info); \
+      printf("             scause %p pid=%d\n", r_scause(), p->pid); \
+      printf("             sepc=%p stval=%p\n", r_sepc(), r_stval()); \
+}
+	if(va >= p->sz || va < PGROUNDUP(p->trapframe->sp)){
+	  #if lazyalloc_debug
+	    lazyalloc_warn("vm addr higher then any allocated with sbrk\n");
+      #endif
+	  return 0;
+	}
+	char * mem;
+	uint64 a = PGROUNDDOWN(va);
+	mem = kalloc();
+	if(mem == 0){
+	  #if lazyalloc_debug
+	    lazyalloc_warn("kalloc() == 0\n");
+      #endif
+	  return 0;
+	}
+	memset(mem, 0, PGSIZE);  
+    if(mappages(p->pagetable, a, PGSIZE, (uint64)mem, PTE_W|PTE_X|PTE_R|PTE_U) != 0){
+	  #if lazyalloc_debug
+ 	    lazyalloc_warn("mappages() != 0\n");
+      #endif
+	  kfree(mem);
+	  return 0;
+    }
+
+	return (uint64)mem;
+}

```

## 结果

最后 make grade 看成绩了：

```sh
xv6-labs-2020 $ make grade
...
== Test running lazytests == 
$ make qemu-gdb
(7.7s) 
== Test   lazy: map == 
  lazy: map: OK 
== Test   lazy: unmap == 
  lazy: unmap: OK 
== Test usertests == 
$ make qemu-gdb
(145.8s) 
== Test   usertests: pgbug == 
  usertests: pgbug: OK 
== Test   usertests: sbrkbugs == 
  usertests: sbrkbugs: OK 
== Test   usertests: argptest == 
  usertests: argptest: OK 
== Test   usertests: sbrkmuch == 
  usertests: sbrkmuch: OK 
== Test   usertests: sbrkfail == 
  usertests: sbrkfail: OK 
== Test   usertests: sbrkarg == 
  usertests: sbrkarg: OK 
== Test   usertests: stacktest == 
  usertests: stacktest: OK 
== Test   usertests: execout == 
  usertests: execout: OK 
== Test   usertests: copyin == 
  usertests: copyin: OK 
== Test   usertests: copyout == 
  usertests: copyout: OK 
== Test   usertests: copyinstr1 == 
  usertests: copyinstr1: OK 
== Test   usertests: copyinstr2 == 
  usertests: copyinstr2: OK 
== Test   usertests: copyinstr3 == 
  usertests: copyinstr3: OK 
== Test   usertests: rwsbrk == 
  usertests: rwsbrk: OK 
== Test   usertests: truncate1 == 
  usertests: truncate1: OK 
== Test   usertests: truncate2 == 
  usertests: truncate2: OK 
== Test   usertests: truncate3 == 
  usertests: truncate3: OK 
== Test   usertests: reparent2 == 
  usertests: reparent2: OK 
== Test   usertests: badarg == 
  usertests: badarg: OK 
== Test   usertests: reparent == 
  usertests: reparent: OK 
== Test   usertests: twochildren == 
  usertests: twochildren: OK 
== Test   usertests: forkfork == 
  usertests: forkfork: OK 
== Test   usertests: forkforkfork == 
  usertests: forkforkfork: OK 
== Test   usertests: createdelete == 
  usertests: createdelete: OK 
== Test   usertests: linkunlink == 
  usertests: linkunlink: OK 
== Test   usertests: linktest == 
  usertests: linktest: OK 
== Test   usertests: unlinkread == 
  usertests: unlinkread: OK 
== Test   usertests: concreate == 
  usertests: concreate: OK 
== Test   usertests: subdir == 
  usertests: subdir: OK 
== Test   usertests: fourfiles == 
  usertests: fourfiles: OK 
== Test   usertests: sharedfd == 
  usertests: sharedfd: OK 
== Test   usertests: exectest == 
  usertests: exectest: OK 
== Test   usertests: bigargtest == 
  usertests: bigargtest: OK 
== Test   usertests: bigwrite == 
  usertests: bigwrite: OK 
== Test   usertests: bsstest == 
  usertests: bsstest: OK 
== Test   usertests: sbrkbasic == 
  usertests: sbrkbasic: OK 
== Test   usertests: kernmem == 
  usertests: kernmem: OK 
== Test   usertests: validatetest == 
  usertests: validatetest: OK 
== Test   usertests: opentest == 
  usertests: opentest: OK 
== Test   usertests: writetest == 
  usertests: writetest: OK 
== Test   usertests: writebig == 
  usertests: writebig: OK 
== Test   usertests: createtest == 
  usertests: createtest: OK 
== Test   usertests: openiput == 
  usertests: openiput: OK 
== Test   usertests: exitiput == 
  usertests: exitiput: OK 
== Test   usertests: iput == 
  usertests: iput: OK 
== Test   usertests: mem == 
  usertests: mem: OK 
== Test   usertests: pipe1 == 
  usertests: pipe1: OK 
== Test   usertests: preempt == 
  usertests: preempt: OK 
== Test   usertests: exitwait == 
  usertests: exitwait: OK 
== Test   usertests: rmdot == 
  usertests: rmdot: OK 
== Test   usertests: fourteen == 
  usertests: fourteen: OK 
== Test   usertests: bigfile == 
  usertests: bigfile: OK 
== Test   usertests: dirfile == 
  usertests: dirfile: OK 
== Test   usertests: iref == 
  usertests: iref: OK 
== Test   usertests: forktest == 
  usertests: forktest: OK 
== Test time == 
time: OK 
Score: 119/119
```

---

2021.04.03  CDFMLR

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。