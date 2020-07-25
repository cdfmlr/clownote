---
date: 2020-02-27 20:37:08
title: 关于 Golang if err != nil 泛滥成灾的优化方案
---

# 关于 Golang `if err != nil` 泛滥成灾的优化方案

刚才我尝试用 Golang 写一个项目，其中有一个并不复杂的方法，主要涉及到两次正则匹配和两个字符串读取，然后，我发现这个方法里我写了四段一模一样的代码：

```go
if err != nil {
    log.Println(err)
    return false, err
}
```

顺手搜了一下，发现整个工程里有 78 个 `if err != nil`，要知道，这是个刚刚起步的工程，总共才差不多2K的代码呀！差不多每二十几行代码就要来一发 `if err != nil`，，，太可怕了。

但我尝试在 Google 输入 `if err` 的时候，我看到了搜索建议里的这行代码，于是尬笑着点开了它，然后发现，这是个新手常犯的尴尬，也有很多种优化方法，所以我当然是选择——抄官方的作业了！

这是 [一篇官方的blog](https://blog.golang.org/errors-are-values) 里介绍的解决 `if err != nil` 尴尬的方法：

Lament：

```go
_, err = fd.Write(p0[a:b])
if err != nil {
    return err
}
_, err = fd.Write(p1[c:d])
if err != nil {
    return err
}
_, err = fd.Write(p2[e:f])
if err != nil {
    return err
}
// and so on
```

Grace:

```go
var err error
write := func(buf []byte) {
    if err != nil {
        return
    }
    _, err = w.Write(buf)
}
write(p0[a:b])
write(p1[c:d])
write(p2[e:f])
// and so on
if err != nil {
    return err
}
```

More cleaner:

```go
type errWriter struct {
    w   io.Writer
    err error
}

func (ew *errWriter) write(buf []byte) {
    if ew.err != nil {
        return
    }
    _, ew.err = ew.w.Write(buf)
}

ew := &errWriter{w: fd}
ew.write(p0[a:b])
ew.write(p1[c:d])
ew.write(p2[e:f])
// and so on
if ew.err != nil {
    return ew.err
}
```

