---
title: SQL 基本使用
---

# SQL 基本使用

最近半年多一直都是用 MongoDB，好久没 SQL 了。

这学期有个数据库课，，上了几节课了，还没看过课本😂，但想来后面肯定是学 SQL，要复习一下了。

所以想在下一个项目里用用 SQL，所以先来复习一下基本的 SQL CRUD。

## SQL 基本概念

SQL：Structured Query Language，结构化查询语言，访问和处理数据库用的。

SQL 有这几种能力：

- **DDL**：Data Definition Language，定义数据的：建表、删表、修改表结构的；
- **DQL**：Data Query Language，查询数据的；
- **DML**：Data Manipulation Language，修改数据的：添加、删除、更新数据的；

## SQL 语法特点

- 语句末要写分号

- 关键字不区分大小写；

  表名、列名、(可能)区分大小写。

  一般情况下，我们可以把 SQL 关键字大写，表名、列名等使用小写。

- 文本字段用单引号包裹（e.g. `'String'`），数值字段不能加引号。

## SQL 数据类型

| 名称         | 类型           | 说明                                                         |
| :----------- | :------------- | :----------------------------------------------------------- |
| INT          | 整型           | 4字节整数类型，范围约+/-21亿                                 |
| BIGINT       | 长整型         | 8字节整数类型，范围约+/-922亿亿                              |
| REAL         | 浮点型         | 4字节浮点数，范围约+/-1038                                   |
| DOUBLE       | 浮点型         | 8字节浮点数，范围约+/-10308                                  |
| DECIMAL(M,N) | 高精度小数     | 由用户指定精度的小数，例如，DECIMAL(20,10)表示一共20位，其中小数10位，通常用于财务计算 |
| CHAR(N)      | 定长字符串     | 存储指定长度的字符串，例如，CHAR(100)总是存储100个字符的字符串 |
| VARCHAR(N)   | 变长字符串     | 存储可变长度的字符串，例如，VARCHAR(100)可以存储0~100个字符的字符串 |
| BOOLEAN      | 布尔类型       | 存储True或者False                                            |
| DATE         | 日期类型       | 存储日期，例如，2018-06-22                                   |
| TIME         | 时间类型       | 存储时间，例如，12:20:59                                     |
| DATETIME     | 日期和时间类型 | 存储日期+时间，例如，2018-06-22 12:20:59                     |

## SQL 基本语句

### DDL

#### 库

##### - CREATE

> `CREATE DATABASE` 用来建数据库。

```sql
CREATE DATABASE database_name;
```

##### - DROP

> `DROP DATABASE` 用来删库。

```sql
DROP DATABASE database_name;
```

##### - USE

> `USE` 用来选择要操作的数据库。

```sql
USE database_name;
```

#### 表

##### - CREATE

> `CREATE TABLE` 创建数据表。

```mysql
CREATE TABLE [IF NOT EXISTS] table_name (
    `column_name` column_type,
    `column_name` column_type,
    ...,
    PRIMARY KEY ( `key_column_name` )
)[ENGINE=InnoDB DEFAULT CHARSET=utf8];
```

注：`[]`里的是可选的。

##### - DROP

> `DROP TABLE` 用来删除表。

```sql
DROP TABLE table_name ;
```

### DQL

#### SELECT

>  `SELECT` 语句用于从数据库中选取数据。

SELECT 从数据库中选取字段，把结构放到一个结果表中，成为结果集。

```sql
SELECT column_name,column_name
FROM table_name;
```

也可以：

```sql
SELECT *
FROM table_name;
```

#### SELECT DISTINCT

> `SELECT DISTINCT` 语句用于返回列里唯一不同的值

SELECT DISTINCT 是把所选列去重输出，给你看这一列里有多少种不同情况的，如果查询的是多列会输出每一种不同组合。

```sql
SELECT DISTINCT column_name,column_name
FROM table_name;
```

比如一张放了全国人名的表，`SELECT DISTINCT sex FROM people` 会输出 `男`，`女` 两项）

再举个🌰：

```mysql
mysql> SELECT * FROM userinfo;
+-----+----------+-------------+------------+
| uid | username | department  | created    |
+-----+----------+-------------+------------+
|   2 | Foo      | Bar         | 2020-02-20 |
|   3 | Fuzz     | Bar         | 2020-02-09 |
|   4 | Joe      | Development | 2020-02-02 |
|   5 | Ann      | Development | 2020-02-20 |
+-----+----------+-------------+------------+
4 rows in set (0.00 sec)

mysql> SELECT DISTINCT department FROM userinfo;
+-------------+
| department  |
+-------------+
| Bar         |
| Development |
+-------------+
2 rows in set (0.00 sec)

mysql> SELECT DISTINCT department,created FROM userinfo;
+-------------+------------+
| department  | created    |
+-------------+------------+
| Bar         | 2020-02-20 |
| Bar         | 2020-02-09 |
| Development | 2020-02-02 |
| Development | 2020-02-20 |
+-------------+------------+
4 rows in set (0.00 sec)
```

