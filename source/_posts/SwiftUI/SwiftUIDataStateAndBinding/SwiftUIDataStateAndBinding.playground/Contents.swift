import Combine
import PlaygroundSupport
import SwiftUI
import UIKit

/*:
 # SwiftUI 数据状态和绑定
 
 - `@State` & `@Binding`: 提供 View 内部的状态存储，应该是被标记为 private 的简单值类型，仅在内部使用。
 - `ObservableObject` & `@ObservedObject`: 针对跨越 View 层级的状态共享。处理更复杂的数据类型，在数据变化时触发界面刷新。
 - `@EnvironmentObject`:  对于 “跳跃式” 跨越多个 View 层级的状态。 更方便地使用 ObservableObject，以简化代码。
 */

struct Preview: View {
    var body: some View {
        VStack(spacing: 30) {
            Text("State & Binding").font(.headline)
            HStack(spacing: 10) {
                SBParentView()
                    .padding(20)
//                SBParentView()
//                    .padding(20)
            }

            Text("ObservedObject").font(.headline)
            HStack(spacing: 10) {
                OOParentView()
                    .padding(20)
//                OOParentView()
//                    .padding(20)
            }

            Text("EnvironmentObject").font(.headline)
            HStack(spacing: 10) {
                EOParentView()
                    .environmentObject(Model())
                    .padding(20)
//                EOParentView()
//                    .environmentObject(Model())
//                    .padding(20)
            }
        }
    }
}

PlaygroundPage.current.setLiveView(
    Preview()
        .frame(width: 800, height: 300)
)
