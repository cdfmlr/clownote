---
date: 2021-08-18 19:05:06.912224
title: macOS 设置快捷键启动终端
---
# macOS 设置快捷键启动终端

在 Linux 系统中，习惯了可以随处唤出终端，做一些简单的工作，比如用 aria2c 下载个东西什么的。

换到 macOS 就觉得很麻烦，macOS 系统自带的终端并不支持设置快捷键快速打开一个命令行窗口。但我们可以通过「自动操作」+「Apple Script」来实现这个操作。

## 自动操作

打开“自动操作”（`automator.app`）-> 新建 `服务`。

在里面添加一步 `运行 AppleScript`：

![自动操作的设置截图](https://tva1.sinaimg.cn/large/008i3skNgy1gtl1tnn7mjj611p0u0ae102.jpg)

填入 Apple Script 内容:

```vbscript
on run {input, parameters}
	tell application "Terminal"
		set origSettings to default settings
		set default settings to settings set "mine quick"
		do script ""
		activate
		set default settings to origSettings
	end tell
	
	return input
end run
```

这段代码作用是：

- 让终端 app 设置默认的描述文件
- 用设置的描述文件新建终端窗口
- 最后重置默认的描述文件为之前的默认值

别忘了保存这个自动操作，取个名字，比如叫做 `New Terminal Window`.

**如果你不需要打开的终端窗口指定使用特定的描述文件，删掉那三行 `set` 就行了**：

### 特定描述文件

描述文件就是样式、以及使用什么 shell 之类的配置：（在终端的偏好设置里）

![终端偏好设置里描述文件的设置页](https://tva1.sinaimg.cn/large/008i3skNgy1gtl214g8fwj60wk0u0tbq02.jpg)

我的终端默认描述文件是「Pro」，平时工作用的，你这个是个纯黑色、不透明的，使用 bash，非常古典：

![Pro 描述文件效果](https://tva1.sinaimg.cn/large/008i3skNgy1gtl2ftnhp9j614d0u076f02.jpg)

我还自定义了一个描述文件，取名叫做「mine quick」，这个描述文件，和 Pro 的主要区别是，提供半透明的毛玻璃效果，并且使用 zsh。这个描述文件更现代、更契合现在的 macOS UI 的样式：

![mine quick 描述文件效果](https://tva1.sinaimg.cn/large/008i3skNly1gtl5aw8czuj61600u0t9z02.jpg)

（还有一点：这个 mine quick 会在不活动，也就是鼠标点了其他窗口后，提高透明度，这样就不会遮挡下层窗口的内容，总之这个 mine quick 用来做快速辅助工作更方便）

我希望做严肃的工作时，通过手动从终端 app 图标打开的窗口，获得一个 Pro 样式的。而通过快捷键打开的终端窗口，只是快速随便用用，辅助操作，使用 mine quick 描述文件。

所以就有了那段设置描述文件的操作。

## 设置全局快捷键

设置-> 键盘 -> 快捷键 -> 服务：

![设置快捷键截图](https://tva1.sinaimg.cn/large/008i3skNgy1gtl25jzqmij60x20u0ju702.jpg)



# 参考

- https://cloud.tencent.com/developer/ask/106143
- https://apple.stackexchange.com/questions/122875/opening-new-terminal-app-window-tab-with-a-certain-profile-from-command-line-or
- https://www.zhihu.com/question/20692634