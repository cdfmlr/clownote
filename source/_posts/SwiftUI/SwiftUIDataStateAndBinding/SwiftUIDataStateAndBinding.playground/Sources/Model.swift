import Combine
import Foundation

public class Model: ObservableObject {
    public let objectWillChange = PassthroughSubject<Void, Never>()

    public var foo: Bool = false {
        willSet { objectWillChange.send() }
    }

    public init() {}
}

// // Or, easier:
// // @Published 是个 internal 的，这里不方便 public 所以没有用。
// public class Model: ObservableObject {
//    @Published var foo: Bool = false
// }
