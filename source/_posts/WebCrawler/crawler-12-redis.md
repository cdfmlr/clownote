---
title: Python之Redis
date: 2019-02-21 22:49:55
tags: Crawler
categories:
	- Crawler
---

# Python爬虫储存库的使用之Redis

> 本文主要介绍 Python 下 Redis 的使用（RedisPy库）。



## Redis 简介

> Redis 是一个**基于内存**的高效的键值型非关系型数据库，存取效率极高，而且支持多种存储数据结构。

RedisPy 库提供两个类 Redis 和 StrictRedis 用于实现Redis 的命令操作。
推荐使用的是 StrictRedis，它实现了绝大部分Redis的命令，参数也一一对应。
Redis 主要用来兼容旧版本。

## 连接 Redis

首先需要确定正确在本地安装了Redis，并开启了服务。

#### 使用 StrictRedis 连接
```python
from redis import StrictRedis

redis = StrictRedis(host='localhost', port=6379, db=0, password=None)
# 这里使用的这几个参数和默认值是等效的，即可以直接使用 `StrictRedis()` 来代替。

redis.set('name', 'Foo')    # 设置了一个键值对
print(redis.get('name'))    # 获取一个数据
```

#### 使用 ConnectionPool 连接

```python
from redis import StrictRedis, ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0, password=None)
redis = StrictRedis(connection_pool=pool)

redis.set('age', 100)
print(redis.get('age'))
```

使用 ConnectionPool 还可以用 URL 来构建：

有三种可用的 URL 格式：

* Redis TCP 连接：`redis://[:password]@host:port/db`
* Redis TCP+SSL 连接：`rediss://[:password]@host:port/db`
* Redis Unix Socket连接：`unix://[:password]@/path/to/socket.sock?db=db`

使用的姿势如下：

```python
from redis import StrictRedis, ConnectionPool
# 注意多导入了一个ConnectionPool。

url = 'redis://@localhost:6379/0'
pool = ConnectionPool.from_url(url)
redis = StrictRedis(connection_pool=pool)

redis.set("test", 'test')
r = redis.get('test')
print(type(r), r, sep='\n')
```

## Key 操作

这是一些常用的对 key 的操作，通过使用如 `redis.exists('neme')` 这样的语句来使用他们：

| 方法                 | 作用                      | 参数说明                  | 示例                               | 示例说明               | 示例结果      |
|--------------------|-------------------------|-----------------------|----------------------------------|--------------------|-----------|
| exists(name)       | 判断一个key是否存在             | name: key名            | redis.exists('name')             | 是否存在name这个key      | 1      |
| delete(name)       | 删除一个key                 | name: key名            | redis.delete('name')             | 删除name这个key        | 1         |
| type(name)         | 判断key类型                 | name: key名            | redis.type('name')               | 判断name这个key类型      | b'string' |
| keys(pattern)      | 获取所有符合规则的key            | pattern: 匹配规则         | redis.keys('n*')                 | 获取所有以n开头的key       | [b'name'] |
| randomkey()        | 获取随机的一个key              |                       | randomkey()                      | 获取随机的一个key         | b'name'   |
| rename(src, dst)   | 将key重命名                 | src: 原key名 dst: 新key名 | redis.rename('name', 'nickname') | 将name重命名为nickname  | True      |
| dbsize()           | 获取当前数据库中key的数目          |                       | dbsize()                         | 获取当前数据库中key的数目     | 100       |
| expire(name, time) | 设定key的过期时间，单位秒          | name: key名 time: 秒数   | redis.expire('name', 2)          | 将name这key的过期时间设置2秒 | True      |
| ttl(name)          | 获取key的过期时间，单位秒，-1为永久不过期 | name: key名            | redis.ttl('name')                | 获取name这key的过期时间    | -1        |
| move(name, db)     | 将key移动到其他数据库            | name: key名 db: 数据库代号  | move('name', 2)                  | 将name移动到2号数据库      | True      |
| flushdb()          | 删除当前选择数据库中的所有key        |                       | flushdb()                        | 删除当前选择数据库中的所有key   | True      |
| flushall()         | 删除所有数据库中的所有key          |                       | flushall()                       | 删除所有数据库中的所有key     | True      |

## String 操作

String 是 Redis 中最基本的Value储存方式，他的操作如下，

