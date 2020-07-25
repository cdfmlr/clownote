---
categories:
- Linux
- Beginning
date: 2016-12-27 16:13:00
tags: Linux
title: linux-3.1.0-文件系统与inode
---

# Linux文件系统与inode

## 硬盘分区和文件系统

一个新的硬盘，不能直接使用。首先必须把这个硬盘划分成数个（也可能是一个）<span style="background-color: rgb(255, 250, 165);">分区</span>，之后再把每一个分区<span style="background-color: rgb(255, 250, 165);">格式化</span>为文件系统，然后Linux系统才能在格式化后的硬盘分区上存储数据和进行相应的文件管理及维护。

Linux或UNIX系统上的磁盘分区就相当于Windows系统上的逻辑盘。

把一个分区格式化为文件系统就是将这个分区划分成许多大小相等的小单元，

并将这些小单元顺序地编号。

这些小单元被称为块（block），Linux默认的block大小为4KB。

Block是存储数据的最小单位，

每个block最多只能存储一个文件，

如果一个文件的大小超过4KB，那么就会占用多个blocks。

## inode

### inode 概念

i节点就是一个与某个特定的对象（如文件或目录）相关的信息列表。

i节点实际上是一个数据结构，它存放了有关一个普通文件、目录或其他文件系统对象的基本信息。

当一个磁盘被格式化成文件系统（如ext2或ext3）时，系统将自动生成一个i节点（inode）表；

在该表中包含了所有文件的元数据（metadata，描述数据的数据），每一个文件和目录都会对应于一个唯一的i节点，而这个i节点是使用一个i节点号（inode number简写成inode-no）来标识的；

inodes的数量决定了在这个文件系统中最多可以存储多少个文件，在一个分区（partition）中有多少个i节点就只能够存储多少个文件和目录。

在多数类型的文件系统中，i节点的数目是固定的，并且是在创建文件系统时生成的。

在一个典型的UNIX或Linux文件系统中，i节点所占用的空间大约是整个文件系统大小的1%。

---

### inode 解读

i节点中所有的属性都是用来描述文件的，而不是文件中的内容。

i节点类似图书馆中的图书目录，在每一本书的图书目录中印有该书的内容简介、作者信息、出版日期、页数等**摘要信息**。

通常每个i节点由两部分组成，第1部分是有关文件的基本信息，第2部分是指向存储文件信息的数据块的指针：

![IMG_1066](http://ww2.sinaimg.cn/large/006tNc79ly1g60fl18enfj30go0730tl.jpg)

```
（1）inode-no ：i节点号。
		在一个文件系统中，每一个i节点都有一个唯一的编号。
（2）File type ：文件的类型。
		'-'为  普通文件，
		'd'为 目录。
（3）permission ：权限。
		在i节点中使用数字表示法来表示文件的权限。
（4）Link count ：硬连接（hard link）数。
（5）UID ：文件所有者的UID。
（6）GID ：owner所属群组的GID。
（7）size ：文件的大小。
（8）Time stamp：时间戳。
		时间戳包含了3个时间：
				①Access time（A time） ：最后一次存取的时间。
				②Modify time（M time） ：最后一次编辑的时间。
				③Change time（C time）：该文件inode中任一元数据发生变化的时间。
		如果M time被更新时，通常A time和C time也会跟着一起被更新：
				在更新一个文件之前必须先打开这个文件，所以要先更新A time；
				编辑完之后一般文件的大小要发生变化，所以C time也会被更新。
（9）Other information
（10）pointer：指向保存文件的blocks的指针。

```


### 查看文件的 inode number：

可以使用带有-i选项的ls命令，在每一行记录的开始显示这个文件的i节点号码。


### *普通文件* 与 *目录*

1.普通文件（Regular File）：只存放数据，

可以存放多种不同类型的数据。

2.目录：“特殊”的文件，目录中存储的是文件名和与文件名相关的i节点号码的信息。目录中只能存放一类数据。

```
struct file_list{
    char name[MAX];
    unsign inode;
    struct file_list next;
} * pBarFiles;
char * make_the_list(struct file_list *);
fooDirectoty.content = make_the_list(pBarFiles);
```


### cp、rm、mv 的 operate(inode)

1. `cp`：

（1）找到一个空闲的i节点记录（inode number），把新文件的meta data写入到这个空闲的i节点中并将这个新记录放入inode表中。

（2）产生一条目录记录，把新增的文件名对应到这个空的inode号码。

（3）将文件的内容（数据）复制到新增的文件中去。

2. `rm`：

（1）首先将这个文件的连接数（hard link）减1；

（如原文件的link count为3，运行了rm后，它的link count将为2）

之后这个文件的link count如果小于1，

就释放这个i节点以便重用。

（2）释放存储这个文件内容的数据块；

                （即将这些数据块标记为可以使用）

（3）删除记录这个文件名和i节点号的目录记录。

3. `mv`：

若 *原位置* 与 *目标位置*  位于 **同一文件系统**：  

	（1）首先产生一个新的目录记录，把新的文件名对应到源文件的i节点。  
	
	（2）删除带有旧文件名的原有的目录记录。
	
	/* 这是<u>逻辑移动</u>：除了更新时间戳外，移动文件行为对原本在inode表中的数据不会有任何影响，也**不会将数据移动**到其他的文件中去，即**没有发生真正的数据移动**。\*/

若 *源位置* 与 *目的位置* 是在 **不同文件系统**：

```
cp(source, destination)；
rm(source)；
```

必要情况下：为确保数据确实发生移动，应使用cp，rm而非mv


## 总结

- 关于文件的几个术语：

	（1）文件名是访问和维护文件时最常使用的。

	（2）i节点（inodes）是系统用来记录有关文件信息的对象。

	（3）数据块是用来存储数据的磁盘空间的单位。

- 其中关联：

	每个文件必须具有一个名字并且与一个i节点相关。

	通常系统通过文件名就可以确定i节点，

	之后通过i节点中的指针就可以定位存储数据的数据块

![IMG_1067](http://ww2.sinaimg.cn/large/006tNc79gy1g60oehim96j30go00v0sr.jpg)
