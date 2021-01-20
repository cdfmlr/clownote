---
date: 2020-01-28 17:08:05
tags: Swift
title: Swift 掠影
---

# Swift 掠影

> 本文翻译自 Swift 官网的 [A Swift Tour](https://docs.swift.org/swift-book/GuidedTour/GuidedTour.html#) (Swift 5.1)。

按照传统，学习一门新的编程语言时，我们写的第一个程序应该是在屏幕上打印出“Hello, world!”。在 Swift 中，只要一行代码就可以完成这个仪式：

```swift
print("Hello, world!")
// Prints "Hello, world!"
```

如果你写过 C 或者 Objective-C，一定会觉得 Swift 的语法很亲切。在 Swift 中，这一行代码就是一个完整的程序了。你不必导入任何库就可以完成输入输出以及字符串处理。在全局作用域中写的代码就是程序的入口点，所以你不在需要写 `main` 函数了。在每一个语句的末尾，也不用写分号。

本文会提供足够多的信息让你可以开始用 Swift 写代码，我们会为你展现如何用 Swift 完成各种编程任务。如果你有地方没有理解，请不要担心，这里介绍的所有东西在本书后续的章节中都有详尽的讨论。

> 【注】
>
> 为获得最好的体验，你可以在 Xcode 中打开该节的 playground。Playground 让你可以编辑这里的代码并及时看到运行的结果。
>
> [下载 Playground](https://docs.swift.org/swift-book/GuidedTour/GuidedTour.playground.zip)

## 简单值

Swift 用 `let` 声明常量，用 `var` 声明变量。虽然常量的值在变异的过程中是不需要知道的，但你必须在声明时立刻为其赋值。这意味着你可以用常量来命名一个你决定好不在改变、需要在多处使用的值。

```swift
var myVariable = 42
myVariable = 50
let myConstant = 42
```

常量或变量会拥有与你期望赋给它的值相同的类型，但你不必每次都指明类型，在创建变量或常量时，提供一个值就可以让编译器自动推断它的类型。在上面的例子中，编译器会推测 `myVariable` 是一个整数，因为赋给它的初值是一个整数。

如果通过初值不能提供足够的信息（或不打算赋初值），你可以自己指明类型，在变量名后面写上类型，用冒号隔开即可。

```swift
let implicitInteger = 70
let implicitDouble = 70.0
let explicitDouble: Double = 70
```

> 【实验】
>
> 创建一个常量，显式地指明类型为 `Float`，值为 `4`。

一个值永远不会被隐式转化为其他类型的。如果你需要把某个值转换成其他类型的，需要显式地创建一个目标类型实例：

```swift
let label = "The width is "
let width = 94
let widthLabel = label + String(width)
```

> 【实验】
>
> 尝试在上面代码的最后一把到 `String` 的转化删除，看看会发生什么？

Swift 中，有一个简单的办法让你在字符串中包含一些值：在小括号里写上需要的值，并在括号前面加一个反斜杠（`\`），例如：

```swift
let apples = 3
let oranges = 5
let appleSummary = "I have \(apples) apples."
let fruitSummary = "I have \(apples + oranges) pieces of fruit."
```

> 【实验】
>
> 在一个字符串中使用 `\()` 去包含一个浮点数计算，再包含某人的名字来和他打个招呼。

用三个双引号（`"""`）可以写多行的字符串。其中每行前面的、对齐结束引号的缩进会被自动移除。例如：

```swift
let quotation = """
I said "I have \(apples) apples."
And then I said "I have \(apples + oranges) pieces of fruit."
"""
```

用方括号（`[]`）可以创建数组或字典。通过在方括号中写索引或键，可以取出其中元素。在最后一个元素后面加个逗号也是被允许的。

```swift
var shoppingList = ["catfish", "water", "tulips"]
shoppingList[1] = "bottle of water"

var occupations = [
    "Malcolm": "Captain",
    "Kaylee": "Mechanic",
]
occupations["Jayne"] = "Public Relations"
```

当添加元素时，数组会自动增长：

```swift
shoppingList.append("blue paint")
print(shoppingList)
```

如果要创建空数组或字典，需要使用构造器语法：

```swift
let emptyArray = [String]()
let emptyDictionary = [String: Float]()
```

如果类型可以被推断出来，那你就可以把空数组写成 `[]`，把空字典写成 `[:]`——例如，当你给变量设置新的值，或给函数传参数的时候就可以这么做。

```swift
shoppingList = []
occupations = [:]
```

## 控制流

用 `if` 和 `switch` 来写条件语句，用 `for-in`、`while` 和 `repeat-while` 来写迭代语句。条件或循环变量前后的小括号是可选的，循环/条件主体前后的大括号是必须的。

```swift
let individualScores = [75, 43, 103, 87, 12]
var teamScore = 0
for score in individualScores {
    if score > 50 {
        teamScore += 3
    } else {
        teamScore += 1
    }
}
print(teamScore)
// Prints "11"
```

在 `if` 语句中，条件必须是值为布尔型的表达式——这意味着类似于 `if score {...}` 这样的代码是错误的，其他类型的值不会自动转化为布尔值。

你可以使用 `if` 和 `let` 配合工作，来处理可能缺失的值。这些值使用可选项表示。一个可选的值要么是一个明确的值，要么是 `nil` 来代表该值缺失。在值的类型后面加一个问号（ `?`）来表示该值可选。

```swift
var optionalString: String? = "Hello"
print(optionalString == nil)
// Prints "false"

var optionalName: String? = "John Appleseed"
var greeting = "Hello!"
if let name = optionalName {
    greeting = "Hello, \(name)"
}
```

> 【实验】
>
> 将上述代码中的 `optionalName` 值改为 `nil`，看看你会得到什么。加一个 `else` 情况来当 `optionalName` 为 `nil` 时为问候设置一个默认值。

如果可选值为 `nil`，则条件为 `false`，在大括号中的代码会被跳过。否则，可选值会把其代表的值赋给 `let` 后面的常量，这样这个值就可以在大括号里使用了。

另一种对可选值的处理是使用 `??` 运算符来提供默认值。利用这种方法，一旦可选值缺失，则默认值就会替代它。

```swift
let nickName: String? = nil
let fullName: String = "John Appleseed"
let informalGreeting = "Hi \(nickName ?? fullName)"
```

`switch` 语句可以接受任何类型的数据以及多样的比较运算——不局限于整数和测试相等：

```swift
let vegetable = "red pepper"
switch vegetable {
case "celery":
    print("Add some raisins and make ants on a log.")
case "cucumber", "watercress":
    print("That would make a good tea sandwich.")
case let x where x.hasSuffix("pepper"):
    print("Is it a spicy \(x)?")
default:
    print("Everything tastes good in soup.")
}
// Prints "Is it a spicy red pepper?"
```

> 【实验】
>
> 尝试移除 `default` 选项，看看会得到什么错误。

注意 `let` 可以使匹配某个模式的值赋给一个常量。

在 `switch` 语句中，执行了匹配的 `case` 情况后，程序会自动退出 `switch` 语句，而不会继续执行下一个 `case` 的代码。所以，不必在每个 `case` 的代码结尾写 `break`。

用 `for-in` 来迭代字典中的元素，提供一对名字来取用每一个 key-value 对。字典是无序集合，所以键值对会以随机顺序进行迭代。

```swift
let interestingNumbers = [
    "Prime": [2, 3, 5, 7, 11, 13],
    "Fibonacci": [1, 1, 2, 3, 5, 8],
    "Square": [1, 4, 9, 16, 25],
]
var largest = 0
for (kind, numbers) in interestingNumbers {
    for number in numbers {
        if number > largest {
            largest = number
        }
    }
}
print(largest)
// Prints "25"
```

> 【实验】
>
> 添加一个变量来记录哪一类数最大、最大的数是多少。

用 `while` 重复一块代码，直到条件改变。循环的条件也可以被放在末尾，以确保循环被运行至少一次。

```swift
var n = 2
while n < 100 {
    n *= 2
}
print(n)
// Prints "128"

var m = 2
repeat {
    m *= 2
} while m < 100
print(m)
// Prints "128"
```

你可以用 `..<` 来创建一系列在顺序的索引，并在 `for` 循环中迭代之。

```swift
var total = 0
for i in 0..<4 {
    total += i
}
print(total)
// Prints "6"
```

使用 `..<` 创建的序列不包括上界，用 `...` 创建的序列包括上下界。

## 函数和闭包

用 `func` 来声明函数。调用函数时，写函数的名字，并在其后写一对圆括号，括号里面是一系列参数。用 `->` 来分隔参数列表和返回值类型。

```swift
func greet(person: String, day: String) -> String {
    return "Hello \(person), today is \(day)."
}
greet(person: "Bob", day: "Tuesday")
```

> 【实验】
>
> 把参数 `day` 移除，添加一个包含今天午餐吃什么的参数，将其添加到欢迎语句里。

默认情况下，函数用形式参数的名称作为实际参数的标签。也可以在形参前面加上自定义的实参标签，或者写 `_` 来指明无需标签。

```swift
func greet(_ person: String, on day: String) -> String {
    return "Hello \(person), today is \(day)."
}
greet("John", on: "Wednesday")
```

使用元组可以创建复合值——例如，从函数中返回多个值。元组中的元素可以通过名字或索引调用。

```swift
func calculateStatistics(scores: [Int]) -> (min: Int, max: Int, sum: Int) {
    var min = scores[0]
    var max = scores[0]
    var sum = 0

    for score in scores {
        if score > max {
            max = score
        } else if score < min {
            min = score
        }
        sum += score
    }

    return (min, max, sum)
}
let statistics = calculateStatistics(scores: [5, 3, 100, 3, 9])
print(statistics.sum)
// Prints "120"
print(statistics.2)
// Prints "120"
```

函数可以嵌套。嵌套的内部函数可以访问外部函数中的变量。你可以用嵌套函数来组织代码，以免一个函数太长、太复杂。

```swift
func returnFifteen() -> Int {
    var y = 10
    func add() {
        y += 5
    }
    add()
    return y
}
returnFifteen()
```

函数是*第一类对象*。这意味着一个函数可以返回另一个函数作为返回值。

> 【译者注】From Wikipedia
>
> **第一类对象**（英语：First-class object）在[计算机科学](https://zh.wikipedia.org/wiki/電腦科學)中指可以在[执行期](https://zh.wikipedia.org/wiki/執行期)创造并作为参数传递给其他函数或存入一个[变数](https://zh.wikipedia.org/wiki/變數)的实体[[1\]](https://zh.wikipedia.org/wiki/第一類物件#cite_note-1)。将一个实体变为第一类对象的过程叫做“[物件化](https://zh.wikipedia.org/wiki/物件化)”（Reification）[[2\]](https://zh.wikipedia.org/wiki/第一類物件#cite_note-2)。

```swift
func makeIncrementer() -> ((Int) -> Int) {
    func addOne(number: Int) -> Int {
        return 1 + number
    }
    return addOne
}
var increment = makeIncrementer()
increment(7)
```

一个函数也可以接受其他函数作为参数。

```swift
func hasAnyMatches(list: [Int], condition: (Int) -> Bool) -> Bool {
    for item in list {
        if condition(item) {
            return true
        }
    }
    return false
}
func lessThanTen(number: Int) -> Bool {
    return number < 10
}
var numbers = [20, 19, 7, 12]
hasAnyMatches(list: numbers, condition: lessThanTen)
```

函数其实是一种特殊情形的闭包：一块可以被稍后调用的代码。在闭包中的代码可以访问存在于其声明时的作用域的变量或函数等东西，哪怕这个闭包在其他作用域中被调用执行——嵌套函数正是这样的例子。你可以这样写一个闭包：写一段没有名字的、用花括号（`{}`）包裹的代码。用 `in` 来将参数、返回值同主体代码分离。

```swift
numbers.map({ (number: Int) -> Int in
    let result = 3 * number
    return result
})
```

> 【实验】
>
> 重写闭包，使所有的奇数返回零。

你还有更多的选择来把闭包写得更简洁。当闭包的类型明确时，例如一个委托的回调，你可以省略参数的类型，或省略返回值的类型，或两者都省略。单语句的闭包隐式地返回该语句的值。

```swift
let mappedNumbers = numbers.map({ number in 3 * number })
print(mappedNumbers)
// Prints "[60, 57, 21, 36]"
```

你可以用数字而非名称来使用参数——这个方法在极其简短的闭包中尤为实用。一个闭包作为最后一个参数传给函数时，可以直接写在圆括号后面。当一个闭包是一个函数唯一的参数时，可以直接省略圆括号。

```swift
let sortedNumbers = numbers.sorted { $0 > $1 }
print(sortedNumbers)
// Prints "[20, 19, 12, 7]"
```

## 对象和类

在关键字 `class` 后加上类的名字来创建一个类。类中属性的声明和常量、变量的声明方式是相同的，唯一的一定区别是属性声明是写在一个类里面的。同样地，方法和函数的声明也是同之前的写法一样。

```swift
class Shape {
    var numberOfSides = 0
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```

> 【实验】
>
> 用 `let` 添加一个常量属性，再写一个接受参数的方法。

在类名后面放一对圆括号来创建类的实例。用*点*语法来取实例中的属性和方法。

```swift
var shape = Shape()
shape.numberOfSides = 7
var shapeDescription = shape.simpleDescription()
```

在刚才写的这一版本 `Shape` 类中，缺少了一个重要的东西：用来在实例被创建时对类进行设置的**构造器**。用 `init` 来创建一个构造器。

```swift
class NamedShape {
    var numberOfSides: Int = 0
    var name: String

    init(name: String) {
        self.name = name
    }

    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```

注意 `self` 的使用区分了构造器的参数 `name` 与类的属性 `name`。在创建类的实例时，传入构造器的参数和调用函数时的传参很类似。每一个属性都需要被赋值——要么在声明时赋值（比如 `numberOfSides`），要么在构造器中赋值（比如 `name`）。

如果你需要在对象被销毁前执行一些清理工作的话，用 `deinit` 来创建一个析构器（译注，为保持简洁，我借用了C++里构造函数/析构函数的说法，deinitializer 直译为反构造器）。

子类应该在其类名后面写上父类的名称，用分号分隔。Swift 不要求一个类必须从某个标准的根类开始继承，所以你可以按需求包括或省略父类。

如果子类中需要重写父类中实现的方法，需要标注 `override` 以强调是重写，否则会被编译器认为是错误。编译器同样会检测出标记了 `override` 但在父类中没有实现的方法。

```swift
class Square: NamedShape {
    var sideLength: Double

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 4
    }

    func area() -> Double {
        return sideLength * sideLength
    }

    override func simpleDescription() -> String {
        return "A square with sides of length \(sideLength)."
    }
}
let test = Square(sideLength: 5.2, name: "my test square")
test.area()
test.simpleDescription()
```

> 【实验】
>
> 创建 `NamedShape` 的另一个子类 `Circle`，该类的构造器接受半径radius 和 名字name 两个参数。在 `Circle` 中实现 `area()` 和 `simpleDescription()` 方法。

除了已经提及的简单属性，属性还可以拥有 getter 和 setter。

```swift
class EquilateralTriangle: NamedShape {
    var sideLength: Double = 0.0

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 3
    }

    var perimeter: Double {
        get {
            return 3.0 * sideLength
        }
        set {
            sideLength = newValue / 3.0
        }
    }

    override func simpleDescription() -> String {
        return "An equilateral triangle with sides of length \(sideLength)."
    }
}
var triangle = EquilateralTriangle(sideLength: 3.1, name: "a triangle")
print(triangle.perimeter)
// Prints "9.3"
triangle.perimeter = 9.9
print(triangle.sideLength)
// Prints "3.3000000000000003"
```

在 `perimeter` 的 setter 中，新的值被自动命名为 `newValue`。你也可以提供一个自定义的名称，这个名称在 `set` 后面添加的一对圆括号里写明。

注意，在 `EquilateralTriangle` 类的构造器中有三个不同的步骤：

1. 设置子类中声明的属性值；
2. 调用父类的构造器；
3. 修改父类中定义的属性值。其他各种需要的使用方法、getter、setter的附加设置也在这一步完成。

如果你不需要计算属性，但是需要在设置一个新的值的前后运行一些代码，你可以使用 `willSet` 和 `didSet`。在构造器意外改变值时，其中的代码就会被执行。例如，下面的类保证三角形的边长始终等于正方形的边长：

```swift
class TriangleAndSquare {
    var triangle: EquilateralTriangle {
        willSet {
            square.sideLength = newValue.sideLength
        }
    }
    var square: Square {
        willSet {
            triangle.sideLength = newValue.sideLength
        }
    }
    init(size: Double, name: String) {
        square = Square(sideLength: size, name: name)
        triangle = EquilateralTriangle(sideLength: size, name: name)
    }
}
var triangleAndSquare = TriangleAndSquare(size: 10, name: "another test shape")
print(triangleAndSquare.square.sideLength)
// Prints "10.0"
print(triangleAndSquare.triangle.sideLength)
// Prints "10.0"
triangleAndSquare.square = Square(sideLength: 50, name: "larger square")
print(triangleAndSquare.triangle.sideLength)
// Prints "50.0"
```

当使用可选值时，你可以在方法、属性、下标等操作前面写 `?`。如果 `?` 前面的值是 `nil`，则 `?` 后的一切都会被忽略，整个表达式的值为 `nil`。否则，可选值会被展开，`?` 后的活动作用于展开的值。在两种情况下，整个表达式的值都是可选值。

```swift
let optionalSquare: Square? = Square(sideLength: 2.5, name: "optional square")
let sideLength = optionalSquare?.sideLength
```

## 枚举和结构体

用 `enum` 来创建枚举。和类以及其他有名字的类型一样，枚举可以包含属于自己的方法。

```swift
enum Rank: Int {
    case ace = 1
    case two, three, four, five, six, seven, eight, nine, ten
    case jack, queen, king

    func simpleDescription() -> String {
        switch self {
        case .ace:
            return "ace"
        case .jack:
            return "jack"
        case .queen:
            return "queen"
        case .king:
            return "king"
        default:
            return String(self.rawValue)
        }
    }
}
let ace = Rank.ace
let aceRawValue = ace.rawValue
```

> 【实验】
>
> 写一个通过原始值来比较两个 Rank 值的函数。

在默认情况下，swift 会从零开始为枚举情况赋值，逐个递增。但你可以通过直接指定值来打破这一规律。在上面的例子中，`Ace` 被直接赋予了原始值 `1`，其余的元素随即被顺序依次赋值。你也可以创建用字符串或浮点数来作为原始值的枚举。用 `rawValue` 属性来取出一个枚举情况的原始值。

用构造器 `init?(rawValue:)` 来从原始值实例化枚举实例。当提供的原始值匹配上某枚举情况时，它返回该匹配的枚举情况实例；否则，没有匹配的项就返回 `nil`。

```swift
enum Suit {
    case spades, hearts, diamonds, clubs

    func simpleDescription() -> String {
        switch self {
        case .spades:
            return "spades"
        case .hearts:
            return "hearts"
        case .diamonds:
            return "diamonds"
        case .clubs:
            return "clubs"
        }
    }
}
let hearts = Suit.hearts
let heartsDescription = hearts.simpleDescription()
```

> 【实验】
>
> 为 `Suit` 添加一个 `color()` 函数，当枚举情况是 spades 或 clubs 时该函数返回 `black` ，当枚举情况是 hearts 或 diamonds 时该函数返回 `red` 。

注意上面的代码中，枚举情况 `hearts` 的两种表示方式：当将至赋给 `hearts` 常量时，枚举情况 `Suit.hearts` 是用全名来取用的，因为这个常量没有直接的类型指明。在` switch` 中，枚举情况的取用是用了缩写 `.hearts`，因为已经知道值 `self` 是一个 `Suit`。对于任何已知值的类型的情况，你都可以使用这样的缩写。

如果一个枚举有原始值，则原始值在声明时即被确定，因此，每个特定枚举情况的实例总是拥有相同的原始值。还有另一种枚举情况可以使情况与值相关联——这些值在创建实例时被确定，这种情况下同一枚举情况的不同实例可能拥有不同的关联值。你可以认为这些关联值就像是储存在枚举情况实例中的属性。例如，考虑从服务器请求日出日落时间的场景，服务器要么返回被请求的信息，要么返回发生错误时的描述。

```swift
enum ServerResponse {
    case result(String, String)
    case failure(String)
}

let success = ServerResponse.result("6:00 am", "8:09 pm")
let failure = ServerResponse.failure("Out of cheese.")

switch success {
case let .result(sunrise, sunset):
    print("Sunrise is at \(sunrise) and sunset is at \(sunset).")
case let .failure(message):
    print("Failure...  \(message)")
}
// Prints "Sunrise is at 6:00 am and sunset is at 8:09 pm."
```

> 【实验】
>
> 添加第三种情况到 `ServerResponse` 和 switch。

注意 sunrise 和 sunset 时间是如何从 `ServerResponse` 以匹配 switch case 的形式中提取出来的。

用 `struct` 来创建结构体。结构体支持许多与类相似的行为，包括方法和构造器。结构体和类最重要的区别之一是：当在代码中被传递时，结构体总是会被复制，而类重视被引用。

```swift
struct Card {
    var rank: Rank
    var suit: Suit
    func simpleDescription() -> String {
        return "The \(rank.simpleDescription()) of \(suit.simpleDescription())"
    }
}
let threeOfSpades = Card(rank: .three, suit: .spades)
let threeOfSpadesDescription = threeOfSpades.simpleDescription()
```

> 【实验】
>
> 写一个函数，返回一套完整的扑克牌，并把每张牌的 rank 和 suit 对应起来。

## 协议和拓展

用 `protocol` 来声明协议。

```swift
protocol ExampleProtocol {
    var simpleDescription: String { get }
    mutating func adjust()
}
```

类、枚举和结构体都可以采用协议。

```swift
class SimpleClass: ExampleProtocol {
    var simpleDescription: String = "A very simple class."
    var anotherProperty: Int = 69105
    func adjust() {
        simpleDescription += "  Now 100% adjusted."
    }
}
var a = SimpleClass()
a.adjust()
let aDescription = a.simpleDescription

struct SimpleStructure: ExampleProtocol {
    var simpleDescription: String = "A simple structure"
    mutating func adjust() {
        simpleDescription += " (adjusted)"
    }
}
var b = SimpleStructure()
b.adjust()
let bDescription = b.simpleDescription
```

> 【实验】
>
> 在 `ExampleProtocol` 里添加一个要求，看看需要怎么修改 `SimpleClass` 和 `SimpleStructure` 来使它们仍然遵从协议。

注意，用关键字 `mutating` 来在 `SimpleStructure` 中声明一个会修改结构体的方法。而在 `SimpleClass` 的声明中，不需要标记 `mutating` 是因为类中的任意方法总是可以修改改类的。

用关键词 `extension` 来给现有的类添加一些功能，例如新的方法、计算属性。你可以用 `extension` 给在其他地方声明的（甚至是你在你导入的包中的）类型添加拓展，使其遵守你指定的协议。

```swift
extension Int: ExampleProtocol {
    var simpleDescription: String {
        return "The number \(self)"
    }
    mutating func adjust() {
        self += 42
    }
}
print(7.simpleDescription)
// Prints "The number 7"
```

> 【实验】
>
> 给 `Double` 类型添加一个 `absoluteValue` 属性。

你可以像其他任何命名类型一样使用协议——例如，创建一个集合来存放遵守相同协议但互不相同的类型的对象。当你处理协议类型的值时，协议之外的属性都是不可用的。

```swift
let protocolValue: ExampleProtocol = a
print(protocolValue.simpleDescription)
// Prints "A very simple class.  Now 100% adjusted."
// print(protocolValue.anotherProperty)  // Uncomment to see the error
```

即时变量 `protocolValue` 在运行时拥有类型 `SimpleClass`， 编译器还是会按照给定的类型 `ExampleProtocol` 来看待它。也就是说，你不可以这个类在协议规定以外额外实现的方法和属性。

## 错误处理

你可以使用任何遵守了 `Error` 协议的类型来代表错误。

```swift
enum PrinterError: Error {
    case outOfPaper
    case noToner
    case onFire
}
```

用 `throw` 来抛出错误，用 `throws` 来标记一个函数有可能会抛出错误。如果你在一个函数中抛出了错误，那么函数就会立刻返回，调用函数的代码会要处理错误。

```swift
func send(job: Int, toPrinter printerName: String) throws -> String {
    if printerName == "Never Has Toner" {
        throw PrinterError.noToner
    }
    return "Job sent"
}
```

Swift 中有多种方法可以处理错误，其中之一是使用 `do-catch`。在 `do` 语句块中，你可以在可能抛出错误的代码前面写上 `try`，在 `catch` 语句块中，错误会被自动赋给名称 `error`，或者你自定义的其他名称。

```swift
do {
    let printerResponse = try send(job: 1040, toPrinter: "Bi Sheng")
    print(printerResponse)
} catch {
    print(error)
}
// Prints "Job sent"
```

> 【实验】
>
> 把 pointer 的名字换成 "Never Has Toner"，使 `send()` 函数抛出一个错误。

你可以提供多个 `catch` 语句块来处理不同的错误。在 `catch` 后面的代码模式类似于你在 switch 语句的 `case` 后面写的。

```swift
do {
    let printerResponse = try send(job: 1440, toPrinter: "Gutenberg")
    print(printerResponse)
} catch PrinterError.onFire {
    print("I'll just put this over here, with the rest of the fire.")
} catch let printerError as PrinterError {
    print("Printer error: \(printerError).")
} catch {
    print(error)
}
// Prints "Job sent"
```

> 【实验】
>
> 添加代码，在 `do` 语句块中抛出一个错误，需要抛出什么错误来使该错误被第一个 `catch` 块处理？第二个、第三个又如何？

另一种处理错误的办法是使用 `try?` 来把结果转化为可选值。如果函数抛出错误，具体的错误会被忽略，返回值为 `nil`。否则，返回值会是包含了函数返回值的可选值。

```swift
let printerSuccess = try? send(job: 1884, toPrinter: "Mergenthaler")
let printerFailure = try? send(job: 1885, toPrinter: "Never Has Toner")
```

用 `defer` 来写一块在函数中的所有代码执行完成后、函数返回之前执行的代码。不论函数是否抛出了错误，这段 defer 代码都会被执行。你可以利用 `defer`，把设置和清理的代码写在一起，即使它们将在不同时候被执行：

```swift
var fridgeIsOpen = false
let fridgeContent = ["milk", "eggs", "leftovers"]

func fridgeContains(_ food: String) -> Bool {
    fridgeIsOpen = true
    defer {
        fridgeIsOpen = false
    }

    let result = fridgeContent.contains(food)
    return result
}
fridgeContains("banana")
print(fridgeIsOpen)
// Prints "false"
```

## 泛型

在一对尖括号中写一个名字来创建泛型函数或类型。

```swift
func makeArray<Item>(repeating item: Item, numberOfTimes: Int) -> [Item] {
    var result = [Item]()
    for _ in 0..<numberOfTimes {
        result.append(item)
    }
    return result
}
makeArray(repeating: "knock", numberOfTimes: 4)
```

你可以创建泛型的函数和方法，也可以创建泛型的类、枚举和结构体。

```swift
// Reimplement the Swift standard library's optional type
enum OptionalValue<Wrapped> {
    case none
    case some(Wrapped)
}
var possibleInteger: OptionalValue<Int> = .none
possibleInteger = .some(100)
```

在函数体前用 `where` 来明确一系列对泛型的要求——例如，要求这种类型要实现某种协议，或者某两个类型要相同，再或者要求一个类有特定的子类。

```swift
func anyCommonElements<T: Sequence, U: Sequence>(_ lhs: T, _ rhs: U) -> Bool
    where T.Element: Equatable, T.Element == U.Element
{
    for lhsItem in lhs {
        for rhsItem in rhs {
            if lhsItem == rhsItem {
                return true
            }
        }
    }
    return false
}
anyCommonElements([1, 2, 3], [3])
```

> 【实验】
>
> 修改函数 `anyCommonElements(_:_:)` 使之返回一个数组，该数组包括所有两个序列中共有的元素。

写 `<T: Equatable>` 和写 `<T> ... where T: Eauatable` 是一样的。

