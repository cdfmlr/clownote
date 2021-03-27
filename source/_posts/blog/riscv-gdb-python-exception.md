---
date: 2021-03-27 09:47:44.388737
title: riscv gdb python exception
---
# riscv gdb: python exception

## 问题描述

`riscv64-unknown-elf-gdb` 报错：

```
Python Exception <type 'exceptions.NameError'> Installation error: gdb._execute_unwinders function is missing: 
```

## 问题分析

`riscv64-unknown-elf-gdb` 缺失 GDB 的 Python 模块。

## 解决方法

手动装一个完整的 GDB，把 Python 模块链接过去：

```sh
brew install gdb
brew link --overwrite gdb
ln -s /usr/local/Cellar/gdb/10.1/share/gdb /usr/local/Cellar/riscv-gnu-toolchain/master/share/gdb
```

