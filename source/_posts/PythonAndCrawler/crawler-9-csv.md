---
categories:
- Crawler
date: 2019-02-18 22:49:55
tags: Crawler
title: Python之CSV
---

# Python爬虫储存库的使用之CSV

> 本文主要介绍储存库 CSV 的使用。



## CSV 简介

**CSV**（Comma-Separated Values），**逗号分隔值**，或**字符分隔值**，以纯文本形式储存表格数据。一个CSV文件的内容如下：

```csv
id,name,age
0,foo,10
1,bar,11
2,foobar,100
```

## Python 写 CSV

#### 列表写入 CSV

```python
import csv

d = [['0', 'foo', '10'], ['1', 'bar', '11'], ['2', 'foobar', '100']]
with open('data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)    # 要改分隔符，可以传入`delimiter='分隔符'`
    
    writer.writerow(['id', 'name', 'age'])  # 写一行，传入list
    writer.writerows(d)     # 写入多行，传入二维list
```

⚠️【注意】写中文的时候，要在open的时候传入 `encoding='utf-8'`，防止乱码。

#### 字典写入 CSV

```python
import csv

with open('data.csv', 'w') as csvfile:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '9', 'name': 'fuzz', 'age': '666'})
```

## Python 读 CSV

#### 用 CSV库 读取

```python
import csv

with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(type(row), row)
```

从结果中可以看到，读取出来的是各行的list。

#### 用 Pandas库 读取

```python
import pandas as pd

df = pd.read_csv('data.csv')
print(df)
print(type(df))
```