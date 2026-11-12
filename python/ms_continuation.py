"""
Market-structure continuation: lower-timeframe structure entries in the direction of the higher timeframe.

Chart structure = structure() with swing length 5 (pine/trend_finder.pine). Entries (long; shorts mirror), at a close:
  BOS       a close above the latest swing high while chart structure was already bullish
  CHoCH     a close above the latest swing high while chart structure was bearish (first break back up)
  pullback  chart structure bullish and a new HIGHER LOW has just been confirmed
Stop = the latest chart swing low (must be below the entry).
Filter (closed higher-timeframe candles, swing length 3):
  none | bias (HTF structure bias agrees) | trend (HTF strict trend agrees) | both (bias agrees on two HTFs)
Exits: 2R | 3R | trail (stop moves up to each new chart swing low; no target; max 300 bars).
Costs: Bybit VIP 3 futures (taker entry, maker target, taker stop, funding). One trade at a time per row.

    python ms_continuation.py <data_dir>   -> results/ms_continuation_trades.csv
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import resample, structure

COINS = ["btc", "eth", "avax", "xrp"]
HTFS = {"15m": ("1h", "4h"), "1h": ("4h", "1D"), "4h": ("1D", "1W")}
MAXBARS = 300


def run(coin, tf, df, rows):
    o, h, l, c = (df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    n = len(c)
    bar_h = df.index.to_series().diff().median().total_seconds() / 3600
    split = int(n * S.SPLIT)
    st = structure(h, l, c, 5)
    hb, ht = [], []
    for rule in HTFS[tf]:
        g, pos = resample(df, rule)
        hs = structure(g["high"].to_numpy(float), g["low"].to_numpy(float), g["close"].to_numpy(float), 3)
        p = np.maximum(pos - 1, 0)
        hb.append(np.where(pos > 0, hs["ms"][p], 0))
        ht.append(np.where(pos > 0, hs["trend"][p], 0))
    ms_prev = np.r_[0, st["ms"][:-1]]
    sig = {}
    for d in (1, -1):
        sig[("BOS", d)] = st["ev"] == d
        sig[("CHoCH", d)] = st["ev"] == 2 * d
        sig[("pullback", d)] = (st["newL"] & (st["loUp"] == 1) & (st["ms"] == 1) & (ms_prev == 1)) if d == 1 else \
                               (st["newH"] & (st["hiUp"] == -1) & (st["ms"] == -1) & (ms_prev == -1))
    filt = {"none": lambda d: np.ones(n, bool), f"bias {HTFS[tf][0]}": lambda d: hb[0] == d, f"bias {HTFS[tf][1]}": lambda d: hb[1] == d,
            f"trend {HTFS[tf][0]}": lambda d: ht[0] == d, f"trend {HTFS[tf][1]}": lambda d: ht[1] == d,
            "bias both": lambda d: (hb[0] == d) & (hb[1] == d)}
    lastH, lastL = st["lastH"], st["lastL"]
    for ename in ("BOS", "CHoCH", "pullback"):
        for fname, F in filt.items():
            ok = {d: sig[(ename, d)] & F(d) for d in (1, -1)}
            idx = np.flatnonzero(ok[1] | ok[-1])
            for mode in ("2R", "3R", "trail"):
                busy = -1
                for i in idx:
                    if i <= busy or i >= n - 1:
                        continue
                    d = 1 if ok[1][i] else -1
                    e = c[i]
                    stop = lastL[i] if d == 1 else lastH[i]
                    if math.isnan(stop) or (e - stop) * d <= 0:
                        continue
                    risk = abs(e - stop)
                    tp = e + d * float(mode[0]) * risk if mode != "trail" else math.nan
                    px, at_t, m = None, False, i + 1
                    end = min(n, i + 1 + MAXBARS)
                    while m < end:
                        if mode == "trail":
                            ns = lastL[m - 1] if d == 1 else lastH[m - 1]
                            if not math.isnan(ns):
                                stop = max(stop, ns) if d == 1 else min(stop, ns)
                        if (l[m] <= stop) if d == 1 else (h[m] >= stop):
                            px = min(o[m], stop) if d == 1 else max(o[m], stop)
                            break
                        if mode != "trail" and ((h[m] >= tp) if d == 1 else (l[m] <= tp)):
                            px, at_t = (max(o[m], tp) if d == 1 else min(o[m], tp)), True
                            break
                        m += 1
                    if px is None:
                        m = end - 1
                        px = c[m]
                    busy = m
                    gross = d * (px - e) / risk
                    rows.append((coin, tf, ename, fname.replace(HTFS[tf][0], "HTF1").replace(HTFS[tf][1], "HTF2"), mode, d,
                                 "IS" if i < split else "OOS", gross, gross - S.cost_fraction(d, at_t, (m - i) * bar_h) * e / risk,
                                 risk / e * 100, m - i))


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, ["15m", "1h", "4h"], coin)
        for tf in ("15m", "1h", "4h"):
            run(coin, tf, S.DATA[tf], rows)
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows, columns=["coin", "tf", "entry", "filter", "exit", "d", "period", "gross", "r", "risk_pct", "bars"]).to_csv(
        "results/ms_continuation_trades.csv", index=False)


if __name__ == "__main__":
    main()
