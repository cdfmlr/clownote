import Foundation
import Combine
import SwiftUI

public struct OOParentView: View {
   @ObservedObject var model: Model = Model()

   public var body: some View {
       VStack(spacing: 25) {
           Text("foo in Parent: \(self.model.foo ? "✔️" : "❌")")
           OOChildView(model: model)
       }
   }
    
    public init() {}
}

public struct OOChildView: View {
   var model: Model

   public var body: some View {
       Button("toggle foo from Child") {
           self.model.foo.toggle()
       }
   }
    
    public init(model: Model) {
        self.model = model
    }
}

