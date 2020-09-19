---
date: 2020-09-19 21:14:24.249358
tags: Python
title: Python gRPC 与跨语言 gRPC 调用
---
# Python gRPC 与跨语言 gRPC 调用

本文是我上一篇文章《 [Go 微服务基础：Protobuf & gRPC](https://blog.csdn.net/u012419550/article/details/108672965)》的延伸，在开始本文前，建议先看一看那篇文章。

在《 [Go 微服务基础：Protobuf & gRPC](https://blog.csdn.net/u012419550/article/details/108672965)》一文中，我们介绍了 protobuf 的基础。随后定义了一个 userinfo proto 作为接口，实现了一套 Golang 版本的服务端、客户端。

这篇文章中，我们继续使用那个 userinfo proto 作为接口，去实现一套 Python 版本的服务端、客户端，在实例中入门 Python gRPC 使用。然后，我们做一个有意思的尝试 —— Golang 与 Python 版本客户端、服务端的跨语言调用。

[TOC]

## Python gRPC 入门

首先，我们了解一下如何配置 Python 的 gRPC 环境，如何把 proto 文件编译出 Python 接口，如何实现服务端、客户端。

### 安装 gRPC Python

安装 gRPC Python 组件：

```sh
pip3 install grpcio
pip3 install grpcio-tools
```

### 编写 proto 生成接口

编写 proto 文件，这里我们直接复制《 [Go 微服务基础：Protobuf & gRPC](https://blog.csdn.net/u012419550/article/details/108672965)》一文中的 proto：

```protobuf
syntax = "proto3";

package proto;

// 用户信息请求参数
message UserRequest {
  string name = 1;
}

// 用户信息请求响应
message UserResponse {
  int32 id = 1;
  string name = 2;
  int32 age = 3;
  repeated string hobby = 4;
}

// 用户信息接口
service UserInfo {
  // 获取用户信息，请求参数为 UserRequest，返回响应为 UserResponse
  rpc GetUserInfo (UserRequest) returns (UserResponse) {}
}
```

编译。注意是使用 `grpc_tools.protoc` 这个 Python 专用的编译器，而不是使用 `protoc` 哦：

```sh
python3 -m grpc_tools.protoc  -I . --python_out=. --grpc_python_out=. ./userinfo.proto
```

会生成两个文件：

- `userinfo_pb2.py`：请求、响应数据结构的定义的类：（proto 文件中的 message）
  - `UserRequest`
  - `UserResponse`
- `userinfo_pb2_grpc.py`：服务端、客户端的定义的类：（proto 文件中的 service）
  - `UserInfoServicer`：服务端
  - `UserInfoStub`：客户端

> 注：这里文件名里的 `pb2` 和 protobuf 语法的版本（`syntax = "proto3"`）没关系。这个 pb2 只是表示是用的 Protocol Buffers Python API 版本为 2。

### 服务端实现

查看 `userinfo_pb2_grpc.py` 里生成的代码可以知道，Python gRPC 的服务实现是写一个子类去继承 proto 编译生成的 `userinfo_pb2_grpc.UserInfoServicer` ，在子类中实现 RPC 的具体服务处理方法。

```python
from concurrent import futures

import grpc

import userinfo_pb2
import userinfo_pb2_grpc


class UserInfoServicer(userinfo_pb2_grpc.UserInfoServicer):
    """UserInfoServicer 具体实现 userinfo_pb2_grpc.UserInfoServicer，处理 RPC 服务
    """

    def GetUserInfo(self, request, context):
        """获取用户信息，请求参数为 UserRequest，返回响应为 UserResponse
        """
        name = request.name

        # Fake query
        if name == "foo":
            return userinfo_pb2.UserResponse(id=1, name="foo", age=12, hobby=["eating", "sleep"])
        raise KeyError(f"unknown user: name = {name}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    userinfo_pb2_grpc.add_UserInfoServicer_to_server(UserInfoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
```

### 客户端实现

客户端很好理解，网络连接得到一个 channel，拿 channel 去实例化一个 stub，通过 stub 调用 RPC 函数。

```python
import grpc

import userinfo_pb2
import userinfo_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = userinfo_pb2_grpc.UserInfoStub(channel)

        req = userinfo_pb2.UserRequest(name="foo")
        resp = stub.GetUserInfo(req)

        print(resp)
        print(type(resp.name), type(resp.id))
        print(type(resp.hobby), resp.hobby, list(resp.hobby))


if __name__ == "__main__":
    run()
```

### 运行测试

先运行服务端：

```sh
$ python3 server.py
```

如果运行 `python3 sever.py` 有如下报错：

```python
AttributeError: module 'google.protobuf.descriptor' has no attribute '_internal_create_key'
```

看一下 `protoc --version` 和 `pip3 show protobuf`。我这里的问题是 pip 的 protobuf 太老了，更新一下就行：

```sh
$ pip3 install -upgrade protobuf -i https://pypi.tuna.tsinghua.edu.cn/simple
```

再运行客户端：

```sh
# Another terminal
$ python3 client.py
id: 1
name: "foo"
age: 12
hobby: "eating"
hobby: "sleep"

<class 'str'> <class 'int'>
<class 'google.protobuf.pyext._message.RepeatedScalarContainer'> ['eating', 'sleep'] ['eating', 'sleep']
```

可以看到，响应返回的 UserResponse 里都是一般的数据格式，但 repeat 的数据并不是我们熟悉的 list 什么的，但可以手动转过去。

如果我们请求一个 name 非 `"foo"` 的调用，服务端的处理是 `raise KeyError(f"unknown user: name = {name}")`，这里客户端就会抛出一个错误：

```python
>>> import grpc
>>> import userinfo_pb2
>>> import userinfo_pb2_grpc
>>> channel = grpc.insecure_channel('localhost:50051')
>>> stub = userinfo_pb2_grpc.UserInfoStub(channel)
>>> req = userinfo_pb2.UserRequest(name="bar")
>>> resp = stub.GetUserInfo(req)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3/site-packages/grpc/_channel.py", line 826, in __call__
    return _end_unary_response_blocking(state, call, False, None)
  File "/usr/local/lib/python3/site-packages/grpc/_channel.py", line 729, in _end_unary_response_blocking
    raise _InactiveRpcError(state)
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNKNOWN
        details = "Exception calling application: 'unknown user: name = bar'"
        debug_error_string = "{"created":"@1600520567.121816000","description":"Error received from peer ipv6:[::1]:50051","file":"src/core/lib/surface/call.cc","file_line":1062,"grpc_message":"Exception calling application: 'unknown user: name = bar'","grpc_status":2}"
```

## 跨语言 gRPC

一直说 gRPC 跨语言，但我们一直跑的服务端、客户端同一种语言的。我们已经学习了 Golang 和 Python 两种语言的 gRPC，现在尝试跨语言去调用它们。

事实上，使用一样的 proto 作为基础，即使服务端和客户端使用不同语言实现，不用做任何处理就可以互相调用。

例如，我们刚才用 Python 实现的 gRPC 服务端、客户端，和上一篇文章《 [Go 微服务基础：Protobuf & gRPC](https://blog.csdn.net/u012419550/article/details/108672965)》中用 Go 语言实现的 gRPC 服务端、客户端，都是基于同一个 proto 文件的。

那么，我们不用动任何具体代码就可以随意组合使用 Golang、Python 的服务端和客户端。

### Python 调用 Golang

第一个尝试是 Python 客户端调用 Golang 实现的服务端。

使用上一篇文章《 [Go 微服务基础：Protobuf & gRPC](https://blog.csdn.net/u012419550/article/details/108672965)》中实现的 `server/main.go`  作为服务端，使用本文前面部分实现的 userinfo 的 `client.py` 作为客户端。

服务端一行代码都不改，直接跑起来：

```sh
$ go run server/main.go
```

把 `client.py` 中的端口改成匹配服务端的：

```python
def run():
    with grpc.insecure_channel('localhost:8080') as channel:
        ...
```

运行客户端：

```sh
$ python3 /Users/c/Desktop/grpcpy/client.py
id: 1
name: "foo"
age: 12
hobby: "eating"
hobby: "sleep"
```

跨语言调用成功，一切正确！

如果你尝试错误调用，得到的是和刚才使用 Python 服务端相同的错误。 

### Golang 调用 Python

反过来，使用 Golang 调用 Python。

除了协调一下端口，还是不需要做任何改动！直接跑起来：

```sh
$ python3 server.py
```

```sh
$ go run client/main.go
resp: &proto.UserResponse{state:impl.MessageState{NoUnkeyedLiterals:pragma.NoUnkeyedLiterals{}, DoNotCompare:pragma.DoNotCompare{}, DoNotCopy:pragma.DoNotCopy{}, atomicMessageInfo:(*impl.MessageInfo)(0xc000186638)}, sizeCache:0, unknownFields:[]uint8(nil), Id:1, Name:"foo", Age:12, Hobby:[]string{"eating", "sleep"}}
```

调用成功。

---

这种跨语言调用简单地似乎有些不可思议，但这种强大的简单正是我们使用 gRPC 的理由。

# 写在最后：蒟蒻的抱怨

又到了这个叫人受不了的季节！

蒟蒻在被褥中蜷缩着、颤抖着。耳机中淡淡的老歌化身利刃，夺心而入，又化身飓风，翻起片片凌乱的回忆。三分美好、七分苦涩从蒟蒻眼前飘过。

不知道是迷离的梦境还是草淡的现实中，蒟蒻再也受不了这心痛的季节、痛苦的歌曲和苦难的回忆。抱起刻满年岁的老吉他。调弦，变调，轻轻奏响。

一样的琴谱，一样的孤独，不停地重复又重复，弹出了新感触——

它呜咽的声响，是内心的旋律，是遗忘的节奏，是回忆的季节，是即将到来的——雪藏更多回忆的冬天。

---

```python
by("CDFMLR", "2020-09-19")
# See you.🎸
```