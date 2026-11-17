"""
Does normalized volume on the break candle help the 1h break-of-structure strategy?

Normalized volume = volume / SMA(volume, 50) × 100 (the "Normalized Volume" study): ≥ 150 high, 75–150 normal, ≤ 75 low.
Base trade: BOS at a 1h close, stop at the latest swing, 2R target (python/ms_continuation.py). Volume is Coinbase spot volume.

    python bos_volume.py <data_dir>   -> results/bos_volume.csv
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import structure

rows = []
for coin in ("btc", "eth", "avax", "xrp"):
    df = pd.read_csv(f"{sys.argv[1]}/{coin}_1h.csv", index_col=0, parse_dates=True)
    df = df[(df[["open", "high", "low", "close"]] > 0).all(axis=1)]
    o, h, l, c, v = (df[k].to_numpy(float) for k in ("open", "high", "low", "close", "volume"))
    n = len(c)
    split = int(n * S.SPLIT)
    nv = v / pd.Series(v).rolling(50).mean().to_numpy() * 100
    nv3 = pd.Series(nv).rolling(3).mean().to_numpy()                 # average of the break candle and the two before it
    st = structure(h, l, c, 5)
    busy = -1
    for i in np.flatnonzero(np.abs(st["ev"]) == 1):
        if i <= busy or i >= n - 1:
            continue
        d = int(st["ev"][i])
        e = c[i]
        stop = st["lastL"][i] if d == 1 else st["lastH"][i]
        if math.isnan(stop) or (e - stop) * d <= 0 or math.isnan(nv[i]):
            continue
        R0 = abs(e - stop)
        tp = e + d * 2 * R0
        px, at_t, m = None, False, i + 1
        end = min(n, i + 301)
        while m < end:
            if (l[m] <= stop) if d == 1 else (h[m] >= stop):
                px = min(o[m], stop) if d == 1 else max(o[m], stop)
                break
            if (h[m] >= tp) if d == 1 else (l[m] <= tp):
                px, at_t = (max(o[m], tp) if d == 1 else min(o[m], tp)), True
                break
            m += 1
        if px is None:
            m = end - 1
            px = c[m]
        busy = m
        r = d * (px - e) / R0 - (S.TAKER + (S.MAKER if at_t else S.TAKER) + d * S.FUNDING_8H * (m - i) / 8) * e / R0
        rows.append((coin, "IS" if i < split else "OOS", d, r, int(at_t), nv[i], nv3[i], R0 / e * 100, abs(c[i] - o[i]) / R0))
t = pd.DataFrame(rows, columns=["coin", "period", "d", "r", "win", "nv", "nv3", "risk_pct", "body"])
t.to_csv("results/bos_volume.csv", index=False)
pd.set_option("display.width", 220)


def io(g):
    a, b = g[g.period == "IS"], g[g.period == "OOS"]
    return pd.Series(dict(n=len(g), IS=a.r.mean(), OOS=b.r.mean(), all=g.r.mean(), target=g.win.mean() * 100, stop_pct=g.risk_pct.median()))


t["class"] = np.where(t.nv >= 150, "3 high (>=150)", np.where(t.nv <= 75, "1 low (<=75)", "2 normal"))
print("all", io(t).round(3).to_dict())
print(t.groupby("class").apply(io).round(3))
t["bucket"] = pd.cut(t.nv, [0, 50, 75, 100, 150, 200, 300, 500, 1e9])
print(t.groupby("bucket", observed=True).apply(io).round(3))
print(t.groupby(["coin", "class"]).apply(io).round(3))
print(t.groupby(["d", "class"]).apply(io).round(3))
t["c3"] = np.where(t.nv3 >= 150, "3 high", np.where(t.nv3 <= 75, "1 low", "2 normal"))
print("3-bar avg"); print(t.groupby("c3").apply(io).round(3))
print("corr nv vs risk", t[["nv", "risk_pct", "body", "r"]].corr(method="spearman").round(2))
