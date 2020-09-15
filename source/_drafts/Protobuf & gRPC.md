---
date: 2020-09-15 14:54:19.363229
title: Protobuf & gRPC
---
# Protobuf & gRPC

## Protobuf

> [Protocol Buffers](https://developers.google.com/protocol-buffers) 是一种序列化数据结构的协议。对于透过管道或存储数据进行通信的程序开发上是很有用的。这个方法包含一个接口描述语言，描述一些数据结构，并提供程序工具根据这些描述产生代码，用于将这些数据结构产生或解析数据流。
>
> ——  [WikiPedia](https://zh.wikipedia.org/zh-cn/Protocol_Buffers)

总而言之， [Protocol Buffers](https://developers.google.com/protocol-buffers)，简称 Protobuf， 是一种数据描述语言（和 XML、JSON 这些类似）。Protobuf 配套的工具可以自动生成将各种语言中的数据结构序列化为 Protobuf 表示，然后反序列化到任意支持的语言中。

在 RPC 中，跨语言的数据编码、解码是个问题， Protobuf 是一种比较高效的解决方案。

### 安装



### 语法

我们把 Protocol Buffers 文档写在 `.proto` 文件中。

Protobuf 的注释还是我们熟悉的 C/C++ 风格：

```protobuf
// 这是注释
/* 这也是注释 */
```

#### 语法版本

`.proto` 的第一行会指明所用的语法版本，我们现在用的是 proto3 版本：

```protobuf
syntax = "proto3";
```

#### 导入

Protocol Buffers 文件也可以导入其他文件中的内容：

```protobuf
import "project/others.proto"
```

#### 包声明

Protocol Buffers 使用 `package` 关键字来声明包（可选）：

```protobuf
package foo.bar;
```

如果需要指定在不同语言中的名称，可以使用 `option`：

```protobuf
option java_package = "com.example.foo";
```

#### 消息

用 `message` 关键字来定义消息。消息，就是 RPC 中客户端给服务端穿的参数以及服务端给客户端返回的结果。使用 `message MsgName {...}` 的语法来声明：

```protobuf
message SongServerRequest {
	string song_name = 1;
}
```

Message 的名称一般用**驼峰命名**。message 的内容是一些个「字段」。

#### 字段

字段的格式为：

```protobuf
{repeated} <type> <field_name> = <fieldNumber> { [ fieldOptions ] };
```

> 这里花括号中的内容是可选的，尖括号中的内容是需要替换的，后面的 `[ fieldOptions ]` 方括号是protobuf 语法的一部分。

去掉所有可选部分，一个最基本的字段写作 `type field_name = fieldNumber`：

```protobuf
string song_name = 1;
```

- `type` 很好理解，就是字段的数据类型，后面会详细介绍。
- `field_name` 是字段名称，采用**下划线命名**。
- `fieldNumber` 是一个数字，字段的编号。

一个 message 的每个字段都要这个唯一编号。建议一次写好后永远也不要改这个编号，因为这个编号是用于以消息二进制格式标识字段的。需要注意一点是，最好把出现频繁的消息元素使用编号 1~15（只需一字节编码），更大的数字就需要更多空间了，可用的取值范围是 `[1, 19000) U (20000, 2^29)`（中间挖掉的是 protocol buffers 保留的 ）

#### 类型

protobuf 支持的基本类型有：

| 类型           | proto                  | 对应 go 类型         | 说明                                   |
| -------------- | ---------------------- | -------------------- | -------------------------------------- |
| 字节数组       | `bytes`                | `[]byte`             | 长度不超过 `2^32`                      |
| 字符串         | `string`               | `string`             |                                        |
| 布尔类型       | `bool`                 | `bool`               |                                        |
| 整数           | `int32`，`int64`       | `int32`，`int64`     | 变长编码，对负数编码效率低             |
| 无符号整数     | `uint32`，`uint64`     | `uint32`，`uint64`   | 变长编码                               |
| 有符号整数     | `sint32`，`sint64`     | `int32`，`int64`     | 变长编码，对负数编码比 `int32/64` 高效 |
| 定长整数       | `fixed32`，`fixed64`   | `int32`，`int64`     | 固定空间，定长编码，适合大数           |
| 定长有符号整数 | `sfixed32`，`sfixed64` | `int32`，`int64`     | 定长编码                               |
| 浮点数         | `float`，`double`      | `float32`，`float64` |                                        |

此外，还有几个复合类型：

**map**

`map` 是键值对类型：

```protobuf
map<string, int64> something = 1;
```

**enum**

```protobuf
enum EnumNotAllowingAlias {
  UNKNOWN2 = 0;
  STARTED2 = 1;
}
```

**reserved**

reserved 用来指明此 message 不使用（保留）某些字段。通过编码或字段名来设置保留：

```protobuf
message AllNormalypes {
  reserved 2, 4 to 6;
  reserved "field14", "field11";
  double field1 = 1;
  // float field2 = 2;
  int32 field3 = 3;
  // int64 field4 = 4;
  // uint32 field5 = 5;
  // uint64 field6 = 6;
  sint32 field7 = 7;
  sint64 field8 = 8;
  fixed32 field9 = 9;
  fixed64 field10 = 10;
  // sfixed32 field11 = 11;
  sfixed64 field12 = 12;
  bool field13 = 13;
  // string field14 = 14;
  bytes field15 = 15;
}
```

声明保留的字段就不能再定义，否则编译会出错。

**message**

一个 message 可以作为另一个 message 的字段出现：

```protobuf
message SomeOtherMessage {
  SearchResponse.Result result = 1;
  message Result {
    string url = 1;
    string title = 2;
    repeated string snippets = 3;
  }
}
```

#### 服务

我们常把 Proto Buffers  用在 RPC 里嘛，所以 Proto Buffers  是可以直接定义 RPC 服务接口的。

```protobuf
service SearchService {
  rpc Search (SearchRequest) returns (SearchResponse);
}
```

编译时 Proto Buffers 会根据选择的语言生成服务接口代码和存根（Stub）。

### 使用





