---
date: 2022-01-05 17:33:41.007290
title: 重装 macOS 开发环境总结与教训
---
# 重装 macOS 开发环境总结与教训

## 整理

工具：OmniDiskSweeper、OnyX

不要的垃圾先删掉。

## 备份

1. Time Machine 完整备份
2. 重要文件
   - 个人文件：打包加密，放移动硬盘：各种文档、收藏的书籍、图片、视频
   - 工作文件：打包压缩，放移动硬盘：各种文档、**密钥**（`~/.ssh`、`~/.bashrc`、`~/.zshrc`、`~/.vimrc`...）、**证书**、**配置文件**（v2啥的 config）
   - 各种项目源码： git 和远端同步一下
   - 艺术作品：分类整理放移动硬盘（`src` 目录归档压缩）：音乐、视频、游戏、画作
   - `brew list > brew.list.txt`
   - `ls /Applications > app.list.txt`
   - `pip3 list > pip3.list.txt`
   - Learning、Working、Desktop 目录：直接复制一份到移动硬盘
3. 其他：
   - Chrome 保存密码导出一下、插件列表
   - Safari 插件列表
   - Terminal 配置文件
   - VS Code 配置
   - JetBrains 家各种 IDE 配置（可以直接把 `~/Library/Application Support/JetBrains` 移到移动硬盘）
   - Garageband、Logic 的音源移到移动硬盘

## 抹掉重装

使用“磁盘工具”抹掉基于 Intel 的 Mac: https://support.apple.com/zh-cn/HT208496

注意：

> 8. 抹掉操作完成后，选择边栏中的任何其他内部宗卷，然后点按工具栏中的删除宗卷 (–) 按钮以删除对应宗卷。

**在这一步骤中，请忽略名为“Macintosh HD”或“Macintosh HD - Data”的任何内置宗卷，以及边栏中“外置”和“磁盘映像”部分的任何宗卷。**

抹掉之后只有 macOS Base System，要从网上重新下完整的 macOS，10 多 GiB，要等一下。

## 新 macOS 设置

注意开防火墙、隐身。 

## 重装基本环境

0. ~~V2什么U~~
1. Apple 命令行工具 Command Line Tools：`xcode-select --install`
1. brew（先把脚本下下来，配成国内源，再安装）
1. Pyenv、Pipenv
1. GCC、Golang、Java、Rust、Node.js
1. ffmpeg、wget、aria2、tldr，（可以把 V 某也用 brew 重装方便管理）
1. Docker、Chrome、VS Code
1. Typora
1. QQ、微信、网易云、阿里云盘、百度网盘、WPS
1. Pages、Numbers、Keynotes、Garageband、iMovie
1. Tiles、AppCleaner、OmniDiskSweeper、OnyX、AdGuard

（我的 JetBrains 全家桶是直接用 Toolbox 装在移动硬盘的，不用重装，其他重型软件也是）

安装过程中，brew 自己依赖出来的新版本 Python@3.9、Python@3.10 用上一篇文章**《将 Homebrew 安装的 Python 加入 pyenv 版本管理》**的方法加到 Pyenv 里，方便以后就不用下载了。

（都是固定操作，应该写个 shell 脚本记一下的 LOL）

## 配置、文档归位

各种配置文件（`~/.xxx`）拉回来。

各种软链接，按照移动硬盘上的 README 来重建。

各种项目目录、文档放回来。