#### WHERE

> `WHERE` 子句用于过滤记录，提取满足指定条件的记录。

```sql
SELECT column_name,column_name
FROM table_name
WHERE column_name operator value;
```

operator 运算符有以下几种：

| 运算符  | 描述                                                       |
| :------ | :--------------------------------------------------------- |
| =       | 等于                                                       |
| <>      | 不等于。**注释：**在 SQL 的一些版本中，该操作符可被写成 != |
| >       | 大于                                                       |
| <       | 小于                                                       |
| >=      | 大于等于                                                   |
| <=      | 小于等于                                                   |
| BETWEEN | 在某个范围内                                               |
| LIKE    | 搜索某种模式                                               |
| IN      | 指定针对某个列的多个可能值                                 |

栗子🌰（还是上面那个例子的表）：

```sql
mysql> SELECT * FROM userinfo WHERE department='Bar';
+-----+----------+------------+------------+
| uid | username | department | created    |
+-----+----------+------------+------------+
|   2 | Foo      | Bar        | 2020-02-20 |
|   3 | Fuzz     | Bar        | 2020-02-09 |
+-----+----------+------------+------------+
2 rows in set (0.00 sec)
```

#### AND & OR

> `AND` & `OR` 运算符用于基于一个以上的条件对记录进行过滤（用在 WHERE 里）。

e.g.

```sql
mysql> SELECT * FROM userinfo WHERE department='Bar' AND created='2020-02-20';
+-----+----------+------------+------------+
| uid | username | department | created    |
+-----+----------+------------+------------+
|   2 | Foo      | Bar        | 2020-02-20 |
+-----+----------+------------+------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM userinfo WHERE department='Bar' OR created='2020-02-20';
+-----+----------+-------------+------------+
| uid | username | department  | created    |
+-----+----------+-------------+------------+
|   2 | Foo      | Bar         | 2020-02-20 |
|   3 | Fuzz     | Bar         | 2020-02-09 |
|   5 | Ann      | Development | 2020-02-20 |
+-----+----------+-------------+------------+
3 rows in set (0.00 sec)
```

#### ORDER BY

> `ORDER BY` 用于对结果集进行排序。

ORDER BY 默认按照**升序**(ASC)对记录进行排序。降序要使用 `DESC` 关键字。

```sql
SELECT column_name,column_name
FROM table_name
ORDER BY column_name,column_name ASC|DESC;
```

#### LIMIT

> `LIMIT` 或 `ROWNUM` 或 `TOP` 用于规定要返回的记录的数目。

TOP、LIMIT、ROWNUM 是不同家的数据库里不同的写法。

- `LIMIT`：MySQL

  ```sql
  SELECT column_name(s)
  FROM table_name
  LIMIT number;
  ```

- `ROWNUM`：Oracle

  ```sql
  SELECT column_name(s)
  FROM table_name
  WHERE ROWNUM <= number;
  ```

- `TOP`：SQL Server，Access

  ```sql
  SELECT TOP number|percent column_name(s)
  FROM table_name;
  ```

### DML

#### INSERT INTO

> `INSERT INTO` 语句用于向表中插入新记录。

```sql
INSERT INTO table_name (column1,column2,column3,...)
VALUES (value1,value2,value3,...);
```

或不指定要插入数据的列名，需要列出插入行的每一列数据

```sql
INSERT INTO table_name
VALUES (value1,value2,value3,...);
```

e.g.

```sql
mysql> INSERT INTO userinfo (username, department, created) VALUES ('WhoKnown','Market','2001-10-12');

Query OK, 1 row affected (0.03 sec)

mysql> SELECT * FROM userinfo WHERE created < '2020-01-01';
+-----+----------+------------+------------+
| uid | username | department | created    |
+-----+----------+------------+------------+
|   6 | WhoKnown | Market     | 2001-10-12 |
+-----+----------+------------+------------+
1 row in set (0.01 sec)
```

#### UPDATE

> `UPDATE` 语句用于更新表中已存在的记录。

```sql
UPDATE table_name
SET column1=value1,column2=value2,...
WHERE some_column=some_value;
```

如果没写 WHERE，表示更新**所有记录**。

e.g.

```sql
mysql> UPDATE userinfo 
    -> SET username='Jack'
    -> WHERE uid=6;
Query OK, 1 row affected (0.03 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM userinfo WHERE created < '2020-01-01';
+-----+----------+------------+------------+
| uid | username | department | created    |
+-----+----------+------------+------------+
|   6 | Jack     | Market     | 2001-10-12 |
+-----+----------+------------+------------+
1 row in set (0.00 sec)
```

#### DELETE

> `DELETE` 用于删除表中的记录。

```sql
DELETE FROM table_name
WHERE some_column=some_value;
```

⚠️注意，漏写 WHERE 就**删除所有记录**了（不如 `sudo rm -rf /*` 得劲🤪）。


