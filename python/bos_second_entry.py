"""
1h break-of-structure strategy with a second entry at 50 % of the way to the stop.

Base trade (pine/trend_finder.pine tracker): BOS at a close, stop at the latest swing, target 2 × the risk (R0).
Second entry: a limit order halfway between the entry and the stop, same stop, same target price.
  If a bar touches the limit and the stop, the second unit is filled and stopped. If a bar touches the limit and
  the target, the second unit is counted as NOT filled (order of events unknown).
Costs: Bybit VIP 3 futures (first unit taker entry, second unit maker entry; maker target, taker stop; funding).
Results are in R0 = the risk of ONE unit entered at the close.

    python bos_second_entry.py <data_dir>
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import structure

rows = []
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(sys.argv[1], ["1h"], coin)
    df = S.DATA["1h"]
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    split = int(n * S.SPLIT)
    st = structure(h, l, c, 5)
    busy = -1
    for i in np.flatnonzero(np.abs(st["ev"]) == 1):
        if i <= busy or i >= n - 1:
            continue
        d = int(st["ev"][i])
        e = c[i]
        stop = st["lastL"][i] if d == 1 else st["lastH"][i]
        if math.isnan(stop) or (e - stop) * d <= 0:
            continue
        R0 = abs(e - stop)
        tp = e + d * 2 * R0
        mid = e - d * 0.5 * R0
        fill2, px, at_t, m = None, None, False, i + 1
        end = min(n, i + 301)
        while m < end:
            hit_stop = (l[m] <= stop) if d == 1 else (h[m] >= stop)
            hit_tp = (h[m] >= tp) if d == 1 else (l[m] <= tp)
            hit_mid = (l[m] <= mid) if d == 1 else (h[m] >= mid)
            if fill2 is None and hit_mid and (hit_stop or not hit_tp):
                fill2 = m
            if hit_stop:
                px = min(o[m], stop) if d == 1 else max(o[m], stop)
                break
            if hit_tp:
                px, at_t = (max(o[m], tp) if d == 1 else min(o[m], tp)), True
                break
            m += 1
        if px is None:
            m = end - 1
            px = c[m]
        busy = m
        r1 = d * (px - e) / R0 - (S.TAKER + (S.MAKER if at_t else S.TAKER) + d * S.FUNDING_8H * (m - i) / 8) * e / R0
        r2 = 0.0
        if fill2 is not None:
            r2 = d * (px - mid) / R0 - (S.MAKER + (S.MAKER if at_t else S.TAKER) + d * S.FUNDING_8H * (m - fill2) / 8) * mid / R0
        rows.append((coin, "IS" if i < split else "OOS", r1, r2, int(fill2 is not None), int(at_t), R0 / e * 100))
t = pd.DataFrame(rows, columns=["coin", "period", "r1", "r2", "filled", "win", "risk_pct"])
t.to_csv("results/bos_second_entry.csv", index=False)
pd.set_option("display.width", 200)


def rep(g):
    f = g[g.filled == 1]
    return pd.Series(dict(trades=len(g), first=g.r1.mean(), filled=g.filled.mean() * 100, second_when_filled=f.r2.mean(), second_per_signal=g.r2.mean(),
                          both=(g.r1 + g.r2).mean(), both_per_risk=((g.r1 + g.r2).sum() / (1 + 0.5 * g.filled).sum()), second_only_win=f.win.mean() * 100,
                          half_half=(0.5 * g.r1 + 0.5 * g.r2).mean()))


print(t.groupby("period").apply(rep).round(3).T.to_string())
print(t.groupby(["coin", "period"]).apply(rep).round(3)[["first", "second_when_filled", "both", "both_per_risk"]].to_string())
x = t.assign(tot=t.r1 + t.r2)
for name, s in (("first only", t.r1), ("both", x.tot), ("second only", t.r2)):
    eq = s.groupby(t.coin).cumsum()
    print(name, "total R0 %.0f" % s.sum(), "worst coin drawdown %.1f" % max((g.cumsum().cummax() - g.cumsum()).max() for _, g in s.groupby(t.coin)))
