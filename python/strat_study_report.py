"""Markdown report for strat_study.py output (results/strat_trades.csv, results/strat_transitions.csv)."""
import math

import pandas as pd

tr = pd.read_csv("results/strat_trades.csv")
tn = pd.read_csv("results/strat_transitions.csv")
TFS = ["15m", "1h", "4h", "1d"]
COMBOS = ["2-1-2 Cont", "2-1-2 Rev", "3-1-2", "1-2-2 RevStrat", "3-2-2 Rev", "2-2 Rev", "Baseline (any candle)"]
L = []


def f(v, fmt="{:+.2f}"):
    return "–" if v is None or (isinstance(v, float) and math.isnan(v)) else fmt.format(v)


def table(h, rows):
    L.append("| " + " | ".join(h) + " |")
    L.append("|" + "|".join("---" for _ in h) + "|")
    L.extend("| " + " | ".join(r) + " |" for r in rows)
    L.append("")


def winrate(s):
    s = s[s != 0]
    return (s == 1).mean() * 100 if len(s) else math.nan


L.append("# The Strat — statistical study (BTC, ETH, AVAX, XRP · 15m / 1h / 4h / 1D)\n")
L.append("Candle types vs the previous candle: **1** inside, **2u** new high only, **2d** new low only, **3** outside. "
         "Combos trigger on the next candle only, through the last candle's high (long) or low (short). Stop = the other "
         "end of the trigger candle. **Magnitude** target = nearest earlier high/low beyond the entry in the last 10 "
         "candles (2R if none). Results are net of Bybit VIP 3 futures fees and funding, in R per trade. "
         "IS = first 70% of each history, OOS = last 30%. **Baseline** = break of ANY previous candle's high/low with the "
         "same stop and targets — a combo only matters if it beats this.\n")

# ── A. candle types
L.append("## A. Candle types — how often, and what comes next (all coins, all periods)\n")
rows = []
for tf in TFS:
    s = tn[tn.tf == tf].groupby("to").n.sum()
    tot = s.sum()
    rows.append([tf] + [f"{s.get(k, 0) / tot * 100:.1f}%" for k in ["1", "2u", "2d", "3"]])
table(["TF", "1 (inside)", "2u", "2d", "3 (outside)"], rows)
L.append("**What follows each candle type** (probability of the next candle's type; 1h, all coins):\n")
rows = []
for tf in ("1h", "4h"):
    s = tn[tn.tf == tf].groupby(["frm", "to"]).n.sum().unstack(fill_value=0)
    for fr in ["1", "2u", "2d", "3"]:
        if fr in s.index:
            r = s.loc[fr] / s.loc[fr].sum() * 100
            rows.append([tf, fr] + [f"{r.get(k, 0):.0f}%" for k in ["1", "2u", "2d", "3"]])
table(["TF", "After a…", "→ 1", "→ 2u", "→ 2d", "→ 3"], rows)

# ── B. combos
for tgt, title in (("mag", "magnitude target"), ("2R", "2R target")):
    L.append(f"## B. Combo results — {title} (all coins pooled; avg net R per trade, IS / OOS)\n")
    rows = []
    for combo in COMBOS:
        cells = [combo]
        for tf in TFS:
            s = tr[(tr.combo == combo) & (tr.tf == tf)]
            a, b = s[s.period == "IS"], s[s.period == "OOS"]
            cells.append(f"{f(a[f'r_{tgt}'].mean())} / {f(b[f'r_{tgt}'].mean())}  (n={len(s)}, win {winrate(s[f'hit_{tgt}']):.0f}%)")
        rows.append(cells)
    table(["Combo"] + TFS, rows)
L.append("Median magnitude-target size (in R) per combo: " + ", ".join(
    f"{c} {tr[tr.combo == c].mag_r.median():.2f}R" for c in COMBOS) + ". Median stop size: " +
    ", ".join(f"{tf} {tr[tr.tf == tf].risk_pct.median():.2f}%" for tf in TFS) + ".\n")

# ── C. FTFC
L.append("## C. Does Full Timeframe Continuity help? (avg net R per trade, 2R target, IS / OOS)\n")
L.append("FTFC **with** = entry beyond the open of the current candle on every higher timeframe in the trade's direction "
         "(15m: 1h/4h/D · 1h: 4h/D/W · 4h: D/W/M · 1D: W/M); **against** = the opposite on all; **mixed** = otherwise.\n")
for tf in TFS:
    L.append(f"**{tf}**\n")
    rows = []
    for combo in COMBOS:
        s = tr[(tr.combo == combo) & (tr.tf == tf)]
        cells = [combo]
        for ft in ("with", "mixed", "against"):
            x = s[s.ftfc == ft]
            a, b = x[x.period == "IS"].r_2R.mean(), x[x.period == "OOS"].r_2R.mean()
            cells.append(f"{f(a)} / {f(b)} (n={len(x)})")
        rows.append(cells)
    table(["Combo", "FTFC with", "Mixed", "FTFC against"], rows)

# ── D. per coin, best-looking cells
L.append("## D. Per coin — combos with FTFC 'with', 2R target, OOS avg net R (n)\n")
rows = []
for tf in TFS:
    for combo in COMBOS:
        cells = [tf, combo]
        for coin in ("btc", "eth", "avax", "xrp"):
            x = tr[(tr.tf == tf) & (tr.combo == combo) & (tr.coin == coin) & (tr.ftfc == "with") & (tr.period == "OOS")]
            cells.append(f"{f(x.r_2R.mean())} ({len(x)})" if len(x) >= 10 else "–")
        rows.append(cells)
table(["TF", "Combo", "BTC", "ETH", "AVAX", "XRP"], rows)

with open("results/strat_study.md", "w") as fh:
    fh.write("\n".join(L) + "\n")
print("wrote results/strat_study.md")
