---
date: 2021-05-04 15:55:36.860873
title: xv6-file-system
---
# Xv6 文件系统

文件系统：

- 目的：
  - 组织和储存文件
- 一般支持：
  - 在用户和应用之间共享数据
  - 持久化：重启后，数据仍可用

实现难点：

- 在磁盘上的数据结构：文件、目录、记录
- 错误恢复
- 多个不同的进程可能同时操作文件系统
- 访问磁盘的速度比内存慢，文件系统应该用内存对热门块做缓存

## Xv6 文件系统总览

七层实现：

- disk 层：从设备（virtio haed drive）读写磁盘块
- buffer cache 层：缓存、同步块
- logging 层：支持高层事务操作：在故障时，一组操作要么全做了，要么全没做
- inode 层：为每个文件提供唯一标识 i-number、储存文件的块。
- directory 层：实现目录——一种特殊的 inode，内容是 directory entries——包含文件名和 i-number。
- pathname 层：实现分级的路径名，支持递归查询：e.g. `/usr/rtm/xv6/fs.c`
- file descriptor 层：用文件描述符抽象各种 unix 资源（管道、设备、文件等）

为了分别储存 inodes 和内容块，xv6 把磁盘分成好几个区域：

- `block 0`：保留，启动扇区
- `block 1`：superblock：包含文件系统元数据（文件系统大小、数据块个数、inode个数...）
  - 由 `mkfs` 填写：初始化文件系统
- `block 2~L`：日志
- `block L~I`：inodes
- `block I~B`：位图：记录那些数据块在使用中
- `block B~`：数据块

## buffer cache 层

buffer cache 的工作：

- 同步访问磁盘块：只有一份块的拷贝存在内存，并且在某一时间只有一个内核线程可以使用该拷贝
- 缓存经常使用的块——不必反复从磁盘读取（硬盘慢）

buffer （`struct buf`：bio.h）是 buffer cache 里的实体。存放拷贝到内存的磁盘块。

buffer cache 是 buffer 组成的双向链表。

关键接口（`bio.c`）：

- `binit`：初始化链表，基于一个大小为 NBUF 的 `buf` 数组
  - 访问都要通过链表：bcache.head
  - 不直接访问 buf 数组
- `bread`：拷贝一个块到 buf，可供读取、修改（在内存）
  - 调用 `bget` 从给定扇区获取 buffer：
    - 返回已存在的缓存：直接返回
    - 没缓存：新分配一个：回收最久最近未使用[^1]的缓存：Recycle the least recently used (LRU) unused buffer
  - 若需要读取，则调用 virtue_disk_rw 读磁盘。
- `bwrite`：把修改后的 buf 块写回硬盘
- `brelse`：释放用完的 buf
  - 把 buffer 移到链表首：维护双向链表头表示最近使用的、尾就是最久未使用的
  - 这样 bget 就可以利用双向链表快速完成扫描了：
    - 第一遍循环从头开始（从bcache.head，往 next 方向），找是否已存在缓存：最近使用的很可能再次使用，这样可能可以减少扫描时间
    - 没找到时，第二遍循环从尾开始（从bcache.head，往 prev 方向），找一个未使用的：很久没用了的更可能满足。

[^1]:  关于 LRU：我记得上课一般是说「最近最久未使用」，但这个听起来很迷，我觉得「最久最近未使用」好一点；或者直接「最久未使用」更好理解；或者按照百度百科写的「最近最少使用」这个也好理解。

线程安全：每一个 buffer 一把 sleep-lock：

- bread 返回上了锁的 buf
- brelse 释放锁

注意：必须保证一个磁盘扇区只能有一个缓存。

在 Xv6 实现中，太多进程同时请求访问文件系统时，buffers 都在忙，bget 就会直接 panic。更优雅的处理方案是睡眠，直到有可用的空闲 buffer，但这个方案可能会死锁。

## Logging 层

Logging 层用来支持故障情况的恢复：原子操作——要么一组操作完整执行完成，要么完全没做。

磁盘操作可能会是一组的，例如文件截断（truncation，这个词好像是截断吧）——把文件长度设为零 & 释放内容块。

发生故障时，可能会出现先释放了内容块，然而原来的 inode 还指向这个块。这样系统就可以在释放了的块放新文件，然后就有两个 inode 指向同一个文件了，这个很有安全问题。

Xv6 通过 logging 层来解决这种异常情况：

- Xv6 系统调用不直接去写磁盘
- 而是把写磁盘的愿望写到一个磁盘的 *log* 中（就是把不是去写真正的那个块，而是写到一个临时的拷贝）
- 当这个系统调用写好了它所有的写愿望后，写入一个特殊的 *commit* 记录，表示这里 log 了一个完整的操作了。
- 然后系统执行这些 log 了的写操作（就是把那些临时拷贝写到真正的位置上去）
- 全部执行完成后就把整条 log 删除。

遇到故障重启时，文件系统会在运行任何进程之前做恢复：

- 如果 log 中包含完整的操作（commit了的），则执行这些写；
- 如果 log 操作不完整（没 commit）就忽略了

（恢复代码执行完成后，log 就空了）

### Log 设计

Log 存放在已知的固定位置，这个位置在 superblock 中指定。

Log 包含：

- header block：头块，包含 log blocks 的个数「conut」、扇区号数组（对应于每个logged block）
- logged blocks：一系列更新了的块的拷贝

header.count：

