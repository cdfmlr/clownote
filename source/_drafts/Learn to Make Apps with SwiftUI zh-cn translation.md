---
title: 用 SwiftUI 制造 App
---



# 用 SwiftUI 制造 App

> 翻译自：Learn to Make Apps with SwiftUI
>
> 英文原文：https://developer.apple.com/tutorials/swiftui/tutorials
>
> （这篇文章是 Apple 给的 SwiftUI 官方教程啊，我随便搜了一下居然没找到中文翻译版。。。没人做我就自己翻吧。）

跟着这一系列教程学习用 SwiftUI 和 Xcode 制作 App。

## SwiftUI 基本

### 创建、组合 Views

这个教程教你构建一个 iOS app —— *Landmarks*。这个 App 是用来发现、分享你喜欢的地点的。我们会从构建一个显示地标(Landmarks) 详情的 View 开始。

要布局这个地标详情的 View，我们用 *stacks* 来组合、堆放[^1] 图片和文本视图组件。我们还要用引入 MapKit 组件来提供地图视图。在你修改视图的时候，Xcode 会给你及时的反馈，让你看到改变的代码。

下载项目文件，跟着下面的步骤开始构建工程吧：

> 预计用时：40 分钟
>
> 下载项目文件：https://docs-assets.developer.apple.com/published/88e110a956/CreatingAndCombiningViews.zip
>
> Xcode 11：https://itunes.apple.com/us/app/xcode/id497799835?mt=12

[^1]: combine and layer，我的理解是 combine 在同一水平面组合，layer 做垂直方向上堆放

#### [§ 1](https://developer.apple.com/tutorials/swiftui/creating-and-combining-views#create-a-new-project-and-explore-the-canvas) 创建新项目和探索画布

在 Xcode 创建一个使用 SwiftUI 的新项目。在里面探索画布、预览和 SwiftUI 的模版代码。

要在 Xcode 里预览视图，并与之交互，需要 macOS Catalina 10.15。[^2]

1. 打开 Xcode，然后在 Xcode 的启动页面点击 **Create a new Xcode project**，或者选择 **File > New > Project**。[^3] ![一张屏幕截图，Welcome to Xcode页面的，当你打开Xcode的时候会显示。当你打开Xcode时，有三个选项可供选择。开始使用一个playground，创建一个新的Xcode项目，和克隆一个现有的项目。第二个选项--创建一个新的Xcode项目--被突出显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1geow8syirjj30tg0xcwg2.jpg)

2. 在模版选择窗口里选择 **iOS** 平台、**Single View App** 模版，然后点击 **Next**。![Xcode中的模板选择表的截图。在最上面一行中，iOS被选为平台。在应用部分，选择了单视图App作为模板；在工作表右下角的下一步按钮上方有一个高亮显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1geox1ilcygj30tg0xcjtr.jpg)

3. 在 Product Name 处输入“Landmarks”，user interface 选择 **SwiftUI**，点击 **Next**。然后选择一个位置在你的 Mac 上保存这个项目。![Xcode中的模板选择表截图。在最上面一行中，iOS被选为平台。在应用部分，选择了单视图App作为模板；在工作表右下角的下一步按钮上方有一个高亮显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1geox5hibhcj30u00xzwhi.jpg)

4. 在项目导航栏(Project navigator)里选择`ContentView.swift`。默认情况下，SwiftUI 声明了两个结构体，第一个遵循了 View 协议，是用来描述视图的内容和布局的；第二个结构体声明了对这个视图的预览。

   ```swift
   //ContentView.swift
   
   import SwiftUI
   
   struct ContentView: View {
       var body: some View {
           Text("Hello World")
       }
   }
   
   struct ContentView_Previews: PreviewProvider {
       static var previews: some View {
           ContentView()
       }
   }
   ```
   预览：
   ![来自Xcode预览版的屏幕截图，就像它在iPhone上显示的那样，文字 "Hello World！"位于显示屏中间。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepcdbhk3aj30n61e60sv.jpg)

5. 在画布(canvas)里点击 **Resume ** 来显示预览。

   Tips：如果画布没有显示，你可以选择**Editor > Editor and Canvas**，来打卡它。

   ![A screenshot of the Preview window, with a Refresh button in its upper-right corner.](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepcq2cqr7j30tg0xc3zm.jpg)

6. 在 body 属性里，把 `“Hello World”` 改成对你自己打招呼的话。

   在你改变视图体(a view’s `body` property)的时候，预览及时地反映出了你的改变。

   ```swift
   //ContentView.swift
   
   import SwiftUI
   
   struct ContentView: View {
       var body: some View {
           Text("Hello SwiftUI!")
       }
   }
   
   struct ContentView_Previews: PreviewProvider {
       static var previews: some View {
           ContentView()
       }
   }
   ```

   预览：![来自于Xcode预览版的屏幕截图，在iPhone上显示，文字 "Hello SwiftUI！"位于显示屏中间。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepcu7nm23j30n61e6glr.jpg)
   
   

【译者拓展】：由于本人使用 MacOS Mojave 10.14，所以无法使用预览的功能。这还是相当痛苦的，没有预览几乎难以进行 UI 设计了，所以我采取的代替方案是在 Playground 中写 SwiftUI。实现的步骤如下：

新建一个 Playground，选择 iOS 平台，Blank 模版。打开 Playground 后，把里面的代码替换如下：

```swift
import SwiftUI
import PlaygroundSupport

struct HelloWoldView: View {
    var body: some View {
        Text("Hello World")
    }
}

PlaygroundPage.current.setLiveView(HelloWoldView())

```

运行 Playground 至第 10 行（鼠标移到第十行的行标处，数字变成表示运行的箭头▶️，点击这个箭头），即可看到预览：

![一张 Playground 的截图，左边写了前文里的 Hello World 程序代码，右边显示出了预览——一个空白的页面中间显示有文本 Hello World](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepdi7wg5vj31e00u01fv.jpg)

这样勉强可以进行 SwiftUI 的开发，只是无法如在 Catalina 的 Xcode 项目里那样和画布交互。



[^2]: 本人使用 MacOS Mojave 10.14，所以无法使用预览的功能，我采取的代替方案是在 Playground 中写 SwiftUI：![一个 Playground 的截图，图中写了一段显示 Hello SwiftUI 文本的程序，右边显示出了预览](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepd5aetotj31e00u0nkd.jpg)
[^3]: 分享一个让我很感动的细节，Apple 的文档里，居然对这样的一张截图写了如此详细的 alt 说明：![Apple文档的截图，显示了 apple 对网页上的一张图片写了特别详细的 alt 说明](https://tva1.sinaimg.cn/large/007S8ZIlgy1geowgmdd4nj31aa0u0tyk.jpg) 扪心自问，我从来不认真写 alt，总认为这东西又看不见写它干嘛！看到了 Apple 的做法，不禁思索，万一正在阅读你的文章的人因为网络、计算机、甚至是视觉问题无法看到这张图片，我们难道没有义务为这样的特殊人群写一段图片说明嘛？尤其是对有视觉障碍的人士！以后我会尽可能认真写 alt！第一步就是——这篇文章翻译里包括这些 alt！

#### [§ 2](https://developer.apple.com/tutorials/swiftui/creating-and-combining-views#customize-the-text-view) 定制文本视图(Text View)





## 绘图和动画



## App 设计和布局



## 框架整合



