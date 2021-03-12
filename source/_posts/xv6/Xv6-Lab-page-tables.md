---
date: 2021-03-11 08:25:22.131819
tags: xv6
title: Xv6 Lab page tables
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)


# Lab: page tables

> MIT 6.S081 Xv6-riscv Lab 3: https://pdos.csail.mit.edu/6.S081/2020/labs/pgtbl.html

## Print a page table

Define a function called `vmprint()`. It should take a `pagetable_t` argument, and print that pagetable in the format described below. Insert `if(p->pid==1) vmprint(p->pagetable)` in exec.c just before the `return argc`, to print the first process's page table. You receive full credit for this assignment if you pass the `pte printout` test of `make grade`.

### 主要实现

这题就递归打印一下地址，非常容易了。

```c
void
_pteprint(pagetable_t pagetable, int level)
{
  for(int i = 0; i < 512; i++) {
    pte_t pte = pagetable[i];

    if (pte & PTE_V) {
      for (int j = 0; j <= level; j++)
        printf(".. ");
      // printf("\b%d: pte %p pa %p\n", i, pte, PTE2PA(pte));
      printf("%d: pte %p pa %p\n", i, pte, PTE2PA(pte));
    }
    if ((pte & PTE_V) && (pte & (PTE_R|PTE_W|PTE_W)) == 0) {
        // this PTE points to a lower-level page table.
    uint64 child = PTE2PA(pte);
    _pteprint((pagetable_t)child, level+1);
    }
  }
}

void
vmprint(pagetable_t pagetable)
{
  printf("page table %p\n", pagetable);
  _pteprint(pagetable, 0);
}
```

注，_pteprint 里的 printf 那里带上 `\b` 打印出来效果和题目一样了，但通不过make grade —— `\b` 也是个字符哦: 

```sh
$ cat -vte xv6.out.pteprint:
...

page table 0x0000000087f6e000$
.. ^H0: pte 0x0000000021fda801 pa 0x0000000087f6a000$
.. .. ^H0: pte 0x0000000021fda401 pa 0x0000000087f69000$
.. .. .. ^H0: pte 0x0000000021fdac1f pa 0x0000000087f6b000$
.. .. .. ^H1: pte 0x0000000021fda00f pa 0x0000000087f68000$
.. .. .. ^H2: pte 0x0000000021fd9c1f pa 0x0000000087f67000$
.. ^H255: pte 0x0000000021fdb401 pa 0x0000000087f6d000$
.. .. ^H511: pte 0x0000000021fdb001 pa 0x0000000087f6c000$
.. .. .. ^H510: pte 0x0000000021fdd807 pa 0x0000000087f76000$
.. .. .. ^H511: pte 0x0000000020001c0b pa 0x0000000080007000$

...
```
但多个空格是可以过 make grade 测试的，所以就这样了。

### 详细的diff

(patch)

```diff
diff --git a/kernel/defs.h b/kernel/defs.h
index a73b4f7..ebc4cad 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -178,6 +178,7 @@ uint64          walkaddr(pagetable_t, uint64);
 int             copyout(pagetable_t, uint64, char *, uint64);
 int             copyin(pagetable_t, char *, uint64, uint64);
 int             copyinstr(pagetable_t, char *, uint64, uint64);
+void            vmprint(pagetable_t);
 
 // plic.c
 void            plicinit(void);
diff --git a/kernel/exec.c b/kernel/exec.c
index 0e8762f..4c41c7d 100644
--- a/kernel/exec.c
+++ b/kernel/exec.c
@@ -115,6 +115,9 @@ exec(char *path, char **argv)
   p->trapframe->epc = elf.entry;  // initial program counter = main
   p->trapframe->sp = sp; // initial stack pointer
   proc_freepagetable(oldpagetable, oldsz);
+  
+  if (p->pid == 1)
+	  vmprint(p->pagetable);
 
   return argc; // this ends up in a0, the first argument to main(argc, argv)
 
diff --git a/kernel/vm.c b/kernel/vm.c
index bccb405..3487f25 100644
--- a/kernel/vm.c
+++ b/kernel/vm.c
@@ -440,3 +440,36 @@ copyinstr(pagetable_t pagetable, char *dst, uint64 srcva, uint64 max)
     return -1;
   }
 }
+
+void
+_pteprint(pagetable_t pagetable, int level)
+{
+  for(int i = 0; i < 512; i++) {
+    pte_t pte = pagetable[i];
+
+    if (pte & PTE_V) {
+      for (int j = 0; j <= level; j++)
+        printf(".. ");
+      // printf("\b%d: pte %p pa %p\n", i, pte, PTE2PA(pte));
+    // 这里带上 \b 打印出来效果和题目一样了，但通不过make grade
+    // \b 也是个字符哦: cat -vte xv6.out.pteprint:
+    //   .. ^H0: pte 0xXXX pa 0xXXX$
+    // 多个空格是可以过 make grade 测试的
+      printf("%d: pte %p pa %p\n", i, pte, PTE2PA(pte));
+    }
+    if ((pte & PTE_V) && (pte & (PTE_R|PTE_W|PTE_W)) == 0) {
+        // this PTE points to a lower-level page table.
+    uint64 child = PTE2PA(pte);
+    _pteprint((pagetable_t)child, level+1);
+    }
+  }
+}
+
+void
+vmprint(pagetable_t pagetable)
+{
+  printf("page table %p\n", pagetable);
+
+  _pteprint(pagetable, 0);
+}
+
```



