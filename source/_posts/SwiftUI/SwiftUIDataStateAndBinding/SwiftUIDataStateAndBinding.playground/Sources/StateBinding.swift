import SwiftUI

public struct SBParentView: View {
    @State private var foo: Bool = false

    public var body: some View {
        VStack(spacing: 25) {
            Text("foo in Parent: \(self.foo ? "✔️" : "❌")")
            SBChildView(foo: $foo)
        }
    }
    
    public init() {}
}

public struct SBChildView: View {
    @Binding var foo: Bool

    public var body: some View {
        Button("toggle foo from Child") {
            self.foo.toggle()
        }
    }
    
    public init(foo: Binding<Bool>) {
        self._foo = foo
    }
}

