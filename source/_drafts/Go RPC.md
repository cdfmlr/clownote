---
date: 2020-09-09 22:26:38.909962
title: Go RPC
---
# Go RPC

## net/rpc

RPC 可以让客户端相对直接地访问服务端的函数，这里说的「相对直接」表示我们不需要在服务端自己写一些比如 web 服务的东西来提供接口，并且在两端手动做各种数据的编码、解码。

Go 标准库的 `net/rpc` 要求用一个导出的结构体来表示 RPC 服务，这个结构体中所有符合特定要求的方法就是提供给客户端访问的：

```go
type T struct {}

func (t *T) MethodName(argType T1, replyType *T2) error
```

- 结构体是导出的。

- 方法是导出的。

- 方法有两个参数，都是导出的类型（或者内置类型）。

- 方法的第二个参数是指针。

- 方法的返回值是 error。

例如，用 `net/rpc` 实现一个 Hello World。

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

**客户端**

服务端 通过 `rpc.DialHTTP`（对 HTTP 服务） `rpc.Dial`（对 TCP 服务）连接服务端，然后用 `rpc.Call("T.MethodName", argType T1, replyType *T2)` 调用具体的 RPC 方法：

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