| 方法                            | 作用                                           | 参数说明                                       | 示例                                                            | 示例说明                               | 示例结果                |
|-------------------------------|----------------------------------------------|--------------------------------------------|---------------------------------------------------------------|------------------------------------|---------------------|
| set(name, value)              | 给数据库中key为name的string赋予值value                 | name: key名 value: 值                        | redis.set('name', 'Bob')                                      | 给name这个key的value赋值为Bob             | True                |
| get(name)                     | 返回数据库中key为name的string的value                  | name: key名                                 | redis.get('name')                                             | 返回name这个key的value                  | b'Bob'              |
| getset(name, value)           | 给数据库中key为name的string赋予值value并返回上次的value      | name: key名 value: 新值                       | redis.getset('name', 'Mike')                                  | 赋值name为Mike并得到上次的value             | b'Bob'              |
| mget(keys, *args)             | 返回多个key对应的value                              | keys: key的列表                               | redis.mget(['name', 'nickname'])                              | 返回name和nickname的value              | [b'Mike', b'Miker'] |
| setnx(name, value)            | 如果key不存在才设置value                             | name: key名                                 | redis.setnx('newname', 'James')                               | 如果newname这key不存在则设置值为James         | 第一次运行True，第二次False  |
| setex(name, time, value)      | 设置可以对应的值为string类型的value，并指定此键值对应的有效期         | name: key名 time: 有效期 value: 值              | redis.setex('name', 1, 'James')                               | 将name这key的值设为James，有效期1秒           | True                |
| setrange(name, offset, value) | 设置指定key的value值的子字符串                          | name: key名 offset: 偏移量 value: 值            | redis.set('name', 'Hello') redis.setrange('name', 6, 'World') | 设置name为Hello字符串，并在index为6的位置补World | 11，修改后的字符串长度        |
| mset(mapping)                 | 批量赋值                                         | mapping: 字典                                | redis.mset({'name1': 'Durant', 'name2': 'James'})             | 将name1设为Durant，name2设为James        | True                |
| msetnx(mapping)               | key均不存在时才批量赋值                                | mapping: 字典                                | redis.msetnx({'name3': 'Smith', 'name4': 'Curry'})            | 在name3和name4均不存在的情况下才设置二者值         | True                |
| incr(name, amount=1)          | key为name的value增值操作，默认1，key不存在则被创建并设为amount   | name: key名 amount:增长的值                     | redis.incr('age', 1)                                          | age对应的值增1，若不存在则会创建并设置为1            | 1，即修改后的值            |
| decr(name, amount=1)          | key为name的value减值操作，默认1，key不存在则被创建并设置为-amount | name: key名 amount:减少的值                     | redis.decr('age', 1)                                          | age对应的值减1，若不存在则会创建并设置为-1           | -1，即修改后的值           |
| append(key, value)            | key为name的string的值附加value                     | key: key名                                  | redis.append('nickname', 'OK')                                | 向key为nickname的值后追加OK               | 13，即修改后的字符串长度       |
| substr(name, start, end=-1)   | 返回key为name的string的value的子串                   | name: key名 start: 起始索引 end: 终止索引，默认-1截取到末尾 | redis.substr('name', 1, 4)                                    | 返回key为name的值的字符串，截取索引为1-4的字符       | b'ello'             |
| getrange(key, start, end)     | 获取key的value值从start到end的子字符串                  | key: key名 start: 起始索引 end: 终止索引            | redis.getrange('name', 1, 4)                                  | 返回key为name的值的字符串，截取索引为1-4的字符       | b'ello'             |

## List 操作

List 是 Redis 中 value 为列表的一种数据。

| 方法                       | 作用                                          | 参数说明                               | 示例                               | 示例说明                                         | 示例结果               |
|--------------------------|---------------------------------------------|------------------------------------|----------------------------------|----------------------------------------------|--------------------|
| rpush(name, *values)     | 在key为name的list尾添加值为value的元素，可以传多个           | name: key名 values: 值               | redis.rpush('list', 1, 2, 3)     | 给list这个key的list尾添加1、2、3                      | 3，list大小           |
| lpush(name, *values)     | 在key为name的list头添加值为value的元素，可以传多个           | name: key名 values: 值               | redis.lpush('list', 0)           | 给list这个key的list头添加0                          | 4，list大小           |
| llen(name)               | 返回key为name的list的长度                          | name: key名                         | redis.llen('list')               | 返回key为list的列表的长度                             | 4                  |
| lrange(name, start, end) | 返回key为name的list中start至end之间的元素              | name: key名 start: 起始索引 end: 终止索引   | redis.lrange('list', 1, 3)       | 返回起始为1终止为3的索引范围对应的list                       | [b'3', b'2', b'1'] |
| ltrim(name, start, end)  | 截取key为name的list，保留索引为start到end的内容           | name:key名 start: 起始索引 end: 终止索引    | ltrim('list', 1, 3)              | 保留key为list的索引为1到3的元素                         | True               |
| lindex(name, index)      | 返回key为name的list中index位置的元素                  | name: key名 index: 索引               | redis.lindex('list', 1)          | 返回key为list的列表index为1的元素                      | b'2'               |
| lset(name, index, value) | 给key为name的list中index位置的元素赋值，越界则报错           | name: key名 index: 索引位置 value: 值    | redis.lset('list', 1, 5)         | 将key为list的list索引1位置赋值为5                      | True               |
| lrem(name, count, value) | 删除count个key的list中值为value的元素                 | name: key名 count: 删除个数 value: 值    | redis.lrem('list', 2, 3)         | 将key为list的列表删除2个3                            | 1，即删除的个数           |
| lpop(name)               | 返回并删除key为name的list中的首元素                     | name: key名                         | redis.lpop('list')               | 返回并删除名为list的list第一个元素                        | b'5'               |
| rpop(name)               | 返回并删除key为name的list中的尾元素                     | name: key名                         | redis.rpop('list')               | 返回并删除名为list的list最后一个元素                       | b'2'               |
| blpop(keys, timeout=0)   | 返回并删除名称为在keys中的list中的首元素，如果list为空，则会一直阻塞等待  | keys: key列表 timeout: 超时等待时间，0为一直等待 | redis.blpop('list')              | 返回并删除名为list的list的第一个元素                       | [b'5']             |
| brpop(keys, timeout=0)   | 返回并删除key为name的list中的尾元素，如果list为空，则会一直阻塞等待   | keys: key列表 timeout: 超时等待时间，0为一直等待 | redis.brpop('list')              | 返回并删除名为list的list的最后一个元素                      | [b'2']             |
| rpoplpush(src, dst)      | 返回并删除名称为src的list的尾元素，并将该元素添加到名称为dst的list的头部 | src: 源list的key dst: 目标list的key     | redis.rpoplpush('list', 'list2') | 将key为list的list尾元素删除并返回并将其添加到key为list2的list头部 | b'2'               |

