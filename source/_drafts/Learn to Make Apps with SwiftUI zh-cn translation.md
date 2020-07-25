---
date: 2020-05-12 08:49:20
title: 用 SwiftUI 创造 App
---



# 用 SwiftUI 创造 App

> 翻译自：Learn to Make Apps with SwiftUI
>
> 英文原文：https://developer.apple.com/tutorials/swiftui/tutorials
>
> 这篇文章是 Apple 给的 SwiftUI 官方教程啊，我随便搜了一下居然没找到中文翻译版。。。没人做我就自己翻吧。

跟着这一系列教程学习用 SwiftUI 和 Xcode 制作 App。

## SwiftUI 基本

### 创建、组合 Views

这个教程教你构建一个 iOS app —— *Landmarks*。这个 App 是用来发现、分享你喜欢的地点的。我们会从构建一个显示地标(Landmarks) 详情的 View 开始。

要布局这个地标详情的 View，我们用 *stacks* 来组合、堆放[^1] 图片和文本视图组件。我们还要用引入 MapKit 组件来提供地图视图。在你修改视图的时候，Xcode 会给你及时的反馈，让你看到改变的代码。

下载项目文件，跟着下面的步骤开始构建工程吧：

> 预计用时：40 分钟
>
> 下载项目文件：https://docs-assets.developer.apple.com/published/b90bcabe8b9615e22850aaf17f3e7dfd/110/CreatingAndCombiningViews.zip
>
> Xcode 11：https://itunes.apple.com/us/app/xcode/id497799835?mt=12

[^1]: combine and layer，我的理解是 combine 在同一水平面组合，layer 做垂直方向上堆放

#### § 1 创建新项目和探索画布

> 原文链接：https://developer.apple.com/tutorials/swiftui/creating-and-combining-views#create-a-new-project-and-explore-the-canvas

在 Xcode 创建一个使用 SwiftUI 的新项目。在里面探索画布、预览和 SwiftUI 的模版代码。

要在 Xcode 里预览视图，并与之交互，需要 macOS Catalina 10.15。[^2]

**Step 1.** 打开 Xcode，然后在 Xcode 的启动页面点击 **Create a new Xcode project**，或者选择 **File > New > Project**。[^3] ![一张屏幕截图，Welcome to Xcode页面的，当你打开Xcode的时候会显示。当你打开Xcode时，有三个选项可供选择。开始使用一个playground，创建一个新的Xcode项目，和克隆一个现有的项目。第二个选项--创建一个新的Xcode项目--被突出显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1geow8syirjj30tg0xcwg2.jpg)

**Step 2.** 在模版选择窗口里选择 **iOS** 平台、**Single View App** 模版，然后点击 **Next**。![Xcode中的模板选择表的截图。在最上面一行中，iOS被选为平台。在应用部分，选择了单视图App作为模板；在工作表右下角的下一步按钮上方有一个高亮显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1geox1ilcygj30tg0xcjtr.jpg)

**Step 3.** 在 Product Name 处输入“Landmarks”，user interface 选择 **SwiftUI**，点击 **Next**。然后选择一个位置在你的 Mac 上保存这个项目。![Xcode中的模板选择表截图。在最上面一行中，iOS被选为平台。在应用部分，选择了单视图App作为模板；在工作表右下角的下一步按钮上方有一个高亮显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1geox5hibhcj30u00xzwhi.jpg)

**Step 4.** 在项目导航栏(Project navigator)里选择`ContentView.swift`。默认情况下，SwiftUI 声明了两个结构体，第一个遵循了 View 协议，是用来描述视图的内容和布局的；第二个结构体声明了对这个视图的预览。

![代码以及来预览的屏幕截图，预览是iPhone上显示的效果，文字"Hello World！"位于预览的中间。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2aqcod8mj30zr0u0gop.jpg)


**Step 5.** 在画布(canvas)里点击 **Resume ** 来显示预览。

Tips：如果画布没有显示，你可以选择**Editor > Editor and Canvas**，来打卡它。

