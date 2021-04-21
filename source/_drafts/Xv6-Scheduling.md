---
date: 2021-04-20 16:05:42.063533
title: Xv6-Scheduling
---
# Xv6-Scheduling

- time-share the CPUs: run more processes than CPUs
- transparent to user processes
- *multiplexing* processes onto CPUs: 
  - illusion: each process has its own virtual CPU

## Multiplexing

Switching CPU among processes:

- sleep/wakeup: process waits for something in the `sleep` syscall
- periodically forces a switch: cope with processes that compute for long periods

Illusion: each process has its own CPU.

Challenges:

- How to switch from one process to another?
- How to force switches in a way that transparent to user processes?
- Avoid races when many CPUs switching among processes concurrently.
- each core must remember which process it is executing
- sleep/wakeup: give up CPU, sleep waiting for an event, wake process up: avoid races, loss wakeup notifications

## Context switching

- save hte old thread's CPU registers
- restore previously-saved registers of the new thread
  - restore sp (stack pointer) & pc (program counter): switch the executing code.

`swtch` ([kernel/swtch.S](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/swtch.S)): save and restore for a kernel thread switch: switch to scheduler

- `void swtch(struct context *old, struct context *new);`
- save and restore *context* (register sets, [kernel/proc.h:2](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/proc.h#L2))
- swtch does not save `pc`: save `ra` -- holds the return address from which `swtch` was called.
- return to instructions pointed by the restored `ra` (the code called swtch)

Yield:

- yield -> sched -> swtch -> return to code called sched: `scheduler`

## Scheduling

Secheduler: a special thread

- per CPU a scheduler
- running  `scheduler()`

`scheduler`:

- choose a process to run
- swtch to run process
- eventually swtch back to scheduler

- scheduler acquires `switch_to_proc->lock`, no release 

Kernel thread gives up CPU: calls `sched` -> switch to scheduler

scheduler & sched: *co-rountines* (switch between two threads).

`p->lock`: 

- often acquires in one thread and releases it in other
  - once scheduler starts to convert a RUNNABLE process to RUNNING, the lock cannot be released until the kernel thread is completely running (after the swtch, for example in yield).
  - interplay between exit and wait, the machinery to avoid lost wakeups
  - avoidance of races between a process exiting and other processes reading or writing its state
  - ...

## mycpu and myproc

`struct cpu`: Xv6 maintains for each CPU:

- currently running process
- saved registers for the CPU scheduler thread
- count of nested spinlocks needed to manage interrupt disabling

RISC-V giving each CPU a *hartid*: stored in that CPU's `tp` register while in the kernel:

- `mstart` sets `tp` in CPU's boot (machine mode)
- `usertrapret` saves `tp` in the trampiline page (user might modify tp)
- `uservec` restores saved `tp` when entering the kernel.


`mycpu` ([kernel/proc.c](https://github.com/mit-pdos/xv6-riscv/blob/077323a8f0b3440fcc3d082096a2d83fe5461d70/kernel/proc.c#L72)):

- returns a pointer to the current CPU's `sturct cpu`
- use `tp` to index an array of `struct cpu` => find the right one.
- interrupts must be disabled to run `mycpu`: if the thread yield and then move to a different CPU, a previously read `cpuid` value would no longer be correct.

`myproc` ([kernel/proc.c](https://github.com/mit-pdos/xv6-riscv/blob/077323a8f0b3440fcc3d082096a2d83fe5461d70/kernel/proc.c#L80)):

- disables interrupts
- invokes `mycpu`
- fetches current process: `c->proc`
- enables interrupts
- return a pointer to a `struct proc`

## sleep and wakeup

sleep & wakeup:  *sequence coordination* or *conditional synchronization* mechanisms:

- one process to sleep waiting for an event
- another process to wake it up once the event has happened.

### busy waiting

```c
struct semaphore {
  struct spinlock lock;
  int count;
};

void
V(struct semaphore *s)  // producer
{
   acquire(&s->lock);
   s->count += 1;
   release(&s->lock);
}

void
P(struct semaphore *s)  // consumer
{
   while(s->count == 0)
     ;  // repeatedly polling: busy waiting
   acquire(&s->lock);
   s->count -= 1;
   release(&s->lock);
}
```

expensive!

### sleep/wakeup

#### intro sleep/wakeup

```c
void
V(struct semaphore *s)  // producer
{
   acquire(&s->lock);
   s->count += 1;
   wakeup(s);
   release(&s->lock);
}

void
P(struct semaphore *s)  // consumer
{
   while(s->count == 0)
     sleep(s);
   acquire(&s->lock);
   s->count -= 1;
   release(&s->lock);
}
```

- `sleep(chan)`: sleep on a *wait channel*: releasing CPU.
- `wakeup(chan)`: wakes all processes sleeping on chan: `sleep` return.

#### *lost wake-up* problem

1. P found `s->count == 0`
2. V runs on another CPU: changes `s->count` to be nonzero
3. V calls wakeup: no processes sleeping -> wakeup do nothing
4. P continues: calles `sleep`: asleep waiting for a V
5. but one V has lost: unless luckly producer calls V again, the consumer will wait forever

To avoid this problem: move the lock acquisition in P: check count and calls sleep atomically:

```c
void
P(struct semaphore *s)  // consumer
{
   acquire(&s->lock);
   while(s->count == 0)
     sleep(s);
   s->count -= 1;
   release(&s->lock);
}
```

#### deadlocks

However, this version also deadlocks: P holds the lock while sleeps, v will block forever waiting for the lock.

To fix this: change the interface of `sleep`:

- pass a *condition lock* to `sleep`
- `sleep` release this lock after process is asleep and waiting on the sleep channel.
- a concurrent V will be forced to wait until P is asleep:
  wakeup will find the sleeping consumer.
- once the consumer awake: sleep reacquires the lock before returning.

final code:

```c
void
V(struct semaphore *s)  // producer
{
   acquire(&s->lock);
   s->count += 1;
   wakeup(s);
   release(&s->lock);
}

void
P(struct semaphore *s)  // consumer
{
   while(s->count == 0)
     sleep(s, &s->lock);
   acquire(&s->lock);
   s->count -= 1;
   release(&s->lock);
}
```

## sleep and wakeup implement

（感觉写英文好多是抄书，学习效果不佳，下面还是写中文，用自己的话来说吧。。）

直接看源码吧，这个挺直接的。

- `sleep`: [kernel/proc.c:529](https://github.com/mit-pdos/xv6-riscv/blob/077323a8f0b3440fcc3d082096a2d83fe5461d70/kernel/proc.c#L529)

```c
// Atomically release lock and sleep on chan.
// Reacquires lock when awakened.
void
sleep(void *chan, struct spinlock *lk)
{
  struct proc *p = myproc();
  
  // Must acquire p->lock in order to
  // change p->state and then call sched.
  // Once we hold p->lock, we can be
  // guaranteed that we won't miss any wakeup
  // (wakeup locks p->lock),
  // so it's okay to release lk.

  acquire(&p->lock);  //DOC: sleeplock1
  release(lk);

  // Go to sleep.
  p->chan = chan;
  p->state = SLEEPING;

  sched();

  // Tidy up.
  p->chan = 0;

  // Reacquire original lock.
  release(&p->lock);
  acquire(lk);
}
```

- `wakeup`: [kernel/proc.c:560](https://github.com/mit-pdos/xv6-riscv/blob/077323a8f0b3440fcc3d082096a2d83fe5461d70/kernel/proc.c#L560) (这个好暴力)

```c
// Wake up all processes sleeping on chan.
// Must be called without any p->lock.
void
wakeup(void *chan)
{
  struct proc *p;

  for(p = proc; p < &proc[NPROC]; p++) {
    if(p != myproc()){
      acquire(&p->lock);
      if(p->state == SLEEPING && p->chan == chan) {
        p->state = RUNNABLE;
      }
      release(&p->lock);
    }
  }
}
```

## Pipes 实现

Pipe 是用 `struct pipe` 来表示的:

- 一个 lock
- data: 环形 buffer
- nread/nwrite: 已读/写的总字节数
  - buffer 为空：`nwrite == nread`
  - buffer 为满：`nwrite == nread + PIPESIZE`
- 读取 buf：`data[nread % PIPESIZE]`

调用接口：

- `pipewrite`
- `piperead`

## wait, exit, kill

- wait：父进程等待任一子进程退出
- exit：（子）进程退出
- kill：杀进程

`exit` 会把进程状态改为 `ZOMBIE`。

`wait` 取得 ZOMBIE 的子进程后将其状态改成 `UNUSED`，读取其退出状态，返回其 pid。

若父在子之前退出，父会把子转让给 `init`。`init` 漫无止境地调用 wait，所以所有就成都可以执行完后被清除。

