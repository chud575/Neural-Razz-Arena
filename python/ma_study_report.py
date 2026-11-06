"""Turn ma_study.py output into a markdown report: move sizes in ATR, edge vs baseline, feature consistency."""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

ev = pd.read_csv("results/ma_study_events.csv")
base = pd.read_csv("results/ma_study_baseline.csv")
TFS = ["15m", "1h", "4h", "1d"]
TG = [1, 1.5, 2, 3, 4, 5]
L = []


def f(v, fmt="{:+.2f}"):
    return "–" if v is None or (isinstance(v, float) and math.isnan(v)) else fmt.format(v)


def hit_rate(s):
    s = s[s != 0]
    return (s == 1).mean() * 100 if len(s) else math.nan


def table(header, rows):
    L.append("| " + " | ".join(header) + " |")
    L.append("|" + "|".join("---" for _ in header) + "|")
    for r in rows:
        L.append("| " + " | ".join(r) + " |")
    L.append("")


L.append("# SMA 50/100/200 — Idea 1: wick below the SMA 200 and close back above, in an uptrend\n")
L.append("Coins BTC, ETH, AVAX, XRP (Coinbase; XRP from Jul 2023). Event: SMA100 above SMA200 for ≥ N bars, previous "
         "close above the SMA200, a wick below it, and a close back above (same bar: K=0, or within 5 bars: K=5). Entry at "
         "that close. ATR = ATR(14) at entry. Stop for the hit-rate and trade numbers = lowest low of the touch − 0.1 ATR. "
         "**Baseline** = every bar in the same uptrend regime above the SMA200, with a stop at the same ATR distance. "
         "Trade results are net of Bybit VIP 3 futures costs. IS = first 70% of each history, OOS = last 30%.\n")

# ── 1. How far does it move?
L.append("## 1. How far does price move after the reclaim? (longs, N = 50, all coins pooled)\n")
rows = []
for tf in TFS:
    for K in (0, 5):
        e = ev[(ev.tf == tf) & (ev.side == "long") & (ev.N == 50) & (ev.K == K)]
        b = base[(base.tf == tf) & (base.side == "long") & (base.N == 50)]
        if not len(e):
            continue
        rows.append([tf, "same bar" if K == 0 else "within 5", f"{len(e)}", f(e.stop_atr.median(), "{:.2f}"),
                     f(e.mfe20.median(), "{:.2f}") + f" ({f(b.mfe20.median(), '{:.2f}')})",
                     f(e.mae20.median(), "{:.2f}") + f" ({f(b.mae20.median(), '{:.2f}')})",
                     f(e.mfe100.median(), "{:.2f}") + f" ({f(b.mfe100.median(), '{:.2f}')})",
                     f(e.mae100.median(), "{:.2f}") + f" ({f(b.mae100.median(), '{:.2f}')})"])
table(["TF", "Reclaim", "Events", "Median stop (ATR)", "Median best move, 20 bars (baseline)", "Median worst move, 20 bars",
       "Median best move, 100 bars", "Median worst move, 100 bars"], rows)

L.append("## 2. How often does it reach +k ATR before the stop? (longs, N = 50, same-bar reclaim; baseline in brackets)\n")
rows = []
for tf in TFS:
    e = ev[(ev.tf == tf) & (ev.side == "long") & (ev.N == 50) & (ev.K == 0)]
    b = base[(base.tf == tf) & (base.side == "long") & (base.N == 50)]
    if not len(e):
        continue
    rows.append([tf, f"{len(e)}"] + [f"{hit_rate(e[f'hit{k}']):.0f}% ({hit_rate(b[f'hit{k}']):.0f}%)" for k in TG])
table(["TF", "Events"] + [f"+{k:g} ATR" for k in TG], rows)

L.append("## 3. Trade result: target +k ATR, stop under the wick, net of fees (avg R per trade; baseline in brackets)\n")
for side in ("long", "short"):
    L.append(f"**{side.title()}s** (N = 50, same-bar reclaim)\n")
    rows = []
    for tf in TFS:
        for per in ("IS", "OOS"):
            e = ev[(ev.tf == tf) & (ev.side == side) & (ev.N == 50) & (ev.K == 0) & (ev.period == per)]
            b = base[(base.tf == tf) & (base.side == side) & (base.N == 50) & (base.period == per)]
            if len(e) < 10:
                continue
            rows.append([tf, per, f"{len(e)}"] + [f"{f(e[f'r{k}'].mean())} ({f(b[f'r{k}'].mean())})" for k in TG])
    table(["TF", "Period", "Events"] + [f"+{k:g} ATR" for k in TG], rows)

