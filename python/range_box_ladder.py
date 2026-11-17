"""
Range-box breakout with a 5-step ladder (range finder = pine/range_broadening.pine, default settings).

Range box: last four alternating swings (length 5); the two highs level and the two lows level (each pair within
0.15 × range height); height ≥ 2 × ATR(14); first to fourth swing ≤ 300 bars. Later swings near a bound stretch it.
The box breaks when a bar CLOSES outside it. H = box height at the break.
Trade: enter 5 units at the break close (long on an up-break, short on a down-break).
  sell 1 unit at each of 1 ×, 2 ×, 3 ×, 4 ×, 5 × H beyond the broken bound
  dump whatever is left if price comes back to the OPPOSITE side of the box (−1 × H)
  stop first if a bar touches both; max 2000 bars, then exit at the close. Positions may overlap.
Costs per unit: Bybit VIP 3 futures (taker entry, maker at a target, taker at the stop, funding).
R = what the full 5 units lose if stopped straight away (5 × distance from entry to the far side of the box).

    python range_box_ladder.py <data_dir>   -> results/range_box_ladder_trades.csv
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from dtdb_backtest import pivots
from srflip_backtest import atr

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
L, TOL, MINH, MAXW, UNITS, MAXHOLD = 5, 0.15, 2.0, 300, 5, 2000


def find_breaks(h, l, c):
    """[(break bar, direction, top, bottom, start bar, touches high, touches low)]"""
    n = len(c)
    ph, pl = pivots(h, l, L)
    a = atr(h, l, c, 14)
    seq = []                                   # (type, price, bar)
    out = []
    on, r_end = False, -1
    top = bot = tol_a = 0.0
    start = th = tl = 0
    for i in range(n):
        changed = False
        for tp, arr in ((1, ph), (-1, pl)):
            if not math.isnan(arr[i]):
                if seq and seq[-1][0] == tp:
                    if (tp == 1 and arr[i] > seq[-1][1]) or (tp == -1 and arr[i] < seq[-1][1]):
                        seq[-1] = (tp, arr[i], i - L)
                        changed = True
                else:
                    seq.append((tp, arr[i], i - L))
                    del seq[:-10]
                    changed = True
        if on:
            if c[i] > top or c[i] < bot:
                out.append((i, 1 if c[i] > top else -1, top, bot, start, th, tl))
                on, r_end = False, i
            else:
                if not math.isnan(ph[i]) and abs(ph[i] - top) <= tol_a:
                    th += 1
                    top = max(top, ph[i])
                if not math.isnan(pl[i]) and abs(pl[i] - bot) <= tol_a:
                    tl += 1
                    bot = min(bot, pl[i])
        elif changed and len(seq) >= 4 and not math.isnan(a[i]):
            p = seq[-4:]
            hs = [x for x in p if x[0] == 1]
            ls = [x for x in p if x[0] == -1]
            if len(hs) == 2 and len(ls) == 2:
                ht = (hs[0][1] + hs[1][1]) / 2 - (ls[0][1] + ls[1][1]) / 2
                first = p[0][2]
                if (ht > 0 and ht >= MINH * a[i] and i - L - first <= MAXW and first > r_end
                        and abs(hs[0][1] - hs[1][1]) <= TOL * ht and abs(ls[0][1] - ls[1][1]) <= TOL * ht):
                    t, b = max(hs[0][1], hs[1][1]), min(ls[0][1], ls[1][1])
                    if b <= c[i] <= t:
                        on, top, bot, tol_a, start, th, tl = True, t, b, TOL * ht, first, 2, 2
    return out


def ladder(o, h, l, c, i, d, top, bot, bar_h, steps=5, be_after=0):
    """Returns dict: pnl per unit list (price), fees, steps hit, exit bars … all in price terms summed over 5 units."""
    e = c[i]
    H = top - bot
    edge, stop = (top, bot) if d == 1 else (bot, top)
    tg = [edge + d * k * H for k in range(1, steps + 1)]
    left = UNITS
    gross = cost = 0.0
    hit = 0
    # targets already behind the entry price are sold at the entry
    while hit < steps and (e - tg[hit]) * d >= 0:
        cost += e * (S.TAKER + S.MAKER)
        hit += 1
        left -= 1
    m = i + 1
    end = min(len(c), i + 1 + MAXHOLD)
    stopped = False
    while m < end and left > 0 and hit < steps:
        if (l[m] <= stop) if d == 1 else (h[m] >= stop):
            px = min(o[m], stop) if d == 1 else max(o[m], stop)
            gross += left * d * (px - e)
            cost += left * e * (S.TAKER + S.TAKER + d * S.FUNDING_8H * (m - i) * bar_h / 8)
            left, stopped = 0, True
            break
        while hit < steps and left > 0 and ((h[m] >= tg[hit]) if d == 1 else (l[m] <= tg[hit])):
            px = max(o[m], tg[hit]) if d == 1 else min(o[m], tg[hit])
            gross += d * (px - e)
            cost += e * (S.TAKER + S.MAKER + d * S.FUNDING_8H * (m - i) * bar_h / 8)
            hit += 1
            left -= 1
            if be_after and hit >= be_after:
                stop = e                                   # optional: stop to the entry after N steps
        m += 1
    if left > 0:                                           # ran out of time (or of steps with units left)
        m = min(end - 1, m)
        gross += left * d * (c[m] - e)
        cost += left * e * (S.TAKER + S.TAKER + d * S.FUNDING_8H * (m - i) * bar_h / 8)
    risk = UNITS * abs(e - (bot if d == 1 else top))
    return gross, cost, hit, stopped, risk, m - i, H / e * 100


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(n * S.SPLIT)
            for i, d, top, bot, start, th, tl in find_breaks(h, l, c):
                if i >= n - 2:
                    continue
                for name, kw in (("5 steps", {}), ("3 steps, rest out at 3x", dict(steps=3)), ("5 steps, stop to entry after 1x", dict(be_after=1))):
                    g, cost, hit, stopped, risk, bars, hpct = ladder(o, h, l, c, i, d, top, bot, bar_h, **kw)
                    rows.append((coin, tf, name, str(df.index[i]), d, "IS" if i < split else "OOS", c[i], g, cost, g - cost, (g - cost) / risk,
                                 g / risk, (g - cost) / (UNITS * c[i]) * 100, hit, int(stopped), bars, hpct, i - start, th + tl))
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows, columns=["coin", "tf", "variant", "time", "d", "period", "entry", "gross", "cost", "net", "r", "gross_r", "pct", "steps",
                                "stopped", "bars", "box_pct", "box_bars", "touches"]).to_csv("results/range_box_ladder_trades.csv", index=False)


if __name__ == "__main__":
    main()
