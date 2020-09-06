---
date: 2020-09-03 22:50:28.321135
tags:
- Web
- Golang
title: Gin入门
---
# Gin 入门

用 Go 好久了，也写了好几个小 Web 服务，基本都是在用标准库的 `net/http` + `database/sql`，其实开发难度、性能都还不错啦。写的多了还是觉得用标准库有些部分代码重复性还是很高的，慢慢地自己总结出一些通用的“框架”，但不成熟，问题很多。所以开始学一些成熟的框架，之前我开始用 Gorm 简化数据库这方面的流程，这次是考虑学一个 Web 框架啦—— Gin 足够简洁，使用的也比较广泛，所以就它了。

## 安装

1. 下载安装 Gin 包：

```sh
$ go get -u github.com/gin-gonic/gin
```

2. 在代码中导入：

```go
import "github.com/gin-gonic/gin"
```

3. (可选)如果要使用诸如 `http.StatusOK` 的常量，还要导入 `net/http`

```go
import "net/http"
```

## 起步

首先，创建一个文件 `example.go`，接下来的代码就写在这个文件里：

```sh
$ touch example.go
```

编辑文件，写代码：

```go
package main

import "github.com/gin-gonic/gin"

func main() {
	r := gin.Default() // r 是 router 的意思
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r.Run() // listen and serve on 0.0.0.0:8080
}
```

运行它：

```sh
$ go run example.go
```

然后就可以在浏览器里访问 ` 0.0.0.0:8080/ping` 了。可以看到返回的 pong，以及终端输出的精美日志。

---

在这个 Ping-Pong 程序里，我们使用 `gin.Default` 来生成一个框架的实例（称为 Engine）。Default 生成的 Engine 里包括了默认的 Logger 和 Recovery 中间件。Engine “继承”了 RouterGroup，所以可以直接往里面添加路由：

`r.GET('/url', handlerFunc)` 声明一个路由。GET 访问 URL 触发 handlerFunc 函数，这个函数（属于函数类型`type HandlerFunc func(*Context)`）响应请求，这里用`c.JSON` 返回一个 `application/json`  的响应。

`r.Run()` 让 Engine 跑起来，默认的服务地址是 `:8080`，可以用 `r.Run(":9999")` 来自定义。

## 路由

Ping-Pong 程序的例子里，已经展现了固定路径、无参数的 GET 请求路由。除了 `r.GET`，还可以在 `r.` 后面使用 `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS` 以及 `Any` 来添加各种请求类型的路由。

### 路径参数

路径参数可以实现动态路由。

- `/user/:name` 匹配 `/user/xxx`

例如，我们希望对不同的用户访问 `/user/foo`、`/user/bar`。则可以使用：

```go
r.GET("/user/:name", func(c *gin.Context) {
    name := c.Param("name")
    c.String(http.StatusOK, "Hello, %s", name)
})
```

结果：

```sh
$ curl 0.0.0.0:8080/user/foobar
Hello, foobar
$ curl 0.0.0.0:8080/user/foobar/
<a href="/user/foobar">Moved Permanently</a>.
$ curl 0.0.0.0:8080/user/
404 page not found
```

- `/user/:name/*action`  匹配 `/user/xxx/` 以及 `/user/xxx/yyy/...`;

要匹配 `/user/:name/...`，使用如下玩法：

```go
r.GET("/user/:name/*action", func(c *gin.Context) {
    name := c.Param("name")
    action := c.Param("action")
    message := name + " is " + action
    c.String(http.StatusOK, message)
})
```

测试：

```sh
$ curl 0.0.0.0:8080/user/foobar/
foobar is /
$ curl 0.0.0.0:8080/user/foobar/doing/something
foobar is /doing/something
```

> P.S. For each matched request Context will hold the route 
>
> ```go
> router.POST("/user/:name/*action", func(c *gin.Context) {
>         c.FullPath() == "/user/:name/*action" // true
> })
> ```

### 重定向

- 外部的重定向，使用 Redirect 通知浏览器去重定向：

```go
// GET 用 301 Moved Permanently
r.GET("/tobaidu", func(c *gin.Context) {
    c.Redirect(http.StatusMovedPermanently, "https://www.baidu.com")
})
// POST 用 302 Found
r.POST("toping", func(c *gin.Context) {
    c.Redirect(http.StatusFound, "/ping")
})
```

结果：

```sh
$ curl -i '0.0.0.0:8080/tobaidu'
HTTP/1.1 301 Moved Permanently
Content-Type: text/html; charset=utf-8
Location: https://www.baidu.com
Date: Fri, 04 Sep 2020 13:23:35 GMT
Content-Length: 56

<a href="https://www.baidu.com">Moved Permanently</a>.
```

