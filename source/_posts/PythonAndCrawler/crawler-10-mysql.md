---
categories:
- Crawler
date: 2019-02-19 22:49:55
tags: Crawler
title: Python之MySQL
---

# Python爬虫储存库的使用之MySQL

> 本文主要介绍 Python 下 MySQL 的使用（PyMySQL库）。



## 连接数据库

我们现在来连接位于本地的MySQL数据库，在这之前要先确定本地的MYSQL正在运行，且处于可访问的状态。

```python
import pymysql  # 导入库

db = pymysql.connect(host='localhost', user='*', password='***') # 连接数据库，还可以传入 port = 整数值 来指定端口，这里使用默认值（3306）。
cursor = db.cursor()    # 获取 MySQL 操作游标，利用操作游标才能执行SQL语句
cursor.execute('SELECT VERSION()')  # 执行SQL语句
data = cursor.fetchone()    # 获取第一条数据
print("Database Version:", data)
cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8")    # 新建一个用来爬虫的数据库
db.close()
```

## 创建表

```python
import pymysql

db = pymysql.connect(host="localhost", user="*", password="***", port=3306, db='spiders')    # 直接连接到刚才新建的数据库
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
cursor.execute(sql)
db.close()
```

## 插入数据

#### 使用一系列变量插入

```python
import pymysql

id = '2099133201'
name = 'Foo.Bar'
age = 101

db = pymysql.connect(host='localhost', user='*', password='***', db='spiders')
cursor = db.cursor()

sql = 'INSERT INTO students (id, name, age) VALUES (%s, %s, %s)'

try:
    cursor.execute(sql, (id, name, age))
    db.commit()
except:
    db.rollback()

db.close()
```

⚠️【注意】：
1. 我们在execute的时候并不必使用python的方法把字符串提前构造好，可以在需要插入的地方使用 `%s`，然后运行execute的时候把参数列表用一个元组传入即可，然而，这样做的重点是：**避免引号的问题！**。
2. 注意MySQL的事务机制，对于数据库的 **插入、更新、删除** 操作的标准模版是：

```python
try:
    cursor.execute(‘更改操作语句’)
    db.commit()
except:
    db.rollback()
```

#### 使用字典插入

```python
import pymysql

db = pymysql.connect(host='localhost', user='*', password='***', db='spiders')
cursor = db.cursor()

data = {
        'id': '2099133202',
        'name': 'Fuzz.Buzz',
        'age': '104'
        }

table = 'students'

keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = 'INSERT  INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)

try:
    if cursor.execute(sql, tuple(data.values())):
        print("Success!")
        db.commit()
except Exception as e:
    print('Failed:\n', e)
    db.rollback()

db.close()
```

在这个例子中如果不使用 `%s` + 传入 tuple 的那个方法动态构造语句，而直接用 `values = ', '.join(data.values())` 然后 `cursor.execute(sql)` 就会 Failed 了。

## 更新数据

#### 简单的数据更新

```python
sql = 'UPDATE students SET age = %s WHERE name = %s'

try:
    cursor.execute(sql, (999, 'Foo.Bar'))
    db.commit()
except:
    db.rollback()

db.close()
```

#### 更实用的字典更新

在实际数据抓取过程中，如果出现了重复数据，我们更希望的做法是更新数据：
如果重复则更新数据，如果数据不存在则插入数据，另外支持灵活的字典传值。

```python
import pymysql

db = pymysql.connect(host='localhost', user='*', password='***', db='spiders')
cursor = db.cursor()

data = {
        'id': '2099133203',
        'name': 'SomeOne',
        'age': '0'
        }

table = 'students'

keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
update = ', '.join([' {key} = %s'.format(key=key) for key in data])

sql += update

try:
    if cursor.execute(sql, tuple(data.values()) * 2):
        print("Success!")
        db.commit()
except Exception as e:
    print('Failed:\n', e)
    db.rollback()

db.close()
```

## 删除数据

```python
import pymysql

db = pymysql.connect(host='localhost', user='*', password='***', db='spiders')
cursor = db.cursor()

table = 'students'
condition = 'age > 200'

sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

db.close()
```

## 查询数据

```python
sql = 'SELECT * FROM students'

try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    one = cursor.fetchone()
    print('One:', one)
    results = cursor.fetchall()
    print('Results:', results)
    print('Results Type:', type(results))
    for row in results:
        print(row)
except:
    print('Error')
```