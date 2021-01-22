/*:
 # 常用 Publisher 和 Operator

 Publisher 和 Subscriber 的调用关系：

 ![Publisher and Subscriber](PublisherSubscriber.png)

 */

import Combine

/*:
 ## 常用 Publisher

 - `Empty`: 不会发布任何 output，只在被订阅的时候发布一个 finished（Empty 可以用于表示某个事件已经发生）
 */

check("Empty") {
    Empty<Int, SampleError>()
}

/*:
 - `Just`: 表示一个单一的值，在被订阅后，这个值会被发送出去，然后 finished
 */

check("Just") {
    Just(1)
}

/*:
 - Sequence Publisher：发布一个序列（数组 or `Range`），被订阅时，Sequence 中的元素被逐个发 送出来。
 */

check("Sequence") {
    Publishers.Sequence<[Int], Never>(sequence: [1, 2, 3])
}

//: Swift 标准库和 Foundation 中的很多类型都有获取 CombinePublisher 的简便方法：

check("Sequence") {
    [4, 5, 6].publisher
}

/*:
 ## 常用 Operator

 Operator 其实是 Publisher 的 extesnion 中所提供的一些方法，作用于 Publisher，返回 Publisher。

 - map

  和普通序列的 map 类似：
 */

let a: [Int] = [1, 2, 3].map { $0 * 2 } // 结果是 [Int]

check("Map") {
    [1, 2, 3].publisher.map { $0 * 2 } // 结果是 publisher
}

check("Map Just") {
    Just(5)
        .map { $0 * 2 }
}

/*:
 - reduce

 和普通序列的 reduce 类似，将一系列元素按照某种规则进行合并，得到一个最终的结果：
 */

[1, 2, 3, 4, 5].reduce(0, +) // (1 => 3 => 6 => 10) => 15

check("Reduce") {
    [1, 2, 3, 4, 5].publisher // output(1), output(2), ... output(5), finished
        .reduce(0, +) // 上游 finished 后，将之前发布的值逐个 reduce，发布结果
}

/*:
 - scan: 和 reduce 类似的操作，但记录下每一个中途的过程
 */

[1, 2, 3, 4, 5].scan(0, +) // 这个方法不在标准库里，是自己 extension Sequence 实现的，See Utils.swift

check("Scan") {
    [1, 2, 3, 4, 5].publisher
        .scan(0, +)
}

/*:
 - `compactMap`: 将 map 结果中那些 nil 的元素去除掉
 */

check("Compact Map") {
    ["1", "2", "3", "cat", "5"].publisher
        .compactMap { Int($0) } // Int("cat) == nil: 被丢弃
}

// compactMap == map + filter:

check("Compact Map By Filter") {
    ["1", "2", "3", "cat", "5"].publisher
        .map { Int($0) }
        .filter { $0 != nil } // Optional<Int>
        .map { $0! } // Int
}

/*:
 - `flatMap`: “嵌套，降维”：将外层 Publisher 发出的事件中的值传递给内层 Publisher，然后汇总内层 Publisher 给出的事件输出
 */

check("Flat Map 1") {
    [[1, 2, 3], ["a", "b", "c"]].publisher
        .flatMap { $0.publisher }
}

check("Flat Map 2") {
    ["A", "B", "C"].publisher
        .flatMap { letter in
            [1, 2, 3].publisher
                .map { number in "\(letter)\(number)" }
        }
}

/*:
 - removeDuplicates: 移除连续的重复事件值
 */

check("Remove Duplicates") {
    ["S", "Sw", "Sw", "Sw", "Swi", "Swif", "Swift", "Swift", "Swif"]
        .publisher.removeDuplicates()
}

/*:
 - `eraseToAnyPublisher`: 抹去 Publisher 的具体嵌套类型，得到 AnyPublisher

 经过层层 Operator 的处理，最终得到的 Publisher 的 Output 类型是很深的嵌套的，用 eraseToAnyPublisher 可以把这些潜逃抹去，只留下最终关注的类型。
 */

check("erase To AnyPublisher") { () -> AnyPublisher<String, Never> in
    let p0 = ["A", "B", "C"].publisher
        .flatMap { letter in
            [1, 2, 3].publisher
                .map { number in "\(letter)\(number)" }
        }
    print("p0:", p0)
    let p1 = p0.eraseToAnyPublisher()
    print("p1:", p1)
    return p1
}