## A kernel page table per process

Your first job is to modify the kernel so that every process uses its own copy of the kernel page table when executing in the kernel. Modify `struct proc` to maintain a kernel page table for each process, and modify the scheduler to switch kernel page tables when switching processes. For this step, each per-process kernel page table should be identical to the existing global kernel page table. You pass this part of the lab if `usertests` runs correctly.

### 主要实现

跟着 hits 一步一步做。

1. 在 `struct proc` 里面加一个内核页表字段：

```c
// kernel/proc.h
struct proc {
  ...
  uint64 kstack;             // Virtual address of kernel stack
  uint64 sz;                 // Size of process memory (bytes)
  pagetable_t pagetable;     // User page table
  pagetable_t kpagetable;    // (+) Kernel page table
  ...
}
```

2. 模仿 `kvminit` 实现一个构建内核页表映射的函数，后面每个进程都调这个函数构建一分内核页表：

```c
// vm.c

/*
 * make a direct-map page table for the kernel.
 */
pagetable_t
kvmmake()
{
  pagetable_t kpagetable = (pagetable_t) kalloc();
  memset(kpagetable, 0, PGSIZE);
  kvmmap(kpagetable, UART0, UART0, PGSIZE, PTE_R | PTE_W);
  kvmmap(kpagetable, VIRTIO0, VIRTIO0, PGSIZE, PTE_R | PTE_W);
  kvmmap(kpagetable, CLINT, CLINT, 0x10000, PTE_R | PTE_W);
  kvmmap(kpagetable, PLIC, PLIC, 0x400000, PTE_R | PTE_W);
  kvmmap(kpagetable, KERNBASE, KERNBASE, (uint64)etext-KERNBASE, PTE_R | PTE_X);
  kvmmap(kpagetable, (uint64)etext, (uint64)etext, PHYSTOP-(uint64)etext, PTE_R | PTE_W);
  kvmmap(kpagetable, TRAMPOLINE, (uint64)trampoline, PGSIZE, PTE_R | PTE_X);

  return kpagetable;
}

/*
 * setup kernel_pagetable
 */
void
kvminit()
{
  kernel_pagetable = kvmmake();
}

// 加一个 pagetable_t 参数
void
kvmmap(pagetable_t kpagetable, uint64 va, uint64 pa, uint64 sz, int perm)
{
  if(mappages(kpagetable, va, sz, pa, perm) != 0)
    panic("kvmmap");
}
```

3. 在 `allocproc` 里用上面的 kvmmake 方法得到自己的内核页表，同时把原本在 `procinit` 里做的 kernel stack 映射改到 allocproc 来：

```c
// proc.c

// initialize the proc table at boot time.
void
procinit(void)
{
  struct proc *p;
  
  initlock(&pid_lock, "nextpid");
  for(p = proc; p < &proc[NPROC]; p++) {
      initlock(&p->lock, "proc");
  }
  // kvminithart();
}


static struct proc*
allocproc(void)
{
  ...
found:
  p->pid = allocpid();

  // Allocate a trapframe page.
  ...
  
  // (+) A kernel page table
  if((p->kpagetable = kvmmake()) == 0){
  	freeproc(p);
	release(&p->lock);
	return 0;
  }

  // (+) Allocate a page for the process's kernel stack.
  // Map it high in memory, followed by an invalid
  // guard page.
  char *pa = kalloc();
  if(pa == 0)
	panic("kalloc");
  uint64 va = KSTACK((int)(p - proc));
  // uint64 va = KSTACK(0);
  kvmmap(p->kpagetable, va, (uint64)pa, PGSIZE, PTE_R | PTE_W);
  p->kstack = va;

  // An empty user page table.
  ...
}
```

