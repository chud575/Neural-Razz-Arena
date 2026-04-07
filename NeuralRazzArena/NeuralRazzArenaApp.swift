import SwiftUI
import AppKit

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApplication.shared.setActivationPolicy(.regular)
        NSApplication.shared.activate(ignoringOtherApps: true)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            if let window = NSApplication.shared.windows.first {
                window.makeKeyAndOrderFront(nil)
                window.title = "Neural Razz Arena"
            }
        }
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}

@main
struct NeuralRazzArenaApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    @StateObject private var serverManager = ServerManager()
    @StateObject private var vm = ArenaViewModel()

    var body: some Scene {
        WindowGroup {
            ContentView(serverManager: serverManager, vm: vm)
                .onAppear {
                    serverManager.start()
                    vm.serverManager = serverManager
                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                        vm.fetchModelInfo()
                    }
                }
                .onDisappear {
                    serverManager.stop()
                }
        }
        .commands {
            CommandGroup(replacing: .appTermination) {
                Button("Quit Neural Razz Arena") {
                    serverManager.stop()
                    NSApplication.shared.terminate(nil)
                }
                .keyboardShortcut("q")
            }
        }
    }
}