![A screenshot of the Preview window, with a Refresh button in its upper-right corner.](https://tva1.sinaimg.cn/large/007S8ZIlgy1gepcq2cqr7j30tg0xc3zm.jpg)

**Step 6.** 在 body 属性里，把 `“Hello World”` 改成对你自己打招呼的话。

在你改变视图体(a view’s `body` property)的时候，预览及时地反映出了你的改变。

![代码以及来预览的屏幕截图，预览是iPhone上显示的效果，文字"Hello SwiftUI！"位于预览的中间。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2atforcrj30zc0u0tbt.jpg)



完成这一节后，我们的主要代码看上去是这样的：

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello SwiftUI!")
    }
}
```



【译注】：由于本人使用 MacOS Mojave 10.14，所以无法使用预览的功能。这还是相当痛苦的，没有预览几乎难以进行 UI 设计了，所以我采取的代替方案是在 Playground 中写 SwiftUI。实现的步骤如下：

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

#### § 2 定制文本视图(Text View)

> 原文链接: https://developer.apple.com/tutorials/swiftui/creating-and-combining-views#customize-the-text-view

通过修改代码，你可以定制视图的显示效果。当然，你也可以用检视器(inspector)来发现你可以做些什么，并帮助你完成代码。

在构建 *Landmarks* app 的过程中，你可以随意使用任何编辑器：代码编辑器(source editor)，画布(canvas)，检视器(inspectors)。无论你使用了那种方式来编辑，代码总会自动保持更新。

<video data-v-f6e12e74="" autoplay="autoplay" muted="muted" playsinline=""><!----><source src="https://docs-assets.developer.apple.com/published/62bc5b3021f9628ad1536bdab67f5781/110/customize-text-view.mp4"></video>

接下来，我们将使用监视器来定制文本视图。

**Step 1.** 在预览中，按住 command 点击我们写了问候的文本，会出现一个结构编辑弹出框(popover)。在这个弹出框里，选择 **Inspect**。

这个弹出框里还有其他的你可以定制的属性，不同的视图可能有不同的属性。

![结构编辑弹出框的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2443doj0j30tg0xcgr0.jpg)



**Step 2.** 在检视器中，把文本(Text)改成 “Turtle Rock” —— 你的 app 中要展现的第一个地标。

![在检视器中，把文本(Text)改成 “Turtle Rock”的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg249uwx45j30tg0xcwmm.jpg)

**Step 3.** 把字体修改成 **Title** (标题)。

这个操作是让文本使用系统字体，这种字体可以跟随用户当前的偏好设置。

【译注】也可以使用代码完成这个更改: `Text("Turtle Rock").font(.title)`。哈哈，这种写法就很 Swift，具体这是什么意思下面的原文有写。

![在检视器中，修改字体的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg248kgh47j30tg0xck13.jpg)

要用 SwiftUI 定制视图，我们可以调用称作修饰器(*modifiers*)的方法。修饰器会包装一个 View 来更改其显示效果或其他属性。每个修饰器都会返回一个新的 View，所以我们常链式调用多个修饰器以叠加效果。

**Step 4.** 手动修改代码，添加一个修饰器：`foregroundColor(.green)`，这是用来把文本颜色改成绿色的：

![修改后的代码和来自Xcode预览的截图，它显示一个在iPhone上的效果预览，绿色的文字，Turtle Rock，在显示器的中间。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2946pjduj317s0pigp3.jpg)

代码才是我们的视图效果的依据，当你用检视器来修改或移除修饰器时，Xcode 都会立刻在代码里做出相应的修改。

**Step 5.** 现在，我们在代码里按住 Command 点击 `Text` 的声明，从弹出框里选择 **Inspect**，这样也可以打开监视器。在 **Color** 菜单里，把颜色设置成 **Inherited**，这样文本的颜色就复原了。

![来自Xcode的结构化编辑器菜单截图，通过Command-点击文本视图的声明打开。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg25eor1eqj30tg0xcqfu.jpg)

**Step 6.** 注意，完成刚才那一步之后， Xcode 自动帮我们把代码做了相应的修改，即去掉了修饰器 `foregroundColor(.green)`：

![原文里的代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg27bz7r5sj317o0ougod.jpg)

完成这一节后，我们的主要代码看上去是这样的：

```swift
struct ContentView: View {
    var body: some View {
        Text("Turtle Rock")
            .font(.title)

    }
}
```

#### § 3 用 Stacks 组合视图

> 原文链接: https://developer.apple.com/tutorials/swiftui/creating-and-combining-views#Combine-Views-Using-Stacks

在上一节我们完成了一个标题。现在，我们将再添加一些文本视图来描述地标的详细信息，比如所处的公园名称和所在的州。

在使用 SwiftUI 创建 View 时，我们在视图的 `body` 属性里描述其内容、布局、行为。但是，body 属性只会返回**一个**视图。所以，我们要把多个视图放到 stack 里来让它们在水平、竖直、前后方向上组合在一起。

![一个VStack的示意图，在视图的上半部分显示了Turtle Rock的标题左对齐。下面是一个被高光包围的HStack。HStack包含三个视图。左边的视图显示文本"Joshua Tree National Park"。中间的视图是一个隔板Spacer。右边的视图显示文字 "California"](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg280wmdfij30f408ct8p.jpg)



在这一节里，我们我们将用一个竖直方向的 stack 来把标题放在一个包含了地标细节的水平 stack 的上方。

（emmm，我一直不太会翻译这种比较长的英文句子，可能是我语文学的不好吧，我不知道怎么解耦这种有嵌套结构的句子）

我们 Xcode 的结构编辑(structured editing)提供把一个 view 嵌入一个容器视图、打开检视器和其他许多有用的操作。

**Step 1.** 按住 Command 点击文本视图的初始化器(构造函数啦)，会显示出结构编辑弹出框，在里面选择 **Embed in VStack**（嵌入VStack）。

![当你Command点击文本初始化器时显示的弹出式菜单的截图。在菜单中，"嵌入VStack "选项被高亮显示。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg28iuv3hrj30tg0xcajy.jpg)

接下来，我们将通过从库里拖一个 Text 放到 Stack 里增加一个文本视图。

**Step 2.** 点击位于 Xcode 窗口右上方的加号（+）打开库。从里面拖一个 Text 出来放到我们的“Turtle Rock”文本视图代码的后面。

![画布和预览的截图，以及库窗口，显示了Turtle Rock下方的新文本视图。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2919jfa8j30tg0xc4bd.jpg)

**Step 3.** 把新的文本视图的内容替换为“**Joshua Tree National Park**”。

![代码和预览截图，预览中显示了Turtle Rock下方的新文本视图。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg296yvagmj317g0q4whx.jpg)

接下来我们还会定制刚刚添加的那个表示*位置*的文本视图，以匹配所需的布局。

**Step 4.** 设置位置文本的字体为 subheadline（副标题）。

```swift
Text("Joshua Tree National Park")
	.font(.subheadline)