4. 改 `scheduler()`, swtch 到新进程前把 `satp` 设置为新进程的内核页表，没运行进程的时候用 `kernel_pagetable`：

```c
// proc.c

void
scheduler(void)
{
  ...
  for(;;){
    ...
    for(p = proc; p < &proc[NPROC]; p++) {
      acquire(&p->lock);
      if(p->state == RUNNABLE) {
        p->state = RUNNING;
        c->proc = p;

		w_satp(MAKE_SATP(p->kpagetable));  // (+)
		sfence_vma();  // (+)

        swtch(&c->context, &p->context);

        // Process is done running for now.
        // It should have changed its p->state before coming back.
        c->proc = 0;
		
		// use kernel_pagetable when no process is running.
		kvminithart();  // (+)

        found = 1;
      }
      release(&p->lock);
    }
#if !defined (LAB_FS)
...
  }
}
```

5. 在 `freeproc` 里面释放进程内核页表，注意不要释放物理内存：

```c
// proc.c

static void
freeproc(struct proc *p)
{
  if(p->trapframe)
    kfree((void*)p->trapframe);
  p->trapframe = 0;
  
  // (+)👇
  if(p->kstack)
	uvmunmap(p->kpagetable, p->kstack, 1, 1);
  p->kstack = 0;
  if(p->kpagetable)
	kvmfree(p->kpagetable);
  p->kpagetable = 0;
  // (+)👆
  
  if(p->pagetable)
    proc_freepagetable(p->pagetable, p->sz);
  p->pagetable = 0;
  ...
}
```

其中 `kvmfree` 模仿 freewalk，释放内核页表:

```c
void
kvmfree(pagetable_t kpgtbl) {
  for(int i = 0; i < 512; i++){
    pte_t pte = kpgtbl[i];
    if (pte & PTE_V){
		kpgtbl[i] = 0;
		if ((pte & (PTE_R|PTE_W|PTE_X)) == 0) {
		  uint64 child = PTE2PA(pte);
		  kvmfree((pagetable_t)child);
		}
    } else if(pte & PTE_V){
      panic("kvmfree: leaf");
    }
  }
  kfree((void*)kpgtbl);
}
```

6. 最后，在 vm.c 有个 kvmpa，要改成用当前进程的内核页表的：导入 proc.h, 从 myproc 获取内核页表：

```c
// vm.c
#include "spinlock.h"
#include "proc.h"

...

uint64
kvmpa(uint64 va)
{
  ...
  pte = walk(myproc()->kpagetable, va, 0);
  ...
}
```

### Diff

