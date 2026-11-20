"""
Impulse legs in a row: how often does the next impulse leg go the same way as the previous one?

Legs = pine/impulse_legs.pine defaults (python/impulse_study.find_legs) on 15m, 1h, 4h and 1D.
"Run" = consecutive legs in the same direction (down, down, up = a run of 2 downs, then a new run starts).
"Expected" = what independent legs would give with the same share of up legs: p² + (1 − p)².

    python leg_sequence_study.py <data_dir>   -> results/leg_sequence.md
"""
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from impulse_study import find_legs

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
D = sys.argv[1]
rows = []
for coin in COINS:
    S.DATA.clear()
    S.load(D, TFS, coin)
    for tf in TFS:
        df = S.DATA[tf]
        h, l, c = (df[k].to_numpy(float) for k in ("high", "low", "close"))
        split = int(len(c) * S.SPLIT)
        legs = find_legs(h, l, c)
        run = 0
        prev = None
        for sB, eB, sP, eP, d, fin in legs:
            if prev is not None:
                pd_, peB, pfin, psize = prev
                rows.append(dict(coin=coin, tf=tf, period="IS" if sB < split else "OOS", prev_d=pd_, d=d, same=int(d == pd_), run_before=run,
                                 gap=sB - peB, prev_size=psize, size=abs(eP - sP) / sP * 100))
            run = run + 1 if (prev is not None and d == prev[0]) else 1
            prev = (d, eB, fin, abs(eP - sP) / sP * 100)
t = pd.DataFrame(rows)
t.to_csv("results/leg_sequence.csv", index=False)
pd.set_option("display.width", 220)


def exp(g):
    p = (g.d == 1).mean()
    return (p * p + (1 - p) * (1 - p)) * 100


L = ["# Impulse legs in a row — study (BTC, ETH, AVAX, XRP)\n",
     "Rules in python/leg_sequence_study.py. 'Same way' = the next impulse leg goes in the same direction as the one before it. "
     "'Expected' = the rate if legs were independent.\n",
     "## How often the next leg goes the same way\n\n| TF | Pairs of legs | Same way | Expected | After a leg up | After a leg down | First 70% | Last 30% | BTC only |\n|---|---|---|---|---|---|---|---|---|"]
for tf in TFS:
    g = t[t.tf == tf]
    b = g[g.coin == "btc"]
    L.append(f"| {tf} | {len(g)} | {g.same.mean()*100:.0f}% | {exp(g):.0f}% | {g[g.prev_d==1].same.mean()*100:.0f}% | {g[g.prev_d==-1].same.mean()*100:.0f}% | "
             f"{g[g.period=='IS'].same.mean()*100:.0f}% | {g[g.period=='OOS'].same.mean()*100:.0f}% | {b.same.mean()*100:.0f}% ({len(b)}) |")
L.append("\n## Does a longer run make another one more likely?\n\nShare of times the next leg goes the same way, given how many in a row there have already been (count in brackets).\n")
L.append("| TF | After 1 | After 2 in a row | After 3 | After 4 | After 5 or more |\n|---|---|---|---|---|---|")
for tf in TFS:
    g = t[t.tf == tf]
    cells = []
    for k in (1, 2, 3, 4, 5):
        x = g[g.run_before == k] if k < 5 else g[g.run_before >= 5]
        cells.append(f"{x.same.mean()*100:.0f}% ({len(x)})" if len(x) else "–")
    L.append(f"| {tf} | " + " | ".join(cells) + " |")
L.append("\n## How long runs are\n\nShare of runs by length (a run ends when a leg goes the other way).\n\n| TF | 1 | 2 | 3 | 4 | 5 or more | Longest |\n|---|---|---|---|---|---|---|")
for tf in TFS:
    g = t[t.tf == tf]
    ends = g[g.same == 0].run_before                       # length of each finished run
    vc = ends.clip(upper=5).value_counts(normalize=True) * 100
    L.append(f"| {tf} | " + " | ".join(f"{vc.get(k, 0):.0f}%" for k in (1, 2, 3, 4, 5)) + f" | {int(g.run_before.max()) + 1} |")
L.append("\n## Does it depend on how soon the next leg starts?\n\nBars between the previous leg's extreme and the next leg's start.\n\n| TF | Starts within 5 bars | 6–20 bars | 21–60 bars | More than 60 bars |\n|---|---|---|---|---|")
for tf in TFS:
    g = t[t.tf == tf]
    cells = []
    for lo, hi in ((-1, 5), (5, 20), (20, 60), (60, 10 ** 9)):
        x = g[(g.gap > lo) & (g.gap <= hi)]
        cells.append(f"{x.same.mean()*100:.0f}% ({len(x)})" if len(x) else "–")
    L.append(f"| {tf} | " + " | ".join(cells) + " |")
L.append("\n## Size of the previous leg (same-way rate by thirds: smallest / middle / largest)\n\n| TF | Smallest third | Middle | Largest third |\n|---|---|---|---|")
for tf in TFS:
    g = t[t.tf == tf].copy()
    g["q"] = pd.qcut(g.prev_size, 3, labels=False)
    L.append(f"| {tf} | " + " | ".join(f"{g[g.q==k].same.mean()*100:.0f}%" for k in range(3)) + " |")
open("results/leg_sequence.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[2:]))
print(t.groupby(["tf", "coin"]).same.agg(["mean", "size"]).round(3).unstack())
