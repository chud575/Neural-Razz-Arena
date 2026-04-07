import Foundation

class ServerManager: ObservableObject {
    @Published var isRunning = false
    @Published var isHealthy = false
    @Published var serverLog: [String] = []

    private var process: Process?
    private var healthTimer: Timer?
    let baseURL = "http://127.0.0.1:5060"

    func start() {
        guard !isRunning else { return }

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3")
        process.arguments = ["server.py"]

        // Find backend directory
        let candidates = [
            URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent("backend"),
            Bundle.main.bundleURL.deletingLastPathComponent().appendingPathComponent("backend"),
            URL(fileURLWithPath: #file).deletingLastPathComponent().deletingLastPathComponent().appendingPathComponent("backend"),
        ]

        var backendDir: URL?
        for candidate in candidates {
            let serverFile = candidate.appendingPathComponent("server.py")
            if FileManager.default.fileExists(atPath: serverFile.path) {
                backendDir = candidate
                break
            }
        }

        // Try harder
        if backendDir == nil {
            let home = FileManager.default.homeDirectoryForCurrentUser
            let fallback = home.appendingPathComponent("Desktop/Poker Apps/Neural Razz Arena/backend")
            if FileManager.default.fileExists(atPath: fallback.appendingPathComponent("server.py").path) {
                backendDir = fallback
            }
        }

        guard let dir = backendDir else {
            log("Cannot find backend/server.py")
            return
        }

        process.currentDirectoryURL = dir

        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe

        pipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            guard !data.isEmpty, let output = String(data: data, encoding: .utf8) else { return }
            DispatchQueue.main.async {
                for line in output.components(separatedBy: .newlines) where !line.isEmpty {
                    self?.serverLog.append(line)
                    if self?.serverLog.count ?? 0 > 200 {
                        self?.serverLog.removeFirst()
                    }
                }
            }
        }

        do {
            try process.run()
            self.process = process
            isRunning = true
            log("Server process started (PID \(process.processIdentifier))")

            DispatchQueue.main.asyncAfter(deadline: .now() + 2) { [weak self] in
                self?.startHealthChecks()
            }
        } catch {
            log("Failed to start server: \(error)")
        }
    }

    func stop() {
        healthTimer?.invalidate()
        healthTimer = nil
        process?.terminate()
        process = nil
        isRunning = false
        isHealthy = false
    }

    private func startHealthChecks() {
        healthTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.checkHealth()
        }
        checkHealth()
    }

    func checkHealth() {
        guard let url = URL(string: "\(baseURL)/api/health") else { return }
        URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            DispatchQueue.main.async {
                let healthy = (response as? HTTPURLResponse)?.statusCode == 200
                if healthy != self?.isHealthy {
                    self?.isHealthy = healthy
                    self?.log(healthy ? "Server is healthy" : "Server not responding")
                }
            }
        }.resume()
    }

    func log(_ message: String) {
        DispatchQueue.main.async {
            self.serverLog.append("[ServerManager] \(message)")
            if self.serverLog.count > 200 { self.serverLog.removeFirst() }
        }
    }
}
