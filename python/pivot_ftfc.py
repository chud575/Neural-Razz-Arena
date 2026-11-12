"""
Pullback to a higher-timeframe pivot in the direction of the bigger candle (timeframe continuity).

Long (shorts mirror it), on 15m candles:
  * Context candle (week or day) is GREEN so far: the last 15m close is above its open.
  * An active pivot LOW of the pivot timeframe (swing low, 3 candles each side, not yet closed through) sits below
    the current price and above the context candle's low so far.
  * Limit buy at that pivot (a gap fills at the open). Each pivot line is traded once.
  * Stop = the context candle's low at the time of the fill (stopped on the fill candle if it trades there).
  * Target = the nearest active pivot HIGH of the same pivot timeframe above the entry ("pivot"), or 2R.
  * Exits from the candle after the fill; stop first if both are touched; max 2000 candles (~3 weeks).
Costs: Bybit VIP 3 futures (maker entry, maker target, taker stop, funding).
"Expected win %" = risk / (risk + reward): the win rate that gives exactly zero before fees.

    python pivot_ftfc.py <data_dir>   -> results/pivot_ftfc_trades.csv
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from htf_pivot_study import PIV, htf_pivot_events

COINS = ["btc", "eth", "avax", "xrp"]
CASES = [("1W", "1D"), ("1W", "4h"), ("1D", "4h"), ("1D", "1h"), ("1M", "1D")]
HORIZON, MAXL = 2000, 8


def ctx_key(idx, rule):
    if rule == "1W":
        return (idx - pd.to_timedelta(idx.weekday, unit="D")).floor("1D")
    if rule == "1M":
        return idx.to_period("M").start_time
    return idx.floor(rule)


def run(coin, df, ctx, ptf, rows):
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    split = int(n * S.SPLIT)
    g = df.groupby(ctx_key(df.index, ctx))
    c_open = g["open"].transform("first").to_numpy(float)
    c_lo, c_hi = g["low"].cummin().to_numpy(float), g["high"].cummax().to_numpy(float)
    newctx = np.r_[True, c_open[1:] != c_open[:-1]]
    mo = df.groupby(ctx_key(df.index, "1M"))["open"].transform("first").to_numpy(float)
    wk = df.groupby(ctx_key(df.index, "1W"))["open"].transform("first").to_numpy(float)
    ev = {}
    for bar, s, px, pb in htf_pivot_events(df, ptf):
        ev.setdefault(bar, []).append((s, px, pb))
    highs, lows = [], []
    for i in range(1, n):
        for s, px, pb in ev.get(i, []):
            closed = c[pb + 1:i]
            if len(closed) and ((closed.max() > px) if s == 1 else (closed.min() < px)):
                continue
            lst = highs if s == 1 else lows
            lst.append(dict(px=px, used=False))
            if len(lst) > MAXL:
                lst.pop(0)
        if not newctx[i]:                                    # context candle needs at least one closed 15m candle
            pc = c[i - 1]
            for d, mine, opp in ((1, lows, highs), (-1, highs, lows)):
                if (pc - c_open[i]) * d <= 0:
                    continue                                 # context candle not in our direction
                ext = c_lo[i - 1] if d == 1 else c_hi[i - 1]  # stop: context low / high so far
                for x in mine:
                    px = x["px"]
                    if x["used"] or (pc - px) * d <= 0 or (px - ext) * d <= 0:
                        continue
                    if not ((l[i] <= px) if d == 1 else (h[i] >= px)):
                        continue
                    x["used"] = True
                    e = min(o[i], px) if d == 1 else max(o[i], px)
                    risk = abs(e - ext)
                    tg = [y["px"] for y in opp if (y["px"] - e) * d > 0]
                    if risk <= 0 or not tg:
                        continue
                    tp_piv = min(tg) if d == 1 else max(tg)
                    for mode, tp in (("pivot", tp_piv), ("2R", e + d * 2 * risk)):
                        px_x, at_t, m = None, False, i
                        if (l[i] <= ext) if d == 1 else (h[i] >= ext):
                            px_x = ext
                        else:
                            m = i + 1
                            end = min(n, i + 1 + HORIZON)
                            while m < end:
                                if (l[m] <= ext) if d == 1 else (h[m] >= ext):
                                    px_x = min(o[m], ext) if d == 1 else max(o[m], ext)
                                    break
                                if (h[m] >= tp) if d == 1 else (l[m] <= tp):
                                    px_x, at_t = (max(o[m], tp) if d == 1 else min(o[m], tp)), True
                                    break
                                m += 1
                            if px_x is None:
                                m = end - 1
                                px_x = c[m]
                        gross = d * (px_x - e) / risk
                        cost = S.MAKER + (S.MAKER if at_t else S.TAKER) + d * S.FUNDING_8H * (m - i) * 0.25 / 8
                        rr = abs(tp - e) / risk
                        rows.append((coin, ctx, ptf, mode, d, "IS" if i < split else "OOS", gross, gross - cost * e / risk,
                                     int(at_t), 1 / (1 + rr), rr, risk / e * 100, (px - c_open[i]) * d > 0,
                                     (e - mo[i]) * d > 0, (e - wk[i]) * d > 0, m - i))
        for s, lst in ((1, highs), (-1, lows)):
            for x in lst[:]:
                if (c[i] > x["px"]) if s == 1 else (c[i] < x["px"]):
                    lst.remove(x)


def main():
    D = sys.argv[1]
    rows = []
    for coin in COINS:
        df = pd.read_csv(f"{D}/{coin}_15m.csv", index_col=0, parse_dates=True)[["open", "high", "low", "close"]]
        df = df[(df > 0).all(axis=1)]
        for ctx, ptf in CASES:
            run(coin, df, ctx, ptf, rows)
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows, columns=["coin", "ctx", "piv", "target", "d", "period", "gross", "r", "win", "exp_win", "rr", "risk_pct",
                                "pivot_green", "month_ok", "week_ok", "bars"]).to_csv("results/pivot_ftfc_trades.csv", index=False)


if __name__ == "__main__":
    main()
