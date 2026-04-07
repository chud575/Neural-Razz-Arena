import Foundation

struct ArenaResult: Identifiable {
    let id = UUID()
    let opponent: String
    let numHands: Int
    let winRate: Double
    let bbPer100: Double
    let foldRate: Double
    let sdWinRate: Double
    var handHistories: [HandHistoryEntry] = []
}

struct HandHistoryEntry: Identifiable {
    let id = UUID()
    let handNum: Int
    let heroStart: String
    let villainStart: String
    let heroDoor: String
    let villainDoor: String
    let heroFinal: String
    let villainFinal: String
    let result: String
    let payoff: Double
    let heroFolded: Bool
    let actions: [String]
    let pot: Double
}

struct AllHandsResult: Identifiable {
    let id = UUID()
    let hand: String
    let bucket: String
    let handsPlayed: Int
    let winRate: Double
    let bbPer100: Double
    let foldRate: Double
    let sdWinRate: Double
    let profit: Double
    let evPct: Double
    let delta: Double
}

struct EVGroupResult: Identifiable {
    let id = UUID()
    let name: String
    let count: Int
    let winRate: Double
    let bbPer100: Double
    let profit: Double
    let profitable: Int
}

struct BatteryResultItem: Identifiable {
    let id = UUID()
    let name: String
    let tier: Int
    let passed: Bool
    let predicted: String
    let expected: [String]
    let confidence: Double
}

class ArenaViewModel: ObservableObject {
    var serverManager: ServerManager?

    // Model
    @Published var modelLoaded = false
    @Published var modelFilename = ""
    @Published var modelParams = 0
    @Published var modelIterations = 0

    // Arena
    @Published var arenaRunning = false
    @Published var arenaResults: [ArenaResult] = []

    // All Hands
    @Published var allHandsRunning = false
    @Published var allHandsResults: [AllHandsResult] = []
    @Published var allHandsSummary: (bbPer100: Double, winRate: Double, profit: Double, hands: Int, profitable: Int, total: Int)?
    @Published var evGroups: [EVGroupResult] = []

    // Battery
    @Published var batteryRunning = false
    @Published var batteryResults: [BatteryResultItem] = []
    @Published var batteryScore: Double = 0
    @Published var batteryTotal: Int = 0
    @Published var batteryPassed: Int = 0

    @Published var statusMessage = ""

    private var baseURL: String { serverManager?.baseURL ?? "http://127.0.0.1:5060" }

    // MARK: - Model

    func fetchModelInfo() {
        get("/api/model/info") { [weak self] result in
            guard let json = result as? [String: Any] else { return }
            DispatchQueue.main.async {
                self?.modelLoaded = json["loaded"] as? Bool ?? false
                self?.modelFilename = json["filename"] as? String ?? ""
                self?.modelParams = json["parameters"] as? Int ?? 0
                self?.modelIterations = json["iterations"] as? Int ?? 0
            }
        }
    }

    func loadModel(path: String) {
        post("/api/model/load", body: ["path": path]) { [weak self] result in
            guard let json = result as? [String: Any] else { return }
            DispatchQueue.main.async {
                if json["error"] != nil {
                    self?.statusMessage = "Failed to load model"
                } else {
                    self?.modelLoaded = true
                    self?.modelFilename = json["filename"] as? String ?? ""
                    self?.modelParams = json["parameters"] as? Int ?? 0
                    self?.modelIterations = json["iterations"] as? Int ?? 0
                    self?.statusMessage = "Model loaded: \(self?.modelFilename ?? "")"
                }
            }
        }
    }

    // MARK: - Arena

    func runArena(opponent: String, numHands: Int, handScope: String?, singleHand: String?) {
        guard !arenaRunning else { return }
        arenaRunning = true
        statusMessage = "Running \(numHands) hands vs \(opponent)..."

        var body: [String: Any] = [
            "opponent": opponent,
            "num_hands": numHands,
        ]
        if let scope = handScope { body["hand_scope"] = scope }
        if let hand = singleHand { body["single_hand"] = hand }

        post("/api/arena/run", body: body) { [weak self] result in
            guard let json = result as? [String: Any] else {
                DispatchQueue.main.async {
                    self?.arenaRunning = false
                    self?.statusMessage = "Arena test failed"
                }
                return
            }
            DispatchQueue.main.async {
                var histories: [HandHistoryEntry] = []
                if let rawHH = json["hand_histories"] as? [[String: Any]] {
                    for hh in rawHH {
                        histories.append(HandHistoryEntry(
                            handNum: hh["hand_num"] as? Int ?? 0,
                            heroStart: hh["hero_start"] as? String ?? "?",
                            villainStart: hh["villain_start"] as? String ?? "?",
                            heroDoor: hh["hero_door"] as? String ?? "?",
                            villainDoor: hh["villain_door"] as? String ?? "?",
                            heroFinal: hh["hero_final"] as? String ?? "?",
                            villainFinal: hh["villain_final"] as? String ?? "?",
                            result: hh["result"] as? String ?? "?",
                            payoff: hh["payoff"] as? Double ?? 0,
                            heroFolded: hh["hero_folded"] as? Bool ?? false,
                            actions: hh["actions"] as? [String] ?? [],
                            pot: hh["pot"] as? Double ?? 0
                        ))
                    }
                }

                let result = ArenaResult(
                    opponent: json["opponent"] as? String ?? opponent,
                    numHands: json["num_hands"] as? Int ?? numHands,
                    winRate: json["win_rate"] as? Double ?? 0,
                    bbPer100: json["bb_per_100"] as? Double ?? 0,
                    foldRate: json["fold_rate"] as? Double ?? 0,
                    sdWinRate: json["sd_win_rate"] as? Double ?? 0,
                    handHistories: histories
                )
                self?.arenaResults.append(result)
                self?.arenaRunning = false
                self?.statusMessage = "\(result.winRate)% win, \(String(format: "%+.1f", result.bbPer100)) BB/100 vs \(opponent)"
            }
        }
    }

