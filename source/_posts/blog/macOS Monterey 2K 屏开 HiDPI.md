---
date: 2022-10-03 15:51:38.706881
title: macOS Monterey 2K 屏开 HiDPI
---
# Intel MacBook Monterey 2K 屏开 HiDPI

苹果原装 2k 和 1080p 都一言难尽啊（什么时候学学隔壁巨硬家极为先进的缩放技术），还是得开 HiDPI。但是系统更新了，以前的流程不好使了，浅记一下解决问题的流程。

---

先装 RDM：

- https://github.com/avibrazil/RDM

MacBook 合盖，查外置显示器 ID：

```sh
ioreg -l | grep "DisplayVendorID"
ioreg -l | grep "DisplayProductID"
```

output：

```sh
    | |   | |         "DisplayVendorID" = 12451
    | |   | |         "DisplayProductID" = 10003
```

两个数字转十六进制：

```c
0x30a3
0x2713
```

制作显示器信息文件：

```sh
mkdir DisplayVendorID-30a3
cd DisplayVendorID-30a3
touch DisplayProductID-2713
```

[在线生成配置文件内容](https://codeclou.github.io/Display-Override-PropertyList-File-Parser-and-Generator-with-HiDPI-Support-For-Scaled-Resolutions/)，`vim DisplayProductID-2713`，粘贴:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>DisplayProductName</key>
  <string>LECOO M2712Q</string>
  <key>DisplayProductID</key>
  <integer>10003</integer>
  <key>DisplayVendorID</key>
  <integer>12451</integer>
  <key>scale-resolutions</key>
  <array>
    <data>AAAKAAAABaAAAAABACAAAA==</data>
    <data>AAAFAAAAAtAAAAABACAAAA==</data>
    <data>AAAPAAAACHAAAAABACAAAA==</data>
    <data>AAAHgAAABDgAAAABACAAAA==</data>
    <data>AAAMgAAABwgAAAABACAAAA==</data>
    <data>AAAGQAAAA4QAAAABACAAAA==</data>
    <data>AAAKAgAABaAAAAABACAAAA==</data>
    <data>AAAKrAAABgAAAAABACAAAA==</data>
    <data>AAAFVgAAAwAAAAABACAAAA==</data>
  </array>
</dict>
</plist>
```

配置文件放到系统中：（下面带 ❌ 的步骤实际不能用了）

---

❌ 关系统完整性保护：

- 重启，⌘+R，进恢复模式，适用工具 -> 终端：

```sh
 csrutil disable 
```

- 重启，正常模式：

```sh
sudo defaults write /Library/Preferences/com.apple.windowserver.plist DisplayResolutionEnabled -bool true
```

❌ 复制配置文件（Bug Sur 以后，这步不成功）：

```sh
cp -r DisplayVendorID-30a3 /System/Library/Displays/Contents/Resources/Overrides/
```

❌ 系统完整性保护开回来：

- 重启，⌘+R，进恢复模式，适用工具 -> 终端：

```sh
 csrutil disable 
```

- 重启，正常模式

---

✅ 配置文件放到系统中的最终**解决方案**：放到另一个没有系统保护，但作用一样的位置：

```sh
sudo mkdir -p /Library/Displays/Contents/Resources/Overrides
sudo cp /Users/c/Desktop/DisplayVendorID-30a3  /Library/Displays/Contents/Resources/Overrides
```

重启，RDM 中选用带闪电的 `1920x1080 ⚡️` 即享 HiDPI。

## 参考文献

- https://post.smzdm.com/p/alpzq4kg/p3/
- https://www.jianshu.com/p/30f986617278