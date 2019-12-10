---
title: Ajax数据爬取
date: 2019-02-22 22:49:55
tags: Crawler
categories:
	- Crawler
---

# Ajax 数据爬取

> 本节主要介绍如何爬取 Ajax 渲染的网页。

## Ajax 简介

> Ajax，全称为 Asynchronous JavaScript and XML，即异步的 JavaScript 和 XML。

Ajax 是一种利用 JavaScript 在保证页面不被刷新、页面链接不改变的情况下与服务器交换数据并更新部分网页的技术。

发送 Ajax 请求到网页更新的这个过程可以简单分为三步：

* 发送请求
* 解析内容
* 渲染网页

#### 发送请求

```js
var xmlhttp;
if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
} else {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
xmlhttp.onreadystatechange=function() {
    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
        document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
    }
}
xmlhttp.open("POST","/ajax/",true);
xmlhttp.send();
```

JavaScript 对 Ajax 最底层的实现，
实际上就是新建了 XMLHttpRequest 对象，
然后调用了onreadystatechange 属性设置了监听，
然后调用 open() 和 send() 方法向某个链接也就是服务器发送了一个请求，
当服务器返回响应时，onreadystatechange 对应的方法便会被触发，
然后在这个方法里面解析响应内容。

#### 解析内容

得到响应之后，onreadystatechange 属性对应的方法便会被触发，此时利用 xmlhttp 的 responseText 属性便可以取到响应的内容。

返回内容可能是 HTML，可能是 Json，接下来只需要在方法中用 JavaScript 进一步处理即可。比如如果是 Json 的话，可以进行解析和转化。

#### 渲染网页

 DOM 操作，即对 Document网页文档进行操作，如更改、删除等。


## Ajax 分析方法

在浏览器开发者工具的Network中，Ajax的请求类型是 `xhr`。

在Request Headers中有一项 `X-Requested-With: XMLHttpRequest` 标记了该请求为 Ajax。

在 Preview 中可以看到响应的内容。

有了Request URL、Request Headers、Response Headers、Response Body等内容，就可以模拟发送Ajax请求了。

## Python 模拟 Ajax 请求

爬取【人民日报】的微博：

```python
import requests
from bs4 import BeautifulSoup

url_base = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=2803301701&containerid=1076032803301701'

headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'X-Requested-With': 'XMLHttpRequest',
        'MWeibo-Pwa': '1'
        }

def get_page(basicUrl, headers, page):
    url = basicUrl + '&page=%s' % page
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()      # Would return a dict
        else:
            raise RuntimeError('Response Status Code != 200')
    except Exception as e:
        print('Get Page False:', e)
        return None


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.get_text()
    

def get_content(data):
    result = []
    if data and data.get('data').get('cards'):
        for item in data.get('data').get('cards'):
            useful = {}
            useful['source'] = item.get('mblog').get('source')
            useful['text'] = parse_html(item.get('mblog').get('text'))

            result.append(useful)

    return result


def save_data(data):    # 这里不保存了，只是把它打印出来
    for i in data:
        print(i)


if __name__ == '__main__':
    for page in range(1, 3):    # 记得调整需要的页数。
        r = get_page(url_base, headers, page)
        d = get_content(r)
        save_data(d)
```