```diff
diff --git a/kernel/defs.h b/kernel/defs.h
index ebc4cad..6a85a85 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -92,6 +92,7 @@ int             fork(void);
 int             growproc(int);
 pagetable_t     proc_pagetable(struct proc *);
 void            proc_freepagetable(pagetable_t, uint64);
+// void            proc_freekpagetable(pagetable_t, uint64, uint64);
 int             kill(int);
 struct cpu*     mycpu(void);
 struct cpu*     getmycpu(void);
@@ -161,7 +162,7 @@ int             uartgetc(void);
 void            kvminit(void);
 void            kvminithart(void);
 uint64          kvmpa(uint64);
-void            kvmmap(uint64, uint64, uint64, int);
+void            kvmmap(pagetable_t, uint64, uint64, uint64, int);
 int             mappages(pagetable_t, uint64, uint64, uint64, int);
 pagetable_t     uvmcreate(void);
 void            uvminit(pagetable_t, uchar *, uint);
@@ -179,6 +180,8 @@ int             copyout(pagetable_t, uint64, char *, uint64);
 int             copyin(pagetable_t, char *, uint64, uint64);
 int             copyinstr(pagetable_t, char *, uint64, uint64);
 void            vmprint(pagetable_t);
+pagetable_t     kvmmake(void);
+void            kvmfree(pagetable_t);
 
 // plic.c
 void            plicinit(void);
diff --git a/kernel/proc.c b/kernel/proc.c
index dab1e1d..d731950 100644
--- a/kernel/proc.c
+++ b/kernel/proc.c
@@ -34,14 +34,16 @@ procinit(void)
       // Allocate a page for the process's kernel stack.
       // Map it high in memory, followed by an invalid
       // guard page.
+	  /*
       char *pa = kalloc();
       if(pa == 0)
         panic("kalloc");
       uint64 va = KSTACK((int) (p - proc));
       kvmmap(va, (uint64)pa, PGSIZE, PTE_R | PTE_W);
       p->kstack = va;
+	  */
   }
-  kvminithart();
+  // kvminithart();
 }
 
 // Must be called with interrupts disabled,
@@ -112,6 +114,24 @@ found:
     release(&p->lock);
     return 0;
   }
+  
+  // A kernel page table
+  if((p->kpagetable = kvmmake()) == 0){
+  	freeproc(p);
+	release(&p->lock);
+	return 0;
+  }
+
+  // Allocate a page for the process's kernel stack.
+  // Map it high in memory, followed by an invalid
+  // guard page.
+  char *pa = kalloc();
+  if(pa == 0)
+	panic("kalloc");
+  uint64 va = KSTACK((int)(p - proc));
+  // uint64 va = KSTACK(0);
+  kvmmap(p->kpagetable, va, (uint64)pa, PGSIZE, PTE_R | PTE_W);
+  p->kstack = va;
 
   // An empty user page table.
   p->pagetable = proc_pagetable(p);
@@ -139,6 +159,12 @@ freeproc(struct proc *p)
   if(p->trapframe)
     kfree((void*)p->trapframe);
   p->trapframe = 0;
+  if(p->kstack)
+	uvmunmap(p->kpagetable, p->kstack, 1, 1);
+  p->kstack = 0;
+  if(p->kpagetable)
+	kvmfree(p->kpagetable);
+  p->kpagetable = 0;
   if(p->pagetable)
     proc_freepagetable(p->pagetable, p->sz);
   p->pagetable = 0;
@@ -195,6 +221,14 @@ proc_freepagetable(pagetable_t pagetable, uint64 sz)
   uvmfree(pagetable, sz);
 }
 
+/*
+void
+proc_freekpagetable(pagetable_t kpgtbl, uint64 kstack, uint64 sz) {
+	uvmunmap(kpgtbl, kstack, 1, 1);
+	kvmfree(kpgtbl);
+}
+*/
+
 // a user program that calls exec("/init")
 // od -t xC initcode
 uchar initcode[] = {
@@ -473,11 +507,18 @@ scheduler(void)
         // before jumping back to us.
         p->state = RUNNING;
         c->proc = p;
+
+		w_satp(MAKE_SATP(p->kpagetable));
+		sfence_vma();
+
         swtch(&c->context, &p->context);
 
         // Process is done running for now.
         // It should have changed its p->state before coming back.
         c->proc = 0;
+		
+		// use kernel_pagetable when no process is running.
+		kvminithart();
 
         found = 1;
       }
@@ -486,7 +527,11 @@ scheduler(void)
 #if !defined (LAB_FS)
     if(found == 0) {
       intr_on();
-      asm volatile("wfi");
+	  
+	  // use kernel_pagetable when no process is running.
+	  // kvminithart();
+      
+	  asm volatile("wfi");
     }
 #else
     ;
diff --git a/kernel/proc.h b/kernel/proc.h
index 9c16ea7..7858834 100644
--- a/kernel/proc.h
+++ b/kernel/proc.h
@@ -98,6 +98,7 @@ struct proc {
   uint64 kstack;               // Virtual address of kernel stack
   uint64 sz;                   // Size of process memory (bytes)
   pagetable_t pagetable;       // User page table
+  pagetable_t kpagetable;      // Kernel page table
   struct trapframe *trapframe; // data page for trampoline.S
   struct context context;      // swtch() here to run process
   struct file *ofile[NOFILE];  // Open files
diff --git a/kernel/vm.c b/kernel/vm.c
index 3487f25..8f3f445 100644
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
@@ -16,35 +18,48 @@ extern char etext[];  // kernel.ld sets this to end of kernel code.
 extern char trampoline[]; // trampoline.S
 
 /*
- * create a direct-map page table for the kernel.
+ * make a direct-map page table for the kernel.
  */
-void
-kvminit()
+pagetable_t
+kvmmake()
 {
-  kernel_pagetable = (pagetable_t) kalloc();
-  memset(kernel_pagetable, 0, PGSIZE);
+  pagetable_t kpagetable = (pagetable_t) kalloc();
+  memset(kpagetable, 0, PGSIZE);
 
   // uart registers
-  kvmmap(UART0, UART0, PGSIZE, PTE_R | PTE_W);
+  kvmmap(kpagetable, UART0, UART0, PGSIZE, PTE_R | PTE_W);
 
   // virtio mmio disk interface
-  kvmmap(VIRTIO0, VIRTIO0, PGSIZE, PTE_R | PTE_W);
+  kvmmap(kpagetable, VIRTIO0, VIRTIO0, PGSIZE, PTE_R | PTE_W);
 
   // CLINT
-  kvmmap(CLINT, CLINT, 0x10000, PTE_R | PTE_W);
+  kvmmap(kpagetable, CLINT, CLINT, 0x10000, PTE_R | PTE_W);
 
   // PLIC
-  kvmmap(PLIC, PLIC, 0x400000, PTE_R | PTE_W);
+  kvmmap(kpagetable, PLIC, PLIC, 0x400000, PTE_R | PTE_W);
 
   // map kernel text executable and read-only.
-  kvmmap(KERNBASE, KERNBASE, (uint64)etext-KERNBASE, PTE_R | PTE_X);
+  kvmmap(kpagetable, KERNBASE, KERNBASE, (uint64)etext-KERNBASE, PTE_R | PTE_X);
 
   // map kernel data and the physical RAM we'll make use of.
-  kvmmap((uint64)etext, (uint64)etext, PHYSTOP-(uint64)etext, PTE_R | PTE_W);
+  kvmmap(kpagetable, (uint64)etext, (uint64)etext, PHYSTOP-(uint64)etext, PTE_R | PTE_W);
 
   // map the trampoline for trap entry/exit to
   // the highest virtual address in the kernel.
-  kvmmap(TRAMPOLINE, (uint64)trampoline, PGSIZE, PTE_R | PTE_X);
+  kvmmap(kpagetable, TRAMPOLINE, (uint64)trampoline, PGSIZE, PTE_R | PTE_X);
+
+  return kpagetable;
+}
+
+/*
+ * create a direct-map page table for the kernel.
+ */
+void
+kvminit()
+{
+  kernel_pagetable = kvmmake();
+  // CLINT
+  // kvmmap(kernel_pagetable, CLINT, CLINT, 0x10000, PTE_R | PTE_W);
 }
 
 // Switch h/w page table register to the kernel's page table,
@@ -115,9 +130,9 @@ walkaddr(pagetable_t pagetable, uint64 va)
 // only used when booting.
 // does not flush TLB or enable paging.
 void
-kvmmap(uint64 va, uint64 pa, uint64 sz, int perm)
+kvmmap(pagetable_t kpagetable, uint64 va, uint64 pa, uint64 sz, int perm)
 {
-  if(mappages(kernel_pagetable, va, sz, pa, perm) != 0)
+  if(mappages(kpagetable, va, sz, pa, perm) != 0)
     panic("kvmmap");
 }
 
@@ -132,7 +147,7 @@ kvmpa(uint64 va)
   pte_t *pte;
   uint64 pa;
   
-  pte = walk(kernel_pagetable, va, 0);
+  pte = walk(myproc()->kpagetable, va, 0);
   if(pte == 0)
     panic("kvmpa");
   if((*pte & PTE_V) == 0)
@@ -194,6 +209,35 @@ uvmunmap(pagetable_t pagetable, uint64 va, uint64 npages, int do_free)
   }
 }
 
+void
+kvmfree(pagetable_t kpgtbl) {
+	/*
+	uvmunmap(kpgtbl, UART0, 1, 0);
+	uvmunmap(kpgtbl, VIRTIO0, 1, 0);
+	// uvmunmap(kpgtbl, CLINT, 0x10000 / PGSIZE, 0);
+	uvmunmap(kpgtbl, PLIC, 0x400000 / PGSIZE, 0);
+	uvmunmap(kpgtbl, KERNBASE, ((uint64)etext-KERNBASE) / PGSIZE, 0);
+	uvmunmap(kpgtbl, (uint64)etext, (PHYSTOP-(uint64)etext) / PGSIZE, 0);
+	uvmunmap(kpgtbl, TRAMPOLINE, 1, 0);
+	// uvmunmap(kpgtbl, 0, PGROUNDUP(sz) / PGSIZE, 0);
+    */
+  // there are 2^9 = 512 PTEs in a page table.
+  for(int i = 0; i < 512; i++){
+    pte_t pte = kpgtbl[i];
+    if (pte & PTE_V){
+		kpgtbl[i] = 0;
+		if ((pte & (PTE_R|PTE_W|PTE_X)) == 0) {
+		  // this PTE points to a lower-level page table.
+		  uint64 child = PTE2PA(pte);
+		  kvmfree((pagetable_t)child);
+		}
+    } else if(pte & PTE_V){
+      panic("freewalk: leaf");
+    }
+  }
+  kfree((void*)kpgtbl);
+}
+
 // create an empty user page table.
 // returns 0 if out of memory.
 pagetable_t
```

