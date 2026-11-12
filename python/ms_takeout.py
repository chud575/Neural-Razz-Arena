"""
Takeout of the last swing high in a bearish higher-timeframe structure (and the mirror).

Structure timeframe S (e.g. daily, swing length 3, closed candles only), execution timeframe E (e.g. 1h):
  * S structure is BEARISH (last structure break was down) and its latest swing high has not been closed through.
  * Takeout: price trades ABOVE that swing high on E.
  * Entry "reclaim": the first E close back below the swing high (short at that close).
    Entry "S close":  the S candle that traded above it closes back below it (short at that close).
  * Stop = the highest high since the takeout began. A swing high is traded once.
  * Target "low" = the S structure's latest swing low; or 2R / 3R. Max 40 S candles in the trade.
Costs: Bybit VIP 3 futures (taker entry, maker target, taker stop, funding).

    python ms_takeout.py <data_dir>   -> results/ms_takeout_trades.csv
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import resample, structure

COINS = ["btc", "eth", "avax", "xrp"]
CASES = [("1h", "1D", 24), ("1h", "4h", 4), ("15m", "1h", 4), ("15m", "4h", 16), ("1h", "1W", 168)]
SWING = 3


def run(coin, df, etf, stf, k, rows):
    o, h, l, c = (df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    n = len(c)
    bar_h = 0.25 if etf == "15m" else 1.0
    split = int(n * S.SPLIT)
    g, pos = resample(df, stf)
    st = structure(g["high"].to_numpy(float), g["low"].to_numpy(float), g["close"].to_numpy(float), SWING)
    last_of = np.r_[pos[1:] != pos[:-1], True]                 # last execution bar of each S candle
    max_hold = 40 * k
    cur = {1: None, -1: None}                                  # per direction d (1 long = takeout of a low)
    for i in range(n):
        p = pos[i] - 1
        if p < 0:
            continue
        for d in (1, -1):
            ms = st["ms"][p]
            lvl = st["lastL"][p] if d == 1 else st["lastH"][p]
            brk = st["lBrk"][p] if d == 1 else st["hBrk"][p]
            lid = st["lastLb"][p] if d == 1 else st["lastHb"][p]
            s = cur[d]
            if ms != d or brk or math.isnan(lvl):
                cur[d] = None
                continue
            if s is None or s["id"] != lid:
                s = cur[d] = dict(id=lid, swept=False, ext=math.nan, done=set(), day_swept=-1)
            beyond = (l[i] < lvl) if d == 1 else (h[i] > lvl)
            if beyond:
                s["ext"] = l[i] if not s["swept"] else (min(s["ext"], l[i]) if d == 1 else max(s["ext"], h[i]))
                if not s["swept"] and d == -1:
                    s["ext"] = h[i]
                s["swept"] = True
                s["day_swept"] = pos[i]
            if not s["swept"]:
                continue
            back = (c[i] > lvl) if d == 1 else (c[i] < lvl)
            modes = []
            if back and "reclaim" not in s["done"]:
                modes.append("reclaim")
            if back and last_of[i] and s["day_swept"] == pos[i] and "S close" not in s["done"]:
                modes.append("S close")
            for mode in modes:
                s["done"].add(mode)
                e, stop = c[i], s["ext"]
                risk = abs(e - stop)
                if risk <= 0:
                    continue
                far = st["lastH"][p] if d == 1 else st["lastL"][p]
                for tg in ("structure", "2R", "3R"):
                    tp = far if tg == "structure" else e + d * float(tg[0]) * risk
                    if math.isnan(tp) or (tp - e) * d <= 0:
                        continue
                    px, at_t, m = None, False, i + 1
                    end = min(n, i + 1 + max_hold)
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
                    gross = d * (px - e) / risk
                    rr = abs(tp - e) / risk
                    rows.append((coin, etf, stf, mode, tg, d, "IS" if i < split else "OOS", gross,
                                 gross - S.cost_fraction(d, at_t, (m - i) * bar_h) * e / risk, int(at_t), 1 / (1 + rr), rr,
                                 risk / e * 100, int(st["trend"][p] == d), int(st["hiUp"][p]), int(st["loUp"][p])))


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    for coin in COINS:
        data = {tf: pd.read_csv(f"{D}/{coin}_{tf}.csv", index_col=0, parse_dates=True)[["open", "high", "low", "close"]] for tf in ("15m", "1h")}
        for etf, stf, k in CASES:
            df = data[etf]
            run(coin, df[(df > 0).all(axis=1)], etf, stf, k, rows)
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows, columns=["coin", "exec", "struct", "entry", "target", "d", "period", "gross", "r", "win", "exp_win", "rr", "risk_pct",
                                "strict", "hiUp", "loUp"]).to_csv("results/ms_takeout_trades.csv", index=False)


if __name__ == "__main__":
    main()