## Set 、Sorted Set操作

详见 [Redis教程](https://germey.gitbooks.io/python3webspider/content/5.3.2-Redis存储.html)。

## Hash 操作

Redis 中可以用name指定一个哈希表的名称，然后表内存储了各个键值对。

| 方法                           | 作用                              | 参数说明                             | 示例                                             | 示例说明                            | 示例结果                                                           |
|------------------------------|---------------------------------|----------------------------------|------------------------------------------------|---------------------------------|----------------------------------------------------------------|
| hset(name, key, value)       | 向key为name的hash中添加映射             | name: key名 key: 映射键名 value: 映射键值 | hset('price', 'cake', 5)                       | 向key为price的hash中添加映射关系，cake的值为5 | 1，即添加的映射个数                                                     |
| hsetnx(name, key, value)     | 向key为name的hash中添加映射，如果映射键名不存在   | name: key名 key: 映射键名 value: 映射键值 | hsetnx('price', 'book', 6)                     | 向key为price的hash中添加映射关系，book的值为6 | 1，即添加的映射个数                                                     |
| hget(name, key)              | 返回key为name的hash中field对应的value   | name: key名 key: 映射键名             | redis.hget('price', 'cake')                    | 获取key为price的hash中键名为cake的value  | 5                                                              |
| hmget(name, keys, *args)     | 返回key为name的hash中各个键对应的value     | name: key名 keys: 映射键名列表          | redis.hmget('price', ['apple', 'orange'])      | 获取key为price的hash中apple和orange的值 | [b'3', b'7']                                                   |
| hmset(name, mapping)         | 向key为name的hash中批量添加映射           | name: key名 mapping: 映射字典         | redis.hmset('price', {'banana': 2, 'pear': 6}) | 向key为price的hash中批量添加映射          | True                                                           |
| hincrby(name, key, amount=1) | 将key为name的hash中映射的value增加amount | name: key名 key: 映射键名 amount: 增长量 | redis.hincrby('price', 'apple', 3)             | key为price的hash中apple的值增加3       | 6，修改后的值                                                        |
| hexists(name, key)           | key为namehash中是否存在键名为key的映射      | name: key名 key: 映射键名             | redis.hexists('price', 'banana')               | key为price的hash中banana的值是否存在     | True                                                           |
| hdel(name, *keys)            | key为namehash中删除键名为key的映射        | name: key名 key: 映射键名             | redis.hdel('price', 'banana')                  | 从key为price的hash中删除键名为banana的映射  | True                                                           |
| hlen(name)                   | 从key为name的hash中获取映射个数           | name: key名                       | redis.hlen('price')                            | 从key为price的hash中获取映射个数          | 6                                                              |
| hkeys(name)                  | 从key为name的hash中获取所有映射键名         | name: key名                       | redis.hkeys('price')                           | 从key为price的hash中获取所有映射键名        | [b'cake', b'book', b'banana', b'pear']                         |
| hvals(name)                  | 从key为name的hash中获取所有映射键值         | name: key名                       | redis.hvals('price')                           | 从key为price的hash中获取所有映射键值        | [b'5', b'6', b'2', b'6']                                       |
| hgetall(name)                | 从key为name的hash中获取所有映射键值对        | name: key名                       | redis.hgetall('price')                         | 从key为price的hash中获取所有映射键值对       | {b'cake': b'5', b'book': b'6', b'orange': b'7', b'pear': b'6'} |

## RedisDump

RedisDump 提供了 Redis 数据的导入和导出功能。

RedisDump 提供两个可执行命令：

* `redis-dump` 用于 导出 数据；详见 `redis-dump -h`
    * e.g. `$ redis-dump -u :foobared@localhost:6379 > ./redis_data.jl`
* `redis-load` 用于 导入 数据；详见 `redis-load -h`
    * e.g. `$ redis-load -u :foobared@localhost:6379 < redis_data.json`
    * 等价于`$ cat redis_data.json | redis-load -u :foobared@localhost:6379`


