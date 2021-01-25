---
date: 2019-12-10 12:59:21
tags: School
title: 利用 C# 语言实现跨平台小闹钟
---


# 利用 C# 语言实现跨平台小闹钟

## 前言

学校的课程要求做一个 C# 小闹钟程序设计，具体要求如下：

1. 做一个小闹钟窗体应用程序。
2. 具备实时显示数字时钟的功能，方便使用者获取当前的时间。
3. 具备实时绘制表盘时钟的功能，根据当前时间再来绘制秒针、分针和时针。
4. 具备整点报时的功能，当处于整点时，系统进行报时。
5. 具备定点报时的功能，根据使用者的设定，进行报时。
6. 把使用者设置的报时时间，记录在文本文件中，系统在启动时，自动加载该文本文件以便获取定点报时的时间。
7. 系统最小化时，缩小为系统托盘。

这个东西不难，就是最简单的 App 开发嘛，但要求用 C# 做 Windows 窗体就很烦。由于我不使用 Windows 系统，所以拿到题目，首先的想法就是**跨平台**，我希望在 Mac 上完成开发，然后直接打包发布到 Windows 平台。

以前看过好几个跨平台的开源的 UI 实现项目都是 C# 写的，比如 Pathos: Nethack Codex 用的 Invention。但因为我之前甚至从没用过 C#，所以对于它们具体的实现不是很了解。经过一阵 Google，我找到了 Microsoft 自家做的跨平台方案——Xamarin。

emmmm，Xamarin 还分好几个部分，Xamarin.Forms，Xamarin.Mac 什么的。其中，Xamarin.Forms 可以一套 UI 代码生成 Android、iOS、UWP(支持不完整，还是预览版)。这个框架下 Android、iOS 可以在 Mac 上用 Visual Studio for Mac 来开发并且生成，UWP 只能在 Windows 下生成。

这个东西感觉还不错，看文档里生成出来的 UI 效果挺好看的，代码也比较简单（相较于原生 Android 开发），所以我决定用这个 Xamarin.Forms 先在 Mac 下完成这个小闹钟的开发，然后借一台 Windows 电脑来生成 UWP。

决定了框架，然后就是 C# 基础语法和 Xamarin.Forms 的学习了。这两个东西微软都有详细的、针对各种不同技术水平的开发者的入门教程，顺着看一遍，把例子写一下也就足够完成这次的小闹钟任务了。

接下来就进入跨平台小闹钟开发的过程了。

## 设计

我们首先思考我们期望的 App 使用场景：用户点击打开 App，屏幕上显示出一个圆盘时钟，然后，可以从导航条（iOS 的习惯是底部，Android 和 UWP 为顶部）切换到一个现实这闹钟条目到界面，用户可以在这里点开一条闹钟条目进行编辑，或着添加新的闹钟条目。

iOS 自带的 “时钟” App 给了我们很好的参考（由于它没有圆盘时钟功能，我截了一张“就寝”界面替代😓）：

