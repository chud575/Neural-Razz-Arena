// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "NeuralRazzArena",
    platforms: [.macOS(.v13)],
    targets: [
        .executableTarget(
            name: "NeuralRazzArena",
            path: "."
        ),
    ]
)