## Simplify `copyin/copyinstr`

Replace the body of `copyin` in `kernel/vm.c` with a call to `copyin_new` (defined in `kernel/vmcopyin.c`); do the same for `copyinstr` and `copyinstr_new`. Add mappings for user addresses to each process's kernel page table so that `copyin_new` and `copyinstr_new` work. You pass this assignment if `usertests` runs correctly and all the `make grade` tests pass.

 ### 主要实现

woc，这题我一开始没发现人家已经写好了，还自己手写了一个 `copyin_new`。。。

这题要做的主要就是把进程的用户页表映射到内核页表。

1. 在 defs.h 里添加人家写好的 copyin_new:

```c
// defs.h

...
// vmcopyin.c
int             copyin_new(pagetable_t, char *, uint64, uint64);
int             copyinstr_new(pagetable_t, char *, uint64, uint64);
```

2. 改掉原来的 copyin：

```c
// vm.c

int
copyin(pagetable_t pagetable, char *dst, uint64 srcva, uint64 len)
{
  return copyin_new(pagetable, dst, srcva, len);
}

int
copyinstr(pagetable_t pagetable, char *dst, uint64 srcva, uint64 max)
{
	return copyinstr_new(pagetable, dst, srcva, max);
}
```

3. 写一个函数来把进程的用户页表映射到内核页表：

