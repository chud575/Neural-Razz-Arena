"""
The 12–24 hours BEFORE a ±5 % day: what is different, and does it predict anything?

Every UTC day of BTC and ETH with complete hourly data (Coinbase, 2016 →). A "big day" moves 5 % or more open to close.
Everything is measured from data available at 00:00 UTC, before the day starts. For each reading the days are split
into five equal groups; the table shows how often the NEXT day was a big day in each group (base rate = all days).
Direction: on big days only, how often the day went UP given the sign of a reading.

    python before_big_day.py <data_dir>   -> results/before_big_day.csv / .md
"""
import sys

import numpy as np
import pandas as pd

from market_structure import structure

D = sys.argv[1]
rows = []
for coin in ("btc", "eth"):
    h1 = pd.read_csv(f"{D}/{coin}_1h.csv", index_col=0, parse_dates=True)
    h1 = h1[(h1[["open", "high", "low", "close"]] > 0).all(axis=1)]
    c1 = h1.close
    e50, e200 = c1.ewm(span=50, adjust=False).mean(), c1.ewm(span=200, adjust=False).mean()
    basis = c1.rolling(20).mean()
    dev = 2 * c1.rolling(20).std(ddof=0)
    pc = c1.shift(1)
    tr = pd.concat([h1.high - h1.low, (h1.high - pc).abs(), (h1.low - pc).abs()], axis=1).max(axis=1)
    sq1 = (dev < 1.5 * tr.rolling(20).mean())
    st = structure(h1.high.to_numpy(float), h1.low.to_numpy(float), c1.to_numpy(float), 5)
    ms = pd.Series(st["ms"], index=h1.index)
    day = h1.index.floor("1D")
    g = h1.groupby(day)
    d = g.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), volume=("volume", "sum"), n=("open", "size"))
    d = d[d.n >= 23]
    d["ret"] = (d.close / d.open - 1) * 100
    d["rng"] = (d.high - d.low) / d.open * 100
    d["big"] = (d.ret.abs() >= 5).astype(int)
    # daily squeeze (BB 20, 2 inside KC 20, 1.5)
    db, dd = d.close.rolling(20).mean(), 2 * d.close.rolling(20).std(ddof=0)
    dtr = pd.concat([d.high - d.low, (d.high - d.close.shift()).abs(), (d.low - d.close.shift()).abs()], axis=1).max(axis=1)
    d["sq_daily"] = (dd < 1.5 * dtr.rolling(20).mean()).astype(int)
    for t in d.index[30:]:
        p = t - pd.Timedelta(days=1)
        if p not in d.index or (t - pd.Timedelta(days=2)) not in d.index:
            continue
        w24 = h1.loc[p:t - pd.Timedelta(hours=1)]
        if len(w24) < 23:
            continue
        w12, w4, e20 = w24.iloc[-12:], w24.iloc[-4:], w24.iloc[:-4]
        hist = d.loc[:p]
        O = d.open[t]
        r20 = hist.rng.iloc[-21:-1].mean()
        v20 = hist.volume.iloc[-21:-1].mean()
        lastbar = w24.index[-1]
        hi20, lo20 = hist.high.iloc[-20:].max(), hist.low.iloc[-20:].min()
        streak = 0
        sgn = np.sign(hist.ret.iloc[-1])
        for x in hist.ret.iloc[::-1]:
            if np.sign(x) == sgn and sgn != 0:
                streak += 1
            else:
                break
        rows.append(dict(coin=coin, day=t, year=t.year, big=int(d.big[t]), ret=d.ret[t], up=int(d.ret[t] > 0),
                         prev_abs_ret=abs(d.ret[p]), prev_ret=d.ret[p], prev_range=d.rng[p], prev_big=int(d.big[p]),
                         prev_range_vs_20d=d.rng[p] / r20 if r20 > 0 else np.nan, range_20d=r20,
                         nr7=int(d.rng[p] <= hist.rng.iloc[-7:].min() + 1e-12), inside_day=int(d.high[p] <= hist.high.iloc[-2] and d.low[p] >= hist.low.iloc[-2]),
                         range_12h=(w12.high.max() - w12.low.min()) / O * 100, range_4h=(w4.high.max() - w4.low.min()) / O * 100,
                         late_expansion=((w4.high.max() - w4.low.min()) / 4) / ((e20.high.max() - e20.low.min()) / len(e20)) if len(e20) else np.nan,
                         ret_12h=(w24.close.iloc[-1] / w12.open.iloc[0] - 1) * 100, ret_4h=(w24.close.iloc[-1] / w4.open.iloc[0] - 1) * 100,
                         vol_vs_20d=d.volume[p] / v20 if v20 > 0 else np.nan, vol_12h_share=w12.volume.sum() / max(w24.volume.sum(), 1e-9),
                         close_loc=(d.close[p] - d.low[p]) / (d.high[p] - d.low[p]) if d.high[p] > d.low[p] else 0.5,
                         pos_20d=(d.close[p] - lo20) / (hi20 - lo20) if hi20 > lo20 else 0.5,
                         sq_1h=int(sq1.loc[lastbar]), sq_1h_share=sq1.loc[w24.index].mean(), sq_daily=int(d.sq_daily[p]),
                         ema_trend=int(np.sign(e50.loc[lastbar] - e200.loc[lastbar])), structure_1h=int(ms.loc[lastbar]),
                         streak=int(streak * sgn), weekday=t.weekday(), three_day_abs=hist.ret.iloc[-3:].abs().sum()))