![IMG_1573](https://tva1.sinaimg.cn/large/006tNbRwly1g9qnn9cnd8j31d50u0qft.jpg)

在我们的设计中，小闹钟 App 可以分为这样几个页面：

- 🕤时钟页：显示一个圆盘时钟，展示当前时间；
- ⏰闹钟页：显示当前设定的所有闹钟条目，可以点开编辑、新建闹钟条目；
- 🧾详情页：新建、编辑一条闹钟的时间、注释的页面，并有保存、删除的功能。

具体到 Xamarin.Forms 中，这些 Pages 如下图所示：

![MyClockPagesDiagram](https://tva1.sinaimg.cn/large/006tNbRwly1g9qes7ga8nj30ea0ehmxj.jpg)

然后，我们还需要设计另外一个重要的部分，一条“闹钟”的表示和储存。

可以考虑用一个 `AlarmItem` 类来代表一条闹钟，这个类要具有 唯一ID、时间、是否打开、注释 这几个属性。

在 Xamarin 中，我们可以很方便地引入 SQLite 储存这个对象，只需要写一个 `Database` 类，简单封装一下 CRUD，方便后续使用。

接下来就要开始代码实现了，先贴出最后成品截图，iOS上的效果：

![IMG_1576](https://tva1.sinaimg.cn/large/006tNbRwly1g9qtdimzaxj31f20u0wop.jpg)

UWP 的效果：

![IMG_1600](https://tva1.sinaimg.cn/large/006tNbRwly1g9vdl50y0qj312o0u0gqs.jpg)

## 实现

整个 App 的基础大概有了，现在考虑一些实现的细节。

（在这里我只列出关键的或者任何我认为有意思的代码片段，完整代码见 [GitHub](https://github.com/cdfmlr/MyClock)）

### 圆盘时钟的实现

![屏幕快照 2019-12-09 13.36.51](https://tva1.sinaimg.cn/large/006tNbRwly1g9qey1safbj305b05bmx7.jpg)

绘制一个如上图所示的圆盘时钟，需要实时的矢量图绘制。Xamarin.Forms 不具有内置的矢量图形系统，但有一个 BoxView 可帮助进行补偿。[BoxView](https://docs.microsoft.com/zh-cn/dotnet/api/xamarin.forms.boxview)  呈现指定的宽度、 高度和颜色的一个简单的矩形。参照微软的文档，我们可以按下面的思路实现一个时钟：

#### 表盘

对于表盘，通过简单的数学计算，就可以得到从12点开始的表盘上 60 个均匀分布的刻度点的位置坐标。在一个可以指定位置的 AbsoluteLayout 中。

```c#
// Create the tick marks
for (int i = 0; i < tickMarks.Length; i++)
{
	tickMarks[i] = new BoxView { Color = Color.Black };
	absoluteLayout.Children.Add(tickMarks[i]);
}
```

上面我们生成了 60 个大小相同的正方形 BoxView，现将模5的点稍微加大，然后把它们放置到指定的位置，针对不同位置的正方形做一个使其正对中心的旋转，表盘就完成了。

```c#
// Size and position a tickMark
double size = radius / (index % 5 == 0 ? 15 : 30);
double radians = index * 2 * Math.PI / tickMarks.Length;
double x = center.X + radius * Math.Sin(radians) - size / 2;
double y = center.Y - radius * Math.Cos(radians) - size / 2;
AbsoluteLayout.SetLayoutBounds(tickMarks[index], new Rectangle(x, y, size, size));
tickMarks[index].Rotation = 180 * radians / Math.PI;
```

#### 指针

接下来是指针，先在之前的 AbsoluteLayout 中实例化三个代表时分秒针的 BoxView：

```xml
<AbsoluteLayout x:Name="absoluteLayout" SizeChanged="OnAbsoluteLayoutSizeChanged">
    <BoxView x:Name="hourHand" Color="Black" />
    <BoxView x:Name="minuteHand" Color="Black" />
    <BoxView x:Name="secondHand" Color="Black" />
</AbsoluteLayout>
```

写一个 `HandParams` 来指定三个时针的形状：

```c#
struct HandParams
{
    public HandParams(double width, double height, double offset) : this()
    {
        Width = width;
        Height = height;
        Offset = offset;
    }

    public double Width { private set; get; }
    public double Height { private set; get; }
    public double Offset { private set; get; }	// 旋转中心
}

static readonly HandParams secondParams = new HandParams(0.02, 1.1, 0.85);
static readonly HandParams minuteParams = new HandParams(0.05, 0.8, 0.9);
static readonly HandParams hourParams = new HandParams(0.125, 0.65, 0.9);
```

然后，写一个 `LayoutHand` 来把指针放到合适的地方：

```c#
void LayoutHand(BoxView boxView, HandParams handParams, Point center, double radius)
{
    double width = handParams.Width * radius;
    double height = handParams.Height * radius;
    double offset = handParams.Offset;

    AbsoluteLayout.SetLayoutBounds(boxView,
                                   new Rectangle(center.X - 0.5 * width,
                                                 center.Y - offset * height,
                                                 width, height));
    boxView.AnchorY = handParams.Offset;
}

LayoutHand(secondHand, secondParams, center, radius);
LayoutHand(minuteHand, minuteParams, center, radius);
LayoutHand(hourHand, hourParams, center, radius);
```

在时间流动时，旋转指针，为了营造一种真实的感觉，我们可以用一个动画效果让秒钟的移动有真实的摆动感，但这个动画需要我们 Timer Tick 的频率高一点：

```C#
public ClockPage()
{
    InitializeComponent();

    ...

    Device.StartTimer(TimeSpan.FromSeconds(1.0 / 60), OnTimerTick);
}

bool OnTimerTick()
{
    DateTime dateTime = DateTime.Now;
    hourHand.Rotation = 30 * (dateTime.Hour % 12) + 0.5 * dateTime.Minute;
    minuteHand.Rotation = 6 * dateTime.Minute + 0.1 * dateTime.Second;

    double t = dateTime.Millisecond / 1000.0;

    if (t < 0.5)
    {
        t = 0.5 * Easing.SpringIn.Ease(t / 0.5);
    }
    else
    {
        t = 0.5 * (1 + Easing.SpringOut.Ease((t - 0.5) / 0.5));
    }

    secondHand.Rotation = 6 * (dateTime.Second + t);
}
```

至此，一个圆盘时钟就完成了。

### 闹钟功能实现

#### 闹钟、数据库模块

我们将使用 `SQLite.NET` 将数据库操作合并到应用程序。

首先要做的是使用 Visual Studio 中的 NuGet 包管理器将 NuGet 包添加到项目。这里我们需要添加的包叫做 `sqlite-net-pcl` （详细操作参考官方文档：[将数据存储在本地 SQLite.NET 数据库中](https://docs.microsoft.com/zh-cn/xamarin/get-started/quickstarts/database)），添加完成后我们就可以将数据存储在本地 SQLite.NET 数据库中了。

接下来我们实现设计中提到的 `AlamItem` 类来表示一条闹钟：

```c#
using System;
using SQLite;

namespace MyClock
{
    public class AlarmItem
    {
        [PrimaryKey, AutoIncrement]
        public int ID { get; set; }
        public TimeSpan Time { get; set; }
        public bool Work { get; set; }
        public string Note { get; set; }

        public override string ToString()
        {
            return Time.ToString();
        }
    }
}

```

这里使用了 `PrimaryKey` 和 `AutoIncrement` 特性标记 `ID` 属性，以确保 SQLite.NET 数据库中的每个 `AlarmItem` 实例都具有 SQLite.NET 提供的唯一 id。

然后，创建一个 `Database` 类，包含用于创建数据库、从中读取数据、向其中写入数据以及从中删除数据的代码：

```c#
using System.Collections.Generic;
using System.Threading.Tasks;

using SQLite;

namespace MyClock
{
    public class Database
    {
        readonly SQLiteAsyncConnection _database;

        public Database(string dbPath)
        {
            _database = new SQLiteAsyncConnection(dbPath);
            _database.CreateTableAsync<AlarmItem>().Wait();
        }

        public Task<List<AlarmItem>> GetAllAlarmItemsAsync()
        {
            return _database.Table<AlarmItem>().ToListAsync();
        }

        public Task<int> SaveAlarmItemAsync(AlarmItem alarmItem)
        {
            if (alarmItem.ID != 0)
            {
                return _database.UpdateAsync(alarmItem);
            }
            else
            {
                return _database.InsertAsync(alarmItem);
            }
        }

        public Task<int> DeleteAlarmItemAsync(AlarmItem alarmItem)
        {
            return _database.DeleteAsync(alarmItem);
        }
    }
}
```

我们使用的全是将数据库操作移动到后台线程的异步 SQLite.NET API。 此外，`Database`构造函数将数据库文件的路径作为参数。

#### 闹钟相关的页面

接下来我们考虑先把和闹钟的CRUD相关的 `AlarmPage` 和 `AlarmEditPage` 页面实现。

首先是 `AlarmPage`，这个界面将罗列所有的已有闹钟条目，并且可以添加新的条目：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyClock.AlarmPage"
             Title="闹钟">
    <ContentPage.ToolbarItems>
        <ToolbarItem Text="+"
                     IconImageSource="add.png"
                     Clicked="OnAlarmItemAddClicked" />
    </ContentPage.ToolbarItems>
    
    <StackLayout Margin="20">
        <ListView x:Name="alarmListView"
              ItemSelected="OnAlarmItemSelected">
            <ListView.ItemTemplate>
                <DataTemplate>
                    <TextCell Text="{Binding TimeString}"
                          Detail="{Binding Note}"/>
                </DataTemplate>
            </ListView.ItemTemplate>
        </ListView>
        <Button Text="添加"
                Clicked="OnAlarmItemAddClicked" />
    </StackLayout>

</ContentPage>
```

这里我在标题栏里写了一个添加新条目的 “`+`” 按钮，但由于调试中发现，它虽然在 Android、iOS 中都能很好的呈现，但在 UWP 里不可见（虽然把鼠标移到那里稍微移动屏幕后可以看到也可以点击到它），用户体验很差，所以就在 ListView 下面加了一个很显眼、也几乎不可能出意外的 “`添加`” Button。

当用户点击 ListView 里的闹钟条目 或者 添加新条目 时，将转到 `AlarmEditPage` 完成闹钟条目的查看、编辑、保存或删除：

```C#
async void OnAlarmItemAddClicked(object sender, EventArgs e)
{
    await Navigation.PushAsync(new AlarmEditPage
	{
		BindingContext = new AlarmItem()
	});
}

async void OnAlarmItemSelected(object sender, SelectedItemChangedEventArgs e)
{
    if (e.SelectedItem != null)
    {
        await Navigation.PushAsync(new AlarmEditPage
		{
			BindingContext = e.SelectedItem as AlarmItem
		});
    }
}
```

`AlarmEditPage` 的界面设计如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyClock.AlarmEditPage"
             Title="设置闹钟">
    <StackLayout Margin="20, 35, 20, 20">
        <Label Text="时间:"/>
        <TimePicker Time="{Binding Time}"
                    Format="T" />
        <StackLayout Orientation="Vertical">
            <Label Text="启用:" />
            <Switch HorizontalOptions="StartAndExpand"
                    IsToggled="{Binding Work}" />
        </StackLayout>
        <Label Text="注释:"/>
        <Editor Placeholder="输入注释"
                Text="{Binding Note}"
                MaxLength="300"
                HeightRequest="100" />
        <Grid Margin="10">
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="*" />
                <ColumnDefinition Width="*" />
            </Grid.ColumnDefinitions>
            <Button Text="保存"
                    Clicked="OnSaveButtonClicked" />
            <Button Grid.Column="1"
                    Text="删除"
                    Clicked="OnDeleteButtonClicked" />
        </Grid>
    </StackLayout>
</ContentPage>
```

#### 闹钟条目的CRUD

因为我们将在整个程序的不同部分通用我们封装的 `Database` 这个数据库，所以在 `App.xaml.cs` 中将其实例化：

```c#
public partial class App : Application
{

    static Database database;

    public static Database Database
    {
        get
        {
            if (database == null)
            {
                database = new Database(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "alarm.db3"));
            }
            return database;
        }
    }

    ...
}
```

然后就可以在各处调用了，接下来我们将数据与界面联系起来。

在 `AlarmPage` 的 `OnAppearing` 中，我们将写这样的一行代码：

```c#
alarmListView.ItemsSource = await App.Database.GetAllAlarmItemsAsync();
```

这行代码将会把数据库中储存的所有闹钟条目读取出来，加载到界面上的 ListView 里。

然后，在 `AlarmEditPage` 中完成 保存、删除 两个按钮的点击事件处理：

```c#
async void OnSaveButtonClicked(object sender, EventArgs e)
{
    var alarmItem = (AlarmItem)BindingContext;
    await App.Database.SaveAlarmItemAsync(alarmItem);
    await Navigation.PopAsync();
}

async void OnDeleteButtonClicked(object sender, EventArgs e)
{
    var alarmItem = (AlarmItem)BindingContext;
    await App.Database.DeleteAlarmItemAsync(alarmItem);
    await Navigation.PopAsync();
}
```

在取出页面里显示的条目后，调用数据库中保存/删除它，然后退出到 `AlarmPage`。

#### 闹钟提醒

现在我们可以新建、保存、编辑、删除闹钟条目了，但这些还都是数据上的操作，接下来实现闹钟的提醒功能。

闹钟需要在指定的时间响起以提醒用户，我们可以要为每一个闹钟条目调用系统级的定时事件（模仿系统自带的闹钟功能），这个方法感觉很牛皮，但在代码实现、尤其是跨平台实现上麻烦，我不确定（没有尝试）这样的操作是否可以显著提升程序性能，我们只是做个简单的小闹钟作业，没有必要如此。所以我采用了最简单直观的方法——每隔一段时间检测一次是否有闹钟到时。这样做法最方便的地方是，可以和 ClockPage 里的时钟指针更新事件共用一个 Timer：

```c#
bool OnTimerTick()
{
    DateTime dateTime = DateTime.Now;

    ... // Do ui changes

    if (dateTime.Second % 30 <= 1 && dateTime.Minute != _lastCheck)  // To avoid high cpu occupying
    {
        _lastCheck = dateTime.Minute;

        // 整点报时
        if (onTheHourToggle.IsToggled && dateTime.Minute == 0)
        {
            Notify(dateTime.Hour);
        }

        // 定时的闹钟
        List<AlarmItem> alarms = App.Database.GetAllAlarmItemsAsync().Result;
        foreach (var a in alarms)
        {
            if (a.Work && isOnTime(a.Time, dateTime))
            {
                Notify(a);
                a.Work = false;
                App.Database.SaveAlarmItemAsync(a);
            }
        }
    }
    return true;
}

bool isOnTime(TimeSpan t, DateTime d)
{
    return t.Hours == d.Hour && t.Minutes == d.Minute;
}
```

注意我们设置的 Timer 在一秒内是要 Tick 好多次的，但闹钟到时检测只应该每分钟0秒时做一次（我再加了一次在30秒时的防止意外），所以有了 `dateTime.Second % 30 <= 1 && dateTime.Minute != _lastCheck` 这样的代码

在 `Notify` 方法中完成具体的通知用户的行为，比如弹出一个对话框：

```C#
// For 闹钟
await DisplayAlert(alarmItem.TimeString, alarmItem.Note, "OK");
```

```c#
// For 整点报时
await DisplayAlert("整点报时", "现在时间" + hour + "点整。", "OK");
```

其实，我还实现了闹钟到时播放音乐以及语音整点报时的功能，只要在 `Notify` 方法中加入对应的操作就行了，在此不赘述。但这些关于音频的实现在 iOS 和 Android 里没有任何问题，但我一次都没有成功在 UWP 上弄出来，可能是需要设置一下解决方案的打包方式什么的，但我没有找到 Microsoft 相应的文档介绍，咱也没深入研究😂。

## 总结

至此，整个跨平台小闹钟项目就大概介绍完了，时间关系，我省略了太多的细节，可以到 Github 阅读源码，https://github.com/cdfmlr/MyClock 。

通过这个项目，我们可以大概了解 C# 语言和 利用 Xamarin.Forms 开发跨平台 App 的方法，但需要一定的 Android/iOS/Flutter/UWP 开发基础才能很好的理解这些代码。其实，写完这个东西，虽然简单，基本稍微设计一下就照着文档写就好了，五六百行代码，几个小时搞定，但我还是很有收获的。C# 的好多地方感觉真的比 Java 写着方便（最显著的是 getter 和 setter），然而命名习惯什么的不太习惯，至于效率咱没详细研究也没有结论。Xamarin 也很好用，写起来代码简单易懂、开发速度比较快，比原生 Android 开发方便很多，跨平台的 UI 效果也确实不错（除了在微软自家的 UWP 下有小 Bugs😂） 。

再说一下不足。第一，我没有下功夫做 UI 设计，所以比较丑；第二，如前面多次提到的，这个实现在 UWP 平台下的效果不佳；最后，其实这个实现并没有完成题目要求的“最小化到系统托盘”（Xamarin 没有提供这种操作，这个东西显然跨不了平台，只能在 Windows 里实现）、“保存为文本文件”（我们知道，SQLite 算是二进制储存，谈不上“文本文件”）等。

## 另一种实现

基于前面所说的诸多不足，我又借了一台 Windows PC，参考马老师多年前的文章 [利用C#语言实现小闹钟](https://blog.csdn.net/lsgo_myp/article/details/53148238)，写了 [Alarm-WindowsForms](https://github.com/cdfmlr/Alarm-WindowsForms) 项目，一个更符合题目要求但更加粗制滥造的 WindowsForms 实现。

WindowsForms 毕竟是上一个年代的产物了，它设计出来的东西也还是老的 Windows 样式，跟微软现在的 Fluent Design 一点边都不沾，除了历史遗留下来那些部分微软现在自家软件的开发也不用这个了，这东西在 VS 2019 里的设计界面里显示的居然都是个 Windows vista/7 样子的窗体😂。

我没有好好研究 C# 写 WindowsForms 的知识，整个实现基本就是凭 直觉 + 马老师的文章 + 小时候学 VB 残存的记忆。而且由于我不熟悉 Windows 和 Visual Studio 的操作，我甚至连对新建出来的类的命名都没做（吐槽一下 Windows 下 VS 的逻辑，新建一个 Class 或者其他什么东西的时候居然没有输入名称的地方，自动搞出些 Class1、Class2 之类的东西来，然后咱也不敢去重命名它，怕解决方案里注册的信息不对了（VS For Mac 有这个毛病，不知道 Win 上的如何）），所以不打算详细写了，大致的设计如下：

```
WindowsForms 小闹钟程序
    |-- UI
    |    |-- 在程序载入时绘制界面，读取储存的闹钟数据
    |    |-- 在 Timer Tick (每1秒) 时:
    |	 |	 	动态更新圆盘时钟
    |	 |		检测是否整点报时或闹钟提醒
    |    |-- 在用户添加新闹钟时创建 Alarm 实例
    |	 |	 	借助 AlarmDatabase 储存，并写入磁盘
    |    |-- 在用户编辑/删除闹钟时:
    |	 |		借助 AlarmDatabase 修改/删除 Alarm 实例
    |	 |	 	同时也从磁盘文件中修改/删除数据
    |    |-- 在最小化/关闭时处理最小化到系统托盘
    |
    |-- 相关类
         |-- class Alarm: 闹钟类，代表程序运行时的一个闹钟对象
         |-- class AlarmDatabase: 闹钟数据库
         |      	处理将内存中的闹钟数据储存到磁盘以及从磁盘读取已保存的数据
         |-- class TickMarkDrawHelper: 计算表盘刻度坐标的辅助类
```

运行效果：

![1](https://tva1.sinaimg.cn/large/006tNbRwly1g9vdfrwji1j30m40d8dg5.jpg)

写这个实现收获就没有太多了，无非是再熟悉了一下 C# 还有 WindowsForms，但感触倒是颇多。写这个东西的时候，我想起自己一开始学编程的时候接触的 VB，当时用一台磁盘只有 10 GB 的 Windows 98 笔记本，跑年纪比自己还大的 VS6.0 （当时好像还是一个个分开的 VC6.0、VB6.0 什么的），那个时候写的 VB 就和现在这个 WindowsForms in C# 一样，还是那几个熟悉的控件，只是开发语言从 BASIC 变成了 C#。这个时候才猛然回忆起，从我的第一个 Hello World 到今天也有8年了......今后也还会一直继续这段程序人生，虽然写代码从来都不是我最喜欢的事，但是没办法，谁让我乐意呢......