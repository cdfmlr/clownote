---
date: 2021-03-16 21:59:28.476938
tags: xv6
title: Xv6 traps and system calls
---

![Meaning Unknown's Head Image](https://api.ixiaowai.cn/api/api.php)


# Traps and system calls

> Learning [xv6-riscv-book](https://github.com/mit-pdos/xv6-riscv-book) Chapter 4 Traps and system calls

[TOC]

---

**Trap**: CPU transfer to speical code to handle events

- **system call**: ecall into the kernel
- **exception**: something illegal
- **interrupt**: from device

---

xv6 kernel handles all traps.


code -> trap (handling in kernel) -> resume

---

trap handling proceeds:

1. **hardware** actions by CPU
2. **vector** prepares for kernel C code
3. trap **handler** decides what to do 
4. do system call / device service

---

three cases of assembly vectors:

- traps from user space
- traps from kernel space
- timer interrupts

## RISC-V trap machinery

### Registers

A set of **registers**: 

- kernel reads about a trap
- kernel writes to tell the CPU how to handle traps.

| register | description                                                  | write by | when                               |
| -------- | ------------------------------------------------------------ | -------- | ---------------------------------- |
| stvec    | address of trap handler                                      | kernel   |                                    |
| sepc     | saved PC when a trap occurs                                  | RISC-V   | when a trap occurs                 |
| scause   | reason of trap                                               | RISC-V   |                                    |
| sscratch | places a value that comes in handy                           | kernel   | at the very start of a traphandler |
| sstatus  | **SIE** bit: device interrupts are enabled? (defer until set)<br />**SPP** bit: trap from user or supervisor mode?(ctrl what mode sret returns) |          |                                    |

These registers  are in **supervisor mode**: cannot be r/w in user mode

**Machine mode** has an equivalent set of these regs: only for **timer interrupts**

Each CPU has its own set: can handling traps at a same time

### hardware trap handling sequence

```python
trap_occurs:
	if trap is DeviceInterrupt:
        sstatus.SIE = 0
        goto end
    sstatus.SIE = 0  # disable interrupts
    sepc = pc
    sstatus.SPP = current_mode()
    scause = trap.cause
    set_mode(.supervisor)
    pc = stvec(trap)
    execute(pc)
end:
```

note: CPU does minimal work: 

- kernel page table / stack are not switched
- registers other than PC are not saved

(kernel must do these tasks 👆)

## Traps from user space

Traps from user space: 

1. trap occurs:
   1. uservec ([trampoline.S:16](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/trampoline.S#L16))
   2. usertrap ([trap.c:37](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/trap.c#L37))
2. handle trap
3. returing:
   1. usertrapret ([trap.c:90](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/trap.c#L90))
   2. userret ([trampoline.S:88)](https://github.com/mit-pdos/xv6-riscv/blob/077323a8f0b3440fcc3d082096a2d83fe5461d70/kernel/trampoline.S#L88))

---

Hardware doesn't switch page tables during a trap:

- user page table includes a mapping for `uservec`
- `uservec` switch `satp` to kernel page table
- `uservec` must be at the same address in k & u. (to continue pc after switch)

So, xv6 use a *trampiline* page （VA at `TRAMPILINE`） to contains uservec. The contents of trampiline pages are set in `trampiline.S`.

---

### uservec

1. starts: all registers -> values of interrupted code (`sscratch` points to `p->trapframe`);
   - `csrrw` instruction: `swaps(a0, sscratch)`
2. save user registers to `trapframe` (at `a0`)
3. save `a0` to `trapframe`
4. switch `satp` to kernel page table (in trapframe)
5. calls `usertrap`

### usertrap

(`usertrap` handle trap from user space, kernel traps are handled by `kerneltrap`)

- determine the cause of the trap
- process trap: 
  - save `sepc` (the saved user program counter)
  - if trap is SystemCall: calls `syscall()`
  - if trap is DeviceIntrrupt: calls `devintr`
- return by `usertrapret`

### usertrapret

sets up the RISC-V control registers to prepare for a future trap from user space:

- stvec
- tramframe
- sepc
- calls `userret`

### userret

```c
userret(TRAPFRAME, userpagetable);
          (a0)         (a1)
```

- switches `satp` to user page table.
- restores saved registers from trapframe.
- `sret` return to user space.

## Calling system calls

e.g. ([user/initcode.S:11](https://github.com/mit-pdos/xv6-riscv/blob/riscv//user/initcode.S#L11)) calling `exec`:

```assembly
# exec(init, argv)
.globl start
start:
        la a0, init
        la a1, argv
        li a7, SYS_exec
        ecall
```

- `a0`, `a1` <- arguments
- `a7` <- system call number
- `ecall` -> uservec -> usertrap -> syscall
- `syscall`: 
  - retrieves syscall number from saved a7 in the trapframe
  - use syscall number to index into `syscalls`
- system call implementation function returns:
  - `syscall` records return value in `p->trapframe->a0`

## System call arguments

system call wrapper functions:

- places arguments in registers
- trap: registers are saved to trapframe
- `argint`, `argaddr`, `argfd`: retrieve arguments as integer, pointer or file descriptor.

---

pointer argument: (e.g. str):

- fetchstr -> copyinstr
- copyinstr: copies bytes from srcva (in user pagetable) to dst.
  - use `walkaddr` to walk the page table (in software) to get pa for srcva

## Traps from kernel space

- `kernelvec` ([kernelvec.S:10](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/kernelvec.S#L10))
- `kerneltrap` ([trap.c:134](https://github.com/mit-pdos/xv6-riscv/blob/riscv//kernel/trap.c#L134))

  - handle types of trap:

    - devintr
    - exception (kernel error => fatal): calls `panic`, stops executing
    - timer interrupt: `yield` to give up CPU.
  - return: restores control registers, return to kernelvec

## Page-fault exceptions

Xv6: exception happens:

- exception from user space: kill the faulting process;
- exception from kernel: panic! 

Real world: more interesting ways. e.g. use page faults to implement *copy-on-write* (COW)  *fork*.

---

- Xv6 fork: calling `uvmcopy` to copy parent's memory into child. (no share)
- COW fork: safely share phyical memory
  - share all physical pages (read-only)
  - when child or patent store: raise a *page-fault exception*
  - response to this exception: 
    - makes a copy of the page that contains the faulted address.
    - both allow to read/write
      - one for child, one for parent
    - resumes the process caused the fault

---

*page-fault exception*: CPU cannot translate a virtual address to a physical address

- load page faults
- store page faults
- instruction page fault

A page-fault exception happen:

- `scause` <- PageFault
- `stval` <- address that couldn't be translated

**avoid complete copy & transparent**

---

Other page faults feature:

- lazy allocation: 
  - sbrk => grows address space, but not marks valid in pgtbl
  - page fault on new address =>  allocates physical memory, maps into the pgtbl
- paging from disk:
  - app need more memory than physical RAM => write some pages to disk
  - pg fault => if in disk: allocates a page of physical memory, read page from disk. (may evict another page to disk)
- automically extending stacks
- memory-mapped files
- ...

---

EOF

---

```sh
# By CDFMLR 2021-03-18
echo "See you."
```

顶部图片来自于[小歪API](https://api.ixiaowai.cn)，系随机选取的图片，仅用于检测屏幕显示的机械、光电性能，与文章的任何内容及观点无关，也并不代表本人局部或全部同意、支持或者反对其中的任何内容及观点。如有侵权，联系删除。


