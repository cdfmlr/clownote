---
date: 2020-02-27 19:13:09
tags: Golang
title: Golang SQL 查询使用 LIKE 分句的坑
---
# Golang SQL 查询使用 LIKE 分句的坑

我想在 golang 里执行一个涉及到模糊查询的 SQL Query。

使用 LIKE 分句的 SQL 语句如下：

```sql
SELECT name,time FROM course WHERE time LIKE '4%';
```

然后我写了如下 Golang 代码，专门搞了一下 `''`：

```go
// BUG
timeLike := fmt.Sprintf("'%d%%'", day)
rows, err := db.Query("SELECT name,time FROM course WHERE time LIKE ?", timeLike)
```

查询出来的是空。

之后，参考 https://www.cnblogs.com/huangliang-hb/p/10048666.html，我发现不能写 `''`，把这东西去掉就行了：

```go
// CORRECT
timeLike := fmt.Sprintf("%d%%", day)
rows, err := db.Query("SELECT name,time FROM course time LIKE ?", timeLike)
```