```sh
$ curl -i '0.0.0.0:8080/toping' -X POST
HTTP/1.1 302 Found
Location: /ping
Date: Fri, 04 Sep 2020 13:23:56 GMT
Content-Length: 0
```

- 内部的重定向，把请求的 Path 硬改了然后重新处理：

```go
r.GET("/test", func(c *gin.Context) {
    c.Request.URL.Path = "/test2"
    r.HandleContext(c)
})
r.GET("/test2", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{"hello": "world"})
})
```

结果：

```sh
$ curl -i '0.0.0.0:8080/test'
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Fri, 04 Sep 2020 13:24:41 GMT
Content-Length: 17

{"hello":"world"}
```

### 路由分组

```go
defaultHandler := func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "endpoint": c.FullPath(),
    })
}

v1 := r.Group("/v1")
{
    v1.GET("/hello", defaultHandler)
    v1.POST("/login", defaultHandler)
}

v2 := r.Group("/v2")
{
    v2.GET("/hello", defaultHandler)
    v2.POST("/login", defaultHandler)
}
```

> P.S. 这里的大括号是代表把其中的内容看作一个单独的语句块（独立的作用域）。

Gin 会自动给分组的路由变成 `/v1/...` 这样的：

```
GET    /v1/hello
POST   /v1/login
GET    /v2/hello
POST   /v2/login
```

调用测试：

```sh
$ curl '0.0.0.0:8080/v1/hello'
{"endpoint":"/v1/hello"}
$ curl -X POST '0.0.0.0:8080/v2/login'
{"endpoint":"/v2/login"}
```



## 请求内容

### Querystring 参数

GET 请求中，我们常用 Querystring 即 `http://example.com/welcome?firstname=Jane&lastname=Doe` 的这种查询方式。

使用 `context.Query()` 来获取参数：

```go
r.GET("/welcome", func(c *gin.Context) {
    firstname := c.DefaultQuery("firstname", "Guest")
    lastname := c.Query("lastname")
    // shortcut for c.Request.URL.Query().Get("lastname")
    c.String(http.StatusOK, "Hello, %s %s", firstname, lastname)
})
```

结果：

```sh
$ curl '0.0.0.0:8080/welcome?firstname=Jane'
Hello, Jane 
$ curl '0.0.0.0:8080/welcome?lastname=Doe'
Hello, Guest Doe
$ curl '0.0.0.0:8080/welcome?firstname=Jane&lastname=Doe'
Hello, Jane Doe
```

### POST Form 参数

对于 POST 等请求方式，我们常用 Multipart/Urlencoded Form 来传递参数信息。

```go
r.POST("/form_post", func(c *gin.Context) {
    message := c.PostForm("message")
    nick := c.DefaultPostForm("nick", "anonymous")

    c.JSON(200, gin.H{
        "status":  "posted",
        "message": message,
        "nick":    nick,
    })
})
```

结果：

```sh
$ curl '0.0.0.0:8080/form_post' -X POST
{"message":"","nick":"anonymous","status":"posted"}
$ curl '0.0.0.0:8080/form_post' -X POST -d 'message=hello&nick=Foobar'
{"message":"hello","nick":"Foobar","status":"posted"}
```

### Map 作为参数

对于使用 Map 作为参数的情况，如：

```
POST /post?ids[a]=1234&ids[b]=hello HTTP/1.1
Content-Type: application/x-www-form-urlencoded

names[first]=thinkerou&names[second]=tianou
```

使用 `QueryMap` 和 `PostFormMap` 来获取：

```go
r.POST("/post", func(c *gin.Context){
    ids := c.QueryMap("ids")
    names := c.PostFormMap("names")
    c.String(http.StatusOK, "ids: %v; names: %v",  ids, names)
})
```

结果：

```sh
$ curl -g 'http://0.0.0.0:8080/post?ids[a]=1234&ids[b]=hello' -X POST -d 'names[first]=thinkerou&names[second]=tianou'
ids: map[a:1234 b:hello]; names: map[first:thinkerou second:tianou]
```

### 上传文件

在上传文件的时候，如果需要，可以设置一个较低的 multipart forms 内存限制（默认是 32 MiB）。

