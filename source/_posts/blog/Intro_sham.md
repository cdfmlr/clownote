---
date: 2020-11-16 19:22:07.677319
title: Introducing Sham
---
# Introducing: Sham

1024那天写了篇的文章《[Python 代码一键转流程图](https://blog.csdn.net/u012419550/article/details/109258117)》。CSDN 居然给了个 “最趣味”奖🏆：https://blogdev.blog.csdn.net/article/details/109536460 。

一开始我是不知道获奖的事的，（害，咱想都不敢想），直到有一天， CSDN 的小姐姐主动来加我微信，怒斥我仍未填写收货地址[捂脸]。。。

经历了一些曲折，前两天我终于还是收到了 CSDN 的奖品：

![截屏2020-11-16 21.49.18](https://tva1.sinaimg.cn/large/0081Kckwly1gkrcr94smgj30vm0u0kjo.jpg)

感谢 CSDN 🙏。

不过，这不是今天的主题，~~只是炫耀一下~~。今天要讲的故事是：

**我这个人不懂什么操作系统，于是我用 Go 语言模拟出了一个......**

## 起因

以前看过一篇文章叫做《[我这个人不懂什么CPU，于是我用代码模拟出了一个](https://mp.weixin.qq.com/s/eezs6MTL-quuG0q5jBoMyw)》。这篇文章介绍了一位大佬一言不合用 Go 语言模拟了一台计算机（项目：[djhworld/simple-computer](https://github.com/djhworld/simple-computer)）的故事，帅爆了好吗。

这学期有操作系统课，上这个课程的主要收获就是，课上那些活在 PPT 中的算法，就很迷！我是不太喜欢这种方式的，我奉行 *Talk is cheap. Show me the code.*

所以，我也用 Go 语言模拟了一个“操作系统”——一个拥有标准输入输出与进程间通信的、基于时间片轮转调度的多道程序运行器：[cdfmlr/sham](https://github.com/cdfmlr/sham) （sham 意为：骗局、虚假事物）。

取名叫做 sham 就是希望大家原谅我的标题党行为，事实上，这个东西远谈不上一个“操作系统”，和 [djhworld/simple-computer](https://github.com/djhworld/simple-computer) 等类似的优秀项目比起来，，我做的什么都不是。但我只做了不到 10 分钟的设计，并用不到 2k 行代码实现了它。作为业余蒟蒻实现的玩具项目，你还能对它有什么更高的要求呢？

下面，介绍 Sham 系统。

## Sham 系统概述

在这里，简要介绍系统中的一些关键设计思路。

至于具体的实现，事实上，这个项目非常简单，而且我写了不少注释，在 git commit message 中也留下了（在我看来）较为详细的说明，如果您不介意，完全可以去读一读源码：

- [https://github.com/cdfmlr/sham](https://github.com/cdfmlr/sham)
- 备份：[https://gitee.com/cdfmlr/sham](https://gitee.com/cdfmlr/sham)

当然，如果你喜欢这个项目，欢迎 Star、Fork、Watch 三连。如果有任何疑问、意见或建议，也欢迎 Issue 和 PR。

### 抽象结构

这个模拟的操作系统中，主要包含以下抽象：

- CPU：一个带有互斥锁的结构，单独在一个协程中运行应用程序的线程。
- 内存：一个无限大的结构，不需要管理。
- IO设备：一个独立的设备，单独在一个协程中运行，可以输入或输出。
- 操作系统：包括操作系统基础结构、调度器、系统调用、中断处理程序组。为例简化模型，操作系统单独运行在一个协程中，它本身不需要在 CPU、内存上运行，而是在内部持有 CPU 和内存。
  - 操作系统基础结构：持有并管理 CPU，内存、IO 设备、进程表和中断向量。
  - 调度器：完成进程调度工作的具体算法。
  - 系统调用：为应用程序提供的“内核态”操作接口。
  - 中断处理程序：处理应用程序或操作系统内部发出的各类中断。
- 进程、线程：为了简化模型，一个进程只能持有且必须持有一个线程。
  - 进程：包括一个可运行的进程、当前状态（运行、就绪、阻塞）以及需要的各种资源（内存等）。
  - 线程：进程具体可执行的部分，包含要运行的“程序代码”以及运行时的上下文。
  - 上下文：包括程序计数器、进程指针、操作系统接口。
- 具体应用程序：进程的实例（在 [sham_test.go](./sham_test.go) 中实现了一些有意思的应用）。

目前的实现中，调度器使用的是一个带时间片轮转的 FCFS 调度器，但可以十分容易地添加、替换新的调度算法。

### 系统的工作流程

![截屏2020-11-13 19.58.42](https://tva1.sinaimg.cn/large/0081Kckwly1gknstu9g88j31e00u0dkx.jpg)

### 线程的运行

关于线程的运行，直接看一部分 Thread 具体代码实现：

```go
// Thread 线程：是一个可以在 CPU 里跑的东西。
type Thread struct {
	// runnable 是实际要运行的内容
	runnable Runnable
	// contextual 是 Thread 的环境
	contextual *Contextual
}

// Runnable 程序：应用程序的具体的代码就写在这里面
// 每一次返回就代表“一条指令”（一个原子操作）执行完毕，返回值为状态：
//  - StatusRunning 继续运行（如果时间片未用尽）
//  - StatusReady 会进入就绪队列（即 yield，主动让出 CPU）
//  - StatusBlocked 会进入阻塞状态（一般不用。需要阻塞时一般通过中断请求）
//  - StatusDone 进程运行结束。
type Runnable func(contextual *Contextual) int

// 进程的状态
const (
	StatusBlocked = -1
	StatusReady   = 0
	StatusRunning = 1
	StatusDone    = 2
)

// Contextual 上下文：线程的上下文。
type Contextual struct {
    // 指向 Process 的指针，可以取用 Process 的资源
	Process *Process
	// 通过 Contextual.OS.XX 调系统调用
	OS OSInterface
	// 程序计数器
	PC uint
}
```

具体的应用程序把“代码”写在一个 Runnable 型的函数中，这个函数每执行完一个原子操作就应该返回一次。同时 runnable 也可以在执行完任何一个原子操作时，被外部事件强行打断（比如时间片用尽）。

 `Thread.Run()`  实现了上述控制，runnable 的返回、外部的打断都会被 `Thread.Run()` 捕获。前面的流程图中，「CPU 运行线程」也就是调用 `Thread.Run()` 方法：

```go
// Run 包装并运行 Thread 的 runnable。
// 该函数返回的 done、cancel 让 runnable 变得可控：
// - 当 runnable 返回，即 Thread 结束时，done 会接收到 Process/Thread 的状态。
// - 当外部需要强制终止 runnable 的运行（调度），调用 cancel() 即可。
func (t *Thread) Run() (done chan int, cancel context.CancelFunc) {
	done = make(chan int)

	_ctx, cancel := context.WithCancel(context.Background())

	go func() {
		for { // 一条条代码不停跑，直到阻塞｜退出｜被取消
			select {
			case <-_ctx.Done(): // 被取消，取消由 CPU 发起
                // 取消时 CPU 会临时置 Status 为需要转到的状态，
				// 这里获取并把这个值传给操作系统
				// 同时把状态重置为 StatusRunning
                //（状态转化需由操作系统完成，这里只是暂时借用这个值，故要还原）
				s := t.contextual.Process.Status
				t.contextual.Process.Status = StatusRunning
				done <- s
				return
			default:
				ret := t.runnable(t.contextual)
                t.contextual.Commit()  // PC++, clockTick()
				if ret != StatusRunning { // 结束|阻塞|就绪，交给调度器处理
					done <- ret
					return
				}
			}
		}
	}()

	return done, cancel
}
```

这里使用 go 语言标准库的 context 包，控制线程运行的取消（外部打断）。如果没有外部打断，runnable 返回时就会将程序计数器和时钟加一。如果 runnable 一直返回 StatusRunning 就可以一直运行下去。在 runnable 内部，通过 `contextual.PC` 以及例如 `switch` 的流程控制语句即可实现一条条代码执行的效果。

例如，下面的这个 Runnable 函数（程序）有 4 个操作（4 条指令）它们会依次执行：

```go
func processSeq(contextual *Contextual) int {
    switch contextual.PC {
    case 0:
        log.Debug("Line 0")
        return StatusRunning
    case 1:
        log.Debug("Line 1")
        return StatusRunning
    case 2:
        log.Debug("Line 2")
        return StatusRunning
    case 3:
        return StatusDone
    }
    return StatusDone
}
```

这样的写法有些像汇编语言，而事实上，runnable 甚至就是这个模拟的操作系统的机器语言！所以写起来略为繁琐，这个难以避免。

运行的效果如下：

![截屏2020-11-13 11.21.54](https://tva1.sinaimg.cn/large/0081Kckwly1gkndrmwyhcj31hm09sn1b.jpg)

**注**：把上面的程序翻译成我们平时的 Go 程序就是：

```c
func processSeq() int {
    log.Debug("Line 0")
	log.Debug("Line 1")
	log.Debug("Line 2")
    return StatusDone
}
```

### 中断与 IO

中断在操作系统中至关重要，所以这个模拟的操作系统也需要中断的实现。

这里对中断的建模如下：

```go
type Interrupt struct {
	Typ     string
	Handler InterruptHandler
	Data    InterruptData
}

// InterruptHandler 是「中断处理程序」
type InterruptHandler func(os *OS, data InterruptData)

// InterruptData 是中断的数据
type InterruptData struct {
	Pid string
	// Channel 是用来给中断发起程序与中断处理程序通信的信道。
	Channel chan interface{}
}
```

中断包含一个类型，处理程序（处理程序和中断类型一一对应），以及附加的数据。

应用程序，或操作系统内部都可以通过一个**系统调用**发出中断（这个模拟中几乎没有硬件，所以不考虑硬件中断）。操作系统受到中断请求，会把中断放入一个中断表，然后在当前时钟周期结束后，调度运行时程序阻塞，依次调用相应中断处理程序处理中断表里的中断。

中断处理程序会做必要的工作，完成后解除发起进程的阻塞状态。

有了这个中断机制，就可以很容易地实现时间片轮转——在时间片用尽后，发出一个时钟中断，其处理程序会把进程就绪。

同时，中断支持了各种 IO 设备的使用。例如，最简单的是使用标准输出，发出一个标准输出的中断请求，传入需要的数据即可：

```go
func helloWorld(contextual *Contextual) int {
    ch := make(chan interface{}, 1)
    ch <- "Hello, world!"
    contextual.OS.InterruptRequest(contextual.Process.Thread, 
                                   StdOutInterrupt, ch)
    return StatusDone
}
```

这个中断的处理程序会使用标准输出设备，完成输出。运行结果：

![截屏2020-11-13 11.18.57](https://tva1.sinaimg.cn/large/0081Kckwly1gkndndoqc4j31jc0dk7au.jpg)

出了标准输入，我还实现了标准输出设备，以及特殊的 Pipe 设备。这两个东西的调用代码都比较复杂，在此不做演示。

标准输入、输出都是模拟的“硬件”，这些东西会单独在一个协程中运行。而 Pipe 设备则是一个虚拟的设备，它是对 Go 语言 channel 的封装。操作系统可以动态生成任意多个 Pipe 并分配给需要的进程，通过 Pipe 进程之间就可以利用 CSP 模型可以完成通信与同步。

利用 Pipe 设备，在这个模拟的操作系统中，可以实现「生产者-消费者」问题。代码稍微复杂（需要约 150 行代码，见 [sham_test.go](./sham_test.go) 之 TestProducerConsumer），但完全可以正确工作：

![截屏2020-11-13 12.07.16](https://tva1.sinaimg.cn/large/0081Kckwly1gknf17o30tj31jj0u0hbm.jpg)

 ## Sham 程序设计

作为系统可用性的~~不严谨~~证明，下面给出一份 Sham 程序设计指南。

在 Sham 源码的 [sham_test.go](https://github.com/cdfmlr/sham/blob/master/sham_test.go) 文件中，包含了一系列开发过程中测试使用的应用程序实现。我们完全可以把这个文章看作 Sham 程序设计的官方实例。下文中任何不明朗部分都请参考那些实例。

### 如何运行 Sham?

```go
shamOS := NewOS()
shamOS.Scheduler = FCFSScheduler{}
// shamOS.ReadyProcs = []*Process{} // No Noop

shamOS.CreateProcess(...)
shamOS.CreateProcess(...)
...

shamOS.Boot()
```

获取一个 OS 实例，指定调度器（FCFSScheduler 是先来先服务算法），添加应用程序进程，然后 Boot 就开始运行了！

系统的就绪队列中默认有一个 Noop（NO OPeration）进程，这个进程什么也不做。如果不需要，可以参考被注释掉的第三行代码删除它。

调用 `shamOS.CreateProcess` 可以给系统中新建进程，新的进程会被正确初始化，并放入就绪队列等待运行：

```go
func (os *OS) CreateProcess(pid string, precedence uint, timeCost uint, runnable Runnable)
```

precedence 和 timeCost 是给留特定的调度算法使用的，如果使用 FCFSScheduler 就没什么用，随便写即可，runnable 就是具体的程序代码了，下面就介绍 runnable 的写法。

### 顺序程序

```go
func processSeq(contextual *Contextual) int {
    switch contextual.PC {
    case 0:
        log.Debug("Line 0")
        return StatusRunning
    case 1:
        log.Debug("Line 1")
        return StatusRunning
    case 2:
        log.Debug("Line 2")
        return StatusRunning
    case 3:
        return StatusDone
    }
    return StatusDone
}
```

借助 `switch contextual.PC` 和 `return StatusRunning` 一个时钟执行一个操作。当程序结束时，`return StatusDone`。

注：这里是调用了 log（github.com/sirupsen/logrus，打一条日志），这其实是个「超系统调用」，调用了 sham 以外的东西。作为测试，这没问题。

### 系统调用

如果你对刚才的「超系统调用」感觉不爽，那没关系，下面就介绍 Sham 的系统调用。其实之前我们使用的 `CreateProcess` 就是一个系统调用：

- `CreateProcess(pid string, precedence uint, timeCost uint, runnable Runnable)`

```go
shamOS.CreateProcess("processFoo", 10, 1, func(contextual *Contextual) int {
    contextual.OS.CreateProcess("ProcessBar", 10, 0, func(contextual *Contextual) int {
        fmt.Println("ProcessBar, a Process dynamic created by processFoo")
        return StatusDone
    })
    return StatusDone
})
```

我们使用 `contextual.OS.XXX` 完成系统调用。这里 processFoo 调用 `CreateProcess` 新建了一个进程 ProcessBar。 

还有一个更有用的系统调用——中断请求：

- `InterruptRequest(thread *Thread, typ string, channel chan interface{})`

thread 是发起中断的进程，一般是当前线程自己： `contextual.Process.Thread` ，typ 是要调用的中断类型，channel 是当前线程与中断处理程序直接通信的。

由于当前线程与中断处理程序显然不同步，channel 必须是带缓冲区的！

```go
func helloWorld(contextual *Contextual) int {
    ch := make(chan interface{}, 1)
    ch <- "Hello, world!"
    contextual.OS.InterruptRequest(contextual.Process.Thread, 
                                   StdOutInterrupt, ch)
    return StatusDone
}
```

目前可用的中断类型有：

| typ                | 说明               | channel                           |
| ------------------ | ------------------ | --------------------------------- |
| `StdOutInterrupt`  | 输出到标准输出     | 放入药输出的东西                  |
| `StdInInterrupt`   | 从标准输入获取输入 | 一个空 chan，标准输入会写东西进去 |
| `NewPipeInterrupt` | 新建一个 Pipe 设备 | 放入 pipeID 和 pipeBufferSize     |
| `GetPipeInterrupt` | 获取一个 Pipe 设备 | 放入 pipeID                       |

关于 Pipe 后面再详细介绍。

使用标准输入时，需要注意，把 chan 放到 sham 线程的内存中，而不是使用一个 go 变量：

```go
shamOS.CreateProcess("processIn", 10, 1, func(contextual *Contextual) int {
    mem := &contextual.Process.Memory[0]

    switch contextual.PC {
    case 0:
        in := make(chan interface{}, 1)
        // in 会在多个周期中被使用，需要放入内存
        mem.Content = map[string]chan interface{}{"in": in}
        contextual.OS.InterruptRequest(contextual.Process.Thread, 
                                       StdInInterrupt, in)
        return StatusRunning
    case 1:
        in := mem.Content.(map[string]chan interface{})["in"]

        content := <-in
        log.WithField("content", content).Debug("got content")

        return StatusDone
    }

    return StatusDone
})
```

### 变量使用

程序中当然是需要使用变量的。但从刚才的标准输出程序可以看到，使用 sham 的内存极为麻烦！而那些从内存读写变量的操作非常套路化，所以我封装了一个 `VarPool` 来方便变量读写：

```go
contextual.InitVarPool()  // 初始化变量池
contextual.SetVar("varName", something)  // 放入（新建或更新）变量
something := contextual.GetVar("varName")  // 读取变量，如果不存在会得到 nil
something, ok := contextual.TryGetVar("varName")  // 读取变量，ok指使变量是否存在
```

E.g.

```go
shamOS.CreateProcess("useVarPool", 1, 1, func(contextual *Contextual) int {
    switch {
    case contextual.PC == 0:
        contextual.InitVarPool()
        
        contextual.SetVar("chOutput", make(chan interface{}, 1))

        return StatusRunning
    case contextual.PC <= 3:
        contextual.SetVar("num", contextual.PC*contextual.PC)

        chOut := contextual.GetVar("chOutput").(chan interface{})
        
        chOut <- fmt.Sprintln(contextual.GetVar("num"), chOut)
        contextual.OS.InterruptRequest(contextual.Process.Thread, StdOutInterrupt, chOut)

        return StatusRunning
    }
    return StatusDone
})
```

### 条件/循环

条件、循环这里做的不太好，比较麻烦。需要大家手动维护额外的程序计数器：

```go
const PipeProduct = "pipe_product"

shamOS.CreateProcess("producer", 10, 100, func(contextual *Contextual) int {
    switch contextual.PC {
    case 0:
        contextual.InitVarPool()
        contextual.SetVar("chOutput", make(chan interface{}, 1))

        return StatusRunning
    case 1:
        pipeArgs := make(chan interface{}, 2)
        pipeArgs <- PipeProduct // pipeId
        pipeArgs <- 3           // pipeBufferSize
        contextual.OS.InterruptRequest(contextual.Process.Thread, 
                                       NewPipeInterrupt, pipeArgs)

        return StatusRunning
    default:
        if contextual.PC > 30 {
            return StatusDone
        }

        _, ok := contextual.TryGetVar("dpc")
        if !ok {
            contextual.SetVar("dpc", 0)
        }
        dpc := contextual.GetVar("dpc").(int)

        switch dpc {
        case 0:
            product := contextual.PC

            contextual.SetVar("product", product)

            contextual.SetVar("dpc", 1)
            return StatusRunning
        default:
            pipe := interface{}(
                contextual.Process.Devices[PipeProduct]).(*Pipe)

            if pipe.Inputable() {
                product := contextual.GetVar("product")

                pipe.Input() <- product

                contextual.SetVar("dpc", 0)
            } else {
                return StatusReady // yield
            }
        }

        return StatusRunning
    }
})
```

这段代码是生产者消费者问题中的生产者线程，我们通过一个 `dpc` 变量实现了类似于 `JMP` 指令的跳转功能。

这段代码中关于 Pipe 不太好理解，所以下面介绍 Pipe。

### 进程通信: Pipe

Pipe 是 Sham 中的一种特殊 IO 设备，它是对 Golang chan 的封装，它提供了 Sham 进程间通信的能力。

创建 Pipe：

```go
pipeArgs := make(chan interface{}, 2)
pipeArgs <- "pipeID"  // pipeId
pipeArgs <- 3         // pipeBufferSize
contextual.OS.InterruptRequest(contextual.Process.Thread, 
                               NewPipeInterrupt, pipeArgs)
```

其他进程获取 Pipe：

```go
pipeArgs := make(chan interface{}, 2)
pipeArgs <- "pipeID" // pipeId

contextual.OS.InterruptRequest(contextual.Process.Thread, 
                               GetPipeInterrupt, pipeArgs)
```

`NewPipeInterrupt` 和 `GetPipeInterrupt` 中断请求被成功处理之后，操作系统会把新建的/获取到的 Pipe 分配给进程，通过 contextual 可以获取：`contextual.Process.Devices["pipeID"]`。我们会获取到一个 Device 类型的东西，为了具体使用时方便，我们需要把它转化为 *Pipe 类型：

```go
pipe := interface{}(contextual.Process.Devices[PipeProduct]).(*Pipe)
```

在读写 Pipe 的时候需要注意边界条件，不可读时强行去读会造成死锁。

写：在 `pipe.Inputable()` 时 `pipe.Input() <- something`，否则说明阻塞，主动让出 CPU：

```go
if pipe.Inputable() {
    pipe.Input() <- contextual.GetVar("product")
} else {
    return StatusReady // yield
}
```

读也是类似的，检测—读取—否则让出 CPU：

```go
if pipe.Outputable() {
    contextual.SetVar("product", <-pipe.Output())
} else {
    return StatusReady // yield
}
```

## 文章结束之前

无论您是技术比我强的大佬，或是在某一方面比我稍弱的同学，看到这里可能都会骂一声——“什么东西？”

为了回答您的疑问，我想重述我对 Sham 的定义：

> [cdfmlr/sham](https://github.com/cdfmlr/sham) （sham 意为：骗局、虚假事物）：一个拥有标准输入输出与进程间通信的、基于时间片轮转调度的多道程序运行器。

这是我在学习操作系统时的个人娱乐作品。它的功能、整体设计、代码细节都做的很差，因为它最初的设计，仅是为了开玩笑写出的 200 余个字符：

![截屏2020-11-16 21.23.28](https://tva1.sinaimg.cn/large/0081Kckwly1gkrbyvn0lkj30u0145gx2.jpg)

如果您喜欢这个项目，欢迎 Star、Fork 和 PR。如果您不喜欢这东西，或有任何看法、疑问、意见或建议，也欢迎 Issue，望不吝赐教为感！

---

```go
shamOS := NewOS()
shamOS.Scheduler = FCFSScheduler{}
shamOS.ReadyProcs = []*Process{}

shamOS.CreateProcess("SeeYou", 0, 0, func(contextual *Contextual) int {
    eof := make(chan interface{}, 1)
    eof <- "By CDFMLR \n 2020.11.16"
    contextual.OS.InterruptRequest(contextual.Process.Thread, 
                                   StdOutInterrupt, eof)
    return StatusDone
})

shamOS.Boot()
```

