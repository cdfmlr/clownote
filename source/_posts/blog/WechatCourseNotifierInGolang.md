---
title: Golang 实战——微信公众号课程提醒系统
tags: Golang
categories:
	- Golang
---

# Golang 实战——微信公众号课程提醒系统

## 起因

最早开始学 Golang 已经是整整一年前了，当时就把基础语法那一块学完了，然后拿 Golang 写了点 leetcode 题。之后由于项目里一直用 Python 和 Java，Golang 这一块就搁置下来没学了。

之前寒假本来是打算学 iOS、Mac 开发这一块的，搞了两个星期，感觉暂时不想学下去了。（我想学 SwiftUI，我觉得这才够酷，但我不想拿赖以生存的老 Macbook 尝试 Catalina，Mojave 写 SwiftUI 没有及时预览，感觉没有灵魂了。）

所以就搬出 Golang 来接着学了。看完了函数、接口、并发这一块，然后就学了一些 Web 开发方面的。（这才实在，不然语言学完就只能刷 leetcode。）

学完了差不多就开学了，刚好我一直憎恶超级课程表广告的烦扰，所以就打算写一个可以自动从教务系统获取课程表、在上课前提醒的课程表项目。这个照理来说是个前端项目，但 iOS 开发这一块还没学完。本来 Android 也行，但我用 iPhone 啊。所以想了个曲线救国的方法——微信公众号开发，纯后端，拿来练习 Golang 再好不过。

---

