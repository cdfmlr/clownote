---
title: CSharpAlarm
tags:
---

# `C#` 实现小闹钟

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

我们首先思考我们期望的 App 使用场景：用户点击打开 App，屏幕上显示出一个圆盘时钟，然后，可以从导航条（iOS的习惯是底部，Android和UWP为顶部）切换到一个现实这闹钟条目到界面，用户可以在这里点开一条闹钟条目进行编辑，或着添加新的闹钟条目。

iOS 自带的 “时钟” App 给了我们很好的参考（由于它没有圆盘时钟功能，我截了一张“就寝”界面替代😓）：

![IMG_1573](https://tva1.sinaimg.cn/large/006tNbRwly1g9qnn9cnd8j31d50u0qft.jpg)

在这个设计中，我们的小闹钟 App 可以分为这样几个页面：

- 🕤时钟页：显示一个圆盘时钟，展示当前时间；
- ⏰闹钟页：显示当前设定的所有闹钟条目，可以点开编辑、新建闹钟条目；
- 🔎详情页：新建、编辑一条闹钟的时间、注释的页面，并有保存、删除的功能。

具体到 Xamarin.Forms 中，这些 Pages 如下图所示：

![MyClockPagesDiagram](https://tva1.sinaimg.cn/large/006tNbRwly1g9qes7ga8nj30ea0ehmxj.jpg)

然后，我们还需要设计另外一个重要的部分，一条“闹钟”的表示和储存。

可以考虑用一个 `AlarmItem` 类来代表一条闹钟，这个类要具有 唯一ID、时间、是否打开、注释 这几个属性。

在 Xamarin 中，我们可以很方便地引入 SQLite 储存这个对象，只需要写一个 `Database` 类，简单封装一下 CRUD，方便后续使用。

## 实现

整个 App 的基础大概有了，现在考虑一些实现的细节。

（在这里我只列出关键的或者任何我认为有意思的代码片段，完整代码见 [GitHub](https://github.com/cdfmlr/MyClock)）

### 圆盘时钟的实现

![屏幕快照 2019-12-09 13.36.51](https://tva1.sinaimg.cn/large/006tNbRwly1g9qey1safbj305b05bmx7.jpg)

绘制一个如上图所示的圆盘时钟，需要实时的矢量图绘制。Xamarin.Forms 不具有内置的矢量图形系统，但有一个 BoxView 可帮助进行补偿。[BoxView](https://docs.microsoft.com/zh-cn/dotnet/api/xamarin.forms.boxview)  呈现指定的宽度、 高度和颜色的一个简单的矩形。参照微软的文档，我们可以按下面的思路实现一个时钟：

对于表盘，通过简单的数学计算，就可以得到从12点开始的表盘上 60 个均匀分布的刻度点的位置坐标。在一个可以指定位置的 AbsoluteLayout 中。

```c#
// Create the tick marks
for (int i = 0; i < tickMarks.Length; i++)
{
	tickMarks[i] = new BoxView { Color = Color.Black };
	absoluteLayout.Children.Add(tickMarks[i]);
}
```

生成 60 个大小相同的正方形 BoxView，并将模5的点稍微加大，然后把它们放置到指定的位置，针对不同位置的正方形做一个使其正对中心的旋转，表盘就完成了。

```c#
// Size and position a tickMark
double size = radius / (index % 5 == 0 ? 15 : 30);
double radians = index * 2 * Math.PI / tickMarks.Length;
double x = center.X + radius * Math.Sin(radians) - size / 2;
double y = center.Y - radius * Math.Cos(radians) - size / 2;
AbsoluteLayout.SetLayoutBounds(tickMarks[index], new Rectangle(x, y, size, size));
tickMarks[index].Rotation = 180 * radians / Math.PI;
```

接下来是指针，先在之前的 AbsoluteLayout 中实例化三个代表时分秒针的 BoxView：

```xaml
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

在时间流动时，旋转指针，为了营造一种真实的感觉，我们可以用一个动画效果让秒钟的移动有真实的摆动感：

```c#
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

        public List<AlarmItem> GetAlarmItems()
        {
            return _database.Table<AlarmItem>().ToListAsync().Result;
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

除了一个为了 Debug 方便临时加入的阻塞方法 `GetAlarmItems` （完全可以、也应该不使用这个方法），我们使用的全是将数据库操作移动到后台线程的异步 SQLite.NET API。 此外，`Database`构造函数将数据库文件的路径作为参数。

#### 闹钟相关的页面

接下来我们考虑先把和闹钟的CRUD相关的 `AlarmPage` 和 `AlarmEditPage` 页面实现。

首先是 `AlarmPage`，这个界面将罗列所有的已有闹钟条目，并且可以添加新的条目：

```xaml
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
        <Button Text="添加"
                Clicked="OnAlarmItemAddClicked" />
        <ListView x:Name="alarmListView"
              ItemSelected="OnAlarmItemSelected">
            <ListView.ItemTemplate>
                <DataTemplate>
                    <TextCell Text="{Binding TimeString}"
                          Detail="{Binding Note}"/>
                </DataTemplate>
            </ListView.ItemTemplate>
        </ListView>
    </StackLayout>


</ContentPage>
```

这里我在标题栏里写了一个添加新条目的 “`+`” 按钮，但由于调试中发现，它虽然在 Android、iOS 中都能很好的呈现，但在 UWP 里不可见（虽然把鼠标移到那里稍微移动屏幕后可以看到也可以点击到它），用户体验很差，所以就在 ListView 上面加了一个很显眼、也几乎不可能出意外的 “`添加`” Button。

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

```xaml
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

闹钟需要在指定的时间响起以提醒用户，我们可以要为每一个闹钟条目调用系统级的定时事件（模仿系统自带的闹钟功能），这个方法感觉很牛皮，但在代码实现、尤其是跨平台实现上麻烦，我不确定（没有尝试）这样的操作是否可以显著提升程序性能，我们只是做个简单的小闹钟作业，没有必要如此。所以我采用了最简单直观的方法——每隔一段时间检测一次是否有闹钟到时。这样做法最方便的地方是，可以和 ClockPage 里的时钟指针更新事件共用一个 Timer。

