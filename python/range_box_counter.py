"""
Counter-trade after a range-box break (range finder = pine/range_broadening.pine, default settings).

After the box breaks DOWN (a close below the bottom): a resting buy order at the BOTTOM of the box, filled when price
comes back up through it (a gap fills at the open). 5 units long.
  stop    = bottom − 1 × box height (dump everything left)
  targets = top of the box, then 1 ×, 2 ×, 3 ×, 4 × the box height above the top (sell 1 unit at each)
After a break UP the mirror image: sell 5 units at the top when price comes back down through it.
The order is cancelled if price first travels 5 × the box height in the break direction, or after 2000 bars.
Stop first if a bar touches both; max 2000 bars in the trade. Positions may overlap.
Costs per unit: Bybit VIP 3 futures (taker entry, maker at a target, taker at the stop, funding).
R = what the full 5 units lose at the stop (5 × box height).

    python range_box_counter.py <data_dir>   -> results/range_box_counter_trades.csv
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from range_box_ladder import COINS, MAXHOLD, TFS, UNITS, find_breaks

CAP = 5.0


def run(o, h, l, c, i, bd, top, bot, bar_h):
    """bd = direction of the break; the counter-trade goes the other way. Returns None if never filled."""
    H = top - bot
    d = -bd
    lvl = bot if bd == -1 else top                         # the broken bound = entry level
    cap = lvl + bd * CAP * H
    ext = l[i] if bd == -1 else h[i]                       # furthest travel in the break direction before the fill
    n = len(c)
    f = None
    for m in range(i + 1, min(n, i + 1 + MAXHOLD)):
        if (h[m] >= lvl) if d == 1 else (l[m] <= lvl):
            f = m
            break
        ext = min(ext, l[m]) if bd == -1 else max(ext, h[m])
        if (ext - cap) * bd >= 0:
            return None
    if f is None:
        return None
    gap = (o[f] >= lvl) if d == 1 else (o[f] <= lvl)
    e = o[f] if gap else lvl
    stop = lvl - d * H
    tg = [lvl + d * k * H for k in range(1, UNITS + 1)]
    left, gross, cost, hit, stopped = UNITS, 0.0, 0.0, 0, False
    m = f
    end = min(n, f + 1 + MAXHOLD)
    while m < end and left > 0:
        if (m > f or gap) and ((l[m] <= stop) if d == 1 else (h[m] >= stop)):
            px = min(o[m], stop) if (d == 1 and m > f) else max(o[m], stop) if (d == -1 and m > f) else stop
            gross += left * d * (px - e)
            cost += left * e * (2 * S.TAKER + d * S.FUNDING_8H * (m - f) * bar_h / 8)
            left, stopped = 0, True
            break
        while left > 0 and ((h[m] >= tg[hit]) if d == 1 else (l[m] <= tg[hit])):
            px = tg[hit] if m == f else (max(o[m], tg[hit]) if d == 1 else min(o[m], tg[hit]))
            gross += d * (px - e)
            cost += e * (S.TAKER + S.MAKER + d * S.FUNDING_8H * (m - f) * bar_h / 8)
            hit += 1
            left -= 1
        m += 1
    if left > 0:
        m = min(end - 1, m)
        gross += left * d * (c[m] - e)
        cost += left * e * (2 * S.TAKER + d * S.FUNDING_8H * (m - f) * bar_h / 8)
    risk = UNITS * H
    return f, d, e, gross, cost, hit, stopped, risk, m - f, f - i, abs(ext - lvl) / H


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    stats = []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(n * S.SPLIT)
            br = [b for b in find_breaks(h, l, c) if b[0] < n - 2]
            filled = 0
            for i, bd, top, bot, start, th, tl in br:
                r = run(o, h, l, c, i, bd, top, bot, bar_h)
                if r is None:
                    continue
                filled += 1
                f, d, e, g, cost, hit, stopped, risk, bars, wait, trav = r
                rows.append((coin, tf, str(df.index[f]), d, "IS" if f < split else "OOS", e, g, cost, g - cost, (g - cost) / risk, g / risk,
                             (g - cost) / (UNITS * e) * 100, hit, int(stopped), bars, wait, trav, (top - bot) / e * 100))
            stats.append((coin, tf, len(br), filled))
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows, columns=["coin", "tf", "time", "d", "period", "entry", "gross", "cost", "net", "r", "gross_r", "pct", "steps", "stopped",
                                "bars", "wait", "travel", "box_pct"]).to_csv("results/range_box_counter_trades.csv", index=False)
    pd.DataFrame(stats, columns=["coin", "tf", "breaks", "filled"]).to_csv("results/range_box_counter_fills.csv", index=False)


if __name__ == "__main__":
    main()