由于时间、空间有限很多地方我写的不太清晰。所以在开始阅读本文之前，我建议你打开源码，对照阅读。：[https://github.com/cdfmlr/CoursesNotifier](https://github.com/cdfmlr/CoursesNotifier)。

---

我在这个项目中的很多地方尝试了 Golang 的“面向对象”。Go 不是一个面向对象的语言，这给写惯了 Java、Python 的我们还是带来了一些不适应的。但没关系，正如它的发明者们所说，Go 是用来构建系统的实用语言。面向对象不可否认是构建系统的强有力工具，Golang 当然会有所支持。当然，也只是有所支持，而不是真正的面向对象，我在 coding 的时候，就在一个需要多态的地方碰到了困难，最后不得不更改设计，稍微没那么优雅了。

在这篇文章中，我尝试记录我开发这个系统的整个过程、解释尽可能多的代码设计。但因为毕竟整个项目有接近3000行代码，我不可能逐一解释到位。如果你想看懂所有东西，请去 GitHub 打开这个项目的源码对照来看，我也是个初学者，写出的代码应该还是很简单的。

另外，这篇文章不是 Golang 的入门，在开始阅读前请确保你掌握了（起码是有所了解）以下技能：

- Go语言基础：[A Tour of Go](https://tour.go-zh.org/welcome/1) ：全部内容；
- Go语言Web开发基础：[astaxie/build-web-application-with-golang](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/preface.md) ：1～7章；
- 微信公众号开发基础：[微信公众号入门指引](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Getting_Started_Guide.html) ：1、2、4节；

## 目标

我的目的很明确，就是做一个微信公众号系统，在上课前发个通知提醒快上课了。但我不想手动输入课程信息，不然 iDaily Corp 开发的《课程表·ClassTable》就已经很好了。

所以还需要自动从教务系统获取课程表，学校用的新教务系统是：

![屏幕快照 2020-03-09 10.35.24](https://tva1.sinaimg.cn/large/00831rSTgy1gcnh3mn82nj318t0u07wh.jpg)

嗯，我研究了一下，他这个web端反爬虫还是做的不错的，可以爬，但不好爬！那我们怎么搞到课表？

还好我发现了这个项目：[TLingC](https://github.com/TLingC)/**[QZAPI](https://github.com/TLingC/QZAPI)**。这位大佬爬了强智的 App，抓出了这公司的 API。可以直接调用这个接口获取课表了：

![image-20200309170649126](https://tva1.sinaimg.cn/large/00831rSTgy1gcnse0hy1gj318t0u0kcz.jpg)

这个 API 文档做的挺好，无可挑剔；但这个 API 着实很恶心，看看他返回的课表：

![image-20200309105136147](https://tva1.sinaimg.cn/large/00831rSTgy1gcnhjlijzyj30t0090dii.jpg)

这就是我们“领先的教学一体化平台”——强(ruo)智教务系统！

我找不到一个合适的、不带个人感情色彩的词语来客观公正地评价这个设计。不管了，也只能将就着用了。

---

肿的来说，我们的系统有两方面：

- 一个是输入(I)：自动从教务系统获取课表；
- 还有是输出(O)：自动提醒学生上课。

接下来我们就一步一步把这个系统实现：

## 设计与实现

### 数据库

首先是数据库设计。

本来写这东西 MongoDB 用挺方便的，但这学期有数据库课嘛，肯定不学这些 NoSQL，所以还是复习一下 SQL，用一下关系型数据库。

其实这个东西挺传统啊，就是数据库书上的例子嘛，主要就三个表：

* 一个 Student 表，存学号、微信号（公众号里的openid）还有教务密码（这个可以不存的，存了还不安全，我不知道我设计的时候是怎么想的，后悔了，但懒得改😂）
* 一个 Course 表，存课程名、上课时间、教室地点、授课老师......（就是强智API返回的那些）
* 还有就是 S-C 选课关系表。
* 最后，还有一个储存当前是那个学期之类的信息的表。

来看最后设计好的表结构：

![屏幕快照 2020-03-04 16.03.36](https://tva1.sinaimg.cn/large/00831rSTgy1gchylz4iwyj30ra0f20vl.jpg)

### 数据模型

有了数据库，我们还要在程序里使用数据库。也就要把数据库里的记录对应到程序里的结构体（Models）中。

为了方便（懒），我们直接把数据库里的东西对应过来，弄成这几个模型，里面的属性和数据库的属性一一对应（那个current太简单了，就是一个时间嘛， `time.Time`直接就可以用了，不用再去封装了）：·Student

* Course
* Relationship

![屏幕快照 2020-03-04 16.28.03 2](https://tva1.sinaimg.cn/large/00831rSTgy1gchz85gatjj313m0kq0w7.jpg)

> `蓝T`是结构体，下面的`黄f`是属性，`红f`是函数/方法

（这些图都是从 IDEA 截图出来自己随手拼的，没时间好好调，所以有点丑）

（对，没错，我用 IDEA 写 Golang，MacBook 硬盘小鸭，没办法，咱坚强的 IDEA 带上几个插件就肩负起了我家 Java、Android、Python、Go 的所有“大型“项目开发）

注意这里强智系统API请求来的课程是没有 `cid` 的，但我们为了唯一识别一个课程，所以在构造函数 `NewCourse` 里自动通过计算 Name,Teacher,Location,Begin,End,Week,When 的 md5 和得出。

有了模型，我们再实现数据操作(Data) :`StudentDatabase`、`CourseDatabase`、`StudentCourseRelationshipDatabase`。

这几个东西实现数据库与模型的转化，提供增删改查操作。

![屏幕快照 2020-03-04 16.28.03 3](https://tva1.sinaimg.cn/large/00831rSTgy1gcnj23azd8j319y0q6tor.jpg)

(这里有很多方法其实都是不必要的，都是一样的操作，我只是一开始为了图方便，复制粘贴出来的)

###  教务API&Client

有了这些数据模型，我们就可以访问强智教务系统了。

我们先用 Golang 把【强智教务系统API文档】([TLingC](https://github.com/TLingC)/**[QZAPI](https://github.com/TLingC/QZAPI)**)里我们需要用到的接口封装一下。我们需要用到的只是“课程信息”，但使用“课程信息”，又需要我们请求“登录”和“时间信息”。所以我们需要封装这三个请求。

阅读这个强智教务系统API文档，我们会发现所有请求都是类似的 GET：

```
GET http://jwxt.xxxx.edu.cn/app.do?method=...&...

request.header{token:'运行身份验证authUser时获取到的token，有过期机制'},
request.data{
    'method':'登录/时间/课程信息等的方法名',
    '...':  '一些特定的参数'
    ...
}
```

所以我们可以把这种 “强智 API GET” 封装起来，做成一个 `qzApiGet` 函数，简化后面的工作。这个函数通过给定学校域名（就是`jwxt.xxxx.edu.cn`的`xxxx`，例如华电是`ncepu`）、token（如果是登录不需要token就传空字符串`""`）、还有解析请求结果的结构体实例res、以及一个请求参数的map（就是method那些）：

```go
func qzApiGet(school string, token string, res interface{}, a map[string]string) error {
	// Make URL
	rawUrl := fmt.Sprintf("http://jwxt.%s.edu.cn/app.do", school)
	Url, err := url.Parse(rawUrl)
	
    // Add params
	params := url.Values{}
	for k, v := range a {
		params.Set(k, v)
	}
	Url.RawQuery = params.Encode()
	urlPath := Url.String()

	// Make Request
	client := &http.Client{}
	req, err := http.NewRequest("GET", urlPath, nil)
    
    // Add token
	if token != "" {
		req.Header.Add("token", token)
	}

	// GET and Parse Response
	resp, err := client.Do(req)
	if err != nil {
		log.Println(err)
		return err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	err = json.Unmarshal(body, res)
    
    // Handle Error and Return
	if err != nil {
		log.Println(err)
		return err
	}
	return nil
}
```

有了这个 `qzApiGet`，我们就可以方便地封装出我们需要的三个请求了：

![屏幕快照 2020-03-04 16.28.03 4](https://tva1.sinaimg.cn/large/00831rSTgy1gcnssefvudj319y0q6tga.jpg)

这里面的个函数大同小异，我举其中一个例子就好了：

```go
func GetCurrentTime(school, token, currDate string) (*GetCurrentTimeRespBody, error) {
	resp := &GetCurrentTimeRespBody{}
	q := map[string]string{
		"method":   "getCurrentTime",
		"currDate": currDate,
	}
	err := qzApiGet(school, token, resp, q)
	if err != nil {
		log.Println(err)
		return &GetCurrentTimeRespBody{}, err
	}
	return resp, nil
}
```

这些都是一些相当于面向对象里的 `public static` 的方法啊，调用起来还是不方便。

我们希望有一个 `QzClient`，这个东西的实例就像我们使用 app 一样的一个客户端，给这个客户端用户名、密码他就可以登录了，然后你要课表就直接取这个实例的 `Courses` 属性，一切请求都在黑箱里完成。

我们把这个 Client 写出来：

![image-20200309173318272](https://tva1.sinaimg.cn/large/00831rSTgy1gcnt5k5hgrj30si0iaq6h.jpg)

。。。这乍一看，还是很可怕的。没关系，我们一个个慢慢解释。

首先说属性，

- `Student`：就是来用这个强智客户端的学生，
- `token`：是该学生登录后获取的 token，
- `CurrentXnxqId`：表示当前学年学期Id（别问我为什么这么命名，找强智公司去！），
- `CurrentWeek`：当前周次
- `Courses`：就是当前学期这个同学的所有课程啦，因为需要去重，所以我直接用了一个 map，key 放我们的 `Cid`（md5和），value 是 `Course` ，这样就保证了数据不重复。

再来看方法：

- `AuthUser`：调用我们 强智 api 里的 `AuthUser`，登录强智系统，获取操作 token，在该 token 过期之前可以做其他操作;
- `FetchCurrentTime`：调用 强智api 获取当前学期、周次，储存在 `CurrentXnxqId`、`CurrentWeek` 里；
- `FetchWeekCoursesSlowly`：获取某个星期的课表，要反爬虫，所以里面放了一个Sleep，速度很慢，用 chan 去“返回”结果。
- `FetchAllTermCourses`，对一个学期的每个周调用 `FetchWeekCoursesSlowly`，获取真学期的课表，并通过 `appendCourse` 把这些课程添加到结构体的 `Courses` 属性中。
- `Save`：分别调用 `saveStudent`, `saveCourses`, `saveSCRelationships` 把这个客户端的学生、课程、选课关系写入库！这就是我们唯一写入数据的地方！

呼——终于写完这些了，这里有点枯燥，用强智烂系统的恶心 API 嘛，没多少意思。

小结一下，到现在为止，我们有了数据模型、数据库，可以访问教务系统、从教务系统自动获取给定学生的课表，并把学生、课程、选课关系写入数据库了。

接下来就比较有意思了，我们来看课程时钟的设计。

### 课程时钟

啥？课程时钟？什么是课程时钟？就是说，咱们要在上课前提醒同学们上课，这就需要服务器知道现在是什么时间、上课在什么时间。也就是一个像“钟”一样的东西，不停地走，在指定的几个时间点“响”（提醒上课），所以我们把这个模块叫做课程时钟——CourseTicker。

这个 CourseTicker 的实现很简单也很直观，就像钟“滴答滴答”地走嘛。CourseTicker 需要定时启动，检测当前是不是快上课了，如果是，就提醒学生，不是就什么都不做。

在 Go 中，要实现这样的定时启动任务很方便，只需要在一个 for 无限循环中睡眠一段时间，然后启动执行任务即可，当然，我们不希望这样永不停止的任务运行在主线程中，所以用一个「匿名函数立即执行」手法把它包装起来：

```go
go func() {
    for {
        // 计算下一个执行时间
        now := time.Now()
        next := now.Add(t.period)
        // 等待到时间
        timer := time.NewTimer(next.Sub(now))
        <-timer.C
        // 执行任务
        RunTickTask()
    }
}()
```

#### 抽象周期运行器

上面这个方法虽然做到了不停运行、定时执行，但是我们不方便控制它的开始、结束，而且这段代码也不方便复用。所以我们考虑封装一个可以控制开始、结束，能不停运行、定时执行的 Ticker 结构体（相当于 OOP 的类）：

![image-20200306084846495](https://tva1.sinaimg.cn/large/00831rSTgy1gcjx4wz2sbj30e609k3z9.jpg)

解释一下它是怎么工作的：

- `tickerId`: 只是一个标识符，因为我们完全可以在一个系统中使用多个这样的 Ticker 实例，所以搞一个 tickerId ，打日志的时候做区分。
- `period`: 就是间隔的时间了，每隔这么久就跑一次 `RunTickTask` 方法。
- `end`: 这是用来控制结束的 channel，往里面传值就代表结束 Ticker 的周期性运行了。
- `task`: 就是你要用这个 Ticker 周期性完成的工作，直接传一个函数进来（函数是 Go 的一等公民嘛）
- `Start`: 开始周期性任务。传一个时间进来，代表从这个时候再开始，这么做是因为我们可能希望比如每个小时整点的时候跑任务，但我们不想等到正点再去开启这个服务，就可以通过给 Start 传一个 `08:00`(这里只是举个例子，你要传的是完整的时间，比如 `time.Now()` 哦)，这样它第一次开始就是正点，睡眠一个小时后再运行，还是正点......这样就比较方便了。
- `RunTickTask`: 要周期性运行的任务，其实就是打个日志，然后调用属性里的 `task`。单独搞一个函数出来做这个，一个是把功能划分细，不在 Start 里写具体运行的逻辑，还有一个就是方便你可以在非周期到的时候手动调用任务。
- `End`: 通知 TickTask 终止运行。实际上就是往 `end` 里传个值，让 Start 里开始的周期性匿名函数收到这个消息，终止运行。

来看一下大概的代码实现（空间有限，我删了不必要的注释和空行，看起来可能有点丑）：

```go
type Ticker struct {
	tickerId string
	period   time.Duration
	end      chan bool
	task     func()
}

func (t *Ticker) Start(time2Start time.Time) {
	time2Start = time2Start.Add(t.period * -1)
	if time2Start.Sub(time.Now()) > 0 {
		timer := time.NewTimer(time2Start.Sub(time.Now()))
		<-timer.C
	}
	go func() {
		for {
			select {
			case <-t.end:
				log.Printf("(Ticker {%s}) TickTask End Exed...\n", t.tickerId)
				return
			default:
				now := time.Now()
				next := now.Add(t.period)
				timer := time.NewTimer(next.Sub(now))
				<-timer.C
				t.RunTickTask()
			}
		}
	}()
}

func (t *Ticker) RunTickTask() {
	log.Printf("(Ticker {%s}) TickTask Run...\n", t.tickerId)
	if t.task != nil {
		t.task()
	}
}

func (t *Ticker) End() {
	t.end <- true
}
```

#### 课程时钟

现在有了周期运行器 Ticker，再来看之前说的 CourseTicker，不过就是一个简单的继承嘛。我们让 CourseTicker “继承” Ticker，这样它就有了周期性运行的技能，再给他一些具体的检查是否快要上课了、以及提醒上课的功能就行了：

![image-20200309111736674](https://tva1.sinaimg.cn/large/00831rSTgy1gcnianyzkaj30t40dwju8.jpg)

哈哈，说起来简单，实现起来还是不容易的。由于强智教务系统的鬼畜设计，我们不得不把代码写得很恶心了。

这里大概的思路就是 CoursesTicker 的 `NotifyApproachingCourses` 方法作为 Ticker 的周期性 task，这个方法会查询现在有没有课快开始了（就是 `开始上课时间 - 当前时间 <= minuteBeforeCourseToNotify`），如果有课快开始了，就找出上这些课的学生，去发通知给他们。

具体的实现里我们需要这几个辅助的函数：

- `getNearestBeginTime` 获取距离当前最近的课程时间，就是用 `SELECT DISTINCT begin FROM course` 查询出所有可能的上课时间，找出最近的一个。
- `getCurrentWeek` 获取当前教学周次
- `isCourseInWeek` 判断一个 models.Course 是否在指定周次(week) 有课

而这几个辅助函数的实现又会调用这几个辅助辅助函数(这里我直接抄了代码里的文档注释)：

- `_getPossibleCourseBeginTime`: 返回数据库中今、明两天的所有可能上课时间
- `_durationToWeek`: convert a duration into week
- `_roundTime`: helps getting a reasonable int from a float, which is of great help when converting the duration into week

`NotifyApproachingCourses` 的内部实现就是首先调用 `getCurrentWeek` 获取今天是第几周、调用 `time.Now().Weekday()` 获取今天是星期几（这里还需要把系统的星期表示方式换算成强智系统内的星期表示方式），然后调用 `getNearestBeginTime` 最近一个可能上课的时间，如果这个时间距离现在已经 `<= minuteBeforeCourseToNotify` 了，就要找出在这个时间开始的所有课程，并通过 `isCourseInWeek` 过滤出本周这个时间要上的课，最后就找上这些课的学生，通知ta们要开始上课了。

到这里 CourseTicker 要做的事就完了，我们可不想在已经这么复杂的一个模块里再实现一个微信通知的功能了，那样这个“类”就长到爆炸了呀。

通知应该是一个通知模块做的事。但在 CourseTicker 里我们要完成通知呀！怎么办？

调用暂时没有具体实现的东西——当然是使用**接口**了。

### 通知接口

这个通知接口很简单就两三行代码，只需要提供一个通知函数 `Notify`。通过给定要通知的学生、要通知的课程，这个 `Notify` 函数去完成通知。

```go
type Notifier interface {
	Notify(student *models.Student, course *models.Course)
}
```

我们还可以顺手实现一个 `Notifier` 接口的实现—— `LogNotifier`，把通知的学生、课程打印到 Log 里：

```go
type LogNotifier string

func (l LogNotifier) Notify(student *models.Student, course *models.Course) {
	log.Printf("(LogNotifier %s) Course Notify:\n\t|--> student: %s\n\t|--> course: %s (%s)", l, student.Sid, course.Cid, course.Name)
}
```

至于微信提醒，就比较复杂了，我们在下面单独来说。

### 微信系统

我们这个系统是基于微信公众号的，现在我们终于讲到微信系统了。我们需要的微信系统有两个方面，一个是微信公众号的被动服务，就是接受用户发来的消息，完成课程提醒的订阅、退订操作的；还有一方面就是通过微信公众号发送上课提醒给用户了。

#### 微信上课通知

我们继续刚才的通知接口，先看微信提醒的实现：

![image-20200310095953835](https://tva1.sinaimg.cn/large/00831rSTgy1gcolo3lgl3j31kk07swg8.jpg)

这个 `WxNotifier` 只有一个 public 的方法，就是实现 Notifier 的 `Notify`。调用这个 `Notify` 的时候，我们要完成微信通知的构造和发送，这两个任务分别由 `makeCourseNoticeBody` 和 `postCourseNotify` 完成。

让我们研究一下怎么通过微信公众号发消息，消息体又需要构造成什么样的：

通过微信公众号主动发送消息给用户，我大概看了一遍文档，最简单的应该就是[发送模版消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html)了。所以我们来实现这个。

---

（先来读文档：）

要使用模版消息，要先定义一个模版：

```
"{ {result.DATA} }\n\n领奖金额:{ {withdrawMoney.DATA} }\n领奖  时间:    { {withdrawTime.DATA} }\n银行信息:{ {cardInfo.DATA} }\n到账时间:  { {arrivedTime.DATA} }\n{ {remark.DATA} }
```

发送模版消息的 http 请求方式:

```
POST https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
```

POST 请求体 JSON：

```json
{
    "touser":"OPENID",
    "template_id":"ngqIpbwh8bUfcSsECmogfXcV14J0tQlEpBO27izEYtY",
    "url":"http://weixin.qq.com/download",  
    "miniprogram":{
        "appid":"xiaochengxuappid12345",
        "pagepath":"index?foo=bar"
    },          
    "data":{
        "first": {
            "value":"恭喜你购买成功！",
            "color":"#173177"
        },
        "keyword1":{
            "value":"巧克力",
            "color":"#173177"
        },
        "keyword2": {
            "value":"39.8元",
            "color":"#173177"
        },
        "keyword3": {
            "value":"2014年9月22日",
            "color":"#173177"
        },
        "remark":{
            "value":"欢迎再次购买！",
            "color":"#173177"
        }
    }
}
```

（：文档读完了，接下来实现咱自己的）

---

我们首先来写一个自己的消息模版：

```
{{first.DATA}}
课程：{{course.DATA}}
地点：{{location.DATA}}
老师：{{teacher.DATA}}
时间：{{time.DATA}}
教学周：{{week.DATA}}
--- 
{{bullshit.DATA}}
{{remark.DATA}}
```

这个模版消息的效果大概是这样（这个截图是开发过程中的老版本的，和上面的模版稍有区别）：

![IMG_0486](https://tva1.sinaimg.cn/large/00831rSTgy1gcomni4m6ij30go0h97hi.jpg)

然后就是在 Golang 里封装这个请求了。这需要我们把JSON写成结构体：

![屏幕快照 2020-03-10 09.55.50](https://tva1.sinaimg.cn/large/00831rSTgy1gcolkz8llzj31iq0ey436.jpg)

然后就可以写一个 `makeCourseNoticeBody` 方法来填充数据了(为了节省空间我删了一些代码，很简单，大家可以自行脑补出来)：

```go
// makeCourseNoticeBody 构建微信上课通知 json
func (w WxNotifier) makeCourseNoticeBody(toUser, course, location, teacher, begin, end, week string) ([]byte, error) {
	notice := WxNotice{
		ToUser:     toUser,
		TemplateId: w.courseNoticeTemplateID,
		Data: CourseData{
			First: NoticeItem{
				Value: "滚去上课" + "\n\n",
				Color: "#e51c23",
			},
			Course: NoticeItem{
				Value: course + "\n\n",
				Color: "#173177",
			},
			Location: NoticeItem{...},
			Teacher: NoticeItem{...},
			BETime: NoticeItem{...},
			Week: NoticeItem{...},
			Bullshit: NoticeItem{...},
			Remark: NoticeItem{
				Value: "但还是要好好听课哦💪" + "\n\n",
				Color: "#000000",
			},
		},
	}
	return json.MarshalIndent(notice, " ", "  ")
}
```

构建出了消息，然后就是 POST 发送了：

```go
// postCourseNotify 发送微信公众号上课通知请求
func (w WxNotifier) postCourseNotify(CourseNoticeBody []byte) error {
	url := fmt.Sprintf(
		"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s",
		w.wxTokenHolder.Get(),
	)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(CourseNoticeBody))
	if err != nil {
		log.Println("postCourseNotify Failed:", err)
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		body, _ := ioutil.ReadAll(resp.Body)
		err = NotifyFailed("postCourseNotify Failed")
		log.Println(err)
		return err
	}

	return nil
}

// NotifyFailed 请求返回状态值不为200时抛出的错误
type NotifyFailed string
func (n NotifyFailed) Error() string {
	return string(n)
}
```

代码里有一个 `wxTokenHolder.Get()`，看上去是获取 Token 用的，其实它还真是获取 Token 的。

#### 全局微信 Token Holder

微信公众平台[关于 access_token 的文档](https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html)里说了：

> 建议公众号开发者使用中控服务器统一获取和刷新access_token，其他业务逻辑服务器所使用的access_token均来自于该中控服务器，不应该各自去刷新，否则容易造成冲突，导致access_token覆盖而影响业务。

所以咱们就按照这个思路，做一个全局的 Token Holder。

![image-20200310100931107](https://tva1.sinaimg.cn/large/00831rSTgy1gcoly3zu7qj30l20ba3zu.jpg)

这个 Token Holder 只在咱们的整个系统中实例化一次（其实就是个单例，但我没有尝试怎么用 Go 写单例模式），在需要用到 微信 access_token 的地方，就通过这一个全局唯一的 Token Holder 获取。

调用 Get 的时候，Holder 会自动检测上一次获取的 token 有没有过期，没有的话就直接返回上一次获取的，如果过期了那就重新获取一个，这样就完成了微信文档里建议的统一 token 获取机制。

#### 微信前台服务

现在我们已经实现了自动从教务系统获取课表，自动在上课前发送微信提醒。其实这个系统现在已经可以使用了！你随便写个 `main`，在里面 New 一个 Student 把自己的学号、教务密码、微信open_id 传进去，然后实例化一个强智 Client，登录、获取时间、获取课表、保存，然后开一个 CourseTicker，你就可以收到课程提醒了！

这么做对咱们开发者来说倒是方便了，但对用户可不太友好、或者说是完全没有可用性！用户需要一套可以看得懂、完得成的操作界面。所以还有最后一步——微信的前台服务。

这最后一步可不容易。这一步才真正开始了Web服务开发呢。

先看看我们想要达到的目的（也就是最后完成后的结果）：

![屏幕快照 2020-03-10 11.06.18](https://tva1.sinaimg.cn/large/00831rSTgy1gconlhwh9jj31nr0u07wh.jpg)

是不是有种10086的感觉😂

没办法，这种实现是最简单方便的了，而且就这个看似简单的服务都要花上不少代码来实现呢！

首先，我们来实现一个基本的微信公众号服务：

##### 微信公众号服务Hello World

在这里我不想详细介绍怎么写一个微信公众号Hello World，我只是把代码贴出来（我也是到处东拼西凑刚学来的），你如果不熟悉微信公众号服务，可以结合着我在文章一开始列出的那片微信公众号入门教程，对应着看：

```go
import (
	"bytes"
	"crypto/sha1"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"sort"
	"strings"
	"time"
)

// 开微信服务：

const (
	WxToken = "wwwwwww"
)

func main() {
	http.HandleFunc("/wx", weixinSer)
	http.ListenAndServe(":80", nil)
}

func weixinSer(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	if !validateWechatRequest(w, r) {
		log.Println("Wechat Service: this http request is not from Wechat platform!")
		return
	}
	if r.Method == "POST" {
		textRequestBody := parseTextRequestBody(r)
		if textRequestBody != nil {
		}
		fmt.Printf("Wechat Service: Recv text msg [%s] form user [%s]\n",
			textRequestBody.Content,
			textRequestBody.FromUserName,
		)
		responseTextBody, err := makeTextResponseBody(
			textRequestBody.ToUserName,
			textRequestBody.FromUserName,
			"Hello, "+textRequestBody.FromUserName,
		)
		if err != nil {
			log.Println("Wechat Service: makeTextResponseBody error: ", err)
			return
		}
		fmt.Fprint(w, string(responseTextBody))
	}
}

// 验证消息是否来自微信：

func validateWechatRequest(w http.ResponseWriter, r *http.Request) bool {
	r.ParseForm()

	signature := r.FormValue("signature")

	timestamp := r.FormValue("timestamp")
	nonce := r.FormValue("nonce")

	echostr := r.FormValue("echostr")

	hashcode := makeSignature(WxToken, timestamp, nonce)

	log.Printf("Try validateWechatRequest: hashcode: %s, signature: %s\n", hashcode, signature)
	if hashcode == signature {
		fmt.Fprintf(w, "%s", echostr)
		return true
	} else {
		fmt.Fprintf(w, "hashcode != signature")
	}
	return false
}

func makeSignature(token, timestamp, nonce string) string {
	sl := []string{token, timestamp, nonce}
	sort.Strings(sl)

	s := sha1.New()
	io.WriteString(s, strings.Join(sl, ""))

	return fmt.Sprintf("%x", s.Sum(nil))
}

// 微信消息解析：

type TextRequestBody struct {
	XMLName      xml.Name `xml:"xml"`
	ToUserName   string
	FromUserName string
	CreateTime   time.Duration
	MsgType      string
	Content      string
	MsgId        int
}

func parseTextRequestBody(r *http.Request) *TextRequestBody {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Fatal(err)
		return nil
	}
	fmt.Println(string(body))
	requestBody := &TextRequestBody{}
	xml.Unmarshal(body, requestBody)
	return requestBody
}

// 微信消息响应：

type TextResponseBody struct {
	XMLName      xml.Name `xml:"xml"`
	ToUserName   CDATAText
	FromUserName CDATAText
	CreateTime   time.Duration
	MsgType      CDATAText
	Content      CDATAText
}

type CDATAText struct {
	Text string `xml:",innerxml"`
}

func value2CDATA(v string) CDATAText {
	return CDATAText{"<![CDATA[" + v + "]]>"}
}

func makeTextResponseBody(fromUserName, toUserName, content string) ([]byte, error) {
	textResponseBody := &TextResponseBody{}
	textResponseBody.FromUserName = value2CDATA(fromUserName)
	textResponseBody.ToUserName = value2CDATA(toUserName)
	textResponseBody.MsgType = value2CDATA("text")
	textResponseBody.Content = value2CDATA(content)
	textResponseBody.CreateTime = time.Duration(time.Now().Unix())
	return xml.MarshalIndent(textResponseBody, " ", "  ")
}
```

可别被这些代码吓到呀，其实思路很简单的，只是实现有些繁琐：其实就是开一个web服务，这个服务接收到请求的时候调用 `validateWechatRequest` 来验证该请求是否发自微信，若验证通过确实是微信，那么就用 `parseTextRequestBody` 解析这个消息(我们只处理文本消息)，解析出来有些发送用户啊、消息内容啊这些东西，然后就可以用 `makeTextResponseBody` 构造一个响应返回给微信了。

从这个 HelloWorld 里，我们可以想到，只要我们根据 `parseTextRequestBody` 出来的东西处理后传一个合适的 `content` 给 `makeTextResponseBody`，就可以实现微信消息的响应了。

按照这个思路，我们就可以做出一个**通用**的微信公众号服务框架。

##### 通用微信公众号服务框架

其实这个服务框架基本就是上面的 HelloWorld 做一个抽象。

我们不是需要对 `parseTextRequestBody` 出来的结果做一些处理然后得到要 `makeTextResponseBody` 的 content 嘛。所以我们要做一些操作，但我们暂时还没有写出这个操作来，所以我们就想：

“啊～如果这里有一个写好的函数就好了，我们直接调用这个函数，把请求传给它，它就把需要的 content 返回出来”

这个问题是不是很熟悉，解决方法呼之欲出 —— 和我们写 CourseTicker 的时候一样 —— **接口**！

来把 helloworld 里的代码改一改：

```go
...
textRequestBody := parseTextRequestBody(r)
if textRequestBody != nil {
    thisSer := textRequestBody.ToUserName
    reqUser := textRequestBody.FromUserName
    reqContent := textRequestBody.Content

    respContent := responser.Do(reqUser, reqContent)
    // 👆上面这行代码有个不知道哪来的 responser

    responseTextBody, err := makeTextResponseBody(thisSer, reqUser, respContent)
    _, err = fmt.Fprint(w, string(responseTextBody))

    ...
}
...
```

就是这样！我们希望有一个 `responser.Do(reqUser, reqContent)` ，调用它要返回的响应结果就出来了。所以，我们就写出这样的接口：

```go
type Responser interface {
	Do(reqUser string, reqContent string) (respContent string)
}
```

Ok，除了一个 responser，我们再来想想我们的 Helloworld 里跑起微信服务还需哪些东西。我们还有一个服务token（不是我们写了 holder 的那种 access_token 啊，是验证请求的 token）。

以 responser 和 token 为属性，helloworld 里那一大堆验证、消息解析/构造函数为私有方法，我们就可以写出微信服务框架“类”了，来看结构图：

![image-20200310113210047](https://tva1.sinaimg.cn/large/00831rSTgy1gcooc46z5lj310t0u00yf.jpg)

哈哈，这个东西也是说起来简单，实现起来一大堆东西挺吓人的。不过，这就是 helloworld 加了个 responser，写成了结构体，你细品。

> 【勘误】这里有个`databaseSource`属性，这显然不是一个通用的微信服务框架该有的，微信服务框架本身可不会去读写数据库，数据库操作应该是 Responser 的私事，这是我实现的错误。
>
> 事实上，好像我也没有在除了构造函数的地方使用这个`databaseSource`，所以它是没用的、应该删除掉的）

我们先不管实现，来看他的使用。

```go
func main() {
	WxToken := "wwwwwww"
	responser := NewSomething();
	databaseSource := "who:psd@where/database?charset=utf8";
    
	WxSer = wxPlatformServer.New(WxToken, responser, databaseSource)
    
	http.HandleFunc("/wx", WxSer.Handle)
	http.ListenAndServe(":80", nil)
}
```

这个用起来可以说是很方便的了。

##### 实现CourseNotifierResponser

现在，我们来实现一个具体的 Responser。我们的系统叫做 CoruseNotifier，所以这个系统的 Responser 就叫做 `CourseNotifierResponser` 好了。

这个`CourseNotifierResponser`应该要可以接受用户的消息，完成课程提醒的**订阅**、**退订**操作。

![image-20200310143818625](https://tva1.sinaimg.cn/large/00831rSTgy1gcotpt3g8cj30v209a0uh.jpg)

这个东西还是比较有意思的，我们来看工作流程图（我不擅长画这个，可能表达的不是很清晰）：

![Untitled Diagram-3](https://tva1.sinaimg.cn/large/00831rSTgy1gcow9pl2aqj30rt0dtjsl.jpg)

来解释一下，我们想考虑订阅、退订到底是个什么流程：

**订阅**课表首先是粗略判断用户输入是否合法，然后尝试拿用户的输入登录强智系统，如果登录成功，则返回真实姓名、系、课表以及一个验证码给用户，问他正不正确、要不要办。然后我们就等待用户返回验证码，如果这时接收到一条消息是之前的用户发的，同时内容是刚才那个验证码，就给他写入库，告诉他服务开好了。

**退订**也差不多这个流程：判断 -> 预操作 -> 验证码 -> 写库。

我把这个操作模式总结成三个方法：Verify、GenerateVerification、Continue。

还是以订阅为例，在 Verify 中，我们完成登录强智系统，如果登录成功，则返回真实姓名、系、课表的操作，然后返回一个 GenerateVerification 生成的验证码，然后这时，如果*接收到一条消息是之前的用户发*，然后就调用 Continue 检测验证码是否正确，是则完成数据库操作。

也就是说我们的操作流程为： `Verify() -> return GenerateVerification() -> Continue()`

既然订阅和退订的操作类似，我们就把它们相似的地方抽象出来，做成一个“虚拟类”，然后去继承实现它。

![Untitled Diagram](https://tva1.sinaimg.cn/large/00831rSTgy1gcovabfugbj31dw0ev143.jpg)

这里我们是真的要继承了！用 Go 实现虚拟类继承，我认为比较方便的一种方式是「结构体 + 接口」，我们来实现这样的一个结构体和一个接口作为“父类”：

```go
type CoursesSerSession struct {		// 结构体
	verification   string
	databaseSource string
}

func (s *CoursesSerSession) GenerateVerification() {
	randI := rand.New(rand.NewSource(time.Now().UnixNano())).Int31n(10000) // 4位随机数
	randS4 := fmt.Sprintf("%04v", randI)                                   // 4位随机数字字符串
	s.verification = randS4
}

type VerifySerSession interface {	// 接口
	GenerateVerification()
	Verify() string		// 虚方法，需要在“子类”中实现
	Continue(verificationCode string) string	// 虚方法，需要在“子类”中实现
}
```

然后去“继承”这个“父类”：

```go
type CoursesSubscribeSession struct {
	CoursesSerSession	// 继承结构体，同时也就继承了父类中实现的方法

	reqUser    string
	reqContent string

	qzClient     *qzclient.Client
}

func NewCoursesSubscribeSession(reqUser string, reqContent string, databaseSource string) *CoursesSubscribeSession {
	s := &CoursesSubscribeSession{reqUser: reqUser, reqContent: reqContent}
	s.CoursesSerSession.databaseSource = databaseSource	// 初始化父类
	return s
}

///////////////////////
// 下面实现接口中的方法 //
//////////////////////

// Verify 尝试拿用户请求中的信息登录强智系统，检测是否具有办理订阅课表的资格
func (s *CoursesSubscribeSession) Verify() string {
	// 尝试登录强智系统，如果登录成功，则返回真实姓名、系、课表
    // 出错就地返回
	s.GenerateVerification()
	return // 真实姓名、系、课表 和 验证码，提示用户继续操作
}

// Continue 为用户办理课程提醒登记，完成数据库操作
func (s *CoursesSubscribeSession) Continue(verificationCode string) string {
	// 完成数据库操作
}
```

退订是类似的，这里就不写了。

有了这个我们就可以继续实现 CourseNotifierResponser 了：

```go
type CourseNotifierResponser struct {
	sessionMap     map[string]VerifySerSession	// 这里是我们的“父类”里的接口
	databaseSource string
}

func NewCourseNotifierResponser(databaseSource string) *CourseNotifierResponser {
	c := &CourseNotifierResponser{databaseSource: databaseSource}
	c.sessionMap = make(map[string]VerifySerSession)
	return c
}

func (c CourseNotifierResponser) Do(reqUser string, reqContent string) (respContent string) {
	switch {
	case isReqSubscribe(reqContent):
		c.sessionMap[reqUser] = NewCoursesSubscribeSession(reqUser, reqContent, c.databaseSource)
		return c.sessionMap[reqUser].Verify()
	case isReqUnsubscribe(reqContent):
		c.sessionMap[reqUser] = NewCoursesUnsubscribeSession(reqUser, reqContent, c.databaseSource)
		return c.sessionMap[reqUser].Verify()
	case isReqVerification(reqContent):
		if c.sessionMap[reqUser] != nil {
			ret := c.sessionMap[reqUser].Continue(reqContent)
			c.sessionMap[reqUser] = nil
			return ret
		} else {
			return "无法处理的信息"
		}
	}
	return `欢迎、操作提示`
}

// isReqSubscribe 判断请求是否为**订阅**操作，是则返回 true，否则 false
func isReqSubscribe(reqContent string) bool {
	...
}

// isReqSubscribe 判断请求是否为**退订**操作，是则返回 true，否则 false
func isReqUnsubscribe(reqContent string) bool {
	...
}

// isReqVerification 判断请求是否为**验证码**，是则返回 true，否则 false
func isReqVerification(reqContent string) bool {
	...
}
```

不好意思，这一块变量名取太长了，看起来比较吃力。

总算好了，现在我们把这个系统的所有组件都完成了！我们可以从微信公众号前台服务获取处理用户订阅、退订操作，通过强智Client可以获取、保存课表，然后还有 CourseTicker 完成上课的提醒。

接下来我们只要把这些东西集成在一起，让他们有分工、有合作地工作起来，整个课程提醒系统就完成了！

### 集成

要让这些模块在一起工作，最直接的方式，就是在 main 函数里调用。但是，为了让系统的启动、配置、拓展更为方便，经过考虑，我设计了这样的一个 App “类”：

![Untitled Diagram-4](https://tva1.sinaimg.cn/large/00831rSTgy1gcowy32x5bj31lt0c64aj.jpg)

实例化这个 App 类后，其中的配置部分——AppConf 可以直接解析 JSON 配置文件获取配置；然后 App 类通过 init 和 run，按照配置文件的信息初始化并启动我们的各个运行组件。

这样完成一个 App 类之后，我们的 `main.go` 就可以很简洁了：

```go
package main

import (
	"example.com/CoursesNotifier/app"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

func main() {
	flag.Usage = usage
	// 读取命令行参数
	confFile := flag.String("c", "", "set configuration `file`")
	flag.Parse()

	if *confFile == "" {
		fmt.Fprintln(os.Stderr, "Cannot run without configuration file given.")
		flag.Usage()
		return
	}
	// 初始化 App
	coursesNotifier := app.New(*confFile)
	if err := coursesNotifier.Test(); err != nil {
		fmt.Println(err)
		fmt.Println("Cannot run app with error config.")
		return
	}
    // 运行 App
	coursesNotifier.Run()

	log.Println("CoursesNotifier Running...")

	http.HandleFunc("/", greet)
	http.ListenAndServe(":9001", nil)
}

func greet(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello World! %s", time.Now())
}

func usage() {
	fmt.Fprintf(os.Stderr, `
CoursesNotifier v0.1.0 for NCEPU(Baoding)
All rights reserved (c) 2020 CDFMLR

Usage: CoursesNotifier [-c filename]

Options:
`)
	flag.PrintDefaults()
}
```

我们的 main 完成了从获取命令行参数、初始化并启动app。我想这就是一个 main 函数的意义——程序的入口。

再来小结一下，这次我们从 main 函数开始，把自己当作这个课程提醒系统，看看自己从被管理员启动开始都在做些什么：

1. 管理员在服务器上敲下这行命令，启动服务：`nohup ./coursesNotifier -c ./config.json &`
2. `main` 函数启动，解析命令行参数，尝试读取配置文件，若不成功，则退出；
3. 初始化一个 App 对象，把配置文件传给这个 App 对象；
4. App 对象拿到配置文件，尝试将其中内容读取到自己的 conf 属性中；
5. 验证配置是否齐全，若没有问题，则初始化各运行时组件（全局微信access_token Holder，CourseTicker、微信前台服务）；若配置不足，无法启动，则先 main 函数返回错误，进而由 main 退出；
6. 配置、检测完成，main 函数调用 `app.Run()`，app 启动 CourseTicker、微信前台服务；
7. CourseTicker 定时检查有没有快开始上的课，有则通过微信通知系统通知要上课的学生。
8. 微信前台服务等待用户发送消息，为用户办理订阅、退订业务。

## 结尾

终于写完了！这篇文章可是花了不少时间的。我不认为有很多人可以看到这里，因为我清楚地知道自己的写作能力有限，可能许多地方都表述地不够清晰，不够吸引人。但是我希望每个看这篇文章的人都有所收获吧。Golang 每年都是程序猿们最想学习的技术之一（这是否意味着大家每年都并没有实际去学它😂），希望我这个东西可以给你学习 Go 增添一点乐趣。

除了这个系统本身的功能（我现在每天都在用），我自己写这个系统最大的收获是「Go 的面向对象」，我觉得还是很迷人的。Go 不是面向对象的语言，但我们也能用 Go 写出确实能解决问题、甚至还解决地比较优雅的 OOP 代码。

其实这个系统还有很多需要去完善、改进的地方，如果你感兴趣，欢迎参与这个系统的开发：[https://github.com/cdfmlr/CoursesNotifier](https://github.com/cdfmlr/CoursesNotifier)。

写完这么一个东西，我觉得自己大概勉强可能算是基本完成 Golang 入门了吧。Go 给我的感受还是很好的——我爱用 Go 编程，就像我爱 C 和 Python。

就这样吧，废话不多说了，还有代码要写呢！

**全文终**