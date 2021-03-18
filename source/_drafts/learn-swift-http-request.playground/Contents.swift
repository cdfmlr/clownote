import Combine
import Foundation

/// response from `httpbin.org`
struct Response: Decodable {
    struct Args: Decodable {
        let foo: String
    }

    let args: Args?
}

let url = URL(string: "https://httpbin.org/get?foo=bar")!
URLSession.shared.dataTask(with: url) { data, response, error in
    print(data, response, error)
    DispatchQueue.main.async {
        // ...
    }
}.resume()

check("URL Session") {
    URLSession.shared.dataTaskPublisher(
        for: URL(string: "https://httpbin.org/get?foo=bar")!
    )
    .map { data, _ in data }
    .decode(type: Response.self, decoder: JSONDecoder())
    .compactMap { $0.args?.foo }
}

sleep(3)

Future<Int, Never> { promise in
    DispatchQueue.global().asyncAfter(deadline: .now() + 1.5) {
        promise(.success(123))
    }
}
.receive(on: DispatchQueue.main)
.eraseToAnyPublisher()
.print("[F]")
.sink(receiveCompletion: { _ in }, receiveValue: { _ in })

sleep(3)
