import Combine

class Bar {
    var count: String = ""
}

let bar = Bar()

let foo = (0 ... 5).publisher.map { _ in }

foo
    .scan(0) { value, _ in value + 1 }
    .map { String($0) }
//    .sink { print("foo count: \($0)") }
    .assign(to: \.count, on: bar)

print(bar.count)

let mySubject = PassthroughSubject<Int, Never>()

print("开始订阅了")

mySubject.send(123)  // 没人监听，丢失了
// mySubject.send(completion: .finished) 加这行就之后得到 complete: finished 了

mySubject.sink(
    receiveCompletion: { print("complete: \($0)") },
    receiveValue: { print("value: \($0)")}
)  // 开始监听

mySubject.send(666)
mySubject.send(completion: .finished)

print("---------")

let anotherSubject = CurrentValueSubject<Int, Never>(1024)

anotherSubject.send(2048)
anotherSubject.send(4096)
//anotherSubject.send(completion: .finished)

print("开始监听")
anotherSubject.sink(
    receiveCompletion: { print("complete: \($0)") },
    receiveValue: { print("value: \($0)")}
)

anotherSubject.send(8192)
anotherSubject.send(16384)
anotherSubject.value = 999

anotherSubject.send(completion: .finished)

print(anotherSubject.value)