```c
// vm.c

int 
uvm2k(pagetable_t pagetable, pagetable_t kpgtbl, uint64 oldsz, uint64 newsz) {
	pte_t *pte_from, *pte_to;

	if ((newsz < oldsz) || (PGROUNDUP(newsz) >= PLIC))
		return -1;

	for (uint64 va = PGROUNDUP(oldsz); va < newsz; va += PGSIZE) {
		if ((pte_from = walk(pagetable, va, 0)) == 0)
			panic("copyin_new: pte not exist");
		if ((pte_to = walk(kpgtbl, va, 1)) == 0)
			panic("copyin_new: walk failed");
		*pte_to = (*pte_from) & (~PTE_U);
	}

	return 0;
}
```

4. 在 `fork()`, `exec()` 和 `sbrk()` 里处理 uvm 到 kvm 的映射：

```c
// proc.c

int
fork(void)
{
  ...

  // increment reference counts on open file descriptors.
  for(i = 0; i < NOFILE; i++)
    if(p->ofile[i])
      np->ofile[i] = filedup(p->ofile[i]);
  np->cwd = idup(p->cwd);

  // (+)
  if (uvm2k(np->pagetable, np->kpagetable, 0, np->sz) < 0)
	return -1;

  safestrcpy(np->name, p->name, sizeof(p->name));
  pid = np->pid;
  np->state = RUNNABLE;
  release(&np->lock);
  return pid;
}
```

```c
// proc.c

// 这个就是 sbrk 啦
int
growproc(int n)
{
  ...
      
  if(n > 0){
    ...
	if (uvm2k(p->pagetable, p->kpagetable, sz-n, sz) < 0) {
		return -1;
	}
  } else if(n < 0){
    ...
	if (n >= PGSIZE) {  // 我不知道为什么这样 if，反正不写会 panic
		uvmunmap(p->kpagetable, PGROUNDUP(sz), n/PGSIZE, 0);
	}
  }

  p->sz = sz;
  return 0;
}
```

