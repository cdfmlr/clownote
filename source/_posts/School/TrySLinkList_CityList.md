---
title: 单链表实践——城市列表
tags: School
---

# 单链表实践——城市列表

（多图警告！我放了一大堆类图、截图）

（多废话警告！我不小心在心情不好的时候写了一大堆废话进来）

（多代码警告！我懒得拣关键的代码了，我把整个工程里和题目相关的代码全扔进来了，编辑的时候 Typora 都有点卡了）

## 题目

![UNADJUSTEDNONRAW_thumb_28c8](https://tva1.sinaimg.cn/large/00831rSTgy1gciubwcduej30la0g1jta.jpg)

![UNADJUSTEDNONRAW_thumb_28c9](https://tva1.sinaimg.cn/large/00831rSTgy1gciubzcavxj30lc0fymyl.jpg)

## （蒟蒻的抱怨）

“这可太难了呀！”

电脑前的蒟蒻猛地坐直了身子，那双颤巍巍的手像是来自罹患帕金森的老人，几经尝试，才一只抓起了乱扔的抹布，狠狠地擦拭着并不脏的屏幕；另一只揉起了自己的眼睛——蒟蒻相信，这不是幻觉就是屏幕出了问题。

窗体应用呐！又是窗体应用！蒟蒻还记得几个月前自己为了完成要求用 C# 写的窗体小闹钟，关掉了 IDEA、退出了 Xcode，翻越了保护着他生命财产安全的高墙，下载了 dotnet core，安装了 Visual Studio for Mac，开始在 Xamarin 的世界里四处碰壁，碰得鼻青脸肿、碰得头破血流。最后虽然如期把东西做了出来，却落得个128GB的 MacBook 硬盘爆满的下场。

如今伤痛未愈、磁盘未清，又惨遭窗体作业当头一棒！蒟蒻除了怀疑自己的眼睛或屏幕还有其他选择嘛？

“我***不写 C# 了！Swing 过气了么？PyTk 不能用么？Web 开发不香么？”，蒟蒻无声地在内心咆哮着，“iOS 虽然还不熟，但尝试写也没问题！再不济，我还会 Android 开发......”

......（👆一个让人意外的强行转折👇）......

三月的昆明依然迷人。昨天下了雨，今天又是艳阳高照，窗外长了7层楼高的行道树随风欢舞——春风时而和煦、忽又暴躁，谁知道是哪来的力气，它似乎从不疲惫，它不断地把未散尽泥土芳香的甘甜空气送进蒟蒻塞满了纸张、书籍和电子产品的房间。调皮的~~风元素~~风儿走时还不忘在蒟蒻的清茶上漾起一个微笑。

“呼——”，一时被这景象吸取了魂魄的蒟蒻这才缓缓回神，看着不知不觉在 Typora 里敲下的这堆文字，一时心里不是滋味。

是啊，最近蒟蒻有些迷茫，不知道该用什么语言、什么框架写作业或是自己的项目了。蒟蒻学的太杂了，每次开发都必须从那么多种技术中挑一个出来用，这时的蒟蒻总是不堪承受抛弃其他语言的痛苦。

“但是没办法，谁让我乐意呢......”

蒟蒻没有办法，只好让上天来决定这一切了。蒟蒻闭上了眼睛，仿佛这样能减轻内心的痛苦。摸起桌上的 D12，蒟蒻的手颤抖地更厉害了，现在是线性马达而不是帕金森了——掷骰子的结果着实让蒟蒻吃了一惊——

是 Xamarin！

不过 Xamarin 就 Xamarin 吧，上天总是对蒟蒻做些奇奇怪怪的事情，蒟蒻已经不相信上帝或任何神灵了。

双眼的焦距在慢慢恢复，手指的颤动像是断了电般骤然止住，在触控板上一划一点，分毫不差，Visual Studio for Mac 在蒟蒻眼前浮现。

----

（这两天心里颇不宁静......一不小心就写了这么多有的没的，浪费了自己的时间，没有任何意义......）

（生活、梦境、学习中的事都让人头疼，还是写代码让人愉快啊！所以写代码去了，一会儿再接着写这篇文章。）

## 成果展示

Ok，代码我写好了，回来接着水博客。现在距离写上面那一段东西过去了两天。中间遇到了一些问题严重拖延了进度，最后还是或优雅或笨拙地解决了，一会儿我们会提到。

话不多说，先看成果！

![IMG_467](https://tva1.sinaimg.cn/large/00831rSTgy1gcmbm5cgscj32b50u0hac.jpg)

（是的，这个城市链表只是这个 App 里的一个功能！我想把这个 App 写成一个比较全的数据结构与算法演示。）

再看看 Android 中的效果（我设计 UI 的时候是按全面屏来的，我的老 Android 手机屏幕小，效果不太好）：

![IMG_455](https://tva1.sinaimg.cn/large/00831rSTgy1gclnjf1t53j32ce0u0n5o.jpg)

这就是比起 Flutter，我有时更喜欢 Xamarin 的地方，我几乎完全没有自定义布局，得到的 App 在 iOS 上就是遵守 Human Interface Guidelines 的原生 iOS 的感觉，在 Android 上就是符合 Material Design 的谷歌原生的感觉！我用 Mac 不能生成 UWP，不然这套代码还可以生成一个在 Windows 10 上实现 Fluent Design 的微软原生的版本！

而且在这里我还有意外的发现，在 iOS 13 上，Xamarin 生成的 App 自动支持 Dark Mode！只要是没指定颜色的控件，都会自动按照 Apple 的设计准则支持暗色模式。但由于我一开始写了几个 `Background="#FAFAFA"` 之类的细节颜色指定，就会在暗色中夹杂一块纯白，很丑，我之后再想办法解决。

接下来，我们讨论如何实现这样的一个 Demo App（我们只着重讨论题目部分的东西，也就是“城市链表”点进去的具体 Demo 部分）。

## 城市列表设计实现

因为我们的目标很明确，就是一个链表放城市，实现增删改查。涉及到的功能也不多，所以设计这个东西不难。我们先从数据结构讲起。

数据结构这一块大体上就是按照上课讲的写。不过按照自己的命名习惯，我修改了一些命名，还有内部的实现也是按照我自己的喜好写的，和老师的稍微有点区别。

### 线性表

在这个 Demo 里，我们用到了顺序表 `SeqList`、单链表 `SLinkList`。这两个东西都实现了线性表接口 `ILinearList`，提供 `Insert`，`Remove`，`IsEmpty`，`Clear`，`Search` 和取下标等操作，具体的类图如下（用软件生成的好像有点错，不管了，以实际代码为准）：

![LinearList](https://tva1.sinaimg.cn/large/00831rSTgy1gcmn3fojbaj311u0qw79h.jpg)

**代码实现**（由于文章空间有限，代码我做过一些调整）：

线性表接口：

```csharp
// DataStructureAlgorithm/LinearList/ILinearList.cs

using System;
namespace DataStructureAlgorithm.LinearList
{
    public interface ILinearList<T> where T : IComparable<T>
    {
        int Length { get; }
        T this[int index] { get; set; }
        void Insert(int index, T data);
        int Search(T data);
        void RemoveAt(int index);
        bool IsEmpty();
        void Clear();
    }
}
```

顺序表：

```csharp
// DataStructureAlgorithm/LinearList/SeqList.cs

using System;
namespace DataStructureAlgorithm.LinearList
{
    public class SeqList<T> : ILinearList<T> where T : IComparable<T>
    {
        private readonly T[] dataSet;

        public int Length { get; private set; }

        public int MaxLength { get; }

        public SeqList(int maxLength)
        {
            if (maxLength < 0)
            {
                throw new ArgumentOutOfRangeException("max Length should >= 0.");
            }
            MaxLength = maxLength;
            dataSet = new T[MaxLength];
            Length = 0;
        }

        public T this[int index]
        {
            get
            {
                if (index < 0 || index > Length - 1)
                {
                    throw new IndexOutOfRangeException();
                }
                return dataSet[index];

            }
            set
            {
                if (index < 0 || index > Length - 1)
                {
                    throw new IndexOutOfRangeException();
                }
                dataSet[index] = value;
            }
        }

        public void Clear()
        {
            Length = 0;
        }

        public void Insert(int index, T data)
        {
            if (index < 0 || index > Length)
            {
                throw new IndexOutOfRangeException();
            }
            if (Length == MaxLength)
            {
                throw new Exception("Failed to Insert: SeqList is already full (Length == MaxLength)");
            }
            for (var i = Length; i > index; i--)
            {
                dataSet[i] = dataSet[i - 1];
            }
            dataSet[index] = data;
            Length++;
        }

        public bool IsEmpty()
        {
            return (Length == 0);
        }

        public void RemoveAt(int index)
        {
            if (index < 0 || index > Length - 1)
            {
                throw new IndexOutOfRangeException();
            }
            for (var i = index; i < Length - 1; i++)
            {
                dataSet[i] = dataSet[i + 1];
            }
            Length--;
        }

        public int Search(T data)
        {
            for (var i = 0; i < Length; i++)
            {
                if (data.CompareTo(dataSet[i]) == 0)
                {
                    return i;
                }
            }
            return -1;
        }
    }
}
```

单链表：

```csharp
// DataStructureAlgorithm/LinearList/SLinkList.cs + SNode.cs

using System;
using System.ComponentModel;

namespace DataStructureAlgorithm.LinearList
{
    public class SNode<T> where T : IComparable<T>
    {

        public T Data { get; set; }
        public SNode<T> Next { get; set; }

        public SNode(T data, SNode<T> next)
        {
            Data = data;
            Next = (next != null ? next : null);
        }

        public SNode(T data) : this(data, null) { }
    }
    
    public class SLinkList<T> : ILinearList<T>, INotifyPropertyChanged where T : IComparable<T>
    {
        public int Length { get; private set; }

        protected string LengthStr = "Length";

        public SNode<T> HeadNode { get; private set; }

        protected string HeadNodeStr = "HeadNode";

        public SLinkList()
        {
            Length = 0;
            HeadNode = null;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected SNode<T> NodeAt(int index)
        {
            if (index < 0 || index > Length - 1)
            {
                throw new IndexOutOfRangeException();
            }

            SNode<T> node = HeadNode;
            for (var i = 0; i < index; i++)
            {
                node = node.Next;
            }
            return node;

        }

        public T this[int index]
        {
            get
            {
                return NodeAt(index).Data;
            }
            set
            {
                NodeAt(index).Data = value;
                OnPropertyChanged(IndexerName);
            }
        }

        protected string IndexerName = "this[]";

        public void Clear()
        {
            HeadNode = null;
            Length = 0;
        }

        public void Insert(int index, T data)
        {
            if (index < 0 || index > Length)
            {
                throw new IndexOutOfRangeException();
            }

            SNode<T> current = new SNode<T>(data);

            if (index == 0)
            {
                current.Next = HeadNode;
                HeadNode = current;
            }
            else
            {
                SNode<T> prev = NodeAt(index - 1);
                current.Next = prev.Next;
                prev.Next = current;
            }

            Length++;
            OnPropertyChanged(LengthStr);
            OnPropertyChanged(IndexerName);

        }

        public void InsertAtHead(T data)
        {
            Insert(0, data);
        }

        public void InsertAtRear(T data)
        {
            Insert(Length, data);
        }

        public bool IsEmpty()
        {
            return (Length == 0);
        }

        public void RemoveAt(int index)
        {
            if (index < 0 || index > Length - 1)
            {
                throw new IndexOutOfRangeException();
            }

            if (index == 0)
            {
                HeadNode = HeadNode.Next;
            }
            else
            {
                SNode<T> prev = NodeAt(index - 1);
                prev.Next = prev.Next.Next;
            }

            Length--;

            OnPropertyChanged(LengthStr);
            OnPropertyChanged(IndexerName);
        }

        public int Search(T data)
        {
            int index = 0;
            for (var current = HeadNode; current != null; current = current.Next)
            {
                if (data.CompareTo(current.Data) == 0)
                {
                    return index;
                }
                index++;
            }
            return -1;
        }

        event PropertyChangedEventHandler INotifyPropertyChanged.PropertyChanged
        {
            add
            {
                PropertyChanged += value;
            }
            remove
            {
                PropertyChanged -= value;
            }
        }

        private void OnPropertyChanged(string propertyName)
        {
            OnPropertyChanged(new PropertyChangedEventArgs(propertyName));
        }

        protected virtual void OnPropertyChanged(PropertyChangedEventArgs e)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, e);
            }
        }
    }
}
```

(里面有些看不懂的代码对吧，比如 `INotifyPropertyChanged` 什么的，这些先不管，之后再讨论。)

写完这些东西，随手做个单元测试，然后就可以开始考虑怎么用它们了。

### 城市、坐标

我们的目标是写城市列表，那当然一个 `City` 类是必不可少的，这只是一个简单的 data 类，但是因为题目有个用距离去搜索的要求，我觉得让 `City` 类或是使用 `City` 类的其他东西去实现两点之间距离的计算不够优雅，所以再抽象出一个 `Point2D` 类来描述一个平面点，同时提供点间距离的计算方法。

![CityAndPoint2D](https://tva1.sinaimg.cn/large/00831rSTgy1gcmn2v20aej30ew0kmwgd.jpg)

**代码实现**：

City:

```csharp
// DataStructureAlgorithm/LinearList/City.cs

using System;
namespace DataStructDemo
{
    public class City : IComparable<City>
    {
        public string Name { get; set; }
        public Point2D Location { get; set; }

        public string LocationStr
        {
            get
            {
                return Location.ToString();
            }
        }

        public City(string name, Point2D location)
        {
            Name = name;
            Location = location;
        }

        public int CompareTo(City other)
        {
            return this.Location.CompareTo(other.Location);
        }

        public override string ToString()
        {
            return $"{Name} {Location}";
        }
    }
}
```

Point2D:

```csharp
// DataStructureAlgorithm/LinearList/Point2D.cs

using System;
namespace DataStructDemo
{
    public class Point2D : IComparable<Point2D>, IEquatable<Point2D>
    {
        public double X { get; }
        public double Y { get; }

        public Point2D(double x, double y)
        {
            X = x;
            Y = y;
        }

        public double DistanceTo(Point2D other)
        {
            double xd = this.X - other.X;
            double yd = this.Y - other.Y;
            return Math.Sqrt(xd * xd + yd * yd);
        }

        public int CompareTo(Point2D other)
        {
            if ((this.X == other.Y) && (this.Y == other.Y))
            {
                return 0;
            }
            else if ((this.X <= other.X) || (this.Y == other.Y))
            {
                return -1;
            }
            return 1;
        }

        public bool Equals(Point2D other)
        {
            return (this.CompareTo(other) == 0);
        }

        public override string ToString()
        {
            return $"({X}, {Y})";
        }
    }
}
```

好了，现在我们表示出了城市。结合刚才的线性表，我们就可以储存满足题目需要的若干城市数据了！但是，我们直接用 `ILinearList<City>` 的话，还有一点不足。问题是什么呢？题目需要我们完成通过城市名和通过中心半径两种方式进行搜索。而我们的 `ILinearList` 只能完成给定完整的 object 的搜索，也就是说只能同时给出城市名、坐标去查找这个城市在不在我们的线性表中。

### 城市列表

要实现题目要求的两种搜索，我们就要往已经实现的基础线性表中加方法。所以我们考虑构建一个新的 `CityList` 去继承已经实现好的 `SLinkList`，同时添加城市链表所特需的两种搜索操作。

我们的 ILinearList 接口里的 Search 是返回一个整数的，但这里我们的搜索结果可不一定是只有一个数，所以搜索的结果还得用一个集合去存，所以我们可以尝试在这里使用我们实现的另一种线性表——`SeqList`。

![CityList](https://tva1.sinaimg.cn/large/00831rSTgy1gcmn4rlejcj30mq0ayq45.jpg)

**代码实现：**(这里我们额外还实现了IEnumerable, INotifyPropertyChanged这两个接口，理由后面再讨论)

```csharp
// Demo/DataStructDemo/CityListPage.xaml.cs

using System;
using System.Collections;
using System.Collections.Generic;
using DataStructureAlgorithm.LinearList;

using System.ComponentModel;

namespace DataStructDemo
{
    public class CityList : SLinkList<City>, IEnumerable, INotifyPropertyChanged
    {
        // SearchByName 通过城市名搜索，返回给定名称的城市索引列表(SeqList<int>)
        public SeqList<int> SearchByName(string name)
        {
            SeqList<int> find = new SeqList<int>(Length);

            int index = 0;
            for (var current = HeadNode; current != null; current = current.Next)
            {
                if (name.CompareTo(current.Data.Name) == 0)
                {
                    find.Insert(0, index);
                }
                index++;
            }
            return find;
        }

        // SearchByLocation 通过给定中心点、搜索半径搜索城市，返回给定范围内的城市索引列表(SeqList<int>)
        public SeqList<int> SearchByLocation(Point2D center, double radius)
        {
            SeqList<int> find = new SeqList<int>(Length);

            int index = 0;
            for (var current = HeadNode; current != null; current = current.Next)
            {
                if (center.DistanceTo(current.Data.Location) <= radius)
                {
                    find.Insert(0, index);
                }
                index++;
            }
            return find;
        }

        public IEnumerator<City> GetEnumerator()
        {
            for (var current = HeadNode; current != null; current = current.Next)
            {
                yield return current.Data;
            }
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return (IEnumerator)GetEnumerator();
        }

        public ArrayList ToArrayList()
        {
            ArrayList arrayList = new ArrayList();
            for (var current = HeadNode; current != null; current = current.Next)
            {
                arrayList.Add(current.Data);
            }
            return arrayList;
        }
    }
}
```

现在，核心的数据表示、存储部分就全部搞定了：我们可以表示了城市，然后把它们储存到链表中，并提供了要求的几种增删改查操作。

接下来就是实行一个 UI 界面去展示这个城市链表，并给用户提供完成各种操作的接口了。

### UI

之前讨论过了，由于一些不知名的原因，我们选择了使用 Xamarin 完成 UI（准确地说是跨平台的 Xamarin.Forms）。

很自然的，展现一个列表，我们当然是使用 `ListView`，而用户要操作数据，就需要有接收用户输入的 `Entry` 以及发起操作的 `Button` 了。

还有如果我们给每个增删改查操作都在界面上分配一个按钮的话手机屏幕肯定放不下（放下了也极端不好看），所以我们可以考虑在运行时用 `DisplayActionSheet` 来让用户选择操作，这样界面就比较清爽了。

至于搜索功能，因为涉及到两种搜索，比较复杂。如果我们在一个页面里又要完成城市显示，又要提供增删改查操作，还有有两种不同的搜索，界面就会变得和老师提供的参考页面一摸一样，很复杂，往你手机那几寸屏幕里塞这么多东西是不优雅、不简洁、不易用的。所以我们把搜索功能单独放到一个 Page 里，在 City List Page 只留下一个进入 Search Page 按钮。完成这些之后，我们就得到了这样的 City List Page，差强人意，但我可以接受了：

![IMG_448](https://tva1.sinaimg.cn/large/00831rSTgy1gclsi51c5vj30u00whq4x.jpg)

**代码实现**：

界面：`Demo/DataStructDemo/CityListPage.xaml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="DataStructDemo.CityListPage"
             Title="City List">
    <ContentPage.ToolbarItems>
        <ToolbarItem Text="Search"
                     Clicked="OnSearchClicked" />
    </ContentPage.ToolbarItems>
    <StackLayout BackgroundColor="#FAFAFA">
        <ListView x:Name="CityListView"
              Margin="20"
              BackgroundColor="#FAFAFA"
              ItemSelected="OnListViewItemSelected">
            <ListView.ItemTemplate>
                <DataTemplate>
                    <TextCell Text="{Binding Name}"
                          Detail="{Binding LocationStr}" />
                </DataTemplate>
            </ListView.ItemTemplate>
        </ListView>
        <StackLayout BackgroundColor="#FFF"
                     x:Name="SelectedAndOperate">
            <BoxView Color="#000000"
                     WidthRequest="10000"
                     HeightRequest="0.17"/>
            <Label Text="Selected:" 
                   HorizontalOptions="Start"
                   VerticalOptions="CenterAndExpand"
                   Margin="20, 5, 20, 5"/>
            <StackLayout Orientation="Horizontal"
                         HorizontalOptions="Center">
                <Entry Placeholder="City Name"
                   x:Name="InputCityName"
                   HorizontalTextAlignment="Center"
                   WidthRequest="125"
                   Margin="5, 0, 5, 0"/>
                <Entry Placeholder="Index"
                   x:Name="InputIndex"
                   WidthRequest="125"
                   HorizontalTextAlignment="Center"
                   Margin="5, 0, 5, 0"/>
            </StackLayout>
            <StackLayout Orientation="Horizontal" 
                         HorizontalOptions="Center">
                <Entry Placeholder="Location X"
                   x:Name="InputLocationX"
                   HorizontalTextAlignment="Center"
                   WidthRequest="125"
                   Margin="5, 0, 5, 0"/>
                <Entry Placeholder="Location Y"
                   x:Name="InputLocationY"
                   HorizontalTextAlignment="Center"
                   WidthRequest="125"
                   Margin="5, 0, 5, 0"/>
            </StackLayout>

            <Button Text="&gt;&gt; Operate &lt;&lt;"
                    Clicked="OnOperateClicked"
                    Margin="10, 10, 10, 10"/>
        </StackLayout>
    </StackLayout>
</ContentPage>
```

逻辑：

```csharp
// Demo/DataStructDemo/CityListPage.xaml.cs

using System;
using System.Collections.Generic;
using Xamarin.Forms;
using System.Collections.ObjectModel;
using System.Threading;
using System.Threading.Tasks;

namespace DataStructDemo
{
    public partial class CityListPage : ContentPage
    {

        private CityList cities;

        //private ObservableCollection<City> lst;

        public CityListPage()
        {
            InitializeComponent();

            cities = new CityList();
            AddSomeCitys(cities);

            // lst = new ObservableCollection<City>();

            // lst.Add(new City("Foo", new Point2D(500, 500)));
            // lst.Add(new City("Bar", new Point2D(703, 500)));

        }

        protected override void OnAppearing()
        {
            base.OnAppearing();

            CityListView.ItemsSource = cities;
        }

        public async void OnSearchClicked(object sender, EventArgs e)
        {
            // DisplayAlert("未完成的功能", "现在还不能用哦", "取消");
            await Navigation.PushAsync(new CitySearchPage(cities));
        }

        public void OnListViewItemSelected(object sender, SelectedItemChangedEventArgs e)
        {
            InputCityName.Text = (e.SelectedItem as City).Name;
            InputIndex.Text = (e.SelectedItemIndex).ToString();
            InputLocationX.Text = ((e.SelectedItem as City).Location.X).ToString();
            InputLocationY.Text = ((e.SelectedItem as City).Location.Y).ToString();
        }

        public async void OnOperateClicked(object sender, EventArgs e)
        {
            try
            {
                if (InputCityName.Text == "")
                {
                    throw new Exception("City Name cannot be empty.");
                }
                if (InputLocationX.Text == "" || InputLocationY.Text == "")
                {
                    throw new Exception("Location X/Y cannot be empty.");
                }

                string cityName = InputCityName.Text;
                double locX = double.Parse(InputLocationX.Text);
                double locY = double.Parse(InputLocationY.Text);
                int index = int.Parse(InputIndex.Text);

                string action = await DisplayActionSheet($"以选择 {cityName} ({locX}, {locY}), index={index}", "Cancel", null, "头插", "尾插", "插入到index处", "删除index处的城市", "更新index处的城市");
                await HandOperateAction(action, cityName, locX, locY, index);

            }
            catch (Exception ex)
            {
                await DisplayActionSheet("输入有误，无法继续操作: \n" + ex.Message, "Cancel", null);
            }

        }

        private async Task<bool> HandOperateAction(string action, string cityName, double locX, double locY, int index)
        {
            bool ok = false;
            try
            {
                City city = new City(cityName, new Point2D(locX, locY));
                switch (action)
                {
                    case "头插":
                        cities.InsertAtHead(city);
                        // lst.Insert(0, city);
                        break;
                    case "尾插":
                        cities.InsertAtRear(city);
                        // lst.Add(city);
                        break;
                    case "插入到index处":
                        cities.Insert(index, city);
                        break;
                    case "删除index处的城市":
                        cities.RemoveAt(index);
                        break;
                    case "更新index处的城市":
                        cities[index] = city;
                        break;
                }
                ok = true;
            }
            catch (Exception ex)
            {
                await DisplayAlert("出错啦!", "不能完成操作:\n" + ex.Message, "取消");
            }
            finally
            {
                RefreshCityListView();
            }
            return ok;
        }

        private void RefreshCityListView()
        {
            CityListView.BeginRefresh();
            CityListView.ItemsSource = null;
            CityListView.EndRefresh();
            CityListView.ItemsSource = cities;
        }

        private void AddSomeCitys(CityList cities)
        {
            cities.InsertAtRear(new City("Foo", new Point2D(500, 500)));
            cities.InsertAtRear(new City("Bar", new Point2D(703, 500)));
            cities.InsertAtRear(new City("Gophers' City", new Point2D(600, 1200)));
            cities.InsertAtRear(new City("川坨", new Point2D(100, 20)));
        }
    }
}
```

继续，写我们刚才落下的搜索页面。其实这里要实现的好看很麻烦了，你可以去根据用户选择搜名字还是搜坐标而动态响应，给出不同的搜索框，然后进行搜索、结果展示。我不想这么做（我还是个 Xamarin 新手，我有点害怕这么复杂的页面），还是简单暴力一点，直接把两种输入做到一起比较方便：

![IMG_449](https://tva1.sinaimg.cn/large/00831rSTgy1gclstvjqawj30u00whgn8.jpg)

**代码实现：**

界面：`Demo/DataStructDemo/CitySearchPage.xaml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="DataStructDemo.CitySearchPage"
             Title="City Search">
    <StackLayout Margin="20">
        <Grid>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="0.2*" />
                <ColumnDefinition Width="0.2*" />
                <ColumnDefinition Width="0.2*" />
                <ColumnDefinition Width="0.25*" />
            </Grid.ColumnDefinitions>
            <Grid.RowDefinitions>
                <RowDefinition/>
                <RowDefinition/>
                <RowDefinition/>
                <RowDefinition/>
            </Grid.RowDefinitions>
            <Label Text="通过城市名搜索："
                   HeightRequest="25"
                   Grid.Row="0"
                   Grid.ColumnSpan="4"/>
            <Entry Placeholder="City Name"
                   x:Name="InputName"
                   HorizontalTextAlignment="Center"
                   Grid.Row="1"
                   Grid.Column="0" Grid.ColumnSpan="3" />
            <Button Text="Search"
                   Clicked="SearchByNameClicked"
                   Grid.Row="1"
                   Grid.Column="3" Grid.ColumnSpan="1"/>
            <Label Text="或 通过中心坐标、半径搜索："
                   Margin="0,10,0,10"
                   HeightRequest="25"
                   Grid.Row="2"
                   Grid.ColumnSpan="4"/>
            <Entry Placeholder="X"
                   x:Name="InputX"
                   HorizontalTextAlignment="Center"
                   Grid.Row="3"
                   Grid.Column="0"/>
            <Entry Placeholder="Y"
                   x:Name="InputY"
                   HorizontalTextAlignment="Center"
                   Grid.Row="3"
                   Grid.Column="1"/>
            <Entry Placeholder="Radius"
                   x:Name="InputRadius"
                   HorizontalTextAlignment="Center"
                   Grid.Row="3"
                   Grid.Column="2"/>
            <Button Text="Search"
                   Clicked="SearchByLocationClicked"
                   Grid.Row="3"
                   Grid.Column="3" Grid.ColumnSpan="1"/>
        </Grid>
        <BoxView Color="#000000"
                   WidthRequest="10000"
                   HeightRequest="0.17"/>
        <Label Text="搜索结果:"
               HeightRequest="25"
               Margin="0,10,0,10"/>
        <ListView x:Name="CitySearchListView"
              HeightRequest="300"
              ItemSelected="OnListViewItemSelected">
            <ListView.ItemTemplate>
                <DataTemplate>
                    <TextCell Text="{Binding Name}"
                          Detail="{Binding LocationStr}" />
                </DataTemplate>
            </ListView.ItemTemplate>
        </ListView>
    </StackLayout>

</ContentPage>
```

逻辑：

```csharp
// Demo/DataStructDemo/CitySearchPage.xaml.cs

using System;
using DataStructureAlgorithm.LinearList;
using System.Collections.Generic;

using Xamarin.Forms;

namespace DataStructDemo
{
    public partial class CitySearchPage : ContentPage
    {
        private CityList cities;

        public CitySearchPage(CityList cityList)
        {
            InitializeComponent();
            cities = cityList;
        }

        public void OnListViewItemSelected(object sender, SelectedItemChangedEventArgs e)
        {
            DisplayAlert("未完成的功能", "你点它干嘛啊，我想不出这里要做什么操作。", "取消");
        }

        void SearchByNameClicked(object sender, EventArgs e)
        {
            try
            {
                if (InputName.Text == "")
                {
                    throw new Exception("要搜索的城市名不能为空。");
                }

                SeqList<int> indices = cities.SearchByName(InputName.Text);
                ShowFoundCities(indices);

            }
            catch (Exception ex)
            {
                DisplayActionSheet("发生错误，未能完成搜索: \n" + ex.Message, "Cancel", null);
            }
        }

        void SearchByLocationClicked(object sender, EventArgs e)
        {
            try
            {
                if ((InputX.Text == "") || (InputY.Text == "") || (InputRadius.Text == ""))
                {
                    throw new Exception("要搜索的中心坐标X、Y以及搜索半径Radius不能为空。");
                }

                Point2D center = new Point2D(double.Parse(InputX.Text), double.Parse(InputY.Text));
                double radius = double.Parse(InputRadius.Text);

                SeqList<int> indices = cities.SearchByLocation(center, radius);
                ShowFoundCities(indices);
            }
            catch (Exception ex)
            {
                DisplayActionSheet("发生错误，未能完成搜索: \n" + ex.Message, "Cancel", null);
            }
        }

        void ShowFoundCities(SeqList<int> indices)
        {
            CityList foundCities = new CityList();
            for (var i = 0; i < indices.Length; i++)
            {
                foundCities.InsertAtHead(cities[indices[i]]);
            }

            CitySearchListView.ItemsSource = foundCities;

            if (foundCities.IsEmpty())
            {
                NoResultFound();
            }
        }

        void NoResultFound()
        {
            DisplayAlert("无结果", "没有找到符合条件的城市。", "取消");
        }
    }
}
```

OK了，界面的设计也完成了，，，这个东西好像已经全部介绍完了，因为简单嘛，没多少好说的。我先去睡个觉再接着介绍一下我遇到的一些问题。

...... Me.Sleep(11 * time.Hour);	// 几个小时过去了

## 实现难点

我前面给出代码的里面有些 IEnumerable, INotifyPropertyChanged 之类的东西，我没有解释这是干什么的，是因为这个问题比较复杂（是因为我还没有优雅地解决问题），留到这里来单独讨论。

在我们实现的设计的时候，城市放到了继承自 `SLinkList` 的 `CityList`，然后我们把这个 `CityList` 放到了 Xamarin 提供的 `ListView` 中显示出来。注意到了没有？问题就是人家 Xamarin 的组件为什么支持咱自己实现的野生数据结构？

`ListView` 是通过 set `ItemsSource` 来给定要显示的列表的，而这个 `ItemsSource` 的接收的是 `IEnumerable` 接口的实现。所以我们只需要让 `CityList` 实现一个 `IEnumerable` 就可以显示出来了。

但，仅仅是现实出来！如果你去尝试运行，会发现，在 `CityList` 在屏幕上显示出来后，你尽管往里面添加、删除、修改，显示出来的列表总是纹丝不动！

这看上去好像是我们自己实现的 `CityList` 还是有缺陷，不能支持 ListView 的自动更新，那么我们换一个系统的列表实现，用 `List<City>` 代替 `CityList`。再次尝试，你还是会发现 ListView 不会自动更新！

这就有点离谱了啊，ListView 不支持系统标准实现的 List!

事已至此，我们只好看谷歌眼色行事。网上一些大佬给出的 Xamarin.Forms ListView 最佳实践中，总是会在代码里给 `ItemsSource` 传一个 `List<>` 的数据，然后顺便提那么一句：“这里更推荐用 ObservableCollection，以实现数据刷新后列表的更新显示......”

那好吧，看来我们按照大佬的建议 把 List 换成 `ObservableCollection`，然后数据更新真的会自动显示了！

我继续研究了一下这个 `ObservableCollection`，网上说因为 ObservableCollection 实现了`INotifyPropertyChanged`，所以 ListView 才可以自动更新。

仿照 [INotifyPropertyChanged Interface的文档](https://docs.microsoft.com/en-us/dotnet/api/system.componentmodel.inotifypropertychanged?view=netframework-4.8) 我实现的 INotifyPropertyChanged 大概是这样的：

```csharp
public event PropertyChangedEventHandler PropertyChanged;

protected void NotifyPropertyChanged(String info)
{
    if (this.PropertyChanged != null)		// 这里还可以简化成委托，效果是一样的
    {
        this.PropertyChanged(this, new PropertyChangedEventArgs(info));
    }
}

public void Remove(int index)
{
    ...
    NotifyPropertyChanged("remove");
}

public void Insert(int index, T data)
{
    ...
    NotifyPropertyChanged("insert");

}
```

但是，这样也不行！数据还是不会自动刷新。

然后我查了 [ObservableCollection的源码](https://referencesource.microsoft.com/#System/compmod/system/collections/objectmodel/observablecollection.cs,4eb38b95b10327e7) ，我尝试抄他的代码，得到了一个这样的 SLinkList（这里简化细节了，详细的代码就是之前设计实现部分给出的 SLinkList 源码）：

```csharp
using System;
using System.ComponentModel;

namespace DataStructureAlgorithm.LinearList
{
    public class SLinkList<T> : ILinearList<T>, INotifyPropertyChanged where T : IComparable<T>
    {
        public int Length { get; private set; }
        protected string LengthStr = "Length";
        
        public SNode<T> HeadNode { get; private set; }
        protected string HeadNodeStr = "HeadNode";

        public SLinkList() {...}

        public event PropertyChangedEventHandler PropertyChanged;

        protected SNode<T> NodeAt(int index) { ... }
        
        public T this[int index]
        {
            get {...}
            set
            {
                ...
                OnPropertyChanged(IndexerName);
            }
        }
        protected string IndexerName = "this[]";

        public void Clear()
        {
            ...
            OnPropertyChanged(LengthStr);
            OnPropertyChanged(IndexerName);
        }

        public void Insert(int index, T data)
        {
            ...
            OnPropertyChanged(LengthStr);
            OnPropertyChanged(IndexerName);

        }

        public void InsertAtHead(T data) { Insert(0, data); }

        public void InsertAtRear(T data) { Insert(Length, data); }

        public bool IsEmpty() { }

        public void Remove(int index)
        {
            ...
            OnPropertyChanged(LengthStr);
            OnPropertyChanged(IndexerName);
        }

        public int Search(T data) { }

        event PropertyChangedEventHandler INotifyPropertyChanged.PropertyChanged
        {
            add
            {
                PropertyChanged += value;
            }
            remove
            {
                PropertyChanged -= value;
            }
        }

        private void OnPropertyChanged(string propertyName)
        {
            OnPropertyChanged(new PropertyChangedEventArgs(propertyName));
        }

        protected virtual void OnPropertyChanged(PropertyChangedEventArgs e)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, e);
            }
        }
    }
}
```

但是，这样还是不行。。。。。。我觉得问题可能是出在我写的 `OnPropertyChanged(IndexerName)`、`protected string IndexerName = "this[]";` 这里，我觉得不应该是 `this[]`，但我完全不知道这个 `propertyName` 是什么东西、应该写什么。。。

---

目前，我解决的方法是，强制 ListView 去重新载入数据源，这肯定不是个好办法，这样去刷新界面会快速闪出新数据，而不是像使用 ObservableCollection 作为数据源那样修改数据后会自动有平滑的动画去展示列表变动：

```csharp
private void refreshCityListView()
{
    // CityListView.BeginRefresh();
    CityListView.ItemsSource = null;
    CityListView.ItemsSource = cities;
    // CityListView.EndRefresh();

}
```

这么做实在笨拙，但一时半会我确实无能解决如何实现一个 `ObservableCollection` 的问题。如果你有更好的解决方案请务必与我分享🥺

## 关于整体 App 设计与展望

在一开始我提到过我把这个城市链表只写成了这个 App 里的一个功能！我想把这个 App 写成一个比较全的数据结构与算法演示。

但其实这也挺难的，是个不小的工程了！在我的构想中，这个 App 的完整形态应该是分成 4 个板块的：

- *学习*：就是放数据结构与算法学习的资料，参考“算法动画图解”；
- *试验*：就是放比如我们这次的城市链表这样的数据结构使用实践的地方，即现在已经实现的“目录”页；
- *交流*：就是一个 WebView 打开个 Wordpress 论坛了；
- *我的*：登录、收藏、设置、关于、反馈这一套。

这个要做起来时间就比较长了，慢慢来吧，有机会就把它做出来。(主要是咱交不起99美元的年费，不然这东西做出来感觉都可以上架 App Store 了:)

## （蒟蒻的抱怨-Part2）

~~“这 App 开发还是不容易啊......”, 瘫坐在椅子上的蒟蒻抱怨到。~~

“这 App 开发还是很有意思的～”，蒟蒻兴高采烈地写下这篇文章的最后一句。