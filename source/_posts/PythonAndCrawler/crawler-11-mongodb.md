---
title: Python之MongoDB
date: 2019-02-20 22:49:55
tags: Crawler
categories:
	- Crawler
---

# Python爬虫储存库的使用之MongoDB

> 本文主要介绍 Python 下 MongoDB 的使用（PyMongo库）。



## MongoDB 简介

> MongoDB 是由 C++ 语言编写的非关系型数据库，是一个基于分布式文件存储的开源数据库系统，其内容存储形式类似 Json 对象，它的字段值可以包含其他文档，数组及文档数组，非常灵活。

在使用前要先确定 MongoDB 安装好，并已经开启了服务：

```bash
$ brew services start mongodb
$ sudo mongod
$ mongo
```

以上三条命令开启了 MongoDB 的服务，并打开客户端。

## 连接数据库

```python
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
# client = pymongo.MongoClient('mongodb://localhost:27017/')    效果是一样的
```

## 指定数据库

```python
db = client.test
# db = client['test']   等价
```

## 指定集合

```python
collection = db.students    # 还是可以用`['']`来取
```

## 插入数据

插入数据有3种方法：

* `collection.insert()`：插入一个或多个数据，传入一个对象则插入一个，传入一个对象的list可以插入多个（官方不推荐使用）；
* `collection.insert_one()`：插入一个数据，传入一个dict；
* `collection.insert_many()`：插入多个数据，传入一个dict的list；


```python
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students

student1 = {
        'id': '2099133201',
        'name': 'Foo',
        'age': 10,
        'gender': 'male'
        }

student2 = {
        'id': '2099133202',
        'name': 'Bar',
        'age': 11,
        'gender': 'male'
        }

student3 = {
        'id': '2099133203',
        'name': 'Moo',
        'age': 12,
        'gender': 'female'
        }

result0 = collection.insert_one(student1)
result1 = collection.insert_many([student2, student3])
print(result0, result0.inserted_id, sep='\n')
print(result1, result1.inserted_ids, sep='\n')
```

## 查询

查询使用如下方法：

* `find_one()`：查得单个结果
* `find()`：返回一个结果的生成器

如果查询的结果不存在，会返回 `None`。

```python
res_of_find = collection.find()     # 得到所有数据
print('find:\n', res_of_find)
for i in res_of_find:
    print(i)

res_of_findone = collection.find_one({'name': 'Foo'})   # 通过传入一组字典键值来查询
print('find_one:\n', res_of_findone)
```

如果要通过 MongoDB 为每条数据添加的 `_id` 属性来查询，需要这样做：

```python
res_of_find_by_id = collection.find_one({'_id': ObjectId('5c78e0c6b92a4e5f17d70cfa')})
print('find by id:\n', res_of_find_by_id)
```

如果要查询 “年龄大于10” 的数据：

```python
collection.find({'age': {'$gt': 10}})
```

这里查询条件的value变成了一个符号加运算值的字典，可用的操作如下：

| 符号   | 含义    | 示例                          |
|------|-------|-----------------------------|
| `$lt`  | 小于    | `{'age': {'$lt': 20}}`        |
| `$gt`  | 大于    | `{'age': {'$gt': 20}}`        |
| `$lte` | 小于等于  | `{'age': {'$lte': 20}}`       |
| `$gte` | 大于等于  | `{'age': {'$gte': 20}}`       |
| `$ne`  | 不等于   | `{'age': {'$ne': 20}}`        |
| `$in`  | 在范围内  | `{'age': {'$in': [20, 23]}}`  |
| `$nin` | 不在范围内 | `{'age': {'$nin': [20, 23]}}` |

还有多种查询方式：

```python
collection.find({'name': {'$regex': '^M.*'}})
```

常用操作如下：

| 符号      | 含义     | 示例                                                | 示例含义                   |
|---------|--------|---------------------------------------------------|------------------------|
| `$regex`  | 匹配正则   | `{'name': {'$regex': '^M.*'}}`                      | name 以 M开头             |
| `$exists` | 属性是否存在 | `{'name': {'$exists': True}}`                       | name 属性存在              |
| `$type`   | 类型判断   | `{'age': {'$type': 'int'}}`                         | age 的类型为 int           |
| `$mod`    | 数字模操作  | `{'age': {'$mod': [5, 0]}}`                         | 年龄模 5 余 0              |
| `$text`   | 文本查询   | `{'$text': {'$search': 'Mike'}}`                    | text 类型的属性中包含 Mike 字符串 |
| `$where`  | 高级条件查询 | `{'$where': 'obj.fans_count == obj.follows_count'}` | 自身粉丝数等于关注数             |

#### 去掉 `_id`

Mongo 返回的数据中会有一项 `_id` （Mongo自动加入的用来识别对象的字段），我们常不想看它 ，可以在查询时加入对结果的过滤：

```python
collection.find(projection={'_id': False})
```

## 计数

要统计查询到的结果条数，可以直接调用查询结果的 `count()` 方法。



```python
collection.find({'age': {'$gt': 0}}).count()
```

---

P.S. 一点题外话：
> 写到这里，又是一个熄灯后的美丽夜晚。调暗屏幕背光，小心翼翼地捧起那蠢蠢欲动的白色樱桃机械键盘，把它安置到光明之外，避开红绿蓝的纷争。趁着这五彩缤纷的黑暗，把下一行让人迷醉的代码，作为虔诚的礼物，送给饥饿良久的编译器。静待她施展动人的魔法，变出一串没有间断点的二进制位向量，在 0 和 1 的排列组合中，光影流转，似现星河鹭起，似有高山流水。在心驰神往的一瞬，不妨再分个神，欣赏开和关之间，一扇回到未来的古朴大门。

---

## 排序

我们可以通过调用 `sort()` 方法，传入用来排序的字段、升降序的标志即可对查询的结果排序。

* `pymongo.ASCENDING`：指定升序；
* `pymongo.DESCENDING`：指定降序；

```python
r = collection.find().sort('name', pymongo.ASCENDING)
for i in r:
    print(i['name'])
```

## 偏移

偏移：偏移x个元素，即忽略（跳过）前面的x个元素，得到第x+1开始个元素。
这个操作调用查询结果的 `skip()` 方法。

```python
r = collection.find().skip(2)
print([i for i in r])
```

## 更新

更新与插入类似，主要有三种方法：

* `update()`：更新一条或多条数据，不推荐使用
* `update_one()`：更新一条数据
* `update_many()`：更新多条数据

```python
condition = {'name': 'Foo'}
student = collection.find_one(condition)
student['age'] = 25
result = collection.update(condition, {'$set': student})
print(result)
```

这里，我们先查询出了目标条目，然后把它修改成了新的数据，调用update，传入查询条件和一个代表操作的字典完成更新。
常用的操作有:

* `$set`: `{'$set': value}`: 把value中有的属性更新成新的
* `$inc`: `{'$inc': {'age': 1}}`: 把age加1

## 删除

也是有三个：`remove()`，`delete_one()`，`delete_many()`

```python
collection.remove({'name': 'Kevin'})
```

## 更多

更完善的MongoDB还在官网等待我们去学习：[官方文档🔗链接](http://api.mongodb.com/python/current/api/pymongo/)。