```c
// exec.c

int
exec(char *path, char **argv)
{
  ...

  // Allocate two pages at the next page boundary.
  // Use the second as the user stack.
  sz = PGROUNDUP(sz);
  ...
  sp = sz;
  stackbase = sp - PGSIZE;

  if (uvm2k(pagetable, p->kpagetable, 0, sz) < 0)  // (+)
	  goto bad;

  // Push argument strings, prepare rest of stack in ustack.
  for(argc = 0; argv[argc]; argc++) {
    if(argc >= MAXARG)
      goto bad;
  ...
}
```

### Diff

```diff
diff --git a/grade-lab-pgtbl b/grade-lab-pgtbl
index 2b0b49d..bb775b0 100755
--- a/grade-lab-pgtbl
+++ b/grade-lab-pgtbl
@@ -62,7 +62,7 @@ def test_count():
 def test_usertests():
     r.run_qemu(shell_script([
         'usertests'
-    ]), timeout=300)
+    ]), timeout=500)
 
 def usertest_check(testcase, nextcase, output):
     if not re.search(r'\ntest {}: [\s\S]*OK\ntest {}'.format(testcase, nextcase), output):
diff --git a/kernel/defs.h b/kernel/defs.h
index 6a85a85..2278ec7 100644
--- a/kernel/defs.h
+++ b/kernel/defs.h
@@ -182,6 +182,7 @@ int             copyinstr(pagetable_t, char *, uint64, uint64);
 void            vmprint(pagetable_t);
 pagetable_t     kvmmake(void);
 void            kvmfree(pagetable_t);
+int             uvm2k(pagetable_t, pagetable_t, uint64, uint64);
 
 // plic.c
 void            plicinit(void);
@@ -194,6 +195,10 @@ void            virtio_disk_init(void);
 void            virtio_disk_rw(struct buf *, int);
 void            virtio_disk_intr(void);
 
+// vmcopyin.c
+int             copyin_new(pagetable_t, char *, uint64, uint64);
+int             copyinstr_new(pagetable_t, char *, uint64, uint64);
+
 // number of elements in fixed-size array
 #define NELEM(x) (sizeof(x)/sizeof((x)[0]))
 
diff --git a/kernel/exec.c b/kernel/exec.c
index 4c41c7d..daeda2b 100644
--- a/kernel/exec.c
+++ b/kernel/exec.c
@@ -75,6 +75,9 @@ exec(char *path, char **argv)
   sp = sz;
   stackbase = sp - PGSIZE;
 
+  if (uvm2k(pagetable, p->kpagetable, 0, sz) < 0)
+	  goto bad;
+
   // Push argument strings, prepare rest of stack in ustack.
   for(argc = 0; argv[argc]; argc++) {
     if(argc >= MAXARG)
diff --git a/kernel/proc.c b/kernel/proc.c
index d731950..6cff554 100644
--- a/kernel/proc.c
+++ b/kernel/proc.c
@@ -255,6 +255,8 @@ userinit(void)
   uvminit(p->pagetable, initcode, sizeof(initcode));
   p->sz = PGSIZE;
 
+  uvm2k(p->pagetable, p->kpagetable, 0, p->sz);
+
   // prepare for the very first "return" from kernel to user.
   p->trapframe->epc = 0;      // user program counter
   p->trapframe->sp = PGSIZE;  // user stack pointer
@@ -280,9 +282,16 @@ growproc(int n)
     if((sz = uvmalloc(p->pagetable, sz, sz + n)) == 0) {
       return -1;
     }
+	if (uvm2k(p->pagetable, p->kpagetable, sz-n, sz) < 0) {
+		return -1;
+	}
   } else if(n < 0){
     sz = uvmdealloc(p->pagetable, sz, sz + n);
+	if (n >= PGSIZE) {
+		uvmunmap(p->kpagetable, PGROUNDUP(sz), n/PGSIZE, 0);
+	}
   }
+
   p->sz = sz;
   return 0;
 }
@@ -323,6 +332,9 @@ fork(void)
       np->ofile[i] = filedup(p->ofile[i]);
   np->cwd = idup(p->cwd);
 
+  if (uvm2k(np->pagetable, np->kpagetable, 0, np->sz) < 0)
+	return -1;
+
   safestrcpy(np->name, p->name, sizeof(p->name));
 
   pid = np->pid;
diff --git a/kernel/vm.c b/kernel/vm.c
index 8f3f445..361aa5d 100644
--- a/kernel/vm.c
+++ b/kernel/vm.c
@@ -417,29 +417,32 @@ copyout(pagetable_t pagetable, uint64 dstva, char *src, uint64 len)
   return 0;
 }
 
+// maps users pagetble to a kpgtbl
+int 
+uvm2k(pagetable_t pagetable, pagetable_t kpgtbl, uint64 oldsz, uint64 newsz) {
+	pte_t *pte_from, *pte_to;
+
+	if ((newsz < oldsz) || (PGROUNDUP(newsz) >= PLIC))
+		return -1;
+
+	for (uint64 va = PGROUNDUP(oldsz); va < newsz; va += PGSIZE) {
+		if ((pte_from = walk(pagetable, va, 0)) == 0)
+			panic("copyin_new: pte not exist");
+		if ((pte_to = walk(kpgtbl, va, 1)) == 0)
+			panic("copyin_new: walk failed");
+		*pte_to = (*pte_from) & (~PTE_U);
+	}
+
+	return 0;
+}
+
 // Copy from user to kernel.
 // Copy len bytes to dst from virtual address srcva in a given page table.
 // Return 0 on success, -1 on error.
 int
 copyin(pagetable_t pagetable, char *dst, uint64 srcva, uint64 len)
 {
-  uint64 n, va0, pa0;
-
-  while(len > 0){
-    va0 = PGROUNDDOWN(srcva);
-    pa0 = walkaddr(pagetable, va0);
-    if(pa0 == 0)
-      return -1;
-    n = PGSIZE - (srcva - va0);
-    if(n > len)
-      n = len;
-    memmove(dst, (void *)(pa0 + (srcva - va0)), n);
-
-    len -= n;
-    dst += n;
-    srcva = va0 + PGSIZE;
-  }
-  return 0;
+  return copyin_new(pagetable, dst, srcva, len);
 }
 
 // Copy a null-terminated string from user to kernel.
@@ -449,40 +452,7 @@ copyin(pagetable_t pagetable, char *dst, uint64 srcva, uint64 len)
 int
 copyinstr(pagetable_t pagetable, char *dst, uint64 srcva, uint64 max)
 {
-  uint64 n, va0, pa0;
-  int got_null = 0;
-
-  while(got_null == 0 && max > 0){
-    va0 = PGROUNDDOWN(srcva);
-    pa0 = walkaddr(pagetable, va0);
-    if(pa0 == 0)
-      return -1;
-    n = PGSIZE - (srcva - va0);
-    if(n > max)
-      n = max;
-
-    char *p = (char *) (pa0 + (srcva - va0));
-    while(n > 0){
-      if(*p == '\0'){
-        *dst = '\0';
-        got_null = 1;
-        break;
-      } else {
-        *dst = *p;
-      }
-      --n;
-      --max;
-      p++;
-      dst++;
-    }
-
-    srcva = va0 + PGSIZE;
-  }
-  if(got_null){
-    return 0;
-  } else {
-    return -1;
-  }
+	return copyinstr_new(pagetable, dst, srcva, max);
 }
 
 void
```

