"""
Premium / discount zones and the Trend Finder v1.6 strategy (1h break of structure).

Strategy = the script's defaults: BOS at a 1h close, stop at the latest swing (skipped if closer than 2.9 × ATR 14),
2R target, second entry at 50 % of the way to the stop, max 300 bars, Bybit VIP 3 fees. R = the first entry's risk.

Premium / discount: take a "dealing range" (a low and a high) and see where the entry price sits in it.
  position 0 % = the range low, 50 % = equilibrium, 100 % = the range high. Above 50 % is PREMIUM, below is DISCOUNT.
  The textbook rule: buy in discount, sell in premium. "With the rule" = a long entered in discount or a short entered in
  premium; "against" = the opposite.
Dealing ranges tried:  the last 50 / 100 / 200 / 500 1h candles; the latest confirmed 4h and daily swing high / low
  (closed candles, swing length 3); the previous day's and the previous week's range.

    python bos_premium_discount.py <data_dir>   -> results/bos_premium_discount.csv / .md
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import resample, structure
from srflip_backtest import atr

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
    rng = {}
    for N in (50, 100, 200, 500):
        rng[f"last {N} candles"] = (pd.Series(l).rolling(N).min().to_numpy(), pd.Series(h).rolling(N).max().to_numpy())
    for rule, name in (("4h", "4h swing range"), ("1D", "daily swing range")):
        g, pos = resample(df, rule)
        hs = structure(g["high"].to_numpy(float), g["low"].to_numpy(float), g["close"].to_numpy(float), 3)
        p = np.maximum(pos - 1, 0)
        rng[name] = (np.where(pos > 0, hs["lastL"][p], np.nan), np.where(pos > 0, hs["lastH"][p], np.nan))
    for rule, name in (("1D", "previous day"), ("1W", "previous week")):
        g, pos = resample(df, rule)
        p = np.maximum(pos - 1, 0)
        rng[name] = (np.where(pos > 0, g["low"].to_numpy(float)[p], np.nan), np.where(pos > 0, g["high"].to_numpy(float)[p], np.nan))
    busy = -1
    for i in np.flatnonzero(np.abs(st["ev"]) == 1):
        if i <= busy or i >= n - 1 or i < 520:
            continue
        d = int(st["ev"][i])
        e = c[i]
        stop = st["lastL"][i] if d == 1 else st["lastH"][i]
        if math.isnan(stop) or (e - stop) * d <= 0 or math.isnan(a14[i]):
            continue
        R0 = abs(e - stop)
        if R0 < 2.9 * a14[i]:
            continue                                       # the script's tight-stop filter
        tp = e + d * 2 * R0
        mid = e - d * 0.5 * R0
        fill2, px, at_t, m = None, None, False, i + 1
        end = min(n, i + 301)
        while m < end:
            hs_ = (l[m] <= stop) if d == 1 else (h[m] >= stop)
            ht = (h[m] >= tp) if d == 1 else (l[m] <= tp)
            hm = (l[m] <= mid) if d == 1 else (h[m] >= mid)
            if fill2 is None and hm and (hs_ or not ht):
                fill2 = m
            if hs_:
                px = min(o[m], stop) if d == 1 else max(o[m], stop)
                break
            if ht:
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
        row = dict(coin=coin, period="IS" if i < split else "OOS", d=d, r1=r1, r=r1 + r2)
        for name, (lo, hi) in rng.items():
            a, b = lo[i], hi[i]
            row[name] = (e - a) / (b - a) if (not math.isnan(a) and not math.isnan(b) and b > a) else np.nan
            row[name + " | 2nd"] = (mid - a) / (b - a) if (not math.isnan(a) and not math.isnan(b) and b > a) else np.nan
        rows.append(row)
t = pd.DataFrame(rows)
t.to_csv("results/bos_premium_discount.csv", index=False)
names = ["last 50 candles", "last 100 candles", "last 200 candles", "last 500 candles", "4h swing range", "daily swing range", "previous day", "previous week"]
pd.set_option("display.width", 230)


def cell(g, col="r"):
    a, b = g[g.period == "IS"], g[g.period == "OOS"]
    return f"{a[col].mean():+.2f} / {b[col].mean():+.2f} ({len(g)})" if len(g) else "–"


print("all", cell(t), "first entry only", cell(t, "r1"))
L = ["# Premium / discount zones and the Trend Finder v1.6 strategy (1h BOS)\n",
     "Rules in python/bos_premium_discount.py. Strategy = script defaults (tight-stop filter, second entry at 50%). Average R per signal (R = the first entry's risk), "
     "IS / OOS (trades), four coins, after fees. Position of the ENTRY PRICE in the dealing range: below 50% = discount, above = premium. "
     "'With the rule' = long in discount or short in premium.\n",
     f"All trades: {cell(t)}. First entry only: {cell(t, 'r1')}.\n",
     "| Dealing range | With the rule | Against the rule | Longs in discount | Longs in premium | Shorts in premium | Shorts in discount |\n|---|---|---|---|---|---|---|"]
for nm in names:
    x = t.dropna(subset=[nm])
    disc = x[nm] < 0.5
    withr = ((x.d == 1) & disc) | ((x.d == -1) & ~disc)
    cells = [cell(x[withr]), cell(x[~withr]), cell(x[(x.d == 1) & disc]), cell(x[(x.d == 1) & ~disc]), cell(x[(x.d == -1) & ~disc]), cell(x[(x.d == -1) & disc])]
    print(f"{nm:20}", " | ".join(cells))
    L.append(f"| {nm} | " + " | ".join(cells) + " |")
L.append("\n## Finer bands (position turned so 0% is the 'cheap' end for the trade: range low for longs, range high for shorts)\n")
L.append("| Dealing range | beyond the cheap end (<0%) | 0–25% | 25–50% | 50–75% | 75–100% | beyond the expensive end (>100%) |\n|---|---|---|---|---|---|---|")
for nm in names:
    x = t.dropna(subset=[nm])
    al = np.where(x.d == 1, x[nm], 1 - x[nm])
    b = pd.cut(al, [-1e9, 0, 0.25, 0.5, 0.75, 1.0, 1e9], labels=False)
    cells = [cell(x[b == k]) for k in range(6)]
    print(f"{nm:20}", " | ".join(cells))
    L.append(f"| {nm} | " + " | ".join(cells) + " |")
L.append("\n## First entry only (no second entry), with / against the rule\n\n| Dealing range | With the rule | Against the rule |\n|---|---|---|")
for nm in names:
    x = t.dropna(subset=[nm])
    disc = x[nm] < 0.5
    withr = ((x.d == 1) & disc) | ((x.d == -1) & ~disc)
    L.append(f"| {nm} | {cell(x[withr], 'r1')} | {cell(x[~withr], 'r1')} |")
    print("r1", f"{nm:20}", cell(x[withr], "r1"), "|", cell(x[~withr], "r1"))
open("results/bos_premium_discount.md", "w").write("\n".join(L) + "\n")
x = t.dropna(subset=["daily swing range"]); disc = x["daily swing range"] < 0.5; withr = ((x.d == 1) & disc) | ((x.d == -1) & ~disc)
print(x.assign(w=withr).groupby(["coin", "w", "period"]).r.mean().round(2).unstack(["w", "period"]))
