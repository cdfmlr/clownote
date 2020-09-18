---
date: 2020-09-09 22:26:38.909962
tags: Golang
title: Go RPC 远程过程调用
---
# Go RPC 远程过程调用

今天来学习 Go 语言的*远程过程调用* RPC（ Remote Procedure Call）。

> 在分布式计算，远程过程调用是一个计算机通信协议。该协议允许运行于一台计算机的程序调用另一个地址空间的子程序，而程序员就像调用本地程序一样，无需额外地为这个交互作用编程。RPC是一种服务器-客户端模式，经典实现是一个通过发送请求-接受回应进行信息交互的系统。
>
> From WikiPedia

RPC 可以让客户端相对直接地访问服务端的函数，这里说的「相对直接」表示我们不需要在服务端自己写一些比如 web 服务的东西来提供接口，并且在两端手动做各种数据的编码、解码。

本文包括两部分，第一部分介绍 Golang 标准库的 `net/rpc`，第二部分动手实现一个玩具版 PRC 框架来加深理解。

[TOC]

## Part0. net/rpc

> 这一部分参考 [《Go语言高级编程》4.1 RPC入门](https://chai2010.cn/advanced-go-programming-book/ch4-rpc/ch4-01-rpc-intro.html)。未尽之处可移步阅读原文。

Go 标准库的 `net/rpc` 实现了基本的 RPC，它使用一种 Go 语言特有的 Gob 编码方式，所以服务端、客户端都必须使用 Golang，不能跨语言调用。

对于服务端， `net/rpc` 要求用一个导出的结构体来表示 RPC 服务，这个结构体中所有符合特定要求的方法就是提供给客户端访问的：

```go
type T struct {}

func (t *T) MethodName(argType T1, replyType *T2) error
```

- 结构体是导出的。
- 方法是导出的。
- 方法有两个参数，都是导出的类型（或者内置类型）。
- 方法的第二个参数是指针。
- 方法的返回值是 error。

服务端通过 `rpc.Dial`（对 TCP 服务）连接服务端，然后用使用 Call 调用 RPC 服务中的方法：

```go
rpc.Call("T.MethodName", argType T1, replyType *T2)
```

例如，用 `net/rpc` 实现一个 Hello World。

### Hello World

**服务端**

首先构建一个 `HelloService` 来表示提供的服务：

```go
// server.go

// HelloService is a RPC service for helloWorld
type HelloService struct {}

// Hello say hello to request
func (p *HelloService) Hello(request string, reply *string) error {
	*reply = "Hello, " + request
	return nil
}
```

接下来注册并开启 RPC 服务，我们可以基于 HTTP 服务：

```go
// server.go

func main () {
    // 用将给客户端访问的名字和HelloService实例注册 RPC 服务
	rpc.RegisterName("HelloService", new(HelloService))

	// HTTP 服务
	rpc.HandleHTTP()
	err := http.ListenAndServe(":1234", nil)
	if err != nil {
		log.Fatal("Http Listen and Serve:", err)
	}
}
```

也可以使用 TCP 服务，替换上面的第 8～12 行代码：

```go
	// TCP 服务
	listener, err := net.Listen("tcp", ":1234")
	if err != nil {
		log.Fatal("ListenTCP error:", err)
	}

	conn, err := listener.Accept()
	if err != nil {
		log.Fatal("Accept error:", err)
	}

	rpc.ServeConn(conn)
```

注意，这里服务端只 Accept 一个请求，在客户端请求过后就会自动关闭。如果需要一直保持处理，可以把后半部分代码换成：

```go
    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Fatal("Accept error:", err)
        }

        go rpc.ServeConn(conn)
    }
```

**客户端**

```go
package main

import (
	"fmt"
	"log"
	"net/rpc"
)

func main() {
	// HTTP
	// client, err := rpc.DialHTTP("tcp", "localhost:1234")
	
    //TCP
	client, err := rpc.Dial("tcp", "localhost:1234")
	if err != nil {
		log.Fatal("dialing:", err)
	}

	var reply string
	err = client.Call("HelloService.Hello", "world", &reply)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(reply)
}
```

先启动服务端：

```sh
$ go run helloworld/server/server.go
```

在另一个终端调用客户端，即可得到结果：

```sh
$ go run helloworld/client/client.go
Hello, world
```

### 更规范的 RPC 接口

之前的代码服务端、客户端的注册、调用 RPC 服务都是写死的。所有的工作都放到了一块，相当不利于维护，需要考虑重构 HelloService 服务和客户端实现。

**服务端**

首先，用一个 interface 抽象服务接口：

```go
// HelloServiceName is the name of HelloService
const HelloServiceName = "HelloService"

// HelloServiceInterface is a interface for HelloService
type HelloServiceInterface interface {
	Hello(request string, reply *string) error
}

// RegisterHelloService register the RPC service on svc
func RegisterHelloService(svc HelloServiceInterface) error {
	return rpc.RegisterName(HelloServiceName, svc)
}
```

在实例化服务时，注册用：

```go
RegisterHelloService(new(HelloService))
```

其余的具体服务实现没有改变。

**客户端**

在客户端，考虑将 RPC 细节封装到一个客户端对象 `HelloServiceClient` 中：

```go
// HelloServiceClient is a client for HelloService
type HelloServiceClient struct {
	*rpc.Client
}

var _ HelloServiceInterface = (*HelloServiceClient)(nil)

// DialHelloService dial HelloService
func DialHelloService(network, address string) (*HelloServiceClient, error) {
	c, err := rpc.Dial(network, address)
	if err != nil {
		return nil , err
	}
	return &HelloServiceClient{Client: c}, nil
}

// Hello calls HelloService.Hello
func (p *HelloServiceClient) Hello(request string, reply *string) error {
	return p.Client.Call(HelloServiceName + ".Hello", request, reply)
}
```

具体调用时，就不用去暴露处理 RPC 的细节了：

```go
client, err := DialHelloService("tcp", "localhost:1234")
if err != nil {
    log.Fatal("dialing:", err)
}

var reply string
err = client.Hello("world", &reply)
if err != nil {
    log.Fatal(err)
}

fmt.Println(reply)
```

### 实例

运用上面的内容，做一个简单的计算器 RPC 服务。项目目录如下：

```
calc/
├── calcrpc.go
├── client
│   └── client.go
└── server
    ├── calc.go
    └── server.go
```

首先写一个 `calcrpc.go` 定义服务端/客户端通用的 RPC 接口：

```go
package calc

import "net/rpc"

// ServiceName 计算器服务名
const ServiceName = "CalcService"

// ServiceInterface 计算器服务接口
type ServiceInterface interface {
	// CalcTwoNumber 对两个数进行运算
	CalcTwoNumber(request Calc, reply *float64)  error
	// GetOperators 获取所有支持的运算
	GetOperators(request struct{}, reply *[]string)  error
}

// RegisterCalcService register the RPC service on svc
func RegisterCalcService(svc ServiceInterface) error {
	return rpc.RegisterName(ServiceName, svc)
}

// Calc 定义计算器对象，包括两个运算数
type Calc struct {
	Number1 float64
	Number2 float64
	Operator string
}
```

然后写服务端实现，在 `calc.go` 中写一个常规的计算器抽象实现：

```go
// 简单计算器实现

package main

import (
	"errors"
)

/* 抽象的计算函数类型 */

// Operation 是计算的抽象
type Operation func(Number1, Number2 float64) float64

/* 加减乘除的具体 Operation 实现 */

// Add 是加法的 Operation 实现
func Add(Number1, Number2 float64) float64 {
	return Number1 + Number2
}

// Sub 是减法的 Operation 实现
func Sub(Number1, Number2 float64) float64 {
	return Number1 - Number2
}

// Mul 是乘法的 Operation 实现
func Mul(Number1, Number2 float64) float64 {
	return Number1 * Number2
}

// Div 是除法的 Operation 实现
func Div(Number1, Number2 float64) float64 {
	return Number1 / Number2
}

/* 工厂 */

// Operators 注册所有支持的运算
var Operators = map[string]Operation {
	"+": Add,
	"-": Sub,
	"*": Mul,
	"/": Div,
}

// CreateOperation 通过 string 表示的 operator 获取适合的 Operation 函数
func CreateOperation(operator string) (Operation, error) {
	var oper Operation
	if oper, ok := Operators[operator]; ok {
		return oper, nil
	}
	return oper, errors.New("Illegal Operator")
}
```

接下来是 RPC 服务的实现，在 `server.go` 中：

```go
package main

import (
	"gorpctest/calc"
	"net/http"
	"net/rpc"
)

/* RPC 服务实现 */

// CalcService 是计算器 RPC 服务的实现
type CalcService struct{}

// CalcTwoNumber 对两个数进行加减乘除运算
func (c *CalcService) CalcTwoNumber(request calc.Calc, reply *float64) error {
	oper, err := CreateOperation(request.Operator)
	if err != nil {
		return err
	}
	*reply = oper(request.Number1, request.Number2)
	return nil
}

// GetOperators 获取所有支持的运算
func (c *CalcService) GetOperators(request struct{}, reply *[]string) error {
	opers := make([]string, 0, len(Operators))
	for key := range Operators {
		opers = append(opers, key)
	}
	*reply = opers
	return nil
}

/* 运行 RPC 服务 */

func main() {
	calc.RegisterCalcService(new(CalcService))
	rpc.HandleHTTP()
	http.ListenAndServe(":8080", nil)
}
```

然后是客户端实现，在 `client.go` 中：

```go
package main

import (
	"gorpctest/calc"
	"log"
	"net/rpc"
)

/* 定义客户端实现 */

// CalcClient is a client for CalcService
type CalcClient struct {
	*rpc.Client
}

var _ calc.ServiceInterface = (*CalcClient)(nil)

// DialCalcService dial CalcService
func DialCalcService(network, address string) (*CalcClient, error) {
	c, err := rpc.DialHTTP(network, address)
	if err != nil {
		return nil , err
	}
	return &CalcClient{Client: c}, nil
}

// CalcTwoNumber 对两个数进行运算
func (c *CalcClient) CalcTwoNumber(request calc.Calc, reply *float64)  error {
	return c.Client.Call(calc.ServiceName + ".CalcTwoNumber", request, reply)
}

// GetOperators 获取所有支持的运算
func (c *CalcClient) GetOperators(request struct{}, reply *[]string)  error {
	return c.Client.Call(calc.ServiceName + ".GetOperators", request, reply)
}

/* 使用客户端调用 RPC 服务 */

func main () {
	client, err := DialCalcService("tcp", "localhost:8080")
	if err != nil {
		log.Fatal("Err Dial Client:", err)
	}

    // Test GetOperators
	var opers []string
	err = client.GetOperators(struct{}{}, &opers)
	if err != nil {
		log.Println(err)
	}
	log.Println(opers)

    // Test CalcTwoNumber
	testAdd := calc.Calc {
		Number1: 2.0,
		Number2: 3.14,
		Operator: "+",
	}
	var result float64
	client.CalcTwoNumber(testAdd, &result)
	log.Println(result)
}
```

### net/rpc/jsonrpc

`net/rpc` 允许 RPC 数据打包时通过插件实现自定义的编码和解码：

```go
// 服务段的编码
rpc.ServeCodec(SomeServerCodec(conn)) // SomeServerCodec 是个编码器

// 客户端的解码
conn, _ := net.Dial("tcp", "localhost:1234")
client := rpc.NewClientWithCodec(SomeClientCodec(conn)) // SomeClientCodec 是个解码器
```

`net/rpc/jsonrpc` 就是这样的一种实现，它使用  JSON 而不是 Gob 编码，可以用来做跨语言 RPC。在真实的使用中，`net/rpc/jsonrpc` 在内部封装了上面提到的编码、解码实现，提供大致上和 `net/rpc` 相同的 API。

服务端在之前的 Hello World 基础上，只需要改动 main 的最后一行代码（不算 `}`）即可变为使用 JSON RPC：

```go
// Instead of `go rpc.ServeConn(conn)`
go jsonrpc.ServeConn(conn)
```

> `jsonrpc.ServeConn` 的实现是 `rpc.ServeCodec(jsonrpc.NewServerCodec(conn))`

在调用时，将 `DialHelloService` 中连接服务的代码改一改就可以使用了：

```go
// Instead of `c, err := rpc.Dial(network, address)`
c, err := jsonrpc.Dial(network, address)
```

> 这里也可以用：
>
> ```go
> conn, _ := net.Dial("tcp", "localhost:1234")
> client := rpc.NewClientWithCodec(jsonrpc.NewClientCodec(conn))
> ```

这样开的服务是基于 TCP 的。我们可以关闭服务端程序，运行 `nc -l 1234` 启动一个 TCP 服务，然后再次运行客户端程序，nc 会输出客户端请求的内容：

```sh
$ nc -l 1234
{"method":"HelloService.Hello","params":["world"],"id":0}
```

可以看到请求体是 JSON 数据。反过来，模仿这个请求体，我们可以手动向正在运行的客户端发送模拟请求，查看响应体：

```sh
$ echo -e '{"method":"HelloService.Hello","params":["JSON-RPC"],"id":1}' | nc localhost 1234
{"id":1,"result":"Hello, JSON-RPC","error":null}
```

总结一下，请求、响应的结构体大概为：

```go
type Request struct {
    Method string           `json:"method"`
    Params *json.RawMessage `json:"params"`
    Id     *json.RawMessage `json:"id"`
}

type Response struct {
    Id     uint64           `json:"id"`
    Result *json.RawMessage `json:"result"`
    Error  interface{}      `json:"error"`
}
```

（其实真正的实现中，客户端和服务端请求、响应定义是略有区别的）

使用其他语言，只要遵循这样的请求/响应结构，就可以和 Go 的 RPC 服务进行通信了。

### JSON-RPC in HTTP

刚才的实现是基于 TCP 的，有时候不方便使用，我们可能更希望使用熟悉的 HTTP 协议。

`net/rpc` 的 RPC 服务是建立在抽象的 `io.ReadWriteCloser` 接口之上的（conn），所以略作改变，就可以将 RPC 架设在不同的通讯协议之上。这里我们将尝试将 `net/rpc/jsonrpc` 架设到 HTTP 服务上：

```go
func main() {
	RegisterHelloService(new(HelloService))

	// HTTP 服务
	http.HandleFunc("/jsonrpc", func(w http.ResponseWriter, r *http.Request) {
		var conn io.ReadWriteCloser = struct {
			io.Writer
			io.ReadCloser
		} {
			ReadCloser: r.Body,
			Writer: w,
		}

		rpc.ServeRequest(jsonrpc.NewServerCodec(conn))
	})

	http.ListenAndServe(":1234", nil)
}
```

然后就可以通过 HTTP 很方便地从不同的语言中访问 RPC 服务了：

```sh
curl -X POST http://localhost:1234/jsonrpc  --data '{"method":"HelloService.Hello","params":["world"],"id":0}'
{"id":0,"result":"Hello, world","error":null}
```

但是，这里有个问题是，不方便使用 Go 写客户端，你需要自己去构建一个客户端实现，来完成请求的编码、发送以及响应的解码、绑定😂。或者，也可以使用一个 JSON-RPC 的库。

## Part1. 简单 RPC 的实现

> 这一部分参考 [《从0开始学习微服务框架》 P9~P14  RPC](https://www.bilibili.com/video/BV137411H7t9?p=9)。未尽之处可移步学习原视频。

为了加深理解，我们手写一个简单的 RPC 服务，从自定义协议到编码、解码，再到 RPC 服务端、客户端实现。

我们写一个 `package rpc` 来实现这东西：

```
/rpc
├── client.go
├── codec.go
├── server.go
└── session.go
(省略了测试文件)
```

### 网络通信

我们基于 TCP 通信，使用如下自定义的协议进行通信：

| **网络字节流**| Header                  | Data     |
| -------- | ----------------------- | -------- |
|大小 | `uint32`（定长：4字节） | `[]byte`（长度由Header指明） |
| 说明| Data 的长度信息         | 具体数据 |

我们通过一个 `Session` 结构体实现这个基本的协议：

```go
// session.go PART 0

// Session 是 RPC 通信的一个会话连接
type Session struct {
	conn net.Conn
}

// NewSession 从网络连接新建一个 Session
func NewSession(conn net.Conn) *Session {
	return &Session{conn: conn}
}
```

之后的 RPC 通信就通过 `Session`  来对 TCP 连接进行数据读写操作：

```go
// session.go PART 1

// Write 向 Session 中写数据
func (s *Session) Write(data []byte) error {
	buf := make([]byte, 4+len(data))
	// Header
	binary.BigEndian.PutUint32(buf[:4], uint32(len(data)))
	// Data
	copy(buf[4:], data)

	_, err := s.conn.Write(buf)

	return err
}

// Read 从 Session 中读数据
func (s *Session) Read() ([]byte, error) {
	// 读取 Header，获取 Data 长度信息
	header := make([]byte, 4)
	if _, err := io.ReadFull(s.conn, header); err != nil {
		return nil, err
	}
	dataLen := binary.BigEndian.Uint32(header)

	// 按照 dataLen 读取 Data
	data := make([]byte, dataLen)
	if _, err := io.ReadFull(s.conn, data); err != nil {
		return nil, err
	}
	return data, nil
}
```

### 编码解码

在 RPC 的过程中，我们需要按照一定的格式传递函数的参数与结果。我们可以定义如下 `RPCData` 来格式化 RPC 通信的内容：

```go
// codec.go PART 0

// RPCData 定义 RPC 通信的数据格式
type RPCData struct {
	Func string        // 访问的函数
	Args []interface{} // 函数的参数
}
```

在整个 RPC 中，所有网络通信都利用 `Session` 对 `RPCData` 编码成的 `[]byte` 进行传输。要把 `RPCData` 在一端编码成字节，并在另一端解码会原本的 Go 数据类型，可以利用 `encoding/gob`：

```go
// codec.go PART 1

// encode 将 RPCData 编码
func encode(data RPCData) ([]byte, error) {
	var buf bytes.Buffer
	encoder := gob.NewEncoder(&buf)
	if err := encoder.Encode(data); err != nil {
		return nil, err
	}
	return buf.Bytes(), nil
}

// decode 将数据解码为 RPCData
func decode(data []byte) (RPCData, error) {
	buf := bytes.NewBuffer(data)
	decoder := gob.NewDecoder(buf)

	var rpcData RPCData
	err := decoder.Decode(&rpcData)
	return rpcData, err
}
```

有了网络通信的方案以及编码解码的方式，就可以开始构建 RPC 服务的服务端框架以及客户端实现了。

### 服务端

RPC 服务端的核心是，维护一个函数名到本地函数的映射。实现这个映射，并开启一个网络服务，就可以支持客户端通过给定函数名和参数即可调用服务端函数的操作了。

这里可以简单地把服务定义如下：

```go
// server.go PART 0

// Server 是简单的 RPC 服务
type Server struct {
	funcs map[string]reflect.Value
}

func NewServer() *Server {
	return &Server{funcs: map[string]reflect.Value{}}
}
```

通过反射机制，来实现 funs 的映射：

```go
// server.go PART 1

// Register 注册绑定要 RPC 服务的函数
// 将函数名与函数对应起来
func (s *Server) Register(name string, function interface{}) {
	// 已存在则跳过
	if _, ok := s.funcs[name]; ok {
		return
	}
	fVal := reflect.ValueOf(function)
	s.funcs[name] = fVal
}
```

接下来是开启网络服务，监听  TCP 连接，对访问进行服务：

```go
// server.go PART 2

// ListenAndServe 监听 address，运行 RPC 服务
func (s *Server) ListenAndServe(address string) error {
	listener, err := net.Listen("tcp", address)
	if err != nil {
		return err
	}
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("accept error:", err)
			continue
		}
		s.handleConn(conn)
	}
}
```

具体对连接的处理在 `handleConn` 中完成。对 conn 创建一个 RPC 会话，解码请求体，得到客户端希望请求的函数和参数。调用本地函数完成工作，将返回值编码，返回给客户端：

```go
// server.go PART 3

// handleConn 处理 RPC 服务的 conn 请求
func (s *Server) handleConn(conn net.Conn) {
	// 创建会话
	srvSession := NewSession(conn)

	// 读取、解码数据
	data, err := srvSession.Read()
	if err != nil {
		log.Println("session read error:", err)
		return
	}
	requestRPCData, err := decode(data)
	if err != nil {
		log.Println("data decode error:", err)
		return
	}

	// 获取函数
	f, ok := s.funcs[requestRPCData.Func]
	if !ok {
		log.Printf("unexpected rpc call: function %s not exist", requestRPCData.Func)
		return
	}

	// 获取参数
	inArgs := make([]reflect.Value, 0, len(requestRPCData.Args))
	for _, arg := range requestRPCData.Args {
		inArgs = append(inArgs, reflect.ValueOf(arg))
	}

	// 反射调用方法
	returnValues := f.Call(inArgs)

	// 构造结果
	outArgs := make([]interface{}, 0, len(returnValues))
	for _, ret := range returnValues {
		outArgs = append(outArgs, ret.Interface())
	}
	replyRPCData := RPCData{
		Func: requestRPCData.Func,
		Args: outArgs,
	}
	replyEncoded, err := encode(replyRPCData)
	if err != nil {
		log.Println("reply encode error:", err)
		return
	}

	// 写入结果
	err = srvSession.Write(replyEncoded)
	if err != nil {
		log.Println("reply write error:", err)
	}
}
```

### 客户端

RPC 客户端的一个特点是，像调用本地函数一样去调用远程的函数。要调用的函数并不是在本地实现的，但我们希望让它像本地函数一样工作。反射机制可以提供这种“欺骗自己”的特性。

首先我们写出客户端结构，其实就是对一个网络连接的包装：

```go
// client.go PART 0

// Client 是 RPC 的客户端
type Client struct {
	conn net.Conn
}

func NewClient(conn net.Conn) *Client {
	return &Client{conn: conn}
}
```

然后实现一个 `Call` 方法，把原创的函数通过 RPC 带到本地来：

```go
// client.go PART 1

func (c *Client) Call(name string, funcPtr interface{}) {
	// 反射初始化 funcPtr 函数原型
	fn := reflect.ValueOf(funcPtr).Elem()
    
    // RPC 调用远程的函数
	f := func(args []reflect.Value) []reflect.Value {
		// 参数
		inArgs := make([]interface{}, 0, len(args))
		for _, arg := range args {
			inArgs = append(inArgs, arg.Interface())
		}
        
		// 连接服务
		cliSession := NewSession(c.conn)

		// 请求
		requestRPCData := RPCData{
			Func: name,
			Args: inArgs,
		}
		requestEncoded, err := encode(requestRPCData)
		if err != nil {
			panic(err)
		}
		if err := cliSession.Write(requestEncoded); err != nil {
			panic(err)
		}

		// 响应
		response, err := cliSession.Read()
		if err != nil {
			panic(err)
		}
		respRPCData, err := decode(response)
		if err != nil {
			panic(err)
		}
		outArgs := make([]reflect.Value, 0, len(respRPCData.Args))
		for i, arg := range respRPCData.Args {
			if arg == nil {
				outArgs = append(outArgs, reflect.Zero(fn.Type().Out(i)))
			} else {
				outArgs = append(outArgs, reflect.ValueOf(arg))
			}
		}
        
        // 返回远程函数的返回值
		return outArgs
	}

	// 将 RPC 调用函数赋给 fn
	v := reflect.MakeFunc(fn.Type(), f)
	fn.Set(v)
}
```

这个函数接受两个参数，`name` 为 RPC 服务端提供的函数名，`funcPtr` 是要调用的函数的原型。该函数运行的结果是将一个「封装了 RPC 调用远程函数的函数」“赋给” `funcPtr`，让 `funcPtr` 从一个空有其表的原型变成一个可调用的真实函数，调用它就等于通过 RPC 调用服务端相应的函数。

例如，我们在服务端实现并注册了函数：

```go
func queryUser(uid int) (User, error) {
	... // queryUser 的具体实现
}
```

在客户端，我们就可以通过一个 queryUser 函数的原型来获得其能力：

```go
var query func(int) (User, error) // query 是 queryUser 的原型
client.Call("queryUser", &query) // “拿到”远程的 queryUser 函数
u, err := query(1) // 像调用本地函数一样去使用来自远程的函数
```

如果对反射不太熟悉，难以理解代码实现的话，这里可能有点迷。再来看一个具体调用的例子吧：

```go
// rpc_test.go
package rpc

import (
	"encoding/gob"
	"fmt"
	"net"
	"testing"
)

// User  测试用的用户结构体
type User struct {
	Name string
	Age  int
}

// queryUser 模拟查询用户的方法
func queryUser(uid int) (User, error) {
	// Fake data
	user := make(map[int]User)
	user[0] = User{Name: "Foo", Age: 12}
	user[1] = User{Name: "Bar", Age: 13}
	user[2] = User{Name: "Joe", Age: 14}

	// Fake query
	if u, ok := user[uid]; ok {
		return u, nil
	}
	return User{}, fmt.Errorf("user wiht id %d is not exist", uid)
}

func TestRPC(t *testing.T) {
	gob.Register(User{}) // gob 编码要注册一下才能编码结构体

	addr := ":8080"

	// 服务端
	srv := NewServer()
	srv.Register("queryUser", queryUser)
	go srv.ListenAndServe(addr)

	// 客户端
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		t.Error(err)
	}
	cli := NewClient(conn)
	var query func(int) (User, error)
	cli.Call("queryUser", &query)

	u, err := query(1)
	if err != nil {
		t.Error(err)
	}
	fmt.Println(u)
}
```

`TestRPC` 中模拟了服务端以及客户端调用 RPC 服务。

至此，一个完整的玩具版 RPC 就完成了，自己来写这东西还是挺有意思。完整的代码我放到了这个 Gist 里 [cdfmlr/toy-rpc-golang](https://gist.github.com/cdfmlr/a1e275959eb06e5335fcafb7285eb82f)：

- https://gist.github.com/cdfmlr/a1e275959eb06e5335fcafb7285eb82f

<script src="https://gist.github.com/cdfmlr/a1e275959eb06e5335fcafb7285eb82f.js"></script>

---

```go
By("CDFMLR", "2020-09-12")
// See you.💪
```