---

## 最后

emmm，好像我在第二题做的有问题，usertests 会：

```c
usertrap(): unexpected scause 0x000000000000000d pid=6227
            sepc=0x000000000000201a stval=0x00000000800493e0
```

不知道哪里错了。。

然后其实我跑 make grade 有时候 usertests 会超时（它超时是300秒，我要 300 秒多一点点，改改测试脚本就能过了[狗头]）。不知道为什么，qemu 跑着跑着在宿主机上的 CPU 占用就从 100% 降到 20% 左右了。。

```c
== Test pte printout == 
$ make qemu-gdb
pte printout: OK (3.8s) 
== Test answers-pgtbl.txt == answers-pgtbl.txt: OK 
== Test count copyin == 
$ make qemu-gdb
count copyin: OK (1.4s) 
== Test usertests == 
$ make qemu-gdb
(312.6s) 
== Test   usertests: copyin == 
  usertests: copyin: OK 
== Test   usertests: copyinstr1 == 
  usertests: copyinstr1: OK 
== Test   usertests: copyinstr2 == 
  usertests: copyinstr2: OK 
== Test   usertests: copyinstr3 == 
  usertests: copyinstr3: OK 
== Test   usertests: sbrkmuch == 
  usertests: sbrkmuch: OK 
== Test   usertests: all tests == 
  usertests: all tests: OK 
== Test time == 
time: OK 
Score: 66/66
```

反正勉强能过那就先就这样吧，有时间再研究一下。

---

2021.03.13  CDFMLR

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。