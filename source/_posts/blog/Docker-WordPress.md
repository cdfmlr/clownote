---
title: 用Docker部署WordPress
tag: Docker
---



# 用 Docker 部署 WordPress

## 前言

我们都爱用 WordPress，(几乎)一行代码都不用写，就能得到一个好看、实用的动态网站。

这东西用来~~敷衍~~帮助各种找你写奇怪小网站的朋友再好不过了。通常，帮朋友部署 WordPress 的这个场景下，你可以找朋友开一台新的服务器，初始化一套 LAMP，直接把 WordPress 给 wget 进去，就可以在你的浏览器里完成配置了。 有时候，比如您的朋友使用阿里云、百度云或是其他比较大的云服务商，您甚至可以直接初始化一个 WordPress 应用镜像，直接在浏览器里开始设置。

但是，前两天我需要在自己的服务器上部署一个 WordPress 服务。我这样的蒟蒻当然是无缘使用世界上最好的编程语言—— PHP 的啦。没有 PHP，还部署个屁的 WordPress。装一个 PHP 吧，平时也不用，还增加了安全风险，不划算。

还是有一台全新的 LAMP 服务器好啊，但不可能再买一台服务器吧。所以就想到了—— **Docker**，用容器去把它装起来就好了嘛。

想到就动手做，接下来我们就看看怎么用 Docker 部署 WordPress。

所以，现在，您的服务器或个人电脑上应该已经安装好了 Docker，在绝大多数非 Windows 的常规系统下，安装 Docker 就是几条简单的命令。

## 在继续之前......

根据法律规定，任何探讨容器的文章都必须附上满载集装箱的集装箱船的图片，正如下图所示：

![image-20200316163711817](https://tva1.sinaimg.cn/large/00831rSTgy1gcvuveckw8j30m80dfqfs.jpg)

（这个传统是从 [IBM Developer 上的这篇文章](https://www.ibm.com/developerworks/cn/cloud/library/cl-getting-started-docker-and-kubernetes/index.html) 学的，咱也不知道为什么，但遵纪守法的优秀共青团员当然是要遵守规定的啦。）

## 拉取镜像

WordPress 这么常用的东西当然是有现成的镜像的，我们就不用自己去建了。

果断拉一个 wordpress 镜像：

```bash
$ docker pull wordpress:latest
```

然后，您应该知道，WordPress 需要 MySQL。

这里我们有两种选择，一是使用宿主机或是其他任何服务器上的 MySQL 数据库；二是用一个 MySQL Docker 镜像。为了方便，同时也多练习 Docker 的使用，我们干脆再拉一个 mysql 镜像，让整套服务完全在 docker 里运行：

```bash
$ docker pull mysql:latest
```

注意，这篇文章写在 2020 年春，所以这里 `mysql:latest` 是 `MySQL V8.0.19 `。

## 启动服务

废话不多说，有了镜像，我们直接开服务：

```bash
$ docker run -d --privileged=true --name Mysql_Test -v /data/mysql:/var/lib/mysql -e MYSQL_DATABASE=wordpress -e MYSQL_ROOT_PASSWORD=233333  mysql
$ docker run -d --name Wordpress_Test -e WORDPRESS_DB_HOST=mysql -e WORDPRESS_DB_PASSWORD=233333 -p 2020:80 --link Mysql_Test:mysql wordpress
```

OK，这就是 Docker 的魔力，不用装 PHP，不用为了安全悉心考虑、大肆设置，前前后后就 4 个命令搞的！（当然，我只是开一个简单的小服务，基本没人用，所以也就几乎没有安全风险，但您在部署的时候还是要花点时间认真考虑安全问题的）

接下来就是在您的浏览器访问 `http://xxx:2020/wp-admin/index.php`，完成 “著名的” wordpress 5分钟安装了！

## 但是......

当你满心欢喜打开您的新网站时，，你会发现，wordpress 提醒你：连不上 mysql。（我忘截图了，它会写一堆英文告诉你这个事，你能看懂）

Google 会告诉您，这个问题是由于 mysql 8 的默认用户认证方式改了，wordpress 不认识。要解决不难，打开 mysql 设置一下，把认证方式改成 Wordpress 认识的样子就行：

```bash
$ docker exec -it Mysql_Test mysql -p
```

执行 mysql 命令：

```mysql
mysql> use mysql;
mysql> select host, user, plugin from user;
mysql> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '233333';
mysql> select host, user, plugin from user;
```

我们把 root 的 plugin 从 `caching_sha2_password` 改成了 `mysql_native_password`，这样就没问题了。

然后再次浏览器访问 `http://xxx:2020/wp-admin/index.php`，这次就应该是 “著名的” wordpress 5分钟安装了，您可以自行完成 :)



