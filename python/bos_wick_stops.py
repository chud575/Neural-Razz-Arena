"""
1h break-of-structure strategy: trades stopped by a WICK (the candle traded through the stop but closed back on the
right side of it). What if you re-enter at that candle's close?

Base trade: BOS at a 1h close, stop at the latest swing, 2R target, max 300 bars (python/ms_continuation.py).
Stop candle = "wick" if it closed back beyond the stop level, "close" if it closed through it.
Re-entry (wick stops only): enter at the stop candle's close, new stop = that candle's low (high for shorts).
   A  target = the ORIGINAL target price          B  target = 2 × the new risk
Also: the base strategy with a close-only stop (exit at the close of the first candle that closes through the stop).
Costs: Bybit VIP 3 futures (taker entry, maker target, taker stop, funding). R = that trade's own risk; R0 = the
original trade's risk.

    python bos_wick_stops.py <data_dir>   -> results/bos_wick_stops.csv
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import structure
from srflip_backtest import atr


def run(o, h, l, c, i, d, e, stop, tp, maxbars=300):
    n = len(c)
    m = i + 1
    end = min(n, i + 1 + maxbars)
    while m < end:
        if (l[m] <= stop) if d == 1 else (h[m] >= stop):
            return m, (min(o[m], stop) if d == 1 else max(o[m], stop)), "stop"
        if (h[m] >= tp) if d == 1 else (l[m] <= tp):
            return m, (max(o[m], tp) if d == 1 else min(o[m], tp)), "target"
        m += 1
    m = end - 1
    return m, c[m], "time"


def net(d, e, px, risk, kind, bars):
    return d * (px - e) / risk - (S.TAKER + (S.MAKER if kind == "target" else S.TAKER) + d * S.FUNDING_8H * bars / 8) * e / risk


rows = []
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(sys.argv[1], ["1h"], coin)
    df = S.DATA["1h"]
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    split = int(n * S.SPLIT)
    a14 = atr(h, l, c, 14)
    st = structure(h, l, c, 5)
    busy = -1
    for i in np.flatnonzero(np.abs(st["ev"]) == 1):
        if i <= busy or i >= n - 1:
            continue
        d = int(st["ev"][i])
        e = c[i]
        stop = st["lastL"][i] if d == 1 else st["lastH"][i]
        if math.isnan(stop) or (e - stop) * d <= 0 or math.isnan(a14[i]):
            continue
        R0 = abs(e - stop)
        tp = e + d * 2 * R0
        m, px, kind = run(o, h, l, c, i, d, e, stop, tp)
        busy = m
        row = dict(coin=coin, period="IS" if i < split else "OOS", d=d, kind=kind, r=net(d, e, px, R0, kind, m - i), stop_atr=R0 / a14[i], stopkind="")
        # close-only stop version of the same trade
        k = i + 1
        end = min(n, i + 301)
        cpx, ck = None, "time"
        while k < end:
            if (c[k] <= stop) if d == 1 else (c[k] >= stop):
                cpx, ck = c[k], "stop"
                break
            if (h[k] >= tp) if d == 1 else (l[k] <= tp):
                cpx, ck = (max(o[k], tp) if d == 1 else min(o[k], tp)), "target"
                break
            k += 1
        if cpx is None:
            k = end - 1
            cpx = c[k]
        row["r_close_stop"] = net(d, e, cpx, R0, ck, k - i)
        row["kind_close_stop"] = ck
        if kind == "stop":
            wick = (c[m] > stop) if d == 1 else (c[m] < stop)
            row["stopkind"] = "wick" if wick else "close"
            if wick and m < n - 2:
                e2 = c[m]
                s2 = l[m] if d == 1 else h[m]
                r2 = abs(e2 - s2)
                row["pierce_R0"] = abs(s2 - stop) / R0
                row["newrisk_R0"] = r2 / R0
                if r2 > 0:
                    if (tp - e2) * d > 0:
                        mA, pA, kA = run(o, h, l, c, m, d, e2, s2, tp)
                        row["A_r"] = net(d, e2, pA, r2, kA, mA - m)
                        row["A_r0"] = row["A_r"] * r2 / R0
                        row["A_kind"] = kA
                        row["A_rr"] = abs(tp - e2) / r2
                    mB, pB, kB = run(o, h, l, c, m, d, e2, s2, e2 + d * 2 * r2)
                    row["B_r"] = net(d, e2, pB, r2, kB, mB - m)
                    row["B_r0"] = row["B_r"] * r2 / R0
                    row["B_kind"] = kB
                    row["newrisk_pct"] = r2 / e2 * 100
        rows.append(row)
t = pd.DataFrame(rows)
t.to_csv("results/bos_wick_stops.csv", index=False)
pd.set_option("display.width", 220)
s = t[t.kind == "stop"]
print("trades", len(t), "stops", len(s), "wick share %.1f%%" % ((s.stopkind == "wick").mean() * 100))
print(s.groupby("period").stopkind.value_counts(normalize=True).unstack().round(3))
w = s[s.stopkind == "wick"]
print("wick stops: median pierce %.2f R0, median new risk %.2f R0 (%.2f%%)" % (w.pierce_R0.median(), w.newrisk_R0.median(), w.newrisk_pct.median()))


def io(g, col):
    a, b = g[g.period == "IS"][col].dropna(), g[g.period == "OOS"][col].dropna()
    return f"{a.mean():+.3f} ({len(a)}) / {b.mean():+.3f} ({len(b)})"


for col in ("A_r", "A_r0", "B_r", "B_r0"):
    print(col, io(w, col))
print("A outcomes", w.A_kind.value_counts(normalize=True).round(3).to_dict(), "median RR %.1f" % w.A_rr.median())
print("B outcomes", w.B_kind.value_counts(normalize=True).round(3).to_dict())
print(w.groupby(["coin", "period"])[["A_r", "B_r"]].mean().round(3).unstack())
print(w.groupby(["d", "period"])[["A_r", "B_r"]].mean().round(3).unstack())
w = w.assign(nb=pd.cut(w.newrisk_R0, [0, 0.1, 0.2, 0.4, 10]))
print(w.groupby(["nb", "period"], observed=True)[["A_r", "B_r"]].agg(["mean", "size"]).round(3).to_string())
print("base", io(t, "r"), "| close-only stop", io(t, "r_close_stop"), t.kind_close_stop.value_counts(normalize=True).round(3).to_dict())
t["plusA"] = t.r + t.A_r0.fillna(0)
t["plusB"] = t.r + t.B_r0.fillna(0)
print("base + re-entry A (R0 per signal)", io(t, "plusA"), "| + B", io(t, "plusB"))
f = t[t.stop_atr >= 2.9]
print("with tight-stop filter: base", io(f, "r"), "| +A", io(f, "plusA"), "| +B", io(f, "plusB"), "| close-only", io(f, "r_close_stop"))