```

**Step 5.** 编辑 VStack 的初始化器来指定视图前缘对齐（align the views by their leading edges，就是把左边对齐了，Android 里的 `gravity="start"` 这种意思吧）。

默认情况下，stack 会沿其轴线把内容中心对齐，并且只提供适合内容的空间。

![代码和预览的截图，预览是显示的是iPhone上的效果，Turtle Rock和Joshua Tree National Park文本在显示屏的中间左对齐。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg29moovfzj317s0ou0w9.jpg)

接下来，我们要在表示位置的文本右边增加一个文本，表示其所在的州。

**Step 6.** 在画布中，按住 Command 点击 **Joshua Tree National Park**，选择 **Embed in HStack**（嵌入HStack）。

![弹出窗口的截图，菜单中高亮显示Embed in HStack。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg29rui2mhj30tg0xcwnl.jpg)

**Step 7.** 在位置后面新建一个文本视图，把内容改成州名，把字体设置为 subheadline。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg29wvmdrrj30zf0u0td7.jpg)

**Step 8.**  为了让我们的布局占满整个设备的屏幕宽度，我们在包含公园和州名的 HStack 里添加一个 **Spacer** 来把两个文本视图分开。

`Spacer` 用来“撑大”容器布局，使其占满整个水平或竖直方向的父视图（its parent view）空间，而不再只是恰好包含内容。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2ahwhhvwj30zm0u0433.jpg)

**Step 9.** 最后，使用 `padding()` 修饰方法给地标的名称和细节增加一点空间。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2alkmh6oj30zn0u0791.jpg)

完成这一节后，我们的主要代码看上去是这样的：

```swift
struct ContentView: View {
    var body: some View {
        VStack(alignment: .leading) {
            Text("Turtle Rock")
                .font(.title)
            HStack{
                Text("Joshua Tree National Park")
                    .font(.subheadline)
                Spacer()
                Text("California")
                    .font(.subheadline)
            }
        }
        .padding()
    }
}
```

#### § 4 创建自定义图片视图(Custom Image View)

现在，咱们的地标名称、位置都已经安排好了。下一步，我们打算加一张地标的图片。

我们将创建一个新的自定义视图，而不是直接在现在的文件里继续写更多的代码了。这个自定义视图将包含有遮罩、边框和投影。

<video data-v-f6e12e74="" autoplay="autoplay" muted="muted" playsinline=""><!----><source src="https://docs-assets.developer.apple.com/published/dd83089688f823328fbd9cb9a26238c5/110/custom-image-view.mp4"></video>

首先，我们要先添加图片到项目的资产目录( asset catalog)。

**Step 1.** 把 `turtlerock.png` （在Apple给的项目文件里的 Resources 文件夹里有）把它拖到 资产目录 编辑器里，Xcode 会为这个新图片创建一个图片集。

![资产目录的截图，图片放在1倍槽中。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2bi3sx88j30tg0xc76h.jpg)

【译注】那个图片就是下面这张👇

![turtlerock](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2blu752tj306y06y0us.jpg)

接下来，我们要创建一个新的 SwiftUI View 来写我们的自定义图片视图。

**Step 2.** 选择 **File > New > File**，打开模版选择器，在 **User Interface** 中，选择 **SwiftUI View**，然后点 **Next**，把文件名取成 `CircleImage.swift`，然后点 **Create**。

![新文件类型选择器的截图，高亮显示SwiftUI View和下一步按钮。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2gd8yh7lj30tg0q1424.jpg)

现在，我们就准备好插入图片，然后修改显示效果来达到我们的预期目标了。

**Step 3.** 用我们刚才准备好的图片来替换新建的文件里的文本视图，用 `Image(_:)` 来显示一张图片。

![使用Image显示图片的代码和预览截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2gj64fgfj30zi0u0am7.jpg)

【译注】在 Playground 里写 `Image("turtlerock")` 要不成，要用 `Image(uiImage: UIImage(named: "turtlerock.jpg")!)`

**Step 4.** 添加一个 `clipShape(Circle())` 调用来把图片裁剪为圆形。

`Circle` 类型是一个形状，你可以把它当遮罩(mask)用，也可以把它作为一个圆形的视图（有圆形的笔触或者圆形填充的）。

![把Image显示图片变成圆形的代码和预览效果截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2hfamef6j317w0psaki.jpg)



**Step 5.** 再创建一个新的灰色笔触的圆，然后把它作为 `overlay` 加到我们之前的 Image 上，这样可以作出一个边框效果。

![代码和预览效果截图，加了灰色的圆形边框](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2hodymblj317u0pqtj5.jpg)



**Step 6.** 接下来，添加一个半径为 10 点的阴影。

![代码和预览效果截图，加了阴影](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2hrhhj7tj317c0q2n8b.jpg)



**Step 7.** 把边框颜色改成白色。

![代码和预览效果截图，把边框颜色改成了白色](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2hta2gs3j31960p8wq2.jpg)

现在，我们的自定义图片视图就完成了。

完成这一节后，我们的主要代码看上去是这样的：

```swift
struct CircleImage: View {
    public var body: some View {
        // Playground 里换成：Image(uiImage: UIImage(named: "turtlerock.jpg")!)
        Image("turtlerock")
            .clipShape(Circle())
            .overlay(
                Circle().stroke(Color.white, lineWidth: 4))
            .shadow(radius: 10)
}
```

#### § 5 同时使用 SwiftUI 和 UIKit

现在，咱打算做一个地图视图了。我们可以用一个来自 `MapKit` 的 `MKMapView` 类来提供一个地图视图。

要在 SwiftUI 中使用 `UIView` 的子类，我们要把它用一个实现了 `UIViewRepresentable` 协议的 SwiftUI 视图包裹起来。SwiftUI 也对 WatchKit 和 AppKit 的视图提供了相似的协议。



![MapKit视图截图，约书亚树国家公园上有一个标记。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2i5762mvj30oy0bcwha.jpg)

首先，我们要自定义一个视图来包装 MKMapView。

**Step 1.** 选择 **File > New > File**，打开模版选择器，在 **User Interface** 中，选择 **SwiftUI View**，然后点 **Next**，把文件名取成 `MapView.swift`，然后点 **Create**。

![新建文件类型选择器的截图，高亮显示SwiftUI View和下一步按钮。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2itovm2cj30tg0q1427.jpg)

**Step 2.** 添加一个 import 语句来导入 `MapKit`，然后让 `MapView` 遵循 `UIViewRepresentable` 协议：

```swift
// MapView.swift

import SwiftUI
import MapKit

struct MapView: UIViewRepresentable {
    var body: some View {
        Text("Hello World")
    }
}

struct MapView_Previews: PreviewProvider {
    static var previews: some View {
        MapView()
    }
}
```

别介意 Xcode 提示的错误，我们将在接下来几步里解决这些问题。

接下来我们要完成 `UIViewRepresentable` 要求两个实现：

- `makeUIView(context:)`：这个方法用来创建 MKMapView；
- `updateUIView(_:context:)`：这个方法用来设定视图，并对任意改变作出响应。

**Step 3.** 把新建的视图里的 body 属性的代码替换成定义一个 `makeUIView(context:)` 方法，这个方法用来创建并返回一个新的 `KMapView`。

```swift
struct MapView: UIViewRepresentable {
    func makeUIView(context: Context) -> MKMapView {
        MKMapView(frame: .zero)
    }
}
```

**Step 4.** 在 MapView 里添加一个 `updateUIView(_:context:)` 方法来设置我们的地图把要显示的位置放到中心位置。

```swift
func updateUIView(_ uiView: MKMapView, context: Context) {
    let coordinate = CLLocationCoordinate2D(
        latitude: 34.011286, longitude: -116.166868)
    let span = MKCoordinateSpan(latitudeDelta: 2.0, longitudeDelta: 2.0)
    let region = MKCoordinateRegion(center: coordinate, span: span)
    uiView.setRegion(region, animated: true)
}
```

由于在静态模式（static mode）下预览只会渲染 SwiftUI 视图，而我们的地图是个 UIView 的子类，所以我们需要把预览调到 live 模式（live preview）才能看见地图。

**Step 5.** 点击 **Live Preview** 按钮来把预览调至 live 模式。然后，你可能还需要点击 **Try Again** 或者 **Resume** 按钮才能显示出预期的效果。

![Xcode画布的截图，选择了Live Preview按钮。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2kfi6wy2j30tg0xc48n.jpg)

现在，我们将看见一张显示着 Joshua Tree National Park 的地图——这就是我们的地标 Turtle Rock 的家。

这一节里，我们完成的主要代码看上去是这样的：

```swift
struct MapView: UIViewRepresentable {
    func makeUIView(context: Context) -> MKMapView {
        MKMapView(frame: .zero)
    }
    
