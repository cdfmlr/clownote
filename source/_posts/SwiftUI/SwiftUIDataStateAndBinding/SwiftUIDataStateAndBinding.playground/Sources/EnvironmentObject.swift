import SwiftUI

public struct EOParentView: View {
   @EnvironmentObject var model: Model

   public var body: some View {
       VStack(spacing: 25) {
           Text("foo in Parent: \(self.model.foo ? "✔️" : "❌")")
           EOChildView()
       }
   }
    
    public init() {}
}

public struct EOChildView: View {
   @EnvironmentObject var model: Model

   public var body: some View {
       Button("toggle foo from Child") {
           self.model.foo.toggle()
       }
   }
    
    public init() {}
}
