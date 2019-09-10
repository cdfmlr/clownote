---
title:  python请求库urllib
date: 2019-02-11 22:49:55
tags: Crawler
categories:
	- Crawler
---

# 爬虫请求库的使用之Urllib

> 本文主要介绍 **Urllib 库**。



## urllib

`urllib` 是 Python 内置的 HTTP 请求库。

urllib 有 request，error，parse，robotparser 四个模块。

### urllib.request 发送请求

#### `urlopen()`: 发送请求

```python
# 获取 python 官网 HTML 源码
import urllib.request

response = urllib.request.urlopen('https://www.python.org')

print(response.read().decode('utf-8'))  # 查看response内容
print(type(response))                   # 查看response类型
print(response.status)                  # 查看response状态码
print(response.getheaders())            # 查看响应头
print(response.getheader('Server'))     # 查看特定的响应头项
```

`urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)`

##### `urlopen()` 带 `data` 参数: 用 POST 发送一些数据

```python
import urllib.parse
import urllib.request

data = bytes(
    urllib.parse.urlencode({'Hello': 'World'}),
    encoding='utf-8'
    )
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read().decode('utf-8'))
```

##### `urlopen()` 带 `timeout` 参数: 如果请求超出了设置的这个时间，还没有得到响应，就会抛出异常。
设置`timeout=Sec`，Sce 为超时的秒数（可以为小数）。

```python
import socket
import urllib.request

try:
    response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
except Exception as e:
    print(e)
        
print(response.read().decode('utf-8'))
```

#### Request 类构建 Headers

利用更强大的 Request类来构建一个完整的请求。

```python
import urllib.request

request = urllib.request.Request('http://python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
```

##### Request类 的构建参数

`class urllib.request.Request(ur1, data=None, headers={},origin_req_host=None, unverifiable=False, method=None)`


```python
from urllib import request, parse

url = 'http://httpbin.org/post'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Host': 'httpbin.org'
        }
dic = {
        'name': 'CDFMLR'
        }
data = bytes(parse.urlencode(dic), encoding='utf-8')

req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
```

#### 高级用法

##### Handler

Handler 包含 各种处理器，有专门处理登录验证的，有处理 Cookies 的，有处理代理设置的...

urllib.request 模块里的 `BaseHandler` 类是所有其他 Handler 的父类，它提供最基本的方法。

