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
- `block 2~l`：日志
- `block l~i`：inodes
- `block i~b`：位图：记录那些数据块在使用中
- `block b~`：数据块

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

