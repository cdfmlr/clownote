---
categories:
- Crawler
date: 2019-02-14 22:49:55
tags: Crawler
title: Python爬虫抓取电影排行
---

# 爬虫基本库实践 -- 抓取电影排行

> 爬虫实践：利用 Requests 和正则表达式来抓取猫眼电影 TOP100 的相关内容。



### 目标

我们打算提取出 [猫眼电影 TOP100 榜](http://maoyan.com/board/4) 的电影名称、时间、评分、图片等信息，提取的结果我们以文件形式保存下来。

### 准备

* 系统环境：macOS High Sierra 10.13.6
* 开发语言：Python 3.7.2 (default)
* 第三方库：Requests

### 分析

[目标站点](https://maoyan.com/board/4)：`https://maoyan.com/board/4`

打开页面后我们可以发现，页面中显示的有效信息有 **影片名称**、**主演**、**上映时间**、**上映地区**、**评分**、**图片**。

然后，我们查看一下排名第一的条目的 html 源码，一会儿我们就从这段代码入手设计正则表达式：

```html
<dd>
        <i class="board-index board-index-1">1</i>
        <a href="/films/1203" title="霸王别姬" class="image-link" data-act="boarditem-click" data-val="{movieId:1203}">
                <img src="//s0.meituan.net/bs/?f=myfe/mywww:/image/loading_2.e3d934bf.png" alt=""
                        class="poster-default" />
                <img data-src="https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c"
                        alt="霸王别姬" class="board-img" />
        </a>
        <div class="board-item-main">
                <div class="board-item-content">
                        <div class="movie-item-info">
                                <p class="name"><a href="/films/1203" title="霸王别姬" data-act="boarditem-click"
                                                data-val="{movieId:1203}">霸王别姬</a></p>
                                <p class="star">
                                        主演：张国荣,张丰毅,巩俐
                                </p>
                                <p class="releasetime">上映时间：1993-01-01</p>
                        </div>
                        <div class="movie-item-number score-num">
                                <p class="score"><i class="integer">9.</i><i class="fraction">6</i></p>
                        </div>

                </div>
        </div>

</dd>
```

再来看看翻页会发生什么：
url 从 `https://maoyan.com/board/4` 变成了 `https://maoyan.com/board/4?offset=10`。
嗯，多了一个 `?offset=10`。
再下一页，变成了`?offset=20`。
原来，每翻一页offset就加10（一页显示刚好是10个条目，这很合理。）
其实我们甚至可以尝试把值改成0（首页），或任何在范围 `[0, 100)` 内的值。

### 设计

我们现在设计一个可以完成目标的爬虫程序。

这个爬虫应该有这几个部分：

* 抓取页面（同时也要注意配合翻页的问题处理）：可以用 `requests.get()` 来请求，最好再伪造一组headers。
* 正则提取（匹配出 影片名称、主演、上映时间、上映地区、评分、图片）：用 `re.findall()` 和适当的正则表达式来提取信息。
* 写入文件（用JSON格式去保存信息）：涉及到 `json.dumps()` 与 文件写入

现在，我们还需要设计尤为关键的正则表达式：

```
'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)@.*?title="(.*?)".*?主演：(.*?)\s*</p>.*?上映时间：(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>'
匹配到的顺序是：(排名, 图片地址, 名称, 主演, 上映时间, 评分整数部分, 评分小数部分)
需要使用 re.S
```

### 实现

我们现在来按照设计实现第一个版本的程序：

```python
import re
import json
import time

import requests

url = 'https://maoyan.com/board/4'
filename = './movies.txt'
pattern = r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)@.*?title="(.*?)".*?主演：(.*?)\s*</p>.*?上映时间：(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>'

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Language': 'zh-cn'
        }

def get_page(url):   # 抓取页面，返回html字符串
    print('\tGetting...')
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        print('[Error]', e)
        return ''


def extract(html):  # 正则提取，返回结果dict的list
    print('\tExtracting...')
    raws = re.findall(pattern, html, re.S)   # [(排名, 图片地址, 名称, 主演, 上映时间, 评分整数部分, 评分小数部分), ...]
    result = []
    for raw in raws:
        dc = {                      # 在这里调整了顺序
                'index': raw[0],
                'title': raw[2],
                'stars': raw[3],
                'otime': raw[4],
                'score': raw[5] + raw[6],   # 合并整数、小数
                'image': raw[1]
                }
        result.append(dc)

    return result
    

def save(data):      # 写入文件
    print('\tSaving...')
    with open(filename, 'a', encoding='utf-8') as f:
        for i in data:
            f.write(json.dumps(i, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    for i in range(0, 100, 10):     # 翻页
        target = url + '?offset=' + str(i)
        print('[%s%%](%s)' % (i, target))
        page = get_page(target)
        data = extract(page)
        save(data)
        time.sleep(0.5)     # 防制请求过密集被封

    print('[100%] All Finished.\n Results in', filename)
```

### 调试

运行程序，如果一切顺利，我们将得到结果：

```python
{"index": "1", "title": "霸王别姬", "stars": "张国荣,张丰毅,巩俐", "otime": "1993-01-01", "score": "9.6", "image": "https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg"}
{"index": "2", "title": "肖申克的救赎", "stars": "蒂姆·罗宾斯,摩根·弗里曼,鲍勃·冈顿", "otime": "1994-10-14(美国)", "score": "9.5", "image": "https://p0.meituan.net/movie/283292171619cdfd5b240c8fd093f1eb255670.jpg"}
{"index": "3", "title": "罗马假日", "stars": "格利高里·派克,奥黛丽·赫本,埃迪·艾伯特", "otime": "1953-09-02(美国)", "score": "9.1", "image": "https://p0.meituan.net/movie/54617769d96807e4d81804284ffe2a27239007.jpg"}
{"index": "4", "title": "这个杀手不太冷", "stars": "让·雷诺,加里·奥德曼,娜塔莉·波特曼", "otime": "1994-09-14(法国)", "score": "9.5", "image": "https://p0.meituan.net/movie/e55ec5d18ccc83ba7db68caae54f165f95924.jpg"}
{"index": "5", "title": "泰坦尼克号", "stars": "莱昂纳多·迪卡普里奥,凯特·温丝莱特,比利·赞恩", "otime": "1998-04-03", "score": "9.6", "image": "https://p1.meituan.net/movie/0699ac97c82cf01638aa5023562d6134351277.jpg"}
```

乍一看好像没有问题了，我们需要的结果都得到了。
但是，仔细查看，发现还是会有几个问题存在：

1. 主演（stars）一般都有几个人，我们最好把他们分开用一个list或是tuple来安置。
2. 信息每一个条目直接相互分离，不便于传输与取用。

要解决第一个问题，我们可以在 extract 中增加一部分来处理这个问题，而第二个问题则需要我们将所有页都读取完成，放到指定位置，再统一写入文件。

修改源程序：

新增 函数，处理主演信息，得到一个list:
```python
def stars_split(st):
    return st.split(',')
```

修改 extract()，在其中添加 stars_split 的调用:
```python
def extract(html):  # 正则提取，返回结果dict的list
    print('\tExtracting...')
    raws = re.findall(pattern, html, re.S)   # [(排名, 图片地址, 名称, 主演, 上映时间, 评分整数部分, 评分小数部分), ...]
    result = []
    for raw in raws:
        dc = {                      # 在这里调整了顺序
                'index': raw[0],
                'title': raw[2],
                'stars': stars_split(raw[3]),   # 【修改】：分离主演
                'otime': raw[4],
                'score': raw[5] + raw[6],       # 合并整数、小数
                'image': raw[1]
                }
        result.append(dc)

    return result
```

新增 一个全局变量、函数，实现结果的整合:

```python
result = {'top movies': []}

def merge(data):
    print('\tMerging...')
    result['top movies'] += data
```

修改 save：

```python
def save(data):      # 写入文件
    print('Saving...')
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
```

修改程序框架：

```python
if __name__ == '__main__':
    for i in range(0, 100, 10):     # 翻页
        target = url + '?offset=' + str(i)
        print('[%s%%](%s)' % (i, target))
        page = get_page(target)
        data = extract(page)
        merge(data)
        time.sleep(0.5)     # 防制请求过密集被封
        
    save(result)
    print('[100%] All Finished.\n Results in', filename)
```

整合代码：

```python
import re
import json
import time

import requests

url = 'https://maoyan.com/board/4'
result = {'top movies': []}
filename = './movies.json'      # （最好把保存的文件名改一下，否则会添加到上次运行结果的后面）

pattern = r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)@.*?title="(.*?)".*?主演：(.*?)\s*</p>.*?上映时间：(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>'

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Language': 'zh-cn'
        }


def get_page(url):   # 抓取页面，返回html字符串
    print('\tGetting...')
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        print('[Error]', e)
        return ''


def stars_split(st):
    return st.split(',')


def extract(html):  # 正则提取，返回结果dict的list
    print('\tExtracting...')
    raws = re.findall(pattern, html, re.S)   # [(排名, 图片地址, 名称, 主演, 上映时间, 评分整数部分, 评分小数部分), ...]
    result = []
    for raw in raws:
        dc = {                      # 在这里调整了顺序
                'index': raw[0],
                'title': raw[2],
                'stars': stars_split(raw[3]),   # 分离主演
                'otime': raw[4],
                'score': raw[5] + raw[6],       # 合并整数、小数
                'image': raw[1]
                }
        result.append(dc)

    return result
    

def merge(data):
    print('\tMerging...')
    result['top movies'] += data
    
    
def save(data):      # 写入文件
    print('Saving...')
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    for i in range(0, 100, 10):     # 翻页
        target = url + '?offset=' + str(i)
        print('[%s%%](%s)' % (i, target))
        page = get_page(target)
        data = extract(page)
        merge(data)
        time.sleep(0.5)     # 防制请求过密集被封
        
    save(result)
    print('[100%] All Finished.\n Results in', filename)
```

运行修改完毕的程序，得到新的结果：

```json
{"top movies": [{"index": "1", "title": "霸王别姬", "stars": ["张国荣", "张丰毅", "巩俐"], "otime": "1993-01-01", "score": "9.6", "image": "https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg"}, {"index": "2", "title": "肖申克的救赎", "stars": ["蒂姆·罗宾斯", "摩根·弗里曼", "鲍勃·冈顿"], "otime": "1994-10-14(美国)", "score": "9.5", "image": "https://p0.meituan.net/movie/283292171619cdfd5b240c8fd093f1eb255670.jpg"}, ..., {"index": "100", "title": "龙猫", "stars": ["秦岚", "糸井重里", "岛本须美"], "otime": "2018-12-14", "score": "9.2", "image": "https://p0.meituan.net/movie/c304c687e287c7c2f9e22cf78257872d277201.jpg"}]}
```

这样就比较理想了。

### 完成

该爬虫项目结束了。
总结一下，我们主要用了 `requests.get()` 完成请求，还伪造了 `headers`；用 `re.findall()` 正则解析结果，然后调整了信息的顺序；用 `json` 格式化保存结果。

其实，这个项目只要稍作修改，我们就可以用来爬取其他很多种电影排行榜，如我们其实还实现了一个爬取豆瓣top250的程序，真的只是稍微改动，非常容易了。

我们展现了这个项目开发的过程，从目标到最后完成，一步一步进行，这个开发顺序适用于很多项目，并且富有哲理，我们认为值得感悟与践行。