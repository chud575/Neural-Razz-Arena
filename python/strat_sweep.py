"""
The Strat — sweep-and-reclaim reversal after a big directional candle (2-2 / 2-3 reversal), timed on 15m candles.

Setup (long; shorts are the mirror image)
  * Setup candle (1h or 4h): a 2d (new low, no new high; optionally also a 3) that FELL at least `move` % open→close,
    optionally with a wick on both ends (each ≥ 5 % of its range). H, L, C = its high, low, close.
  * In the next candle(s) price must first SWEEP below L, then come back up to C.
        mode "close": enter at the close of the first 15m candle that closes at or above C after the sweep
        mode "stop":  once a sweep has been seen on an earlier 15m candle, a resting buy-stop at C (a gap fills at
                      the open; if that candle also makes a new low the trade counts as stopped); a candle that
                      both sweeps and closes back above C is entered at its close.
    The entry must happen within `window` setup-timeframe candles after the setup candle.
  * Stop = the sweep low (lowest low since the setup candle closed). Target = H of the setup candle ("high"),
    the middle of the setup candle ("mid"), or 1R / 2R. Max 48 h in a trade, then exit at the 15m close.
  * Stop first if stop and target are touched in the same 15m candle. One trade per setup candle.
Costs: Bybit VIP 3 futures (taker entry, maker target / taker stop, funding). IS = first 70 % of history, OOS = last 30 %.
Random benchmark: random 15m entries in the same period with the same direction, stop distance (%), reward:risk, costs.

    python strat_sweep.py <data_dir>      -> results/strat_sweep_trades.csv, results/strat_sweep.md
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S

COINS = ["btc", "eth", "avax", "xrp"]
SETUP_TFS = {"1h": 4, "4h": 16}                 # 15m candles per setup candle
MOVES = (0.5, 1.0, 1.5, 2.0, 3.0)
TARGETS = ("high", "mid", "1R", "2R")
MAX_HOLD = 192                                  # 15m candles = 48 h


def run(coin, df15, tf, k, rows):
    o, h, l, c = (df15[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    n = len(c)
    grp = df15.index.floor(tf)
    g = df15.groupby(grp).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"),
                              cnt=("open", "size"))
    first = pd.Series(np.arange(n), index=df15.index).groupby(grp).first().to_numpy()
    O, H, L, C, cnt = (g[x].to_numpy(float) for x in ("open", "high", "low", "close", "cnt"))
    split = int(n * S.SPLIT)
    for i in range(1, len(g) - 1):
        if cnt[i] < k or cnt[i - 1] < k:
            continue
        up, dn = H[i] > H[i - 1], L[i] < L[i - 1]
        if not (up or dn):
            continue
        typ = "3" if (up and dn) else ("2u" if up else "2d")
        mv = (C[i] - O[i]) / O[i] * 100
        if typ == "3":
            continue
        d = 1 if typ == "2d" else -1                    # fade: long after a 2d, short after a 2u
        # structure: for how many earlier candles is this the lowest low (highest high)? (capped at 100)
        ll = 0
        for q in range(i - 1, max(-1, i - 101), -1):
            if (L[q] <= L[i]) if d == 1 else (H[q] >= H[i]):
                break
            ll += 1
        rng = H[i] - L[i]
        wicks = min(H[i] - max(O[i], C[i]), min(O[i], C[i]) - L[i]) / rng >= 0.05 if rng > 0 else False
        ext0 = L[i] if d == 1 else H[i]                 # level to sweep
        lvl = C[i]                                      # entry level
        s0 = first[i + 1]
        for window, mode in ((1, "close"), (1, "stop")):
            ext, swept, fill, lost = ext0, False, None, False
            for j in range(s0, min(n, s0 + window * k)):
                new_ext = (l[j] < ext) if d == 1 else (h[j] > ext)
                back = (c[j] >= lvl) if d == 1 else (c[j] <= lvl)
                touch = (h[j] >= lvl) if d == 1 else (l[j] <= lvl)
                if mode == "stop" and swept and touch:      # resting stop order at the level, sweep seen earlier
                    fill = (j, (max(o[j], lvl) if d == 1 else min(o[j], lvl)), False)
                    lost = new_ext                          # same candle also made a new extreme: count as stopped
                    break
                if new_ext:
                    ext = l[j] if d == 1 else h[j]
                    swept = True
                if swept and back:                          # 15m close back through the level: enter at that close
                    fill = (j, c[j], True)
                    break
            if fill is None:
                continue
            j, e, at_close = fill
            stop = ext
            risk = abs(e - stop)
            if risk <= 0:
                continue
            if lost:
                for tg in TARGETS:
                    rows.append(dict(coin=coin, tf=tf, typ=typ, d=d, move=-d * mv, ll=ll, wicks=wicks, window=window, mode=mode,
                                     target=tg, period="IS" if j < split else "OOS", bar=j, e=e, risk_pct=risk / e * 100,
                                     rr=math.nan, gross=-1.0, r=-1.0 - S.cost_fraction(d, False, 0) * e / risk, win=False,
                                     bars=0, same_candle=(j - s0) < k))
                continue
            for tg in TARGETS:
                if tg == "high":
                    tp = H[i] if d == 1 else L[i]
                elif tg == "mid":
                    tp = (H[i] + L[i]) / 2
                else:
                    tp = e + d * float(tg[0]) * risk
                if (tp - e) * d <= 0:
                    continue
                px, at_t, m = None, False, j if not at_close else j + 1
                end = min(n, j + 1 + MAX_HOLD)
                while m < end:
                    if m > j and ((l[m] <= stop) if d == 1 else (h[m] >= stop)):
                        px = min(o[m], stop) if d == 1 else max(o[m], stop)
                        break
                    if (h[m] >= tp) if d == 1 else (l[m] <= tp):
                        px, at_t = (max(o[m], tp) if (d == 1 and m > j) else tp if m == j else min(o[m], tp)), True
                        break
                    m += 1
                if px is None:
                    m = min(n - 1, j + MAX_HOLD)
                    px = c[m]
                gross = d * (px - e) / risk
                net = gross - S.cost_fraction(d, at_t, (m - j) * 0.25) * e / risk
                rows.append(dict(coin=coin, tf=tf, typ=typ, d=d, move=-d * mv, ll=ll, wicks=wicks, window=window, mode=mode, target=tg,
                                 period="IS" if j < split else "OOS", bar=j, e=e, risk_pct=risk / e * 100,
                                 rr=abs(tp - e) / risk, gross=gross, r=net, win=at_t, bars=m - j,
                                 same_candle=(j - s0) < k))


def random_control(df15, sub, reps=10, seed=3):
    """Random 15m entries in the same IS/OOS period: same direction, stop distance, reward:risk, costs, max hold."""
    o, h, l, c = (df15[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    n = len(c)
    split = int(n * S.SPLIT)
    rng = np.random.default_rng(seed)
    out = []
    for t in sub.itertuples():
        lo, hi = (0, split) if t.period == "IS" else (split, n - 2)
        for _ in range(reps):
            i = int(rng.integers(lo, hi))
            e, d = c[i], t.d
            stop = e * (1 - d * t.risk_pct / 100)
            risk = abs(e - stop)
            tp = e + d * t.rr * risk
            px, at_t, m = None, False, i + 1
            end = min(n, i + 1 + MAX_HOLD)
            while m < end:
                if (l[m] <= stop) if d == 1 else (h[m] >= stop):
                    px = min(o[m], stop) if d == 1 else max(o[m], stop)
                    break
                if (h[m] >= tp) if d == 1 else (l[m] <= tp):
                    px, at_t = (max(o[m], tp) if d == 1 else min(o[m], tp)), True
                    break
                m += 1
            if px is None:
                m = min(n - 1, i + MAX_HOLD)
                px = c[m]
            out.append((t.period, d * (px - e) / risk - S.cost_fraction(d, at_t, (m - i) * 0.25) * e / risk))
    return pd.DataFrame(out, columns=["period", "r"])


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    for coin in COINS:
        df = pd.read_csv(f"{D}/{coin}_15m.csv", index_col=0, parse_dates=True)[["open", "high", "low", "close"]]
        df = df[(df > 0).all(axis=1)]
        for tf, k in SETUP_TFS.items():
            run(coin, df, tf, k, rows)
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows).to_csv("results/strat_sweep_trades.csv", index=False)
    print("trades", len(rows), file=sys.stderr)


if __name__ == "__main__":
    main()
