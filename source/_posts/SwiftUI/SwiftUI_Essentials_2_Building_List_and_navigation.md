---
categories:
- Learn to Make Apps with SwiftUI
date: 2020-06-24 08:34:24
tags:
- SwiftUI
title: SwiftUI基础——构建列表和导航
---

# Swift UI 基础

今天是 WWDC20 的第二天了，所以继续来学习 Apple 的 app 开发。😜

> 翻译自 SwiftUI 的官方教程：[Learn to Make Apps with SwiftUI](https://developer.apple.com/tutorials/swiftui/tutorials)
>
> 这篇文章是 Apple 给的 SwiftUI 官方教程的一部分，我自己阅读学习的时候顺便翻译的。

## 构建列表和导航

> 原文链接：https://developer.apple.com/tutorials/swiftui/building-lists-and-navigation

在我们已经完成了基本的地标细节视图后，现在，我们需要提供给用户一种方式，来查看完整的地标列表，并可以查看每一个地标的细节。

我们将构建可以展示任意地标信息的视图，还有动态生成一个滚动列表，用户可以点击列表里的项目来查看对应地标的细节信息。为了微调用户界面，我们将使用 Xcode 的画布在不同的设备尺寸下渲染多个预览。

载项目文件，跟着下面的步骤开始构建工程吧：

> 预计时间：35分钟
>
> 项目文件：https://docs-assets.developer.apple.com/published/f021500afcdf6c3930549f1ffeb65e7e/110/BuildingListsAndNavigation.zip 

### § 1 认识样本数据(Sample Data)

> 原文链接：https://developer.apple.com/tutorials/swiftui/building-lists-and-navigation#Get-to-Know-the-Sample-Data

在之前的教程中，我们把信息用硬编码(hard-coded)写死到了我们的自定义视图中。现在，我们将要学习如何让视图显示我们传进去的指定信息。

首先，下载打开起步项目文件，然后自己熟悉一下样本数据吧。

![一张图显示了如何从JSON数据中提取各种地标的细节](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg33qnycraj30pa0dkq3j.jpg)

**Step 1.** 在项目导航（Project navigator）中选择 **Models** > `Landmark.swift`。

`Landmark.swift` declares a `Landmark`structure that stores all of the landmark information the app needs to display, and imports an array of landmark data from `landmarkData.json`.

`Landmark.swift` 声明了一个 `Landmark` 结构体，用来储存我们的 app 需要显示的所有地标信息（这些信息是从 `landmarkData.json` 读取出来的）。

```swift
// Landmark.swift

import SwiftUI
import CoreLocation

struct Landmark: Hashable, Codable {
    var id: Int
    var name: String
    fileprivate var imageName: String
    fileprivate var coordinates: Coordinates
    var state: String
    var park: String
    var category: Category

    var locationCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(
            latitude: coordinates.latitude,
            longitude: coordinates.longitude)
    }

    enum Category: String, CaseIterable, Codable, Hashable {
        case featured = "Featured"
        case lakes = "Lakes"
        case rivers = "Rivers"
    }
}

extension Landmark {
    var image: Image {
        ImageStore.shared.image(name: imageName)
    }
}

struct Coordinates: Hashable, Codable {
    var latitude: Double
    var longitude: Double
}
```

**Step 2.** 在项目导航中，选择 **Resources** > `landmarkData.json`。

```json
[
    {
        "name": "Turtle Rock",
        "category": "Featured",
        "city": "Twentynine Palms",
        "state": "California",
        "id": 1001,
        "park": "Joshua Tree National Park",
        "coordinates": {
            "longitude": -116.166868,
            "latitude": 34.011286
        },
        "imageName": "turtlerock"
    },
    {
        "name": "Silver Salmon Creek",
        "category": "Lakes",
        "city": "Port Alsworth",
        "state": "Alaska",
        "id": 1002,
        "park": "Lake Clark National Park and Preserve",
        "coordinates": {
            "longitude": -152.665167,
            "latitude": 59.980167
        },
        "imageName": "silversalmoncreek"
    },
    ...
]
```

在接下来的步骤中，我们都将使用这个样本数据文件。

**Step 3.** 注意，在 [创建并组合视图](https://clownote.github.io/2020/06/23/SwiftUI/SwiftUI_Essentials_Creating_and_Combining_Views/) 里我们写的 ContentView 现在重命名成了 `LandmarkDetail`。

在接下来的教程中，我们还有构建更多的其他视图。

```swift
// LandmarkDetail.swift

import SwiftUI

struct LandmarkDetail: View {
    var body: some View {
        VStack {
            MapView()
                .edgesIgnoringSafeArea(.top)
                .frame(height: 300)

            CircleImage()
                .offset(y: -130)
                .padding(.bottom, -130)

            VStack(alignment: .leading) {
                Text("Turtle Rock")
                    .font(.title)

                HStack(alignment: .top) {
                    Text("Joshua Tree National Park")
                        .font(.subheadline)
                    Spacer()
                    Text("California")
                        .font(.subheadline)
                }
            }
            .padding()

            Spacer()
        }
    }
}

struct LandmarkDetail_Previews: PreviewProvider {
    static var previews: some View {
        LandmarkDetail()
    }
}
```

预览效果是这样的：

![Xcode预览的截图，地图视图对准了显示器的顶部](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg35gcegikj30vj0u013u.jpg)

### § 2 创建行视图(Row View)

在本教程中，我们将构建的第一个视图是一个用于显示每个地标详细信息的行。这个行视图将它所显示的地标的信息存储在一个属性中，因此一个这种视图是可以显示任何地标的。之后，我们将把多个这种行组合成一个地标列表。

![一张图描述了你将为本教程构建的行是如何构建的。该行由左边的图像、从JSON文件中提取数据以了解地标细节的文本视图和右边的间隔符组成。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg360dch7nj30md0bo74z.jpg)



**Step 1.** 创建一个新的 SwiftUI View，文件命名为 `LandmarkRow.swift`。

![Xcode的截图，显示文件创建对话框。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg361wqte4j30tg0xcwld.jpg)

**Step 2.** 如果预览没有显示，则通过  **Editor > Canvas** 打开画布，然后点 **Resume**。

![一张图片显示了Xcode中欢迎来到SwiftUI屏幕](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg37cr5otnj30tg0xcmxq.jpg)

**Step 3.** 给 `LandmarkRow` 添加一个 landmark 储存属性。

```swift
// LandmarkRow.swift

import SwiftUI

struct LandmarkRow: View {
    var landmark: Landmark

    var body: some View {
        Text("Hello World")
    }
}

struct LandmarkRow_Previews: PreviewProvider {
    static var previews: some View {
        LandmarkRow()
    }
}
```

当你添加 landmark 属性时，预览会停止工作，因为LandmarkRow类型在初始化时需要一个 Landmark 实例。

为了修复预览，我们要修改一下预览提供器（PreviewProvider）。

**Step 4.** 在 LandmarkRow_Previews 的 previews 静态属性中，给 LandmarkRow 的初始化器中添加 landmark 参数，指定 landmarkData 数组的第一个元素。

现在，预览就可以工作了，显示出了文本 "Hello World"。

![代码和预览截图，预览显示出了Hello World](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg37q6jzywj31940n6whf.jpg)

修复了这个问题之后，就可以开始构建行的视图了。

**Step 5.** 把现有的文本视图嵌入到一个 HStack 里。

![代码和预览截图，代码把现有的文本视图嵌入到一个 HStack 里，预览不变](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg37sj9i5aj318m0podiy.jpg)

**Step 6.** 把文本视图的内容改成 `landmark` 属性的 `name`。

![代码和预览截图，文本视图的内容改成了landmark属性的name，预览显示文本Turtle Rock](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg37zyjvbzj31920oy0vt.jpg)

**Step 7.** 通过在文本视图前添加图像，在文本视图后添加间隔符来完成行。

![代码和预览截图，在文本视图前添加图像，在文本视图后添加间隔](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg38568glgj319g0tstd3.jpg)

---

这一节里我们完成的主要代码是`LandmarkRow.swift`：

```swift
import SwiftUI

struct LandmarkRow: View {
    var landmark: Landmark

    var body: some View {
        HStack {
            landmark.image
                .resizable()
                .frame(width: 50, height: 50)
            Text(landmark.name)
            Spacer()
        }
    }
}

struct LandmarkRow_Previews: PreviewProvider {
    static var previews: some View {
        LandmarkRow(landmark: landmarkData[0])
    }
}
```

也可以在 Playground 里完成这个，但稍微有点麻烦。

新建一个 Playground，打开左侧的 Navigater，展开可以看到 Resources 文件夹，把 Apple 给的那个项目文件中的 Resources 里面的东西（一个 json文件，还有一堆图片文件）

### § 3 自定义行预览

Xcode 的画布可以自动识别并显示当前编辑器中实现了 PreviewProvider 协议的任何类型。预览提供器（preview provider）会返回一个或多个视图，并带有配置大小和设备的选项。

你可以自定义从预览提供器返回的内容，以准确地呈现对工作最有帮助的预览。

![两台iPhone设备并排的图片。左边的iPhone在靠近显示屏中间的四行周围有一个高亮。左边的四行高亮处有一个箭头，这些箭头在右边iPhone的列表视图中得到了复制。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3h6nrl7oj30nt0kgmyz.jpg)



**Step 1.** 在LandmarkRow_Previews中，把 landmark 参数改为 landmarkData 数组中的第二个元素。

修改完代码，预览会立即改变，显示第二个样本地标，而不再是第一个。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3hqssaaaj317f0u0gpw.jpg)

**Step 2.** 使用 `previewLayout(_:)` 修饰器来把预览设置成近似一个行的尺寸大小。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3idkm3npj318o0u0q7l.jpg)

