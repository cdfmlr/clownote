---
title: python请求库requests
date: 2019-02-12 22:49:55
tags: Crawler
categories:
	- Crawler
---

# 爬虫请求库的使用之Requests

> 本文主要介绍 **Requests 库**。



## requests

相较于 Python 内置的 Urllib，第三方库 Requests 为我们提供了一个更加优雅的解决方案。
得益于 `requests` 的强大，我们可以在解决 Cookies、登录验证、代理设置 等问题时更加方便快捷，而无需再琢磨 Urllib 的 Opener、Handler。

### requests.get() —— GET请求

使用 `requests.get(url, *params={}, headers={}, timeout=None)` 可以完成 GET 请求，返回 response 的各种内容。

```python
import requests

r = requests.get('http://httpbin.org/get')
print(r.text)

print('status_code: ', type(r.status_code), r.status_code)
print('headers: ', type(r.headers), r.headers)
print('cookies: ', type(r.cookies), r.cookies)
print('url: ', type(r.url), r.url)
print('history: ', type(r.history), r.history)
```

status_code 属性得到状态码， headers 属性得到 Response Headers，cookies 属性得到 Cookies，url 属性得到 URL，history 属性得到请求历史。

使用 `params={}` ，就等于在url中添加了 `'?xxx&xxx'` 的信息：

```python
import requests

data = {
    'name': 'germey',
    'age': 22
}
r = requests.get("http://httpbin.org/get", params=data)    # 相当于 GET请求 ‘http://httpbin.org/get?name=germey&age=22’
print(r.text)
```

在上例中，我们可以看到返回的 r.text 实际上是 JSON 的字符串，requests 提供了 一个 `Response.json()` 可以直接把 JSON 解析成 dict：

```python
#  承接上一代码块
d = r.json()
print(type(d), d, sep='\n')
```

若返回结果不是 Json 格式，调用 `Response.json()`，会抛出 https://www.zhihu.com/explorejson.decoder.JSONDecodeError 的异常。

我们还可以在调用 requests.get() 的时候传入一个 dict 作为 headers：

```python
import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        }

response = requests.get('http://httpbin.org/get', headers=headers)
print(response.text)
```

我们还可以设置超时，有三种方法：

* `r = requests.get('https://www.taobao.com', timeout=None)`，connect 和 read 二者都是 永久等待，这是默认设置
* `r = requests.get('https://www.taobao.com', timeout=1)`，connect 和 read 二者的 timeout 总和设置为 1 秒
* `r = requests.get('https://www.taobao.com', timeout=(5, 11))`，connect 5秒，read 11秒

### 获取二进制数据

当我们获取得二进制的数据时，Response.text 显然是不好用了，这时我们可以通过 `Response.content` 取得二进制数据。

```python
import requests

r = requests.get("https://github.com/favicon.ico")

print(r.text)       # 输出乱码
print(r.content)    # 输出十六进制码的bytes（b'\x..\x........'）

with open('favicon.ico', 'wb') as f:        # 保存到文件
    f.write(r.content)
```

### 抓取网页

我们来做一个简单的爬虫实践————爬取 [知乎-发现](https://www.zhihu.com/explore) 里的问题。

```python
import requests
import re
# 知乎-发现的url
url = 'https://www.zhihu.com/explore'
# 匹配问题的正则表达式
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</', re.S)       # *？表示惰性匹配

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

try:
    response = requests.get(url, headers=headers)
    questions = re.findall(pattern, response.text)
    for i in questions:
        print(i)
except Exception as e:
    print(e)
```

### requests.post() —— POST请求

用 `requests.post(url, data={})` 我们就可以 POST 请求，这和使用 requests.get() 非常类似。

```python
import requests
data = {'Data': 'Hello, world!'}

r = requests.post('http://httpbin.org/post', data=data)
print(r.text)
```

我们同样可以从 Response 中获取各种数据，例如：status_code 属性得到状态码， headers 属性得到 Response Headers，cookies 属性得到 Cookies，url 属性得到 URL，history 属性得到请求历史。

### 文件上传

我们可以使用 POST请求 来完成文件的上传。

```python
import requests

files = {'file': open('favicon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files=files)

print(r.text)
```

### Cookies

#### 获取Cookies

```python
import requests

r = requests.get('https://www.baidu.com')
print(r.cookies)
for key, value in r.cookies.items():
    print(key + '=' + value)
```

#### 调用Cookies

我们先登录一个网站，然后从记录下Cookies，在另一次登录中，把这个Cookies传上去，就可以维持登录。

例如，我们现在用浏览器登录「百度」，然后打开一次百度首页，我们检查 `www.baidu.com` 的 Request Headers，我们会发现一项 `Cookies`，我们把这个值复制下来，让爬虫伪造 headers，带上这个 Cookies，我们就可以模拟登录了:)