# ── 4. Consistency per coin
L.append("## 4. Per coin (longs, N = 50, same-bar reclaim, target +3 ATR): event minus baseline, net R\n")
rows = []
for tf in TFS:
    cells = [tf]
    for coin in ("btc", "eth", "avax", "xrp"):
        parts = []
        for per in ("IS", "OOS"):
            e = ev[(ev.tf == tf) & (ev.coin == coin) & (ev.side == "long") & (ev.N == 50) & (ev.K == 0) & (ev.period == per)]
            b = base[(base.tf == tf) & (base.coin == coin) & (base.side == "long") & (base.N == 50) & (base.period == per)]
            parts.append(f"{f(e.r3.mean() - b.r3.mean())} (n={len(e)})" if len(e) >= 5 else "–")
        cells.append(" / ".join(parts))
    rows.append(cells)
table(["TF", "BTC IS / OOS", "ETH IS / OOS", "AVAX IS / OOS", "XRP IS / OOS"], rows)

# ── 5. Feature buckets
L.append("## 5. What makes it better or worse? (longs, N = 50, both reclaim modes, target +3 ATR, net R per trade)\n")
L.append("Each cell: IS / OOS average for events in that bucket. A feature is only interesting if it moves results the "
         "same way in-sample and out-of-sample, on most timeframes and coins (last column = how many of the 16 "
         "coin × timeframe cells, OOS, are above the overall average for that cell).\n")
e_all = ev[(ev.side == "long") & (ev.N == 50)].copy()
e_all["trend_bucket"] = pd.cut(e_all.trend_bars, [0, 100, 200, 400, 10 ** 9], labels=["50–100", "100–200", "200–400", "400+"])
e_all["depth_bucket"] = pd.cut(e_all.depth_atr, [-1, 0.25, 0.5, 1.0, 100], labels=["<0.25", "0.25–0.5", "0.5–1", ">1"])
e_all["slope_bucket"] = pd.cut(e_all.slope200_atr, [-100, 0, 0.5, 1.5, 100], labels=["falling", "flat 0–0.5", "rising 0.5–1.5", "steep >1.5"])
e_all["gap_bucket"] = pd.cut(e_all.gap100_200_atr, [-100, 1, 3, 6, 1000], labels=["<1", "1–3", "3–6", ">6"])
e_all["recency"] = pd.cut(e_all.bars_since_touch, [-1, 20, 100, 10 ** 9], labels=["<20 bars", "20–100", ">100 (fresh)"])
feats = [("white_crossed", "SMA50 below SMA100 at the touch (white crossed yellow)"),
         ("white_below_200", "SMA50 below SMA200 at the touch"),
         ("same_bar", "Reclaimed on the same candle"),
         ("first_touch", "First 200-touch in this trend"),
         ("trend_bucket", "Bars the uptrend has lasted"),
         ("depth_bucket", "Wick depth below the 200 (ATR)"),
         ("slope_bucket", "SMA200 slope over 20 bars (ATR)"),
         ("gap_bucket", "SMA100–SMA200 gap (ATR)"),
         ("recency", "Bars since the previous touch")]
cell_avg = e_all.groupby(["coin", "tf", "period"]).r3.mean()
for col, title in feats:
    L.append(f"**{title}**\n")
    rows = []
    for val in [v for v in e_all[col].dropna().unique()] if e_all[col].dtype != "category" else list(e_all[col].cat.categories):
        sub = e_all[e_all[col] == val]
        cells = [str(val)]
        for tf in TFS:
            s = sub[sub.tf == tf]
            a, b2 = s[s.period == "IS"].r3.mean(), s[s.period == "OOS"].r3.mean()
            cells.append(f"{f(a)} / {f(b2)} (n={len(s)})")
        g = sub[sub.period == "OOS"].groupby(["coin", "tf"]).r3.agg(["mean", "size"])
        g = g[g["size"] >= 5]
        better = sum(1 for (coin, tf), r in g.iterrows() if r["mean"] > cell_avg.get((coin, tf, "OOS"), np.nan))
        cells.append(f"{better}/{len(g)}")
        rows.append(cells)
    table(["Bucket"] + [f"{tf} IS / OOS" for tf in TFS] + ["OOS cells above average"], rows)

with open("results/ma_study.md", "w") as fh:
    fh.write("\n".join(L) + "\n")
print("wrote results/ma_study.md")