我们可以使用一个 Group 来从一个 preview provider 返回多个预览。

**Step 3.** 将现在 previews 返回的 LandmarkRow 包裹在一个 Group 中，并将第一行再次添加回来。

Group 是对视图内容进行分组的容器。Xcode 在画布中以单独的预览来呈现 Group 的子视图。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3nomqyhzj313a0u00z2.jpg)

**Step 4.** 为了简化代码，将 ` previewLayout(_:)` 的调用移到组的子声明的外面。

视图的孩子 (Children) 会继承视图的上下文设置，例如预览配置。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3o6fyo1vj313m0u0ag3.jpg)

我们在预览提供器(PreviewProvider)中写的代码只会改变画布(canvas)中显示的预览内容，不会影响视图本身。

### § 4 创建地标列表（the List of Landmarks）

使用 SwiftUI 的 `List` 类型，可以显示一个平台特定(platform-specific)的视图列表。列表中的元素可以是静态的，比如到目前为止你创建的那种 stack 的子视图，也可以是动态生成的。我们甚至可以在 List 里混合静态和动态生成的视图。

![两行地标的截图，左边有图片，地标名称，每排右侧边缘有导航箭头。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3ogifginj30m905kdgp.jpg)

**Step 1.** 创建一个新的 SwiftUI View，命名为 `LandmarkList.swift`。

![Xcode的截图，显示新SwiftUI视图正被添加到项目中。](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3oovkeetj30tg0xcdmp.jpg)

**Step 2.** 用一个 List 替换默认的 Text 视图，并提供 LandmarkRow 实例，将前两个地标作为列表的子节点。

![代码和预览的截图](https://tva1.sinaimg.cn/large/007S8ZIlgy1gg3or740ejj318w0nkgpr.jpg)

预览显示两个 LandmarkRow 以适合 iOS 的列表样式呈现出来了。

