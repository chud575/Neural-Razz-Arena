import SwiftUI

struct ContentView: View {
    @ObservedObject var serverManager: ServerManager
    @ObservedObject var vm: ArenaViewModel

    @State private var opponent = "pure_ev"
    @State private var handScope = "allHands"
    @State private var singleHand = ""
    @State private var numHands = 5000
    @State private var handsPerCombo = 100
    @State private var showHandHistory = false
    @State private var showModelPicker = false

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                serverCard
                modelCard
                configCard
                if vm.arenaRunning || vm.allHandsRunning || vm.batteryRunning {
                    ProgressView(vm.statusMessage).padding()
                }
                if !vm.arenaResults.isEmpty { arenaResultsCard }
                if let summary = vm.allHandsSummary { allHandsSummaryCard(summary) }
                if !vm.evGroups.isEmpty { evGroupCard }
                if !vm.allHandsResults.isEmpty { allHandsTableCard }
                if !vm.batteryResults.isEmpty { batteryCard }
                serverLogCard
            }
            .padding()
        }
        .frame(minWidth: 900, minHeight: 600)
        .fileImporter(isPresented: $showModelPicker, allowedContentTypes: [.json], allowsMultipleSelection: false) { result in
            if case .success(let urls) = result, let url = urls.first {
                let accessing = url.startAccessingSecurityScopedResource()
                vm.loadModel(path: url.path)
                if accessing { url.stopAccessingSecurityScopedResource() }
            }
        }
    }

    // MARK: - Server Status

    private var serverCard: some View {
        HStack {
            Circle().fill(serverManager.isHealthy ? .green : .orange).frame(width: 12, height: 12)
            Text(serverManager.isHealthy ? "Backend Server Running" : "Connecting...")
                .font(.headline)
            Spacer()
            if !vm.statusMessage.isEmpty {
                Text(vm.statusMessage).font(.caption).foregroundColor(.secondary)
            }
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - Model

    private var modelCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("Model").font(.headline)
                Spacer()
                if vm.modelLoaded {
                    Image(systemName: "checkmark.circle.fill").foregroundColor(.green)
                }
            }

            if vm.modelLoaded {
                HStack(spacing: 20) {
                    VStack(alignment: .leading) {
                        Text(vm.modelFilename).font(.caption.bold())
                        Text("\(vm.modelParams.formatted()) params, \(vm.modelIterations.formatted()) iterations")
                            .font(.caption).foregroundColor(.secondary)
                    }
                    Spacer()
                    Button("Load Different...") { showModelPicker = true }
                        .buttonStyle(.bordered).controlSize(.small)
                }
            } else {
                HStack {
                    Button("Load Model...") { showModelPicker = true }
                        .buttonStyle(.borderedProminent)
                    Button("Auto-Load") { vm.fetchModelInfo() }
                        .buttonStyle(.bordered)
                    Spacer()
                    Text("Place neural_razz_strategy.json next to the app")
                        .font(.caption).foregroundColor(.secondary)
                }
            }
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - Config

    private var configCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Arena Test").font(.headline)

            HStack {
                Text("Opponent").frame(width: 80, alignment: .leading).font(.caption)
                Picker("", selection: $opponent) {
                    Text("Pure EV").tag("pure_ev")
                    Text("TAG").tag("tag")
                    Text("LAG").tag("lag")
                    Text("ReBeL").tag("rebel")
                    Text("Pure CFR").tag("bucketed_cfr")
                    Text("Calling Station").tag("calling_station")
                    Text("Random").tag("random")
                }.pickerStyle(.menu).frame(width: 150)
            }

            HStack {
                Text("Hero Hands").frame(width: 80, alignment: .leading).font(.caption)
                Picker("", selection: $handScope) {
                    Text("All Hands (455)").tag("allHands")
                    Text("Premium (56)").tag("premium")
                    Text("Top 50% (220)").tag("top50")
                    Divider()
                    Text("G1: Elite 70%+").tag("ev_group_1")
                    Text("G2: Strong 60-70%").tag("ev_group_2")
                    Text("G3: Good 50-60%").tag("ev_group_3")
                    Text("G4: Playable 45-50%").tag("ev_group_4")
                    Text("G5: Marginal 40-45%").tag("ev_group_5")
                    Text("G6: Weak 35-40%").tag("ev_group_6")
                    Text("G7: Bad 25-35%").tag("ev_group_7")
                    Text("G8: Trash <25%").tag("ev_group_8")
                    Divider()
                    Text("Single Hand").tag("single")
                }.pickerStyle(.menu).frame(width: 180)
            }

            if handScope == "single" {
                HStack {
                    Text("Hand").frame(width: 80, alignment: .leading).font(.caption)
                    TextField("e.g. A23, 369", text: $singleHand)
                        .textFieldStyle(.roundedBorder).frame(width: 120)
                }
            }

            HStack {
                Text("Hands").frame(width: 80, alignment: .leading).font(.caption)
                ForEach([1000, 5000, 10000, 25000], id: \.self) { n in
                    Button(n >= 10000 ? "\(n/1000)K" : n == 1000 ? "1K" : "5K") { numHands = n }
                        .buttonStyle(.bordered).controlSize(.small)
                        .tint(numHands == n ? .accentColor : .secondary)
                }
            }

            Divider()

            HStack(spacing: 12) {
                Button(action: {
                    let scope = handScope == "single" ? nil : handScope
                    let single = handScope == "single" ? singleHand : nil
                    vm.runArena(opponent: opponent, numHands: numHands, handScope: scope, singleHand: single)
                }) {
                    Label("Run Arena", systemImage: "play.fill")
                }
                .buttonStyle(.borderedProminent).tint(.blue)
                .disabled(!vm.modelLoaded || vm.arenaRunning || vm.allHandsRunning)

                Button(action: { vm.runBattery() }) {
                    Label("Battery", systemImage: "checklist")
                }
                .buttonStyle(.bordered).tint(.orange)
                .disabled(!vm.modelLoaded || vm.batteryRunning)

                Divider().frame(height: 20)

                HStack {
                    Text("Per combo:").font(.caption)
                    ForEach([100, 500, 1000], id: \.self) { n in
                        Button("\(n)") { handsPerCombo = n }
                            .buttonStyle(.bordered).controlSize(.mini)
                            .tint(handsPerCombo == n ? .purple : .secondary)
                    }
                }

                Button(action: { vm.runAllHands(opponent: opponent, handsPerCombo: handsPerCombo) }) {
                    Label("All Hands Test", systemImage: "tablecells")
                }
                .buttonStyle(.borderedProminent).tint(.purple)
                .disabled(!vm.modelLoaded || vm.allHandsRunning || vm.arenaRunning)
            }
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - Arena Results

    private var arenaResultsCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("Arena Results").font(.headline)
                Spacer()
                if let last = vm.arenaResults.last, !last.handHistories.isEmpty {
                    Button(showHandHistory ? "Hide" : "Hand History") { showHandHistory.toggle() }
                        .buttonStyle(.bordered).controlSize(.small)
                }
            }

            ForEach(vm.arenaResults.suffix(8)) { r in
                HStack {
                    Text(r.opponent.replacingOccurrences(of: "_", with: " ").capitalized)
                        .font(.system(.caption, design: .monospaced)).frame(width: 120, alignment: .leading)
                    Text(String(format: "Win: %.1f%%", r.winRate))
                        .font(.system(.caption, design: .monospaced))
                        .foregroundColor(r.winRate > 50 ? .green : .red).frame(width: 80)
                    Text(String(format: "BB/100: %+.1f", r.bbPer100))
                        .font(.system(.caption, design: .monospaced))
                        .foregroundColor(r.bbPer100 > 0 ? .green : .red).frame(width: 100)
                    Text(String(format: "Fold: %.1f%%", r.foldRate))
                        .font(.system(.caption, design: .monospaced)).frame(width: 70)
                    Text(String(format: "SD Win: %.1f%%", r.sdWinRate))
                        .font(.system(.caption, design: .monospaced)).frame(width: 90)
                    Text("\(r.numHands) hands")
                        .font(.caption2).foregroundColor(.secondary)
                }
            }

            if showHandHistory, let last = vm.arenaResults.last {
                Divider()
                ScrollView {
                    VStack(alignment: .leading, spacing: 4) {
                        ForEach(last.handHistories.prefix(50)) { hh in
                            VStack(alignment: .leading, spacing: 2) {
                                HStack {
                                    Text("#\(hh.handNum)").font(.system(size: 10, design: .monospaced)).foregroundColor(.secondary).frame(width: 40, alignment: .leading)
                                    Text("Hero: \(hh.heroStart)").font(.system(size: 10, design: .monospaced).bold()).foregroundColor(.blue)
                                    Text("vs \(hh.villainDoor)").font(.system(size: 10, design: .monospaced)).foregroundColor(.red)
                                    Spacer()
                                    Text(hh.result).font(.system(size: 10, design: .monospaced).bold())
                                        .foregroundColor(hh.payoff > 0 ? .green : .red)
                                    Text(String(format: "%+.1f", hh.payoff)).font(.system(size: 10, design: .monospaced))
                                        .foregroundColor(hh.payoff > 0 ? .green : .red).frame(width: 40, alignment: .trailing)
                                }
                                ForEach(Array(hh.actions.enumerated()), id: \.offset) { _, action in
                                    Text(action).font(.system(size: 9, design: .monospaced)).foregroundColor(.secondary).padding(.leading, 44)
                                }
                                Divider().opacity(0.3)
                            }
                        }
                    }
                }.frame(maxHeight: 400)
            }
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - All Hands Summary

    private func allHandsSummaryCard(_ s: (bbPer100: Double, winRate: Double, profit: Double, hands: Int, profitable: Int, total: Int)) -> some View {
        VStack(spacing: 12) {
            Text("All Hands Test").font(.headline)
            HStack(spacing: 40) {
                VStack { Text("BB/100").font(.caption).foregroundColor(.secondary); Text(String(format: "%+.2f", s.bbPer100)).font(.title2.bold()).foregroundColor(s.bbPer100 >= 0 ? .green : .red) }
                VStack { Text("Win Rate").font(.caption).foregroundColor(.secondary); Text(String(format: "%.1f%%", s.winRate)).font(.title2.bold()).foregroundColor(.blue) }
                VStack { Text("Profit").font(.caption).foregroundColor(.secondary); Text(String(format: "%+.0f", s.profit)).font(.title2.bold()).foregroundColor(s.profit >= 0 ? .green : .red) }
                VStack { Text("Hands").font(.caption).foregroundColor(.secondary); Text(s.hands.formatted()).font(.title2.bold()) }
            }
            Text("Profitable: \(s.profitable)/\(s.total)").font(.caption).foregroundColor(s.profitable > s.total / 2 ? .green : .orange)
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - EV Groups

    private var evGroupCard: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Results by EV Group").font(.headline)
            HStack(spacing: 0) {
                Text("Group").font(.caption).foregroundColor(.secondary).frame(width: 150, alignment: .leading)
                Text("Hands").font(.caption).foregroundColor(.secondary).frame(width: 50, alignment: .trailing)
                Text("WR%").font(.caption).foregroundColor(.secondary).frame(width: 50, alignment: .trailing)
                Text("BB/100").font(.caption).foregroundColor(.secondary).frame(width: 70, alignment: .trailing)
                Text("Profit").font(.caption).foregroundColor(.secondary).frame(width: 80, alignment: .trailing)
                Text("Prof#").font(.caption).foregroundColor(.secondary).frame(width: 60, alignment: .trailing)
            }
            ForEach(vm.evGroups) { g in
                HStack(spacing: 0) {
                    Text(g.name).font(.system(.caption, design: .monospaced)).frame(width: 150, alignment: .leading)
                    Text("\(g.count)").font(.system(.caption, design: .monospaced)).frame(width: 50, alignment: .trailing)
                    Text(String(format: "%.0f%%", g.winRate)).font(.system(.caption, design: .monospaced)).frame(width: 50, alignment: .trailing)
                    Text(String(format: "%+.1f", g.bbPer100)).font(.system(.caption, design: .monospaced))
                        .foregroundColor(g.bbPer100 >= 0 ? .green : .red).frame(width: 70, alignment: .trailing)
                    Text(String(format: "%+.0f", g.profit)).font(.system(.caption, design: .monospaced))
                        .foregroundColor(g.profit >= 0 ? .green : .red).frame(width: 80, alignment: .trailing)
                    Text("\(g.profitable)/\(g.count)").font(.system(.caption, design: .monospaced))
                        .foregroundColor(g.profitable > g.count / 2 ? .green : .red).frame(width: 60, alignment: .trailing)
                }
            }
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - All Hands Table

    private var allHandsTableCard: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Per-Hand Results (sorted by MC-EV)").font(.headline)

            HStack(spacing: 0) {
                Text("#").font(.caption).foregroundColor(.secondary).frame(width: 30, alignment: .trailing)
                Text("Hand").font(.caption).foregroundColor(.secondary).frame(width: 50, alignment: .leading).padding(.leading, 8)
                Text("Bucket").font(.caption).foregroundColor(.secondary).frame(width: 50, alignment: .center)
                Text("Hands").font(.caption).foregroundColor(.secondary).frame(width: 55, alignment: .trailing)
                Text("Win%").font(.caption).foregroundColor(.secondary).frame(width: 55, alignment: .trailing)
                Text("EV%").font(.caption).foregroundColor(.secondary).frame(width: 50, alignment: .trailing)
                Text("Delta").font(.caption).foregroundColor(.secondary).frame(width: 60, alignment: .trailing)
                Text("BB/100").font(.caption).foregroundColor(.secondary).frame(width: 65, alignment: .trailing)
                Text("Profit").font(.caption).foregroundColor(.secondary).frame(width: 70, alignment: .trailing)
            }
            Divider()

            ScrollView {
                LazyVStack(spacing: 1) {
                    ForEach(Array(vm.allHandsResults.enumerated()), id: \.element.id) { i, r in
                        HStack(spacing: 0) {
                            Text("\(i+1)").font(.system(size: 10, design: .monospaced)).foregroundColor(.secondary).frame(width: 30, alignment: .trailing)
                            Text(r.hand).font(.system(size: 10, design: .monospaced).bold()).frame(width: 50, alignment: .leading).padding(.leading, 8)
                            Text(r.bucket).font(.system(size: 10, design: .monospaced)).foregroundColor(.blue).frame(width: 50, alignment: .center)
                            Text("\(r.handsPlayed)").font(.system(size: 10, design: .monospaced)).frame(width: 55, alignment: .trailing)
                            Text(String(format: "%.1f%%", r.winRate)).font(.system(size: 10, design: .monospaced)).frame(width: 55, alignment: .trailing)
                            Text(String(format: "%.1f%%", r.evPct)).font(.system(size: 10, design: .monospaced)).foregroundColor(.secondary).frame(width: 50, alignment: .trailing)
                            Text(String(format: "%+.1f%%", r.delta)).font(.system(size: 10, design: .monospaced))
                                .foregroundColor(r.delta >= 0 ? .green : .red)
                                .fontWeight(abs(r.delta) > 5 ? .bold : .regular)
                                .frame(width: 60, alignment: .trailing)
                            Text(String(format: "%+.1f", r.bbPer100)).font(.system(size: 10, design: .monospaced))
                                .foregroundColor(r.bbPer100 >= 0 ? .green : .red).frame(width: 65, alignment: .trailing)
                            Text(String(format: "%+.0f", r.profit)).font(.system(size: 10, design: .monospaced))
                                .foregroundColor(r.profit >= 0 ? .green : .red).frame(width: 70, alignment: .trailing)
                        }
                        .padding(.vertical, 2)
                        .background(r.bbPer100 >= 0 ? Color.green.opacity(0.03) : Color.red.opacity(0.03))
                    }
                }
            }
            .frame(maxHeight: 500)
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - Battery

    private var batteryCard: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                Text("Battery Results").font(.headline)
                Spacer()
                Text("\(vm.batteryPassed)/\(vm.batteryTotal) (\(Int(vm.batteryScore * 100))%)")
                    .font(.caption.bold())
                    .foregroundColor(vm.batteryScore >= 0.9 ? .green : vm.batteryScore >= 0.7 ? .orange : .red)
            }

            ForEach(vm.batteryResults) { r in
                HStack {
                    Image(systemName: r.passed ? "checkmark.circle.fill" : "xmark.circle.fill")
                        .foregroundColor(r.passed ? .green : .red).font(.caption)
                    Text("T\(r.tier)").font(.system(size: 10, design: .monospaced)).foregroundColor(.secondary).frame(width: 20)
                    Text(r.name).font(.system(size: 10)).lineLimit(1)
                    Spacer()
                    Text(r.predicted.uppercased()).font(.system(size: 10, design: .monospaced).bold())
                        .foregroundColor(r.passed ? .green : .red).frame(width: 60, alignment: .trailing)
                    Text("\(Int(r.confidence))%").font(.system(size: 10, design: .monospaced))
                        .foregroundColor(.secondary).frame(width: 35, alignment: .trailing)
                }
            }
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }

    // MARK: - Server Log

    private var serverLogCard: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                Text("Server Log").font(.headline)
                Spacer()
                Button("Clear") { serverManager.serverLog.removeAll() }
                    .buttonStyle(.bordered).controlSize(.mini)
            }
            ScrollView {
                VStack(alignment: .leading, spacing: 1) {
                    ForEach(serverManager.serverLog.suffix(20), id: \.self) { line in
                        Text(line).font(.system(size: 10, design: .monospaced)).foregroundColor(.secondary)
                    }
                }
            }
            .frame(maxHeight: 120)
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 10).fill(.ultraThinMaterial))
    }
}
