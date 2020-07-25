---
date: 2019-08-15 14:54:34
tags: Web
title: GitHub加Hexo打造个人博客
---

# GitHub + Hexo => 个人博客

> 打造一个个人博客其实很简单，我们不需要拥有一台服务器、甚至可以对 Web 开发不甚了解。

这篇文章记录我如何在 Mac 上通过 [GitHub](https://github.com)、[Hexo](https://hexo.io) 打造一个*个人博客* —— **[clownote](https://clownote.github.io)**

## 起因

我一直不喜欢 CSDN 和博客园等博客平台，但确实有写东西的习惯。写了东西就要发表，所以在之前，我把我学习计算机知识的笔记都放到了一个自己初学 Web 开发时搞的一个超级简陋的静态网站上。

但它实在是太简陋了导致使用起来**巨**麻烦，发布文章要手动把 markdown 写的文章用自己写的一个转换器渲染成 HTML，然后调用一个可以及时渲染代码颜色的 js 进去，然后 FTP 上传到服务器上，再到手动修改 `index.html`，加入这篇新文章的链接......

这完全不是正常人应该用的操作！

我一直在考虑写一个功能完整的、更方便的博客。计划是用 Flask 写后端，Vue 做前端，Git 来管理内容，然后再写一些 Apple Script、Bash Script 让这个博客系统方便在 Mac 中使用 。但最近一直忙其他项目，没时间来实现。现在我的服务器到期了，百度云的，感觉不太好用（主要是受对这家公司的某些其他产品的不良印象的影响），不续费了。

笔记急需迁出！写之前想的博客系统是来不及了，突然想起来很多人用一个叫 `Hexo` 的东西做博客，于是一番 Google、Bing。最终，我觉定用 `GitHub` + `Hexo` 快速（Less than One Day）打造一个**不用服务器**、**不用写代码**的博客。

## 经过

~~废话不多说，代码赶快写起来~~，，，（哦，错了，咱们今天不用写代码！只是几个简单的命令 + 配置就好了😂）

废话不多说，建站走起！

### 安装

#### 注册GitHub

首先，我们需要注册一个 `GitHub` 账户，我相信绝大多数的读者已经完成了这一步，所以不再赘述；如果您幸运的属于少数人，请打开 [GitHub](https://github.com)，即可按照感觉轻松完成。

#### 创建 GitHub Pages

在您的 GitHub 中，`New` 一个 `Repository`，名字为 `<userName>.github.io`，其中的 `<userName>` 与您的 GitHub 用户名相同。

注意，在这个新建的 Repository 的 `Settings` 中，您应该可以找到，有关 `GitHub Pages` 的设置里写了:

```
Your site is published at https://<userName>.github.io
```

这样就成了，否则请检查之前的步骤是否正确。

#### 安装 Hexo

在安装 `Hexo` 前，需要确定电脑中是否已安装了：

- [Node.js](http://nodejs.org/) (版本至少为 nodejs 6.9)
- [Git](http://git-scm.com/)

```
$ git --version
$ node --version
```

如果没有，要先安装他们。接下来只需要使用 `npm` 即可完成 Hexo 的安装：

```
$ npm install -g hexo-cli
```

### 建站

#### 初始化

安装 Hexo 完成后，执行下列命令，Hexo 将会在指定文件夹中新建您的博客：

```
$ hexo init <folder>
$ cd <folder>
$ npm install
```

然后，可以看到指定文件夹的目录如下：

```
.
├── _config.yml
├── package.json
├── scaffolds
├── source
|   ├── _drafts
|   └── _posts
└── themes
```

#### 配置

目录中的 `_config.yml` 是网站的配置信息，我们需要在此配置一些参数：

```
$ cat _config.yml
# Hexo Configuration
## Docs: https://hexo.io/docs/configuration.html
## Source: https://github.com/hexojs/hexo/
......
```

需要配置的项目有：

| 参数          | 描述                                            |
| :------------ | :---------------------------------------------- |
| `title`       | 网站标题                                        |
| `subtitle`    | 网站副标题                                      |
| `description` | 网站描述                                        |
| `keywords`    | 网站的关键词。使用半角逗号 `,` 分隔多个关键词。 |
| `author`      | 您的名字                                        |
| `language`    | 网站使用的语言                                  |
| `url`         | 网址                                            |
| `theme`  | 当前主题名称。值为`false`时禁用主题 |
| `deploy` | 部署部分的设置                      |

需要说明的是，`deploy` 项的配置就可以把Hexo与GitHub关联起来，即将我们的博客**推送**到 GitHub，打开站点的配置文件_config.yml，`deploy` 项配置为：

```yaml
deploy: 
	type: git
	repo: https://github.com/<userName>/<userName>.github.io
	branch: master
```

然后，我们需要让 Hexo 连接上我们的 GitHub：

```
$ npm install hexo-deployer-git --save

$ hexo clean
$ hexo generate
$ hexo deploy
```

每一条命令的作用都很直观。操作完之后你就会发现你的博客已经上线了，可以在网络上被访问了！

#### 主题

如果你像我一样，觉得 `Hexo` 自带的 `landscape` 主题不太好看，我们可以跟换一个主题。

我们可以在 Hexo 官网上找到很丰富的 [主题资源](https://hexo.io/themes/)，具体的使用方法主题项目的 README 里会写明，照着做就行。

这里以配置一个叫做 [`cactus`](https://github.com/probberechts/hexo-theme-cactus) 的主题为例：

1. 下载、安装：

```
$ cd <folder>		# hexo init 的目录
$ git clone https://github.com/probberechts/hexo-theme-cactus.git themes/cactus		# 拷贝一份主题
```

2. 修改Hexo主题：

```
$ vim ./config.yml
```

修改其中的 `theme` 属性：

```
# theme: landscape
theme: cactus
```

3. 主题配置

在 `themes/cactus/_config.yml` 中按照自己的需要对主题进行配置。

### 写作

其实到这里，我们的博客就已经构建完成了。接下来我们就可以用新建的博客系统写作了😊。

#### 新建文章

你可以执行下列命令来创建一篇新文章。

```
$ hexo new [layout] <title>
```

您可以在命令中指定文章的布局（layout），默认为 `post`，可以通过修改 `_config.yml` 中的 `default_layout` 参数来指定默认布局。

可选的布局有：

| `layout` | 储存路径         | 功能                               |
| -------- | ---------------- | ---------------------------------- |
| `post`   | `source/_posts`  | 存放要发布的博客文章               |
| `page`   | `source`         | 网站中的一些固定页面，比如说"关于" |
| `draft`  | `source/_drafts` | 草稿                               |

`hexo new` 成功后，Hexo 会告诉你新建的文件路径，利用 markdown 编辑器打开它，就可以开始书写了，在我的 Mac 里，默认的 markdown 编辑器是 `Typora`，可以直接用 `open` 命令来用默认程序打开并编辑文件：

```
$ open ~/<blogFolder>/source/_drafts<title>.md
```

#### 草稿

我们在写文章时，可以先写草稿(draft)。草稿默认不会显示在页面中，您可在执行时加上 `--draft` 参数，或是把 `render_drafts` 参数设为 `true` 来预览草稿。

文章写好后，通过 `publish` 命令将草稿移动到 `source/_posts` 文件夹：

```
$ hexo publish [layout] <title>
```

#### Front-matter

Front-matter 是文件最上方以 `---` 分隔的区域，在里面写 YAML 配置，用于指定个别文件的变量，例如：

```yaml
---
title: Hello World
date: 2013/7/13 20:46:25
---
```

以下是一些常用的参数：

| 参数         | 描述                                                 | 默认值       |
| :----------- | :--------------------------------------------------- | :----------- |
| `layout`     | 布局                                                 |              |
| `title`      | 标题                                                 |              |
| `date`       | 建立日期                                             | 文件建立日期 |
| `updated`    | 更新日期                                             | 文件更新日期 |
| `comments`   | 开启文章的评论功能                                   | true         |
| `tags`       | 标签（不适用于分页）                                 |              |
| `categories` | 分类（不适用于分页）                                 |              |
| `permalink`  | 覆盖文章网址                                         |              |
| `keywords`   | 仅用于 meta 标签和 Open Graph 的关键词（不推荐使用） |              |

#### 分类和标签

对于大多数人来讲，对一篇文章分类和标签的设置是必不可少的。

分类和标签听起来很接近，但是在 Hexo 中两者有着明显的差别：**分类(`categories`)** 具有*顺序性*和*层次性*，也就是说 `Foo, Bar` 不等于 `Bar, Foo`；而 **标签(`tags`)** 没有顺序和层次。

在 `Front-matter` 中，分类和标签的设置方法如下：

```yaml
categories:
- Diary
tags:
- PS3
- Games
```

在使用 `categories` 时，请注意：

Hexo不支持指定多个同级分类！下面的指定方法：


```yaml
categories:
- Diary
- Life
```

会使分类 `Life` 成为 `Diary` 的子分类，而不是 *并列分类*。因此，有必要为您的文章选择尽可能准确的分类。

#### 发布

在完成写作后，我们先保存编辑好的 markdown 文件，然后执行如下操作：

```
$ hexo publish post <title>.md		# 如果新建时 layout 为 draft

$ hexo deploy --generate		# 生成文件完成后部署
		# 可以简写为 `$ hexo d -g`
```

#### 操作总结

现在，回顾一下我们用 Hexo 写作的过程:

1. `$ hexo new draft <title>`
2. `$ open ~/<blogFolder>/source/_drafts/<title>.md`
3. `在编辑器中填写Front-matter，并完成内容写作`
4. `$ hexo publish post <title>`
5. `$ hexo deploy --generate`

如果有能力，我们还可以写一个简单的小脚本来简化这些操作。很容易实现，在这里就不介绍了。

### 功能拓展

现在，我们已经完成了博客系统的安装、建站并且学会了在其中写作。

当我们打开自己的博客网站时，会发现，我们的 `Cactus` 主题已经提供了诸如分享、导航的功能。

但或许我们还是觉得它有些太简陋了，我们可能还想让它有一些让用户体验更好的特性，比如，搜索、评论功能，现在我们尝试来实现它们。

其实，我们使用的 `Cactus` 主题中，已经包含了对搜索、评论的支持，直接使用即可。

#### 搜索

安装 hexo 的搜索插件：

```
$ npm install hexo-generator-search --save
```

创建一个新页面，用来承载搜索功能：

```
$ hexo new page search
```

在 Front-matter 里加上 `type: search`：

```yaml
title: Search
type: search
---
```

在 `themes/cactus/_config.yml` 里配置：

```yaml
nav:
  search: /search/
```

#### 评论

 `Cactus` 主题为我们提供的评论工具是 `Disqus`，这是一个各方面都很好的评论系统，但有一点问题是，这个评论系统**在国内无法使用**，所以我们只是简单翻译一下官方的介绍：

首先，在 Disqus 注册我们的站点: [https://disqus.com/admin/create/](http://disqus.com/admin/create/).

然后, 修改 `themes/cactus/_config.yml`:

```
disqus:
  enabled: true
  shortname: SITENAME
```

这里的 `SITENAME` 是在注册 Disqus 时，你给你的站点填写的名字。

## 结尾

好了，我们的博客网站建好了。由于我最迫切的需求就是快速的完成博客建站，所以多余的东西我都没有研究，但其实 Hexo 还可以有很多拓展，GitHub Pages 也还有一些东西可以配置，这些都需要大家自己去研究。

后期我还会持续优化这个网站，比如我计划修改一下源码，把 Cactus 中的 `Disqus` 评论换成墙内能用的如 `livere` 之类的东西 ，如果可以，我会另外发文记录。

其实，这篇文章中的绝大多数内容都来源于咱们使用的各个工具的官网，我只是粗糙地把他们按照一定的逻辑顺序排列到一起。如果需要更详细的说明，大家可以看下面列出的这些参考文档：

* GitHub的注册与使用：https://help.github.com/cn
* Hexo的安装及使用：https://hexo.io/zh-cn/docs/
* Cactus主题的配置：https://github.com/probberechts/hexo-theme-cactus