注意，这个只是限制在上传时程序可以使用的内存，并不是限制上传文件的大小！See [Stackoverflow: gin web framework limit upload file size not working](https://stackoverflow.com/questions/56143325/gin-web-framework-limit-upload-file-size-not-working).

```go
r := gin.Default()
r.MaxMultipartMemory = 8 << 20  // 8 MiB
```

#### 单个文件

```go
r.POST("/upload/single", func(c *gin.Context) {
    file, err := c.FormFile("file")
    if err != nil {
        c.String(http.StatusBadRequest, "get form err: %s")
        return
    }
    filename := filepath.Base(file.Filename)

    if err := c.SaveUploadedFile(file, filepath.Join("./upload", filename)); err != nil {
        c.String(http.StatusBadRequest, "upload file err: %s", err.Error())
        return
    }

    c.String(http.StatusOK, "File %s uploaded successfully", filename)
})
```

⚠️注意，不要直接用 `file.Filename`，详见 [Gin Issue #1693](https://github.com/gin-gonic/gin/issues/1693)。

使用 curl 测试：

```sh
$ curl -X POST '0.0.0.0:8080/upload/single' \
	-F "file=@/Users/c/Desktop/test.png" \
	-H "Content-Type: multipart/form-data"
File test.png uploaded successfully
```

#### 多个文件

```go
r.POST("/upload/multiple", func(c *gin.Context) {
    form, _ := c.MultipartForm()
    files := form.File["upload[]"]

    for _, file := range files {
        filename := filepath.Base(file.Filename)
        c.SaveUploadedFile(file, filepath.Join("./upload", filename))
        log.Println("upload: ", filename)
    }
    c.String(http.StatusOK, "%d files uploaded!", len(files))
})
```

异常处理参考“单个文件”部分的代码，这里略了。

测试：

```sh
$ curl '0.0.0.0:8080/upload/multiple' -X POST \
	-F "upload[]=@/Users/c/Desktop/test1.png" \
	-F "upload[]=@/Users/c/Desktop/test2.png" \
	-H "Content-Type: multipart/form-data"
2 files uploaded!
```

## 响应渲染

### JSON, XML, YAML

前面我们已经用过好几次 JSON 了。XML、YAML 和 JSON 很类似，调用对应的方法，传入状态码以及结果信息的结构体即可写入响应：

- JSON：`func (c *Context) JSON(code int, obj interface{})`
- XML：`func (c *Context) XML(code int, obj interface{})`
- YAML：`func (c *Context) YAML(code int, obj interface{})`

对于一般简单的内容，可以使用 `gin.H` 来表示数据。`gin.H` 是 ` map[string]interface{}` 的简写。

```go
r.GET("/someJSON", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
})

r.GET("/someXML", func(c *gin.Context) {
    c.XML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
})

r.GET("/someYAML", func(c *gin.Context) {
    c.YAML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
})
```

对于复杂的情况，也可以使用 `struct` 。

```go
r.GET("/moreJSON", func(c *gin.Context) {
    var msg struct {
        Name    string `json:"user"`
        Message string
        Number  int
    }
    msg.Name = "Lena"
    msg.Message = "hey"
    msg.Number = 123
    // Note that msg.Name becomes "user" in the JSON
    // Will output  :   {"user": "Lena", "Message": "hey", "Number": 123}
    c.JSON(http.StatusOK, msg)
})
```

对于 JSON，Gin 还提供各种需求的 [SecureJSON](https://github.com/gin-gonic/gin#securejson)，[JSONP](https://github.com/gin-gonic/gin#jsonp)，[AsciiJSON](https://github.com/gin-gonic/gin#asciijson)，[PureJSON](https://github.com/gin-gonic/gin#purejson)。

### ProtoBuf

Gin 还可以直接渲染 ProtoBuf：

```go
r.GET("/someProtoBuf", func(c *gin.Context) {
    reps := []int64{int64(1), int64(2)}
    label := "test"
    // The specific definition of protobuf is written in the testdata/protoexample file.
    data := &protoexample.Test{
        Label: &label,
        Reps:  reps,
    }
    // Note that data becomes binary data in the response
    // Will output protoexample.Test protobuf serialized data
    c.ProtoBuf(http.StatusOK, data)
})
```

### HTML

读取模版 HTML 文件：

-  `func (engine *Engine) LoadHTMLGlob(pattern string)`
- `func (engine *Engine) LoadHTMLFiles(files ...string)`

渲染 HTML，写入响应：

- `func (c *Context) HTML(code int, name string, obj interface{})` 其中 name 是模版文件路径，obj 是要填充的数据。

默认渲染用的是和标准库一样的模版，详见 [text/template](https://golang.org/pkg/text/template/) 和 [html/template](https://golang.org/pkg/html/template/)。

E.g.

```go
func main() {
	router := gin.Default()
	router.LoadHTMLGlob("templates/*")
	//router.LoadHTMLFiles("templates/template1.html", "templates/template2.html")
	router.GET("/index", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.tmpl", gin.H{
			"title": "Main website",
		})
	})
	router.Run(":8080")
}
```

`templates/index.tmpl`:

```html
<html>
	<h1>
		{{ .title }}
	</h1>
</html>
```

还有好多高级用法，我不太用这东西，去看文档吧：[gin#html-rendering](https://github.com/gin-gonic/gin#html-rendering)。

## 文件服务

### 静态文件服务

Serving static files

```go
func main() {
	router := gin.Default()
    
	router.Static("/assets", "./assets")
	router.StaticFS("/more_static", http.Dir("my_file_system"))
	router.StaticFile("/favicon.ico", "./resources/favicon.ico")

	router.Run(":8080")
}
```

- `Static(relativePath, root string)`：在 root 路径处开静态文件服务。
- `StaticFS(relativePath string, fs http.FileSystem)`：类似 `Static()`，但可以用 `http.FileSystem`。
- `StaticFile(relativePath, filepath string)`：注册服务单个文件。

### 文件数据服务

Serving data from file，就是把文件写入响应啦。

```go
func main() {
	router := gin.Default()

	router.GET("/local/file", func(c *gin.Context) {
		c.File("local/file.go")
	})

	var fs http.FileSystem = // ...
	router.GET("/fs/file", func(c *gin.Context) {
		c.FileFromFS("fs/file.go", fs)
	})
}
```

### 用 Reader 数据响应

```go
func main() {
	router := gin.Default()
	router.GET("/someDataFromReader", func(c *gin.Context) {
		response, err := http.Get("https://raw.githubusercontent.com/gin-gonic/logo/master/color.png")
		if err != nil || response.StatusCode != http.StatusOK {
			c.Status(http.StatusServiceUnavailable)
			return
		}

		reader := response.Body
		contentLength := response.ContentLength
		contentType := response.Header.Get("Content-Type")

		extraHeaders := map[string]string{
			"Content-Disposition": `attachment; filename="gopher.png"`,
		}

		c.DataFromReader(http.StatusOK, contentLength, contentType, reader, extraHeaders)
	})
	router.Run(":8080")
}
```

## 模型绑定

日常的开发中，把请求体中的内容放到一个结构体里，并验证给的信息是否完整是很常用的功能。Gin 提供模型绑定(model binding)来完成这一功能。模型绑定可以把 Form 值、JSON、XML、YAML 形式的数据绑定到 Go 的结构体。

Gin 提供两套绑定的方法：`Bind` 和 `ShouldBind`。`Bind` 在绑定出错时把 400 aborted 写入响应（`c.AbortWithError(400, err).SetType(ErrorTypeBind)`）。`ShouldBind` 在绑定失败时返回一个错误，我们需要手动去处理错误。

```go
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type Login struct {
	User string `form:"user" json:"user" xml:"user" binding:"required"`
	Password string `form:"password" json:"password" xml:"password" binding:"required"`
}

func main() {
	router := gin.Default()

	// Example for binding JSON:
	//     {"user": "manu", "password": "123"}
	router.POST("/loginJSON", func(c *gin.Context) {
		var json Login
		if err := c.ShouldBindJSON(&json); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		if json.User != "manu" || json.Password != "123" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
	})

	// Example for binding XML:
	//     <?xml version="1.0" encoding="UTF-8"?>
	//     <root>
	//         <user>manu</user>
	//         <password>123</password>
	//     </root>
	router.POST("/loginXML", func(c *gin.Context) {
		var xml Login
		if err := c.ShouldBindXML(&xml); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		if xml.User != "manu" || xml.Password != "123" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
	})

	// Example for binding a HTML form:
	//     user=manu&password=123
	router.POST("/loginForm", func(c *gin.Context) {
		var form Login
		// This will infer what binder to use depending on the content-type header.
		if err := c.ShouldBind(&form); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		if form.User != "manu" || form.Password != "123" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
	})

	router.Run(":8080")
}
```

```sh
$ curl -v -X POST \
  http://localhost:8080/loginJSON \
  -H 'content-type: application/json' \
  -d '{ "user": "manu" }'
> POST /loginJSON HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.64.1
> Accept: */*
> content-type: application/json
> Content-Length: 18
> 
* upload completely sent off: 18 out of 18 bytes
< HTTP/1.1 400 Bad Request
< Content-Type: application/json; charset=utf-8
< Date: Sun, 06 Sep 2020 13:04:57 GMT
< Content-Length: 100
< 
{"error":"Key: 'Login.Password' Error:Field validation for 'Password' failed on the 'required' tag"}
```

注意在 `/loginForm` 里面用了 `ShouldBind`，这个会自动通过 content-type 来判断你请求用的是 Form、JSON、XML、YAML 的哪一种，然后用对应的 `ShouldBindXXXX` 把请求的内容绑定到结构体。

在结构体的定义中，要使用 tag 来指定字段在各种需要的 格式中的名字，并且制定是否必须绑定：

- `binding:"required"` 则必须绑定，如果请求中没有对应的项则返回错误。
- `binding:"-"`：可选，请求中没有不会报错。

Gin 是使用 `github.com/go-playground/validator/v10`  来完成验证的。这个包提供更复杂的验证功能：

> (Emmmm，学不动了，但感觉这个特别有用，从文档直接抄下来了)

```go
package main

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/go-playground/validator/v10"
)

// Booking contains binded and validated data.
type Booking struct {
	CheckIn  time.Time `form:"check_in" binding:"required,bookabledate" time_format:"2006-01-02"`
	CheckOut time.Time `form:"check_out" binding:"required,gtfield=CheckIn" time_format:"2006-01-02"`
}

var bookableDate validator.Func = func(fl validator.FieldLevel) bool {
	date, ok := fl.Field().Interface().(time.Time)
	if ok {
		today := time.Now()
		if today.After(date) {
			return false
		}
	}
	return true
}

func main() {
	route := gin.Default()

	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		v.RegisterValidation("bookabledate", bookableDate)
	}

	route.GET("/bookable", getBookable)
	route.Run(":8085")
}

func getBookable(c *gin.Context) {
	var b Booking
	if err := c.ShouldBindWith(&b, binding.Query); err == nil {
		c.JSON(http.StatusOK, gin.H{"message": "Booking dates are valid!"})
	} else {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	}
}
```

```sh
$ curl "localhost:8085/bookable?check_in=2030-04-16&check_out=2030-04-17"
{"message":"Booking dates are valid!"}

$ curl "localhost:8085/bookable?check_in=2030-03-10&check_out=2030-03-09"
{"error":"Key: 'Booking.CheckOut' Error:Field validation for 'CheckOut' failed on the 'gtfield' tag"}

$ curl "localhost:8085/bookable?check_in=2000-03-09&check_out=2000-03-10"
{"error":"Key: 'Booking.CheckIn' Error:Field validation for 'CheckIn' failed on the 'bookabledate' tag"}%    
```

Gin 还提供很多其他的关于绑定的功能，比如路径参数的绑定、上传文件的绑定、HTML 复选框的绑定等等。详细的看文档吧：[gin#model-binding-and-validation](https://github.com/gin-gonic/gin#model-binding-and-validation)。

## 中间件

之前我们都是用 `r = gin.Default()` 来实例化 Gin 的，这样搞出来的 r 是自带 Logger 和 Recovery 中间件的，要创建一个全新的，没有中间件的实例，使用 `New` 来替换 `Default`：

```go
r := gin.New()
```

通过 `r.Use(中间件())` 来添加中间件：

```go
func main() {
	// Creates a router without any middleware by default
	r := gin.New()

	// Global middleware
	// Logger middleware will write the logs to gin.DefaultWriter even if you set with GIN_MODE=release.
	// By default gin.DefaultWriter = os.Stdout
	r.Use(gin.Logger())

	// Recovery middleware recovers from any panics and writes a 500 if there was one.
	r.Use(gin.Recovery())

	// Per route middleware, you can add as many as you desire.
	r.GET("/benchmark", MyBenchLogger(), benchEndpoint)

	// Authorization group
	// authorized := r.Group("/", AuthRequired())
	// exactly the same as:
	authorized := r.Group("/")
	// per group middleware! in this case we use the custom created
	// AuthRequired() middleware just in the "authorized" group.
	authorized.Use(AuthRequired())
	{
		authorized.POST("/login", loginEndpoint)
		authorized.POST("/submit", submitEndpoint)
		authorized.POST("/read", readEndpoint)

		// nested group
		testing := authorized.Group("testing")
		testing.GET("/analytics", analyticsEndpoint)
	}

	// Listen and serve on 0.0.0.0:8080
	r.Run(":8080")
}
```

。。。

写不动了，了解更多 Gin 请到 [gin 的 readme](https://github.com/gin-gonic/gin)。