t = pd.DataFrame(rows)
t.to_csv("results/before_big_day.csv", index=False)
pd.set_option("display.width", 230)
L = ["# The 12–24 hours before a ±5% day — BTC and ETH (python/before_big_day.py)\n",
     f"Every UTC day with complete hourly data: {len(t)} days, {t.big.sum()} big days. Base rate of a big day: BTC {t[t.coin=='btc'].big.mean()*100:.1f}%, ETH {t[t.coin=='eth'].big.mean()*100:.1f}%. "
     "All readings use only data from before 00:00 UTC of the day in question.\n",
     "## How often the next day is a big day, by reading (five equal groups, lowest to highest)\n",
     "| Reading before the day | Lowest fifth | 2nd | 3rd | 4th | Highest fifth | Highest ÷ lowest | Same in 2016–2020 / 2021–2026? |\n|---|---|---|---|---|---|---|---|"]
feats = [("prev_abs_ret", "Size of the previous day's move"), ("prev_range", "Previous day's range"), ("prev_range_vs_20d", "Previous day's range vs its 20-day average"),
         ("range_20d", "Average daily range, last 20 days"), ("three_day_abs", "Sum of the last three days' moves"), ("range_12h", "Range of the last 12 hours"), ("range_4h", "Range of the last 4 hours"),
         ("late_expansion", "Last 4 hours' pace vs the 20 hours before"), ("vol_vs_20d", "Previous day's volume vs its 20-day average"), ("sq_1h_share", "Share of the last 24 hours in a 1h squeeze"),
         ("close_loc", "Where the previous day closed in its range (0 low – 1 high)"), ("pos_20d", "Where price sits in its 20-day range (0 low – 1 high)")]
out = []
for f, name in feats:
    x = t.dropna(subset=[f]).copy()
    x["q"] = x.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    r = x.groupby("q").big.mean() * 100
    early, late = x[x.year <= 2020], x[x.year > 2020]
    re_, rl = early.groupby("q").big.mean() * 100, late.groupby("q").big.mean() * 100
    L.append(f"| {name} | " + " | ".join(f"{r[k]:.0f}%" for k in range(5)) + f" | {r[4] / r[0]:.1f}× | {re_[0]:.0f}→{re_[4]:.0f}% / {rl[0]:.0f}→{rl[4]:.0f}% |")
    out.append((name, r[0], r[4]))
L.append("\n## Yes / no readings\n\n| Condition before the day | Days | Next day is big | Otherwise |\n|---|---|---|---|")
for f, name in (("prev_big", "Previous day was itself a big day"), ("nr7", "Previous day had the narrowest range of the last 7 days"), ("inside_day", "Previous day was an inside day"),
                ("sq_1h", "1h squeeze on at 00:00 UTC"), ("sq_daily", "Daily squeeze on")):
    L.append(f"| {name} | {int(t[f].sum())} | {t[t[f]==1].big.mean()*100:.0f}% | {t[t[f]==0].big.mean()*100:.0f}% |")
wk = t.groupby("weekday").big.mean() * 100
L.append("\nBy weekday (Mon–Sun): " + ", ".join(f"{['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][k]} {v:.0f}%" for k, v in wk.items()) + ".\n")
L.append("## Combining the two strongest readings\n\nPrevious day's range (thirds, down) × range of the last 12 hours (thirds, across). Share of next days that are big:\n")
x = t.copy()
x["a"] = x.groupby("coin").prev_range.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
x["b"] = x.groupby("coin").range_12h.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
pv = x.pivot_table(index="a", columns="b", values="big", aggfunc="mean") * 100
L.append("| Previous day's range | Last 12h: quiet | middle | wide |\n|---|---|---|---|")
for k, nm in enumerate(("Narrow", "Middle", "Wide")):
    L.append(f"| {nm} | " + " | ".join(f"{pv.loc[k, j]:.0f}%" for j in range(3)) + " |")
b = t[t.big == 1]
L.append(f"\n## Direction: on big days only ({len(b)} days, {b.up.mean()*100:.0f}% were up)\n\n| Reading before the day | When positive / high: big day went up | When negative / low: big day went up |\n|---|---|---|")
for f, name, thr in (("prev_ret", "Previous day's move", 0), ("ret_12h", "Last 12 hours' move", 0), ("ret_4h", "Last 4 hours' move", 0), ("close_loc", "Previous day closed in the upper half of its range", 0.5),
                     ("pos_20d", "Price in the upper half of its 20-day range", 0.5), ("ema_trend", "1h EMA 50 above EMA 200", 0), ("structure_1h", "1h structure bullish", 0), ("streak", "Previous days were up (streak)", 0)):
    hi, lo = b[b[f] > thr], b[b[f] < thr] if thr == 0 else b[b[f] <= thr]
    L.append(f"| {name} | {hi.up.mean()*100:.0f}% ({len(hi)}) | {lo.up.mean()*100:.0f}% ({len(lo)}) |")
pb = b[b.prev_big == 1]
L.append(f"\nAfter a big day, when the next day is also big ({len(pb)} cases): it went the same way as the previous big day {(np.sign(pb.ret) == np.sign(pb.prev_ret)).mean()*100:.0f}% of the time.")
open("results/before_big_day.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[1:]))
print(t.groupby("coin").big.agg(["mean", "sum", "size"]))
