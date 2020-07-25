---
categories:
- Linux
- Beginning
date: 2016-12-29 22:38:11
tags: Linux
title: linux-3.1.2-磁盘，可移除式媒体
---

# 磁盘，可移除式媒体

- **检查磁盘空间**

监督文件系统的使用情况，可使用如下两个命令：

- df：显示文件系统中磁盘使用和空闲区的数量

```
$ df [选项] [dir|file|设备]
    无[dir|file]：以KB为单位列出每个(Every)文件系统中 所有的空间，已用空间，空闲空间
    加上 dir|file：显示该文件所在的文件系统的情况
    加上 设备(如 /dev/sda1)：显示该设备的文件系统的情况
    选项：
        -h或-H ：以人类容易理解的方式表示
        -i：列出inode的使用情况
```

- du：显示磁盘使用的总量（xx目录，有多大）

du命令<u>以KB为单位</u>🐱显示文件系统磁盘空间使用的总量，并将递归地显示所有子目录的磁盘空间使用量。

如果在这个命令中使用-s选项，命令的结果就只显示一个目录总的磁盘空间使用量。

在du命令中也同样可以加上-h或-H选项。

🐱. 部分UNIX上（如Solaris上），du的单位是 *512B* 的数据块数。

- **可移除式媒体**

**_Removable Media_**（一种翻译为  可移除式媒体）：指USB闪存、软盘、CD、DVD等介质。

_Removable Media_ 的**特点**：

- 在访问之前，必须将这个Removable Media挂载（mount）到系统上。
  
- 在移除之前，必须将这个Removable Media从系统上卸载掉。
  
- 在默认的情况下，一般非root的普通用户只能挂载某些特定的设备（如USB闪存、软盘、CD、DVD等）。
  
- 默认的挂载点一般是根目录下的media，即/media。

**MOUNT** Removable Media：

```
$ mount
    列出当前系统中挂载的所有文件系统
```

* Mount **CD/DVD:**  

在gnome或KDE的中，只要在光驱中放入CD或DVD，就会被自动地挂载到系统中来。

如果没有被自动地挂载到系统中来，就必须手动地挂载CD/DVD。

如果是CD/DVD Reader，将使用 `mount  ...  /media/cdrom` 命令将CD/DVD挂载到 `/media/cdrom` 之下。

如果是CD/DVD Writer，将使用 `mount ... /media/cdrecorder` 命令将CD/DVD挂载到 `/media/cdrecorder` 之下。

可以使用eject命令退出（umount）CD/DVD。

\[⚠️\]<span style="color: #fcb100;">当安装有**多个光盘**软件时，千万**不要将工作目录设为CD所在的目录**，这样将无法更换光盘，因为执行eject或umount命令时系统要求CD目录中没有任何操作。</span>

```
挂载CD／DVD：
# mount  /dev/hdc  /media/cdrom        # Only root can do that
Read it：
$ ls -l /media/cdrom
Umount it：
# eject /media/cdrom
```

* Mount **USB闪存：**  

将USB闪存插入计算机，Linux内核会自动探测到这一设备，并将其自动安装为SCSI设备。

通常它会被挂载在`/media/<Device ID>`。

手动挂载：

```
# mount /media/KINGSTON
或
# mount  /dev/sdb1  /media/KINGSTON
```

只有root可以 umount USB 闪存。