    // MARK: - All Hands

    func runAllHands(opponent: String, handsPerCombo: Int) {
        guard !allHandsRunning else { return }
        allHandsRunning = true
        allHandsResults = []
        evGroups = []
        allHandsSummary = nil
        statusMessage = "Running All Hands Test (455 combos x \(handsPerCombo))..."

        let body: [String: Any] = [
            "opponent": opponent,
            "hands_per_combo": handsPerCombo,
        ]

        post("/api/arena/all-hands", body: body, timeout: 600) { [weak self] result in
            guard let json = result as? [String: Any] else {
                DispatchQueue.main.async {
                    self?.allHandsRunning = false
                    self?.statusMessage = "All Hands Test failed"
                }
                return
            }
            DispatchQueue.main.async {
                // Parse per-hand results
                if let rawResults = json["results"] as? [[String: Any]] {
                    self?.allHandsResults = rawResults.map { r in
                        AllHandsResult(
                            hand: r["hand"] as? String ?? "?",
                            bucket: r["bucket"] as? String ?? "?",
                            handsPlayed: r["hands_played"] as? Int ?? 0,
                            winRate: r["win_rate"] as? Double ?? 0,
                            bbPer100: r["bb_per_100"] as? Double ?? 0,
                            foldRate: r["fold_rate"] as? Double ?? 0,
                            sdWinRate: r["sd_win_rate"] as? Double ?? 0,
                            profit: r["profit"] as? Double ?? 0,
                            evPct: r["ev_pct"] as? Double ?? 0,
                            delta: r["delta"] as? Double ?? 0
                        )
                    }
                }

                // Summary
                self?.allHandsSummary = (
                    bbPer100: json["bb_per_100"] as? Double ?? 0,
                    winRate: json["win_rate"] as? Double ?? 0,
                    profit: json["total_profit"] as? Double ?? 0,
                    hands: json["total_hands"] as? Int ?? 0,
                    profitable: json["profitable_hands"] as? Int ?? 0,
                    total: json["total_combos"] as? Int ?? 0
                )

                // EV groups
                if let rawGroups = json["ev_groups"] as? [[String: Any]] {
                    self?.evGroups = rawGroups.map { g in
                        EVGroupResult(
                            name: g["name"] as? String ?? "?",
                            count: g["count"] as? Int ?? 0,
                            winRate: g["win_rate"] as? Double ?? 0,
                            bbPer100: g["bb_per_100"] as? Double ?? 0,
                            profit: g["profit"] as? Double ?? 0,
                            profitable: g["profitable"] as? Int ?? 0
                        )
                    }
                }

                let elapsed = json["elapsed_seconds"] as? Double ?? 0
                self?.allHandsRunning = false
                self?.statusMessage = "All Hands: \(String(format: "%+.1f", json["bb_per_100"] as? Double ?? 0)) BB/100 (\(Int(elapsed))s)"
            }
        }
    }

    // MARK: - Battery

    func runBattery() {
        guard !batteryRunning else { return }
        batteryRunning = true
        statusMessage = "Running battery test..."

        post("/api/battery", body: [:]) { [weak self] result in
            guard let json = result as? [String: Any] else {
                DispatchQueue.main.async {
                    self?.batteryRunning = false
                    self?.statusMessage = "Battery test failed"
                }
                return
            }
            DispatchQueue.main.async {
                self?.batteryTotal = json["total"] as? Int ?? 0
                self?.batteryPassed = json["passed"] as? Int ?? 0
                self?.batteryScore = (json["score"] as? Double ?? 0) / 100.0

                if let rawResults = json["results"] as? [[String: Any]] {
                    self?.batteryResults = rawResults.map { r in
                        BatteryResultItem(
                            name: r["name"] as? String ?? "?",
                            tier: r["tier"] as? Int ?? 0,
                            passed: r["passed"] as? Bool ?? false,
                            predicted: r["predicted"] as? String ?? "?",
                            expected: r["expected"] as? [String] ?? [],
                            confidence: r["confidence"] as? Double ?? 0
                        )
                    }
                }

                self?.batteryRunning = false
                self?.statusMessage = "Battery: \(self?.batteryPassed ?? 0)/\(self?.batteryTotal ?? 0)"
            }
        }
    }

    // MARK: - HTTP

    func post(_ path: String, body: [String: Any], timeout: TimeInterval = 120, completion: @escaping (Any?) -> Void) {
        guard let url = URL(string: "\(baseURL)\(path)") else { return }
        var req = URLRequest(url: url, timeoutInterval: timeout)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: req) { data, _, error in
            guard let data = data, error == nil,
                  let json = try? JSONSerialization.jsonObject(with: data) else {
                completion(nil)
                return
            }
            completion(json)
        }.resume()
    }

    func get(_ path: String, completion: @escaping (Any?) -> Void) {
        guard let url = URL(string: "\(baseURL)\(path)") else { return }
        URLSession.shared.dataTask(with: url) { data, _, error in
            guard let data = data, error == nil,
                  let json = try? JSONSerialization.jsonObject(with: data) else {
                completion(nil)
                return
            }
            completion(json)
        }.resume()
    }
}
