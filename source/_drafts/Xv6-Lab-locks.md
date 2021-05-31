---
date: 2021-05-13 17:21:07.941402
title: Xv6-Lab-locks
---
# Xv6 Lab: locks



```sh
  $ git fetch
  $ git checkout lock
  $ make clean
```

## Memory allocator

这题就是说，提供了一个用户程序 kalloctest。运行之后结果可以看出，kmem （内存的空闲列表、kalloc、kfree）这一块经常竞争获取锁，效率低了，要想个办法改进一下（尽量减少竞争）。

改进的思路大概是：

- 原来全局只有一个 kmem，一把锁，各个 CPU 争着用
- 现在改成每个 CPU 给一个 kmem，即每个 CPU 都有自己的空闲列表。
  - 分配时（kalloc）：使用当前 CPU 的空闲列表，自己的用完了才去偷别人的。
  - 还内存时（kfree）：不问来路，直接还给当前的 CPU。
  - （偷的过程才有竞态，但很少要偷，所以效率提高了）

代码实现（`kernel/kalloc.c`）：

```c
...

struct kmemd {  //(+) 取个名字方便复用
  struct spinlock lock;
  struct run *freelist;
} kmems[NCPU];  //(+) 每个 CPU 一个

void
kinit()
{
  for(int i = 0; i < NCPU; i++) {  //(+) 初始化全部锁
    initlock(&(kmems+i)->lock, "kmem");
  }
  freerange(end, (void*)PHYSTOP);
}

kfree(void *pa)
{
  ...

  r = (struct run*)pa;

  push_off();  // for cpuid()
  struct kmemd *kmem = kmems + cpuid();
  pop_off();

  acquire(&kmem->lock);
  r->next = kmem->freelist;
  kmem->freelist = r;
  release(&kmem->lock);
}

void *
kalloc(void)
{
  struct run *r;

  push_off();
  struct kmemd *kmem = kmems + cpuid();
  pop_off();

  acquire(&kmem->lock);
  r = kmem->freelist;
  if(r)
    kmem->freelist = r->next;
  release(&kmem->lock);
  
  if(!r) {  // this CPU's free list is empty, steal from others
	struct kmemd *other = kmems, *max=kmems+NCPU;
    for (; /*(other != kmem) &&*/ (other < max); other++) {
	  acquire(&other->lock);
	  r = other->freelist; 
	  if (r) {
	    other->freelist = r->next;
		release(&other->lock);
		break;
	  }
	  release(&other->lock);
	}
  }

  if(r)
    memset((char*)r, 5, PGSIZE); // fill with junk

  return (void*)r;
}
```

Diff:

```diff
diff --git a/kernel/kalloc.c b/kernel/kalloc.c
index fa6a0ac..d6ad380 100644
--- a/kernel/kalloc.c
+++ b/kernel/kalloc.c
@@ -9,6 +9,7 @@
 #include "riscv.h"
 #include "defs.h"
 
+
 void freerange(void *pa_start, void *pa_end);
 
 extern char end[]; // first address after kernel.
@@ -18,15 +19,17 @@ struct run {
   struct run *next;
 };
 
-struct {
+struct kmemd {
   struct spinlock lock;
   struct run *freelist;
-} kmem;
+} kmems[NCPU];
 
 void
 kinit()
 {
-  initlock(&kmem.lock, "kmem");
+  for(int i = 0; i < NCPU; i++) {
+    initlock(&(kmems+i)->lock, "kmem");
+  }
   freerange(end, (void*)PHYSTOP);
 }
 
@@ -56,10 +59,14 @@ kfree(void *pa)
 
   r = (struct run*)pa;
 
-  acquire(&kmem.lock);
-  r->next = kmem.freelist;
-  kmem.freelist = r;
-  release(&kmem.lock);
+  push_off();  // for cpuid()
+  struct kmemd *kmem = kmems + cpuid();
+  pop_off();
+
+  acquire(&kmem->lock);
+  r->next = kmem->freelist;
+  kmem->freelist = r;
+  release(&kmem->lock);
 }
 
 // Allocate one 4096-byte page of physical memory.
@@ -70,13 +77,32 @@ kalloc(void)
 {
   struct run *r;
 
-  acquire(&kmem.lock);
-  r = kmem.freelist;
+  push_off();
+  struct kmemd *kmem = kmems + cpuid();
+  pop_off();
+
+  acquire(&kmem->lock);
+  r = kmem->freelist;
   if(r)
-    kmem.freelist = r->next;
-  release(&kmem.lock);
+    kmem->freelist = r->next;
+  release(&kmem->lock);
+  
+  if(!r) {  // this CPU's free list is empty, steal from others
+	struct kmemd *other = kmems, *max=kmems+NCPU;
+    for (; /*(other != kmem) &&*/ (other < max); other++) {
+	  acquire(&other->lock);
+	  r = other->freelist; 
+	  if (r) {
+	    other->freelist = r->next;
+		release(&other->lock);
+		break;
+	  }
+	  release(&other->lock);
+	}
+  }
 
   if(r)
     memset((char*)r, 5, PGSIZE); // fill with junk
+
   return (void*)r;
 }

```

⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️TODO：这个实现其实不太好，每次都去争第一个 CPU 的内存，还是会有一定竞争。改进：...?













```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <assert.h>
#include <pthread.h>
#include <sys/time.h>

#define NBUCKET 5
#define NKEYS 100000

struct entry {
  int key;
  int value;
  struct entry *next;
};
struct entry *table[NBUCKET];
int keys[NKEYS];
int nthread = 1;

pthread_mutex_t locks[NBUCKET]; // 谨遵hint，每个桶一把锁。但我实际试下来，比一把锁提升不大（emmm，有时候甚至还更慢？？？）。

double
now()
{
 struct timeval tv;
 gettimeofday(&tv, 0);
 return tv.tv_sec + tv.tv_usec / 1000000.0;
}

static void 
insert(int key, int value, struct entry **p, struct entry *n)
{
  struct entry *e = malloc(sizeof(struct entry));
  e->key = key;
  e->value = value;
  e->next = n;
  *p = e;
}

static 
void put(int key, int value)
{
  int i = key % NBUCKET;

  // is the key already present?
  struct entry *e = 0;
  for (e = table[i]; e != 0; e = e->next) {
    if (e->key == key)
      break;
  }
  pthread_mutex_lock(locks + i);
  if(e){
    // update the existing key.
    e->value = value;
  } else {
    // the new is new.
    insert(key, value, &table[i], table[i]);
  }
  pthread_mutex_unlock(locks + i);
}

static struct entry*
get(int key)
{
  int i = key % NBUCKET;


  struct entry *e = 0;
  for (e = table[i]; e != 0; e = e->next) {
    if (e->key == key) break;
  }

  return e;
}

static void *
put_thread(void *xa)
{
  int n = (int) (long) xa; // thread number
  int b = NKEYS/nthread;

  for (int i = 0; i < b; i++) {
    put(keys[b*n + i], n);
  }

  return NULL;
}

static void *
get_thread(void *xa)
{
  int n = (int) (long) xa; // thread number
  int missing = 0;

  for (int i = 0; i < NKEYS; i++) {
    struct entry *e = get(keys[i]);
    if (e == 0) missing++;
  }
  printf("%d: %d keys missing\n", n, missing);
  return NULL;
}

int
main(int argc, char *argv[])
{
  pthread_t *tha;
  void *value;
  double t1, t0;

  for (int i = 0; i < NBUCKET; i++) {
    pthread_mutex_init(locks + i, NULL);
  }

  if (argc < 2) {
    fprintf(stderr, "Usage: %s nthreads\n", argv[0]);
    exit(-1);
  }
  nthread = atoi(argv[1]);
  tha = malloc(sizeof(pthread_t) * nthread);
  srandom(0);
  assert(NKEYS % nthread == 0);
  for (int i = 0; i < NKEYS; i++) {
    keys[i] = random();
  }

  //
  // first the puts
  //
  t0 = now();
  for(int i = 0; i < nthread; i++) {
    assert(pthread_create(&tha[i], NULL, put_thread, (void *) (long) i) == 0);
  }
  for(int i = 0; i < nthread; i++) {
    assert(pthread_join(tha[i], &value) == 0);
  }
  t1 = now();

  printf("%d puts, %.3f seconds, %.0f puts/second\n",
         NKEYS, t1 - t0, NKEYS / (t1 - t0));

  //
  // now the gets
  //
  t0 = now();
  for(int i = 0; i < nthread; i++) {
    assert(pthread_create(&tha[i], NULL, get_thread, (void *) (long) i) == 0);
  }
  for(int i = 0; i < nthread; i++) {
    assert(pthread_join(tha[i], &value) == 0);
  }
  t1 = now();

  printf("%d gets, %.3f seconds, %.0f gets/second\n",
         NKEYS*nthread, t1 - t0, (NKEYS*nthread) / (t1 - t0));
}

```