    func updateUIView(_ uiView: MKMapView, context: Context) {
        let coordinate = CLLocationCoordinate2D(
            latitude: 34.011286, longitude: -116.166868)
        let span = MKCoordinateSpan(latitudeDelta: 2.0, longitudeDelta: 2.0)
        let region = MKCoordinateRegion(center: coordinate, span: span)
        uiView.setRegion(region, animated: true)
    }
}
```

#### § 6 组成 Detail 视图

现在，我们已经构建完了我们需要的一切——地标的名字和位置、一张圆形的图片以及其所在位置的地图。

现在，我们要把这些我们写好的自定义视图组合在一起，来完成一个地标的 Detail 视图的最终设计了！我们要用到的还是已经开始熟悉的那些工具。

![合成视图的图像，上面是地图视图，下面是公园名称，中间是圆形图像视图。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2kw18daoj30lq0lkqbl.jpg)



**Step 1.** 在项目导航（Project navigator）中，选择打开 `ContentView.swift` 文件。

![ContentView.swift文件内的代码和预览截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2kzfv52qj31020u0792.jpg)

**Step 2.** 把之前那个包含三个 Text 的 VStack 用另一个新的 VStack 包裹起来。

![代码和预览效果的截图，在之前的 VStack外面套了一个新的VStack，预览效果不变](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2l1en0s5j312c0u0afy.jpg)

**Step 3.** 把我们自定义的 MapView 放到 stack 的顶部，并用 `frame(width:height:)` 来调整其大小。

当你只指定了 height（高度）属性时，视图会自动把宽度设置成符合内容的。在这里，MapView 会拓展开充满整个可用空间。

**Step 4.** 点击 **Live Preview** 按钮来查看在组合视图中渲染出来的地图。

在显示  Live Preview 的同时，你也还可以继续编辑视图。

![代码和预览效果的截图，添加了MapView](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2lg3l7hpj30zd0u0q5e.jpg)

**Step 5.** 在 stack 里添加一个 CircleImage。

![代码和预览效果的截图，添加了 CircleImage](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2lh5tko1j30yp0u0tn8.jpg)

**Step 6.** 我们要把图片视图移到地图视图的上层：给它竖直偏移(offset) -130 点，底部内补(padding) -130 点。

这个调整通过把图片向上移，来提供给文本更多空间。

![代码和预览效果的截图，移动了圆形图片](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2lsxro6ej310t0u07ie.jpg)

**Step 7.**  在最外层的 VStack 的底部增加一个 spacer，把我们的那些内容推到屏幕顶部。

![代码和预览效果的截图，增加来一个 spacer，内容全在屏幕顶部来了](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg2lw903stj30za0u016z.jpg)

**Step 8.** 最后一步，为了能让我们的地图拓展到屏幕顶部边缘（说直白点就是伸到刘海里😂），给地图视图加一个 `edgesIgnoringSafeArea(.top)` 修饰。



## 绘图和动画



## App 设计和布局



## 框架整合