- 当提交「commit」时，header 中的 count 会增加。
- 当把 logged blocks 拷贝到真实的文件系统中后置为 0。

所以：

- 在 commit 前崩溃，则 count 为 0 => 忽略，不执行；
- 在 commit 后崩溃，则 count 不为 0 => 执行恢复。

*group commit*：把多个文件系统调用集在一个 commit 里：

- 减少磁盘操作的次数
- 提高并发性

   Xv6 固定了磁盘上放 log 的空间——只有有限个可用的 log 块：

- 对于一般的系统调用时够用的
- 对于像 write 这种可能操作大量的块的调用，就需要把大的操作分成多个小调用，使每个小调用满足 log 的尺寸限制。

### Log 实现

在系统调用中，对 log 的调用大致如下：

```c
begin_op();
...
bp = bread(...);
bp->data[...] = ...;
log_write(bp);
...
end_op();
```

- `begin_op` （`log.c`）开始一个文件系统操作（事务）
  - 等待，直到无 commit 正在进行
  - 然后再等待，直到用足够的 log 空间以供使用
  - 增加 `log.outstanding` (这里 outstanding 意同 unresolved ，未完成的)
    - 保留空间
    - 防止 commit 执行
- `log_write` ：
  - 在内存中记录块的扇区号
  - 在硬盘的 log 里为其留下一个位置
    - 如果多次写一个块则保持用同一个位置
      - 这个称为 *absorption*：absorption several disk writes into one
      - 可以节省 log 空间、提高写入性能
  - 然后标记 buffer 正在使用，以防被回收——块要留在缓存里面直到 commit
- `end_op` 结束一次文件系统操作（事务）
  - outstanding 减 1
  - 如果 outstanding 为 0 则调用 `commit()`：
    - `write_log()`：把修改了的块从 cache 写到 log
    - `write_head()`：修改 log header （这里就是 commit 的点：先于这里崩溃则弃之，后于则恢复执行）
    - `install_trans`：把 log 写到文件系统中的实际位置
    - 把 log header 的 counter 置为 0，完成事务

系统启动时，在运行用户进程前，会调用 `fsinit` -> `initlog` -> `recover_from_log` -> `install_trans` 实现恢复。

## Block allocator 实现

文件和目录储存在磁盘的块中，储存新文件就必须从一个空闲池中分配块。

Xv6 利用「空闲位图」（free bitmap）来维护分配。

位图中用一个 bit 代表一个块：

- 0：表示块空闲
- 1：表示块在使用中

`mkfs` 会设置好 boot sector、superblock、log blocks、inode blocks 和 bitmap block 对应的位。

块分配主要提供两个函数：

- `balloc`：分配一个置零的块
  - 考虑每个块，从 0 到 `sb.size`（文件系统中的块总数），这里用了嵌套循环：
    - 外层循环读取 bitmap 的各个块
    - 内层循环检查一个 bitmap 块里的所有 BPB 个位。
  - 若块对应的 bitmap 值为 0 则认为块空闲
  - 找到空闲的块就更新 bitmap 值，返回块
- `bfree` 释放块（使空闲）：
  - 找到正确的 bitmap 块，清除其中对应的位

在 balloc 和 bfree 中不是直接读写 bitmap 中的位，而是间接地通过 bread、brelse 来解决并发问题，避免使用明锁。

注意：balloc、bfree 只能在事务中调用。

## inode 层

inode 有两种：

- on-disk：磁盘上的数据结构：包含文件的大小、数据所在的 block 编号列表
- in-memry：内存中的 on-disk inode 的拷贝，并附加上内核需要的额外信息

在磁盘中，inode 被放在连续的 inode blocks 里。每个 inode 的长度是固定的，所以容易找到第 n 个 inode —— 这里的 n 即为 inode 号（i-number）。

on-disk inode 定义在 `struct dinode` （`fs.h`）：

- type 字段表示文件的类型（file、dir、dev ...），type 为 0 表示 inode 是空闲的。
- nlink 字段记录有多少个目录引用了这个 inode。大于 0 时 inode 就不会被释放
- size：文件内瓤的长度（bytes）
- addrs：数组，记录文件内容的各个块的编号

in-memory inode 定义为 `struct inode`（`file.h`）：

- 包含 `struct dinode` 的全部字段
- 只有当有 C 指针指向 inode 时，内核才会储存一个 in-memory inode，放到一个 cache（itable）中
  - iget：获取一个 inode 指针（`struct inode *`）
  - iput：释放 inode 指针
- 拓展的 ref 字段表示引用这个 in-memory inode 的 C 指针数，ref 为 0 后 内核就会丢弃这个 inode

inode 相关的锁机制：

- `icache.lock` (现在的代码里是 itable.lock)
  - 保证一个 inode 最多只能在 cache（table）中出现一次
  - 保证缓存下来的 inode （在 table 中的）的 ref 字段等于引用 inode 的指针数
- `inode.lock`：每个 in-memory inode 都有一个的 sleep lock
  - 保证互斥访问（同一时间只能有一个访问）：
    - inode 的各字段（比如文件长度）
    - inode 的内容块
- `ilock()`：`iget` 返回的内容可能是无效的（不在缓存中的），为了保证内存拷贝和磁盘中保持一致，必须调用 `ilock`：
  - ilock 锁住 inode （别的进程不能再 ilock 它） 
  - 如果需要（还没读取过）则从磁盘读取 inode 

