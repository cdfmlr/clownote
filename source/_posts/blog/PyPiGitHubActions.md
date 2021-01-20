---
date: 2021-01-16 13:45:04.867873
tags: Python
title: 用GitHub Actions自动打包发布Python项目
---


# 用 GitHub Actions 自动打包发布 Python 项目

## 前言

还在手动打包上传 PyPI？GitHub Actions 自动化真香～！

在《[Python 代码一键转流程图](https://blog.csdn.net/u012419550/article/details/109258117)》一文里，我介绍了我的开源项目 [PyFlowchart](https://github.com/cdfmlr/pyflowchart)。过去这段时间里，已经有好几位小伙伴为这个项目提出了建议，或者报告了 Bug 啦。在这几位朋友的帮助下，项目也迭代了几个版本了。之前，这个项目每次版本更新，我都需要做很多写代码意外的麻烦工作：

1. 在 GitHub 上 publish 一个 release，
2. 手动打包上传 PyPI。

这个过程非常反人类，release 一个版本要做两个工作。更可怕的是，打包上传 PyPI 的工作十分模版化（鄙人拙作《[如何用 pip 安装自己写的包](https://blog.csdn.net/u012419550/article/details/105967006)》一文介绍了这个过程）。我觉得作为开发者，不应该把时间浪费在这种套路工作上。

于是我想去了过去我写过一篇叫做《[还在手动发博客？GitHub Actions自动化真香](https://blog.csdn.net/u012419550/article/details/107594751)》的文章，大致介绍了我是如何利用 GitHub Actions 自动更新博客网站的。所以，今回，我尝试用 GitHub Actions 搭建了一套发布新版本时，自动打包上传 PyPI 📦 的工作流程。

现在，发布新的版本时，就只需在 GitHub 上新建一个 Release。GitHub Actions 会自动帮我完成构建、打包、上传 PyPI 的工作。

本文就介绍如何利用 GitHub Actions 自动发布 Python 包到 PyPI。

（注：我在 PyFlowchart 项目中使用的实现和下文略有不同，我根据需求做了一些修改，如果你感兴趣，可以看一看我的实现：https://github.com/cdfmlr/pyflowchart/tree/master/.github/workflows）



---



> 下文翻译自 PyPA 的文章《Publishing package distribution releases using GitHub Actions CI/CD workflows》
>
> 原文链接：https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/



[GitHub Actions CI/CD](https://github.com/features/actions) 允许在 GitHub 平台上特定的事件发生时自动运行一系列的命令。用这个就可以做设置一个响应 push 事件的工作流程。本文将展示如何当有 git push 时发布一个新的 Python 包发行版（到 PyPI）。我们将使用到 [pypa/gh-action-pypi-publish GitHub Action](https://github.com/marketplace/actions/pypi-publish)。

注意：这个教程假设你已经有在 GitHub 上有一个 Python 项目，并且你知道如何构建包，并把它发布到 PyPI。

## 在 GitHub 上保存 token

在本文中，我们会把项目上传到 PyPI 和 TestPyPI。所以需要生成两份独立的 token，并把它们保存到 GitHub 的仓库设置中。

我们开始吧！🚀

1. 访问 https://pypi.org/manage/account/#api-tokens ，创建一个新的 [API token](https://pypi.org/help/#apitoken)。 如果你已经在 PyPI 里发布过你的项目了，那么你应该把 token 的范围(token scope) 限定为只能操作这个项目的。你可以把新 token 命名为 `GitHub Actions CI/CD —project-org/project-repo` 之类的，方便辨识。生成 token 后**不要关闭浏览器页面—— token 只会显示一次**。
2. 在另一个浏览器选项卡或窗口中，打开 GitHub 上你的项目页面，点击 `Settings` 选项卡，然后点击左侧边栏里的 [Secrets](https://help.github.com/en/articles/virtual-environments-for-github-actions#creating-and-using-secrets-encrypted-variables) 。
3. 创建一个新的 sercret，命令为 `PYPI_API_TOKEN`，然后复制粘贴第一步生成的 token。
4. 访问 https://test.pypi.org/manage/account/#api-tokens ，重复之前的步骤，把 TestPyPI 的 token 保存成 `TEST_PYPI_API_TOKEN`。

**注意**：如果你还没有 TestPyPI 账号，你应该注册一个。TestPyPI 和 PyPI 的账号不共通哦。

## 创建 workflow

GitHub CI/CD 工作流程（workflow）是用 YAML 格式的文件储存到仓库的 `.github/workflows/` 目录里的。

我们创建一个  `.github/workflows/publish-to-test-pypi.yml` 文件。

我们将从一个有意义的名称开始，然后定义触发 GitHub 运行此工作流程的事件：

```yaml
name: Publish Python 🐍 distributions 📦 to PyPI and TestPyPI

on: push
```

## 定义工作流程的工作环境

现在，我们来为工作（job）添加初始设置。这个过程将执行我们稍后定义的命令。在这里，我们将使用Ubuntu 18.04：

```yaml
jobs:
  build-n-publish:
    name: Build and publish Python 🐍 distributions 📦 to PyPI and TestPyPI
    runs-on: ubuntu-18.04
```

## 签出项目，构建发行版

然后，在该 `build-n-publish` 部分下添加以下内容：

```yaml
    steps:
    - uses: actions/checkout@master
    - name: Set up Python 3.7
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
```

这些操作会把我们的项目源码下载到 CI 运行容器里，然后安装并激活 Python 3.7 环境。

现在，我们就可以从源码构建 dist 了。在此示例中，我们将使用`build`包，所以假设项目里已正确设置 `pyproject.toml` （请参见 [PEP 517](https://www.python.org/dev/peps/pep-0517) / [PEP 518](https://www.python.org/dev/peps/pep-0518)）。

（注：emmm，其实这里不写 `pyproject.toml` 问题也不大）

提示：你可以使用任何其他方法来构建发行版，只要将准备好上传的包保存到 `dist/` 文件夹中即可。

将下面的代码加到 `steps` 里：

```yaml
    - name: Install pypa/build
      run: >-
        python -m
        pip install
        build
        --user
    - name: Build a binary wheel and a source tarball
      run: >-
        python -m
        build
        --sdist
        --wheel
        --outdir dist/
        .
```

## 发布到 PyPI 和 TestPyPI

最后，添加如下代码：

```yaml
    - name: Publish distribution 📦 to Test PyPI
      uses: pypa/gh-action-pypi-publish@master
      with:
        password: ${{ secrets.TEST_PYPI_API_TOKEN }}
        repository_url: https://test.pypi.org/legacy/
    - name: Publish distribution 📦 to PyPI
      if: startsWith(github.ref, 'refs/tags')
      uses: pypa/gh-action-pypi-publish@master
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

这两个 step 调用了 [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) GitHub Action：

第一个步骤无条件地将 `dist/` 文件夹的内容上传到TestPyPI。第二个步骤将其内容上传到 PyPI，这一步只会对被打了标签（git tag）的提交执行。

## 完事，收工！

现在，每当你将打了标签（tag）的提交 push 到 GitHub 上时，此工作流程都会将其发布到 PyPI。同时，对于任意 push ，它都会将其打包发布到 TestPyPI，这对于提供 alpha 测试版本以及确保发布渠道保持健康非常有用！

---

```python
by("CDFMLR", "2021-01-17")
# 啊，今天昆明都下雪了，家里巨冷。。。
# See you ❄️
```


