---
date: 2020-07-26 15:43:10.020525
title: GitHub Actions 实践：Hexo GitHub Pages 博客持续部署
---

# GitHub Actions 实践: Hexo GitHub Pages 博客持续部署

我用 Hexo 来管理自己的文章、并部署到 Github Pags 已经有一段时间了。关于我构建这个博客系统的经过可以看这篇文章：《[GitHub + Hexo => 个人博客](https://clownote.github.io/2019/08/15/blog/GitHub加Hexo打造个人博客/)》。

在实际使用这个系统的过程中，很多时候，我都是有想法就打开 Typora 开始写，文章写完了就在开头手动补一个 YAML 配置，然后直接把 `.md` 文件扔到 `_post` 或者 `_draft` 里。然后用 Hexo CLI 生成、部署，然后把源文件用 Git 提交、推送到 GitHub 备份。这个过程基本如下所示：

```sh
$ vim newArticle.md    # 实际上我是用 Typora 的，这里编辑过程用 vim 代替
$ mv newArticle.md ~/clownote/source/_post    # 我的博客系统放在 ~/clownote
$ hexo g -d    # 生成、部署到 GitHub Pages
$ git add .
$ git commit -m "add newArticle"
$ git push
```

hexo 生成、部署、git 提交，这个过程果然还是太冗长了。我在想用没有一种方法可以简化这个套路化的流程。对此，我首先的想法是写一个 shell 脚本来简化整套流程。这个脚本提供如下接口：

```sh
$ clownote new newArticleTitle    # 新建文章，自动打开 Typora 编辑
$ clownote update    # 生成、部署、源码 git 提交
```

但感觉有点死板，而且我其实不太喜欢写 shell 脚本，那语法虽然很简洁、高效，但真的，，真的一言难尽。当然也可以用其他语言来写这东西，Python 就不错，不用编译、写个执行注释加上权限直接就能跑。但是，这样比较无趣嘛，我没有这么做。

现在是云时代了，CI/CD 这一套很流行了，玩这东西可能比写个烂脚本有意思多了，所以我选择用 CI/CD 这一套来完成任务。

## CI, CD & CD

简单说一下 CI/CD —— CI, CD & CD：Continuous Integration，Continuous Delivery，Continuous Deployment。翻译成中文：持续集成、持续交付和持续部署。

- 持续集成CI：提交代码到主分支前，自动编译、自动测试验证，没通过就不能合并；
- 持续交付CD：在 CI 验证通过后，如果没有问题，可以继续手动部署到生产环境中；
- 持续部署CD：把部署到生产环境的过程自动化，不需要手工操作。


> 还不了解 CI/CD 是什么？移步红帽的这篇 《[CI/CD是什么？如何理解持续集成、持续交付和持续部署](https://www.redhat.com/zh/topics/devops/what-is-ci-cd)》，还有这篇《[详解CI、CD & CD](http://www.ttlsa.com/news/ci-cd-cd/)》，还是不懂，就看看 [知乎](https://www.zhihu.com/question/23444990) 吧。

## 博客的持续部署

抛开定义，直观上，持续部署，顾名思义，就是持续不断地去部署，部署自动紧跟代码改变：你的提交了源码修改，部署上就自动更新了。对于我们的博客系统，也就是新建/修改/删除了文章，博客站点就自动更新、修改对应内容。从效果上来说，就是我们不用再去手动 `hexo g -d` 生成、部署了。

我们刚才提出的脚本就能达到这样的目的，但我觉得这样不太算持续部署，写脚本只是把一系列操作合并到一起让计算机逐步完成，本质并没有改变，你终究是自己做了全套的部署工作。但你细品，用持续部署就不一样了，它是先提交源码，然后它在云端就自动给你去生成(编译)、部署了，这个生成、部署的工作是不需要由你在本地完成的。

这些工作不由你来做靠谁做呢？由提供 CI/CD 服务的服务器自动来完成。其实 GitHub 就免费提供来这项服务，叫做 [GitHub Actions](https://github.com/features/actions)。

## GitHub Actions

GitHub Actions 可以自动在你的 GitHub 仓库发生事件时自动完成一些工作，比如在你推送提交(git push)到博客仓库时，自动给你部署上。详细的入门，推荐看看阮一峰老师的《[GitHub Actions 入门教程](http://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)》。当然，[官方文档](https://docs.github.com/en/actions) 也是很好的学习资料。

这个东西用起来有点像 Docker，可以以别人做好的“镜像”（在 GitHub Actions 中称为 Actions）为基础去执行一些工作，当然你也可以构建“镜像”。其实，已经有很多人做过自动在 Github Pages 持续部署 Hexo 博客的 Actions 了，我们甚至可以直接用。你可以在 GitHub 网页顶部看到一个 `Marketplace`，点进去可以搜别人写好的 Actions。

> 注：下文对 Workflow 的介绍：**Forked from [ruanyifeng/GitHub Actions 入门教程](http://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)**，并参考官方文档做了一定的修改、补充。

GitHub Actions 的配置文件叫做 Workflow，存放在代码仓库的 `.github/workflows` 目录。Workflow 文件是用 [YAML](https://yaml.org) 去写的，后缀名为 `.yml`。一个 repo 可以有多个 workflow 文件。GitHub 会发现 `.github/workflows` 目录里所有 `.yml` 文件，自动把他们识别为 Action，在出发其中指定的操作时就自动运行。下面介绍一些 Workflow 的基本写法：

（1）`name`：workflow 的名称。如果省略，则默认为当前 workflow 的文件名。

```yaml
name: GitHub Actions Demo
```

（2）`on`：指定触发 workflow 的事件。比如 push 时出发执行该 Action。

```yaml
on: push
# 如果有多种可以写数组：
on: [push, pull_request]
# 还可以指定分支 on.<push|pull_request>.<tags|branches>：
on:
  push:
    branches:    
      - master
```

（3）`jobs`：表示要执行的一项或多项任务，workflow 的主体。

```yaml
jobs:
  my_first_job:    # job_id
    name: My first job
    # ...
  greeting_job:
    name: This job needs my_first_job
    needs: my_first_job
    runs-on: ubuntu-latest
    steps:
      - name: Print a greeting
        env:
          MY_VAR: Hi there! My name is
          MY_NAME: Mona
        run: |
          echo $MY_VAR $MY_NAME.
      - name: Hello world
        uses: actions/hello-world-javascript-action@v1
        with:
          who-to-greet: 'Mona the Octocat'
        id: hello

```

- `name` ：任务的说明。
- `needs` ：指定当前任务的依赖关系，即运行顺序。
- `runs-on` ：指定运行所需要的虚拟机环境。必填，可以用 ubuntu、windows、macOS，还有好多版本可选，详细的看[文档](https://docs.github.com/en/actions/reference/virtual-environments-for-github-hosted-runners)。
- `steps`：`steps`字段指定每个 Job 的运行步骤，可以包含一个或多个步骤。每个步骤都可以指定以下字段：
  - `jobs.<job_id>.steps.name`：步骤名称。
  - `jobs.<job_id>.steps.id`：步骤的 step_id。
  - `jobs.<job_id>.steps.run`：该步骤运行的命令或者 action。带 env 来设置环境变量。
  - `jobs.<job_id>.steps.uses`：调用别人做好的 action。带 with 来指定运行参数。

接下来我们就开始实践，构建自动部署 GitHub Pages 的 GitHub Action。（GitHub 全家桶警告😨）

## 使用 sma11black/hexo-action

我查看、尝试了多个关于 Hexo 的 Actions，最后觉得 [sma11black/hexo-action](https://github.com/marketplace/actions/hexo-action) 提供了我需要的一切，代码写的也很好，文档也最为完备。所以就决定直接用它了，懒得自己写。

> 插嘴：这个项目真的不错，最后还写了几个[建议的 Hexo 博客设置](https://github.com/marketplace/actions/hexo-action#recommand-hexo-repository-settings)，这些建议确实不错。

下面跟着[文档](https://github.com/marketplace/actions/hexo-action)，使用这个 Action。

1. 设置 `Deploy keys` 和 `Secrets`。

首先在本地生成一对 ssh-key：

```sh
$ ssh-keygen -t rsa -C "your_username@example.com"
```

`your_username@example.com` 要时你自己的、你之后要在 *Github Pages* 仓库里提交的 GitHub 用户邮箱。

注意：参考 Issue [SSH Key doesnt work #6](https://github.com/sma11black/hexo-action/issues/6)，**不要加 passphrase**，让你填写、确认的时候直接回车。把生成文件保存到一个你能找到的地方（比如桌面，不要提交到 git 中，不要用默认位置）。

然后设置公钥：去你的 *Github Pages* 仓库，点 `Settings > Deploy Keys`，新建一个，把刚从生成的 `xxx.pub` 里面的内容填进去。

最后设置密钥：去你的 hexo 博客源文件仓库，点 `Settings > Secrets`，新建一个叫做 `DEPLOY_KEY` 的项，把刚才生成的另一个文件里的内容填进去。

2. 配置 workflows。

去 hexo 博客源文件仓库，在 GitHub 上仓库页面点 Actions，新建一个：

![屏幕快照，新建一个 Action](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh47brdrqgj319g0u07wh.jpg)

其实也可以在 `.github/workflows` 目录里创建一个  `.yml`  文件，开始编辑。是等效的。

然后，在 workflows 配置文件中写入下面代码：

```yml
name: Deploy

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    name: A job to deploy blog.
    steps:
    - name: Checkout
      uses: actions/checkout@v1
      with:
        submodules: true # Checkout private submodules(themes or something else).
    
    # Caching dependencies to speed up workflows. (GitHub will remove any cache entries that have not been accessed in over 7 days.)
    - name: Cache node modules
      uses: actions/cache@v1
      id: cache
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-node-
    - name: Install Dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      run: npm ci
    
    # Deploy hexo blog website.
    - name: Deploy (Hexo g -d)
      id: deploy
      uses: sma11black/hexo-action@v1.0.2
      with:
        deploy_key: ${{ secrets.DEPLOY_KEY }}
        user_name: your_username
        user_email: your_username@example.com
        commit_msg: ${{ github.event.head_commit.message }}  # (or delete this input setting to use hexo default settings)
    # Use the output from the `deploy` step(use for test action)
    - name: Get the output
      run: |
        echo "${{ steps.deploy.outputs.notify }}"
```

注意把 user_name、user_email 换成你刚才创建 ssh-key 的那个。

把编辑好的配置提交上，就完成了！以后每次你 git push 到 GitHub，博客网站就自动更新了！

## 踩坑

1. **Action 内部无法访问 GitHub**

现在 git push 时，你可能发现 Github 发邮件告诉你运行失败了！打开看结果日志里会发现爆出了 这种错误：

```
fatal: could not read Username for 'https://github.com': No such device or address
```

首先确定之前的步骤正确无误，尤其是 user_email 配置和生成的 ssh-key 一致，且 publish key、private key 设置正确。

如果这些都确认正确无误，请参考[sma11black/hexo-action Issue #5](https://github.com/sma11black/hexo-action/issues/5)，在你的 hexo 配置文件 `_config.yml` 中，看看能不能把 deploy repo 的 URL 从 **HTTPS** 的换成 **SSH** 的：

```yaml
deploy:
  type: git
  repo: git@github.com:<username>/<username>.github.io.git
  # 改之前是 https://github.com/...
  branch: master
```

这个解决了我的问题。

2. **博客发布时间错乱**

之前提到过，我平时写文章都是直接打开 Typora 就写，比如现在：

![本文写作过程中 typora 的屏幕快照](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh48f31zmjj315b0u0dwz.jpg)

你可以看到我是没保存的，写完之后我会手动在文章开头写 YAML 配置，然后扔到 `_post` 里：

```yaml
---
title: GitHub Actions 实践: Hexo GitHub Pages 博客持续部署
tags: blog
---
```

其实更一般的，因为懒，我就写个 title😂（有时候甚至连 title 都忘记写）。但如果你用 `hexo new`、`hexo publish` 去新建、公开文章的话，hexo给你自动完成的配置里还会多一项 `date` 写上文章创建的时间。生成网页时，会根据这个 date 来确定文章日期；对于没写date标签的文章，它会自动把文章发布时间设置成你系统上文件创建的时间。

我以前都忽略了这个 date，这对于在本地生成是没问题的，因为本地文件系统中保存着文件创建的时间信息。但是一用上刚才写好的持续部署，我发现一大堆这种手动建立文件的文章发布时间全变成了最后一次自动部署的时间。比如我 7月24日 git push了，然后自动部署执行，一大堆文章的创建时间全变成了7月24日😱。

这个问题是由于，GitHub Actions 是在容器内跑的嘛，它运行时把源码从 GitHub 复制到容器内，所以文件的创建时间全部时运行的时间。然后生成、发布，这些没写 date 标签的文章就都变成了“新”写的。

为了解决这个问题，需要给所有以前没写 date 的文章补上这个配置。还是很容易的，只要找到这些没写 date 的文章，然后在系统中查看文件属性里的创建时间，补上就好：

![查看文件属性里的创建时间，在文件中补充date](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh4960r7kpj31po0qa458.jpg)

但这并不是个小工程呐，涉及的文章有数十篇，肯定不可能手动去做这个操作。所以，写程序来完成这个任务！做这件事的程序思路如下：

![自动完成YAML信息补全的程序流程图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gh4ak19a40j30wz0u0tbm.jpg)

我用 Python 实现了这个程序。

### 文章YAML配置补全脚本

因为配置是写成 YAML 的嘛，所以说，首先，我们需要找一个 Python 的 YAML 库，我可不想手写一份 YAML 解析、生成的代码。Emmm，我的电脑上有其他库依赖安装了一个 [PyYAML](https://pyyaml.org)，所以就直接用这个了。关于 YAML，我们主要只用两种功能：解析和生成，可以用如下代码完成：

```python
import yaml    # 导入 PyYAML

# 从字符串读取 YAML 内容，解析成 Python 对象，正常情况返回一个 dict：
yaml.safe_load(content)

# 把 Python 对象（一般用个 dict）转化成 YAML 内容：
content = yaml.dump(data, allow_unicode=True)
```

然后我们就要来封装我们需要的从博客文件中读取、写入 YAML 配置的函数了：

首先是读取：从一篇文章中读取 YAML 配置，即在文章开头处两行 `---` 之间的符合 YAML 语法的配置信息。返回 `yaml.safe_load` 出来的 Python 对象、原文件中 YAML 配置的起始结束行号（从0开始计数，闭区间），以及一个代表文件中是否存在 YAML 配置的 bool：

```python
def read_yaml(file_path):
    assert os.path.isfile(file_path), f"Target file not exists: {file_path}"

    is_yaml = False
    yaml_content = ''
    yaml_line = []
    lines_cnt = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == '---':
                yaml_line.append(lines_cnt)
                if is_yaml or (lines_cnt > 1):
                    break
                is_yaml = not is_yaml
            if is_yaml:
                yaml_content += line.replace('\t', '  ')
            lines_cnt += 1

    return yaml.safe_load(yaml_content), yaml_line, len(yaml_line) == 2

```

还有是写入，在文件头部写入信息，如果文件特别大还是有点头疼的， 但好在博客文章不可能太长，可以暂不考虑文件太大的情况，只需把文章内容全部先读出来，然后在文件头部覆盖写入 YAML 配置，再把原内容写回去。我们需要写的是一个 `write_yaml`  函数向其参数 file_path 指定的文件开头写入 yaml_data 转化成的 YAML 配置信息，YAML 信息将被前后各一行 `---` 所包裹：

```python
def write_yaml(file_path, yaml_data) -> None:
    yaml_text = yaml.dump(yaml_data, allow_unicode=True)

    wrapper = '---\n'
    yaml_wrapped = wrapper + yaml_text + wrapper

    with open(file_path, "r+") as f:
        file_content = f.read()
        f.seek(0)
        f.write(yaml_wrapped)
        f.write(file_content)

```

注意，我们刚才的 `write_yaml` 写入并没有删除原有的 YAML 信息，所以如果以前有的话就重复了。咱们刚才写的 `read_yaml` 返回了文件中是否有 YAML、YAML 配置的始末位置对吧，依靠这两个，我们就可以把原来存在的 YAML 删除了：

```python
def remove_lines(file_path, lines_range) -> None:
    # 从 file_path 文件中删除 lines_range 指定的行(闭区间[start, end]，从0开始计数)
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    temp_file = os.path.join(file_dir, f'.{file_name}.tmp')
    shutil.copy(file_path, temp_file)

    with open(temp_file, 'r') as f_in:
        with open(file_path, 'w') as f_out:
            f_out.writelines(line for i, line in enumerate(
                f_in) if i not in range(lines_range[0], lines_range[1]+1))

    os.remove(temp_file)

# 在调用的地方，删除原有 YAML 配置：
data, yaml_line, has_yaml = read_yaml(article)
if has_yaml:
	remove_lines(article, yaml_line)

```

Ok，YAML 的读写就做好了。接下来写生成 title、date 的函数，并和文件中读取的合并。 title 取文件名 `a.md` 中的 `a`，date 取文件创建时间（在 Mac 中，可以用 stat 的 birthtime 获取）：

```python
def get_creation_time(file_path):
    if platform.platform().find('Darwin') != -1:
        return os.stat(file_path).st_birthtime
    # ctime: Linux 是 inode 的 change time；据说 Windows 是 creation time
    return os.path.getctime(file_path)

def generate_base_conf(file_path) -> dict:
    title = os.path.basename(file_path)
    title_list = title.split('.')
    if len(title_list) > 1:
        title = ''.join(title_list[:-1])

    creation_time = get_creation_time(file_path)
    date = datetime.datetime.fromtimestamp(creation_time)

    return {'title': title, 'date': date}

# 在调用的地方，合并配置信息：
conf = generate_base_conf(article)
data, yaml_line, has_yaml = read_yaml(article)
if isinstance(data, dict):
    conf.update(data)
```

最后，我们写一个寻找所有博客文章文件的函数，然后遍历文章，完成处理：

```python
def md_files_gen(dir, file_filter=lambda fp: True):
    # 返回一个 generator，生成 dir 目录下所有使 file_filter 返回 True 的 .md 文件的路径
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.lower().endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                if file_filter(file_path):
                    yield file_path

def complete_yaml4blogs(dir):
    blogs = md_files_gen(dir)
    for article in blogs:
        print(article)
        conf = generate_base_conf(article)
        data, yaml_line, has_yaml = read_yaml(article)
        if has_yaml:
            remove_lines(article, yaml_line)
        if isinstance(data, dict):
            conf.update(data)
        write_yaml(article, conf)

# 最后调用 complete_yaml4blogs 就可以完成工作了：
complete_yaml4blogs('/Users/foo/hexo-blog/source')
```

P.S. `md_files_gen` 的 `file_filter` 是为了方便日后拓展使用而做的，比如我们可以利用这个东西过滤，只处理最近一个月内的新文件。

完整的代码我放去一个 Gist 了：[cdfmlr/complete_yaml4blogs.py](https://gist.github.com/cdfmlr/d5a40f670ab71512511a63bf94d8d424)。

<script src="https://gist.github.com/cdfmlr/d5a40f670ab71512511a63bf94d8d424.js"></script>

## 后记

啧，这篇文章写的，，结构好像有点问题。本来是介绍用 GitHub Actions 的，却花了大量的篇幅介绍我怎么处理偷懒造成的 bug 😂。不管了，解决这个问题还是很有趣的，练习一下 Python 文件操作，还顺便学了个 PyYAML 库，也不亏吧。

---

本文由 CDFMLR 原创，收录于个人博客 https://clownote.github.io。