/*:
 - `merge`: 将两个事件流进行合并，在对应的时间完整保留两个事件流的全部事件.

 ![merge](merge.png)
 */

let p0 = [1, 2, 3].publisher
let p1 = [7, 8, 9].publisher

check("merge") {
    p0.merge(with: p1)
}

/*:
 ## 错误处理

 ### 发布错误

 - `Fail` Publisher: 在被订阅时发送一个错误事件
 */

check("Fail") {
    Fail<Int, SampleError>(error: .sampleError) // SampleError 是自己在 Util.swift 里定义的
}

//: - `tryMap`: 可以抛出错误的 map

check("Throw") {
    ["1", "2", "UnexpectedNoNumber", "4"].publisher
        .tryMap { s -> Int in
            guard let value = Int(s) else {
                throw SampleError.sampleError // 抛出错误后 Publisher 就停了
            }
            return value
        }
}

//: 类似 `tryMap` 的还有 `try{Reduce|Scan|Filter}`...

/*:
 ### 错误转换

 - `mapError`: 将 Publisher 的 Failure 转换成 Subscriber 所需要的 Failure 类型

 e.g. Publisher 发的是 SampleError，Subscriber 想要 MyError，则如下处理之：
 */

enum MyError: Error {
    case myError
}

check("Map Error") {
    Fail<Int, SampleError>(error: .sampleError)
        .mapError { _ in MyError.myError }
}

/*:
 ### 错误恢复

 - `replaceError`: 把错误替换成某个值，并且立即发送 finished 事件

 Note: `Publisher<Output, Failure>` --(replaceError)--> `Publisher<Output, Never>`
 */

check("Replace Error") {
    ["1", "2", "UnexpectedNoNumber", "4"].publisher
        .tryMap { s -> Int in
            guard let value = Int(s) else {
                throw SampleError.sampleError // 抛出错误后 Publisher 就停了
            }
            return value
        }
        .replaceError(with: -1)
}

/*:
  - `catch`: 当上游 Publisher 发生错误时，使用一个新的 Publisher 来把原来的 Publisher 替换掉

 ```
  publisher: Publisher<Output, Failure>
  handler: Publisher<Output, Never>

  publisher.catch(handler)
  ```
  */

check("Catch with Just") {
    ["1", "2", "UnexpectedNoNumber", "4"].publisher
        .tryMap { s -> Int in
            guard let value = Int(s) else {
                throw SampleError.sampleError
            }
            return value
        }
        .catch { _ in Just(-1) }
}

check("Catch with Another Publisher") {
    ["1", "2", "UnexpectedNoNumber", "4"].publisher
        .tryMap { s -> Int in
            guard let value = Int(s) else {
                throw SampleError.sampleError
            }
            return value
        }
        .catch { _ in [-1, -2, -3].publisher }
}

/*:
 👆上面处理总而言之都是遇到错误原来的 Publisher 就停了，现实里我们可能像处理完错误值后继续接收原来的发布，这就需要：

 - `flatMap` + `catch`: 处理错误值，然后继续原来的 Publish
 */

check("Catch and Continue") {
    ["1", "2", "UnexpectedNoNumber", "4"].publisher
        .flatMap { s in
            Just(s)
                .tryMap { s -> Int in
                    guard let value = Int(s) else {
                        throw SampleError.sampleError
                    }
                    return value
                }
                .catch { _ in Just(-1) }
        }
}

// Print 大法，看看具体步骤：

check("Catch and Continue with Print") {
    ["1", "2", "UnexpectedNoNumber", "4"].publisher
        .print("[ Original ]")
        .flatMap { s in
            Just(s)
                .tryMap { s -> Int in
                    guard let value = Int(s) else {
                        throw SampleError.sampleError
                    }
                    return value
                }
                .print("[ TryMap ]")
                .catch { _ in Just(-1).print("[ Just ]") }
                .print("[ Catch ]")
        }
}

/*:
 ## 参考

 [1] 王巍 (@onevcat). SwiftUI 与 Combine 编程. ch6
 */