其他的 Handler 详见 [Handler](https://docs.python.org/3/library/urllib.request.html#urllib.request.BaseHandler)

##### Opener

之前用过 urlopen()方法，实际上就是 urllib 提供的一个 Opener。 

urlopen() 相当于类库封装好了极其常用的请求方法，利用它可以完成基本的请求，但如果需要实现更高级的功能，就需要深入一层进行配置，使用更底层的实例来完成操作，就用到了 Opener。 

Opener 可以使用 open()方法，返回的类型和 urlopen()如出一辙。 

我们需要利用 Handler来构建 Opener。 

---
（以下是几个 Hander & Opener 的应用）

##### 处理 `HTTP 基本认证`

`HTTP基本认证`：
> 有一种 web 登录方式不是通过 `cookie`，而是把 `用户名:密码` 用 `base64` 编码之后的字符串放在 request 中的 `header Authorization` 中发送给服务端。
> 当打开网页提示需要输入账号和密码时，假设密码/账号错误，服务器会返回401错误。

这种网站在打开时就会弹出提示框，直接提示输入用户名和密码，验证成功后才能查看页面，我们现在来处理这种页面。

要请求这种页面，可以借用 `HTTPBasicAuthHandler` 完成：

*在我们打算自己实现一个使用 http基本认证 的示例网站时，我们发现了 [一个很好的例子](http://pythonscraping.com/pages/auth/login.php)，所以，我们现在来爬取它。*

```python
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from urllib.error import URLError

username = 'username'
password = 'password'
url = 'http://pythonscraping.com/pages/auth/login.php'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8', errors='ignore')
    print(html)
except URLError as e:
    print(e.reason)
```

在此，我们也想附上这种 `http基本认证` 的 php 实现，以供实践：

```php
<?php
  if (!isset($_SERVER['PHP_AUTH_USER'])) {
    header('WWW-Authenticate: Basic realm="My Realm"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Text to send if user hits Cancel button';
    exit;
  } else {
    echo "<p>Hello {$_SERVER['PHP_AUTH_USER']}.</p>";
    echo "<p>You entered {$_SERVER['PHP_AUTH_PW']} as your password.</p>";
  }
?>
```

 ##### 使用 `代理`

 尝试找一个[免费的代理服务器](https://www.xicidaili.com/nn/)，然后用这个服务器来代理：

 *寻找可用代理的时候可以尝试在浏览器中访问代理服务器的 IP:Port，可用的是会出现结果的:)*

 ```python
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy_handler = ProxyHandler({
    'http': 'http://171.41.80.197:9999',        # 用 ‘<http||https>://代理服务器_IP:代理服务器_端口’
    'https': 'https://171.41.80.197:9999'
    })

opener = build_opener(proxy_handler)

try:
    response = opener.open('http://www.baidu.com')  # 要通过代理爬取的网页
    print(response.read().decode('utf-8', errors='ignore'))
    print(response.getheaders())
except URLError as e:
    print(e.reason)
 ```

##### 处理 Cookies

###### 获取 Cookies

获取 `http://www.baidu.com` 的 Cookies，依次打印出 name = value：

```python
import http.cookiejar
import urllib.request

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

response = opener.open('http://www.baidu.com')

for item in cookie:
    print(item.name, '=', item.value)
```

还是获取 `http://www.baidu.com` 的 Cookies，把它们保存到文件中（正如实际上 Cookies 的保存方式那样）：

```python
import http.cookiejar
import urllib.request

filename = 'cookies_from_baidu.txt'

cookie = http.cookiejar.MozillaCookieJar(filename)      # 用 MozillaCookieJar 类把 Cookies 储存为 Mozilla 型浏览器的格式。
# cookie = http.cookiejar.LWPCookieJar(filename)         # 用这行代替上一行，可以把 Cookies 储存为 libwww-perl(LWP) 的格式。

handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

response = opener.open('http://www.baidu.com')

cookie.save(ignore_discard=True, ignore_expires=True)
```

`MozillaCookieJar` 和 `LWPCookieJar` 都可以**读取**和**保存** Cookies。只是它们的保存格式有别。

###### 取用 Cookies

取用我们刚才保存下来的 Cookies：

```python
import http.cookiejar
import urllib.request

cookie = http.cookiejar.MozillaCookieJar()
cookie.load('cookies_from_baidu.txt', ignore_discard=True, ignore_expires=True)

handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

response = opener.open('http://www.baidu.com')
print(response.read().decode('utf-8', errors='ignore'))
```

### urllib.error 处理异常

#### URLError: 

`URLError` 类来自 `Urllib` 库的 `error` 模块，它继承自 `OSError` 类，是 error 异常模块的基类，由 request 模块生的异常都可以通过捕获这个类来处理。

它具有一个属性 `reason`，即返回错误的原因:

```python
from urllib import request, error
try:
    response = request.urlopen('http://www.google.com')
except error.URLError as e:
    print(e.reason)
```

通过如上操作，我们就可以避免程序异常终止，同时异常得到了有效处理。

#### HTTPError

`HTTPError` 是 `URLError` 的子类。用来处理 **HTTP 请求错误**，比如认证请求失败等等。

`HTTPError` 的属性：

* `code`，返回 HTTP Status Code，即状态码，比如 404 网页不存在，500 服务器内部错误等等。
* `reason`，同父类一样，返回错误的原因。
* `headers`，返回 Request Headers。

```python
from urllib import request,error
try:
    response = request.urlopen('http://cr0123.gz01.bdysite.com/no_such_a_page.html')
except error.HTTPError as e:
    print('\n[Reason]', e.reason,
        '\n[code]', e.code,
        '\n[headers]', e.headers
        )
```

#### 综合使用：

在实际的使用过程中，我们可以先选择捕获子类的错误，再去捕获父类的错误，从而使处理完整，层次清晰。

```python
from urllib import request, error

try:
    response = request.urlopen('http://www.google.com')
except error.HTTPError as e:
    print('HTTPError:')
    print('[Reason]', e.reason, '[code]', e.code, '[headers]', e.headers, sep='\n')
except error.URLError as e:
    print('URLError:')
    print('[Error Reason]\n', e.reason)
except Exception as e:
    print('Exception:')
    print(e)
else:
    print('Request Successfully')
```

### urllib.parse 解析链接

`urllib.parse` 模块定义了处理 URL 的标准接口，例如实现 URL 各部分的抽取，合并以及链接转换。

#### quote() 将内容转化为 URL 编码的格式

可以用来把中文字符转化为 URL 编码：

```python
>>> from urllib.parse import quote
>>> quote('中文')
'%E4%B8%AD%E6%96%87'
>>> url = 'https://www.baidu.com/s?wd=' + quote('URL 编码')    # 合成的网址即可百度搜索‘URL 编码’
>>> print(url)
https://www.baidu.com/s?wd=URL%20%E7%BC%96%E7%A0%81
```

要解码，可是使用对应的 `unquote()`。

#### urlparse() URL的识别和分段

```python
from urllib.parse import urlparse

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(result))
print(result)
print(result.netloc)

'''(results)
<class 'urllib.parse.ParseResult'>
ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5', fragment='comment')
www.baidu.com
'''
```

ParseResult 包含：

* scheme ———— 协议
* netloc ———— 主机名
* path ———— 路径
* params ———— `;XXX`
* query ———— `?XXX`
* fragment ———— `#XXX`

#### urlunparse() 合成URL

**依次**传入六个部分：(scheme, netloc, path, params, query, fragment)，
将合成一个: `scheme://netloc/path;params?query#fragment`

```python
>>> from urllib.parse import urlunparse
>>> data = ['https', 'www.baidu.com', '/index.php', 'user', 'id=5', '123']
>>> urlunparse(data)
'https://www.baidu.com/index.php;user?id=5#123'
```

#### urlencode()  字典类型 转化为 GET请求参数

```python
from urllib.parse import urlencode

params = {
    'name': 'germey',
    'age': 22
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)

'''(result)
http://www.baidu.com?name=germey&age=22
'''
```

#### parse_qs()  GET请求参数 转化为 字典类型

```python
from urllib.parse import parse_qs

query = 'name=germey&age=22'
print(parse_qs(query))

'''(result)
{'name': ['germey'], 'age': ['22']}
'''
```

另有一个 `parse_qsl()` 与 `parse_qs()` 类似，只是得到的结果是 元组

#### 其他

这个库中还有一些 `urljoin` 等方式，可以在 [这里](https://germey.gitbooks.io/python3webspider/content/3.1.3-解析链接.html) 查看。


### urllib.robotparser 分析Robots协议

#### Robots协议

网络爬虫排除标准（Robots Exclusion Protocol），用来告诉爬虫和搜索引擎哪些页面可以抓取，哪些不可以抓取。
它通常是一个叫做 robots.txt 的文本文件，放在网站的根目录下。

Robots协议的写法：

```
User-agent: *               这里的*代表的所有的搜索引擎种类，*是一个通配符
Disallow: /admin/           这里定义是禁止爬寻admin目录下面的目录
Disallow: /require/         这里定义是禁止爬寻require目录下面的目录
Disallow: /ABC/             这里定义是禁止爬寻ABC目录下面的目录
Disallow: /cgi-bin/*.htm    禁止访问/cgi-bin/目录下的所有以".htm"为后缀的URL(包含子目录)。
Disallow: /*?*              禁止访问网站中所有包含问号 (?) 的网址
Disallow: /.jpg$            禁止抓取网页所有的.jpg格式的图片
Disallow:/ab/adc.html       禁止爬取ab文件夹下面的adc.html文件。
Allow: /cgi-bin/　          这里定义是允许爬寻cgi-bin目录下面的目录
Allow: /tmp                 这里定义是允许爬寻tmp的整个目录
Allow: .htm$                仅允许访问以".htm"为后缀的URL。
Allow: .gif$                允许抓取网页和gif格式图片
Sitemap:                    网站地图 告诉爬虫这个页面是网站地图
```

使用例子：

```
禁止所有搜索引擎访问网站的任何部分
User-agent: *
Disallow: /

允许所有的robot访问
User-agent: *
Allow:　/

允许某个搜索引擎的访问
User-agent: Baiduspider
allow:/
```

#### 解析 Robots.txt ---- `urllib.robotparser.RobotFileParser` 类

robotparser 模块提供了一个 `RobotFileParser` 类。它可以根据某网站的 robots.txt 文件来判断一个爬取爬虫是否有权限来爬取这个网页。

##### `RobotFileParser` 实例的构造
```
urllib.robotparser.RobotFileParser(url='')      # 传入 robots.txt 的链接
```


##### `RobotFileParser` 常用方法

* `set_url(url)` 用来设置 robots.txt 的链接
* `read()` 读取 robots.txt 文件并进行分析。
⚠️【注意】如果不 read()，所有的判断函数都会返回 False！
* `parse()` 用来解析 robots.txt 文件，传入的参数是 robots.txt 某些行的内容，它会按照 robots.txt 的语法规则来分析这些内容。
* `can_fetch()` 传入两个参数，第一个是 User-agent，第二个是要抓取的 URL，返回的内容是该搜索引擎是否可以抓取这个 URL，返回结果是 True 或 False。
* `mtime()`，返回的是上次抓取和分析 robots.txt 的时间，这个对于长时间分析和抓取的搜索爬虫是很有必要的，你可能需要定期检查来抓取最新的 robots.txt。
* `modified()`，同样的对于长时间分析和抓取的搜索爬虫很有帮助，将当前时间设置为上次抓取和分析 robots.txt 的时间。

