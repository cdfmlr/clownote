---
title: Python3爬虫环境配置
date: 2019-02-09 22:49:55
tags: Crawler
categories:
	- Crawler
---

# 开发环境配置

> 本文主要介绍 Python 3 网络爬虫 所需要的软件的安装及配置。



## 开发环境

* 我们在 `macOS X` 上使用 `Python 3.7` 来开发爬虫。


## **请求库** 安装

网络爬虫，首先要获取网络上的数据，即抓取页面，这就需要我们模拟浏览器向服务器发出请求。
我们可以安装一些 Python 库来帮助我们比较容易地完成这个操作。

让我们来安装它们吧：

* **requests** : 网络请求: 
    * `pip3 inastal requests`

* **Selenium** : 自动测试工具（驱动浏览器执行特定的动作，如点击、下拉等 操作 ）:
    *  `pip3 install selenium`

* **ChromeDriver** : 用 *Chrome* 与 Selenium 配合工作:
    * 安装 Chrome 浏览器
    * 在 Chrome 菜单（“···”） -> “关于 Google Chrome”，查看当前Chrome版本。
    * 从 [ChromeDriver官网](http://chromedriver.chromium.org/) 下载配对 Chrome 版本的 ChromeDriver（⚠️【注意】ChromeDriver 一定要与 Chrome 的版本兼容！）。
    * 解压下载的文件，得到可执行文件，将其加入环境变量（可以简单地把它放到环境变量中有的目录下）。

* **GeckoDriver**: 用 *Firefox* 与 Selenium 配合工作:
    * *暂时并没有使用 Firefox，所以没有安装这个😂。*

* ~~**PhantomJS**: 还是配合 Selenium 工作的:
    * (PhantomJS 简介)PhantomJS是一个无界面的、可脚本编程的 WebKit浏览器引擎，它原生支持多种 Web标准: DOM操作、 css选择器、 JSON、 Canvas以及 SVG。Selenium支持 PhantomJS，这样在运行的时候就不会再弹出 一个浏览器了 。 而且 PhantomJS 的运行效率也很高，还支持各种参数配置，使用非常方便。
    * 从 [PhantomJS官网](http://phantomjs.org) 下载 PhantomJS。
    * 将下载得到的目录中的 可执行文件 加入环境变量。
    * ⚠️【注意】在 2018年3月4日， PhantomJS 宣布[暂停开发](https://github.com/ariya/phantomjs/issues/15344)了！Selenium 也不再赞同使用 PhantomJS了。~~

* **aiohttp**: 一个异步的 Web 服务库（相比之下 `requests` 是阻塞式的）:
    * `pip3 install aiohttp`

* **cchardet**: 字符编码检测库（aiohttp官方推荐安装的）:
    * `pip3 install cchardet`

* **aiodns**: 加速 DNS 的解析库（aiohttp官方推荐安装的）:
    * `pip3 install aiodns`

## **解析库** 安装

抓取网页之后，我们就要从中提取有用的信息了。
我们当然可以使用令人望而生畏的 **正则表达式** 来完成这一操作；
不过，有很多强大的库可以帮助我们更优雅地处理这一问题。

下面，我们将安装这些库：

* **lxml**: 一个 Python 的 HTML、XML 解析库，支持XPath:
    * `pip3 install lxml`
    * 这个库安装常有问题，主要可能是缺少必要的库，不同的平台，解决办法差异太大，应自行Google。

* **Beautiful Soup**: 一个 Python 的 HTML、XML 解析库，拥有强大的API和多种解析方式:
    * `pip3 install beautifulsoup4`
    * ⚠️【注意】Beautiful Soup 安装好之后的库名是`bs4`，所以 import 的时候是`import bs4`。

* **pyquery**: 一个提供了类似于 jQuery 的语法的 HTML 解析工具，支持 CSS 选择器:
    * `pip3 install pyquery`

* **tesserocr**: 一个 OCR 库，用来处理验证码:
    * tesserocr 是对 tesseract 的 Python API 封装，故要先安装 **tesseract**
        * `$ brew install imagemagick`
        * `$ brew install tesseract`
    * `pip3 install tesserocr pillow`
    * ⚠️ 这时，在 Mac 上试图 `>>> import tesserocr` 会遇到 `!strcmp(locale, "C"):Error:Assert failed:in file baseapi.cpp` 的断言失败，导致 `Illegal instruction: 4` 使 Python 错误退出。
    * 要解决上述问题，可以通过 `$ export LC_ALL=C`（临时性），或把 `export LC_ALL=C` 写入 `~/.bashrc`（永久性）。

## 数据库 安装

* **MySQL**: 关系型数据库:
    * `$ brew install mysql`

* **MongoDB**: 非关系型数据库:
    * `$ brew install mongodb`

* **Redis**: 一个基于内存的高效非关系型数据库:
    * `$ brew install redis`

## **储存库** 安装

储存库 是让 Python 使用我们之前安装好的数据库的库。

* **PyMySQL**: 让 Python 与 MySQL 交互:
    * `pip3 install pymysql`

* **PyMongo**: 让 Python 与 MongoDB 交互:
    * `pip3 install pymongo`

* **redis-py**: 让 Python 与 Redis 交互:
    * `pip3 install redis`

* **RedisDump**: 一个用于 Redis 数据导入/导出的工具，基于Ruby:
    * 安装 RedisDump 首先要安装 `Ruby`，这里我们使用 MacOS 自带的 Ruby。
    * 使用 Ruby 的 gem（类似于pip）安装 RedisDump：
        * `$ sudo gem install redis-dump`
        * ⚠️【注意】由于安装目录是 MacOS 的一部分，必须要sudo，否则无权安装！

## **Web库** 安装

我们需要用到 Web服务程序 来搭建一些 API接口，供爬虫使用。

* **Flask**: 一个轻量级 Web 服务程序，这里用来做一些 API 服务:
    * `pip3 install flask`

* **Tornado**: 一个异步的 Web 框架:
    * `pip3 install tornado`

## **App爬取相关库** 安装

## **爬虫框架** 安装

* **pyspider**:
    * 首先要*解决一个依赖问题*：`$ PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pip3 install --no-cache-dir pycurl`
    * `$ pip3 install pyspider`
    * pyspider v0.3.10 中使用了一个名为 `async` 的变量，这个名字在 `Python 3.7` 中被列为了保留字，这意味着二者合作将无法运行！
    * 在这里，我们为了解决这个问题，简单地把 pyspider 模块中所有的 `async` 替换成了 `async_`😂。

* **Scrapy**: 
    * 大多数的安装教程都要先: `$ xcode-select --install`，但我们跳过了这一步，并没有遇到问题。
    * `pip3 install Scrapy`

* **Scrapy-Splash**: 一个 Scripy 中支持 JavaScript 渲染的工具:
    * 这是一个安装的链条：Scrapy-Splash <- Splash <- Docker
    * 安装 **Docker**：`$ brew cask install docker`
    * 登录 **Docker**：`$ docker login`
    * 安装 **Splash**：`$ docker run -p 8050:8050 scrapinghub/splash`
    * 安装 **Scrapy-Splash**：`pip3 install scrapy-splash`

* **Scrapy-Redis**: Scrapy 的分布式拓展模块:
    * `pip3 install scrapy_redis`

## 部署相关库的安装

* 安装 & 配置 **Docker**：
    * `$ brew cask install docker`
    * [使用 Docker 加速器](https://www.daocloud.io/mirror)

* 安装 **Scrapyd**：
    * `pip3 install scrapyd`
    * `$ sudo mkdir /etc/scrapyd`
    * `$ sudo vim /etc/scrapyd/scrapyd.conf`，当然，也可以使用其他任何文本编辑器打开。
    * 在其中写入以下内容（主要是参考[官方文档](https://scrapyd.readthedocs.io/en/stable/config.html#example)，但做了有限的改动。）：
```
[scrapyd]
eggs_dir    = eggs
logs_dir    = logs
items_dir   =
jobs_to_keep = 5
dbs_dir     = dbs
max_proc    = 0
max_proc_per_cpu = 4
finished_to_keep = 100
poll_interval = 5.0
bind_address = 0.0.0.0
http_port   = 6800
debug       = off
runner      = scrapyd.runner
application = scrapyd.app.application
launcher    = scrapyd.launcher.Launcher
webroot     = scrapyd.website.Root

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
daemonstatus.json = scrapyd.webservice.DaemonStatus
```

* **Scrapyrt**:
    * `pip3 install scrapyrt`

* **Gerapy**:
    * `pip3 install gerapy`