```python
import requests

url = 'https://www.baidu.com'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Cookie': 'BDORZ******3254',
        'Connection': 'keep-alive',
        'Host': 'www.baidu.com'
        }

r = requests.get(url, headers=headers)

print(r.text)
```

从结果中，我们可以看到自己的名字，说明成功模仿登录！

也可以这样：
```python
import requests

cookies = 'q_c1=316******3b0'
jar = requests.cookies.RequestsCookieJar()
headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
for cookie in cookies.split(';'):
    key, value = cookie.split('=', 1)
    jar.set(key, value)
    
r = requests.get('http://www.zhihu.com', cookies=jar, headers=headers)
print(r.text)
```

#### 会话维持

在 Requests 中，我们如果直接利用 get() 或 post() 等方法的确可以做到模拟网页的请求。
但是这实际上是相当于不同的会话，即不同的 Session，也就是说**每请求一次**都相当于用**不同浏览器打开**，会话不会维持。
但我们常需要模拟在一个浏览器中打开同一站点的不同页面，这就需要我们进行会话维持。

###### 不使用会话维持

```python
import requests

requests.get('http://httpbin.org/cookies/set/number/123456789')     # 一次会话
r = requests.get('http://httpbin.org/cookies')      # 另一次会话
print(r.text)

'''(result)
{
  "cookies": {}
}
'''
```

我们得到的结果是空的，说明两次get不是同一会话了。

###### 使用会话维持

使用会话维持最直接的办法就是我们可以获取上一次的 Cookies，下一次请求时把它传上去，但这样做过于繁琐，requests 为我们提供了更加简洁、优雅的解决方案 —— `requests.Session`：

```python
import requests

s = requests.Session()      # 开启一个新会话 s
s.get('http://httpbin.org/cookies/set/number/123456789')    # 会话 s
r = s.get('http://httpbin.org/cookies')     # 同样还是会话 s
print(r.text)

'''(result)
{
  "cookies": {
    "number": "123456789"
  }
}
'''
```

这一次，我们就维持了会话了。

#### SSL 证书验证

Requests 提供了证书验证的功能，当发送 HTTP 请求的时候，它会检查 SSL 证书（针对https），我们可以使用 `verify` 参数来控制是否检查此证书，缺省值是 True，会自动验证。
如果我们不需要检查证书，可以让 `verify=False`：

```python
import requests

response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)
```

指定本地证书用作客户端证书:

客户端证书可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组。

```python
import requests

response = requests.get('https://www.12306.cn', cert=('/path/server.crt', '/path/key'))
print(response.status_code)
```

⚠️【注意】本地私有证书的 key 必须要是解密状态，加密状态的 key 是不支持的。

#### 代理设置

找一个[免费的代理服务器](https://www.xicidaili.com/nn/)，然后用这个服务器来代理。

```python
import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate'
        }

proxies = {
        'http': 'http://110.52.235.57:9999',
        'https': 'https://110.52.235.57:9999'
        }

r = requests.get('http://www.taobao.com', proxies=proxies, headers=headers)

print(r.text)
```

另外，若使用非免费的代理，可能需要使用 HTTP Basic Auth，可以使用类似 http://user:password@host:port 这样的语法来设置代理：

```python
import requests

proxies = {
    'https': 'http://user:password@10.10.1.10:3128/',
}
requests.get('https://www.taobao.com', proxies=proxies)
```

Requests 还支持 SOCKS 协议的代理:

```sh
$ pip3 install "requests[socks]"
```

```python
import requests

proxies = {
    'http': 'socks5://user:password@host:port',
    'https': 'socks5://user:password@host:port'
}
requests.get('https://www.taobao.com', proxies=proxies)
```

#### HTTP 基本认证

```python
import requests
from requests.auth import HTTPBasicAuth

r = requests.get('http://pythonscraping.com/pages/auth/login.php', auth=HTTPBasicAuth('username', 'password'))
print(r.status_code)
```

还可以更简单：

```python
import requests

r = requests.get('http://pythonscraping.com/pages/auth/login.php', auth=('username', 'password'))
print(r.status_code)
```

Requests 还支持其他的认证，如 OAuth。关于这方面，可以查看 [文档](https://requests-oauthlib.readthedocs.io/en/latest/) 。

#### Prepared Request

类似于 Urllib 中的 Request ，我们可以在 Requests 中使用 Prepared Request 来表示一个请求：

```python
from requests import Request, Session

url = 'http://httpbin.org/post'
data = {
    'name': 'germey'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}
s = Session()
req = Request('POST', url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)
print(r.text)
```

这里我们引入了 Request，然后用 url、data、headers 参数构造了一个 Request 对象，这时我们需要再调用 Session 的 prepare_request() 方法将其转换为一个 Prepared Request 对象，然后调用 send() 方法发送即可

通过 Request 对象，我们就可以将一个个请求当做一个独立的对象来看待，这可以方便调度。

