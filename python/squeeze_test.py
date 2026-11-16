"""
Squeeze-fire strategy test (same squeeze as pine/squeeze_box.pine, default settings).

Squeeze: Bollinger Bands (20, 2, SMA) inside Keltner Channels (20, SMA of true range × 2.0 / 1.5 / 1.0).
Momentum: linear regression (20) of close − avg(avg(highest high, lowest low, 20), EMA(close, 20)).
Box: all bars while the squeeze is at least the chosen level; "range" = box high − box low.
Trade: on the bar the squeeze ends (after at least 3 squeeze bars) enter at the close in the direction of momentum.
  stop "range"  = one range from the entry      stop "edge" = the far edge of the box
  target        = k × range from the entry (k = 1, 2, 3)
Stop first if both are touched in one bar; max 300 bars; one trade at a time.
Costs: Bybit VIP 3 futures (taker entry, maker target, taker stop, funding). IS = first 70 %, OOS = last 30 %.

    python squeeze_test.py <data_dir>   -> results/squeeze_trades.csv
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
N, MINBARS, MAXBARS = 20, 3, 300


def squeeze(df):
    h, l, c = df["high"], df["low"], df["close"]
    basis = c.rolling(N).mean()
    dev = 2.0 * c.rolling(N).std(ddof=0)
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    tr.iloc[0] = np.nan
    rng = tr.rolling(N).mean()
    lvl = np.zeros(len(c), int)
    for k, m in ((1, 2.0), (2, 1.5), (3, 1.0)):
        lvl[((basis - dev > basis - rng * m) & (basis + dev < basis + rng * m)).to_numpy()] = k
    x = c - ((h.rolling(N).max() + l.rolling(N).min()) / 2 + c.ewm(span=N, adjust=False).mean()) / 2
    w = np.arange(1, N + 1)
    wma = x.rolling(N).apply(lambda v: np.dot(v, w) / w.sum(), raw=True)
    mom = 3 * wma - 2 * x.rolling(N).mean()                   # linear-regression end point
    return lvl, mom.to_numpy()


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
            lvl, mom = squeeze(df)
            for need in (1, 2, 3):
                on = lvl >= need
                fires = []
                start = None
                for i in range(n):
                    if on[i]:
                        if start is None:
                            start, top, bot, peak = i, h[i], l[i], lvl[i]
                        else:
                            top, bot, peak = max(top, h[i]), min(bot, l[i]), max(peak, lvl[i])
                    elif start is not None:
                        if i - start >= MINBARS and not np.isnan(mom[i]):
                            fires.append((i, 1 if mom[i] >= 0 else -1, top, bot, i - start, peak))
                        start = None
                for stop_kind in ("range", "edge"):
                    for k in (1.0, 2.0, 3.0):
                        busy = -1
                        for i, d, top, bot, bars, peak in fires:
                            if i <= busy or i >= n - 1:
                                continue
                            e, R = c[i], top - bot
                            stop = e - d * R if stop_kind == "range" else (bot if d == 1 else top)
                            if R <= 0 or (e - stop) * d <= 0:
                                continue
                            risk = abs(e - stop)
                            tp = e + d * k * R
                            px, at_t, m = None, False, i + 1
                            end = min(n, i + 1 + MAXBARS)
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
                            gross = d * (px - e) / risk
                            rows.append((coin, tf, need, stop_kind, k, d, "IS" if i < split else "OOS", gross,
                                         gross - S.cost_fraction(d, at_t, (m - i) * bar_h) * e / risk, int(at_t), risk / e * 100,
                                         k * R / risk, bars, peak, int((e > top) if d == 1 else (e < bot))))
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows, columns=["coin", "tf", "level", "stop", "k", "d", "period", "gross", "r", "win", "risk_pct", "rr", "bars", "peak",
                                "outside"]).to_csv("results/squeeze_trades.csv", index=False)


if __name__ == "__main__":
    main()
