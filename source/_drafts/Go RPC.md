---
date: 2020-09-09 22:26:38.909962
title: Go RPC
---
# Go RPC

RPC 可以让客户端相对直接地访问服务端的函数，这里说的「相对直接」表示我们不需要在服务端自己写一些比如 web 服务的东西来提供接口，并且在两端手动做各种数据的编码、解码。

## net/rpc

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
const HelloServiceName = "path/to/pkg.HelloService"

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

## net/rpc/jsonrpc

`net/rpc/jsonrpc` 大致上和 `net/rpc` 相同，但是使用 JSON 而不是 Gob 编码，可以跨语言服务。

服务端在之前的 Hello World 基础上，只需要改动 main 的最后一行代码（不算 `}`）即可变为使用 JSON RPC：

```go
// Instead of `go rpc.ServeConn(conn)`
go rpc.ServeCodec(jsonrpc.NewServerCodec(conn))
```





。。。

Go语言的RPC框架有两个比较有特色的设计：一个是RPC数据打包时可以通过插件实现自定义的编码和解码；另一个是RPC建立在抽象的io.ReadWriteCloser接口之上的，我们可以将RPC架设在不同的通讯协议之上。这里我们将尝试通过官方自带的net/rpc/jsonrpc扩展实现一个跨语言的RPC。