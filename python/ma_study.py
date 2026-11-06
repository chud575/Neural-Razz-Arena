"""
SMA 50 / 100 / 200 study — "Idea 1": in an uptrend (SMA100 above SMA200 for N bars), price wicks below the SMA200
and closes back above it. How far does it move afterwards, in ATRs? Which conditions make it better or worse?

Event (long side; the short side is the exact mirror, used as a check):
  * trend: SMA100 > SMA200 on every one of the last N bars (N = 50 or 100)
  * touch: previous close above SMA200, this bar's low below SMA200 (a wick through the 200 from above)
  * reclaim: a close back above SMA200 — on the touch bar itself ("same bar") or within K bars after it
  * entry at that close. Stop for trade stats = lowest low from touch to reclaim − 0.1 ATR (just under the wick).
Outcomes (ATR = ATR(14) at the entry bar):
  * MFE / MAE: best / worst excursion over the next H bars, in ATR
  * hit rates: does price reach +k ATR before the stop (conservative: stop first if both in one bar)
  * trade expectancy: target +k ATR, stop under the wick, net of Bybit futures costs (run_btc_sweep cost model)
Baseline: every bar in the same regime (trend on for N bars, close above SMA200) with the same measurements and a
stop placed at the same ATR distance as the event's median stop — so "is this better than just being long in an
uptrend?" can be answered.
Split: first 70% of each history = in-sample, last 30% = out-of-sample.

    python ma_study.py <data_dir> [--out results/ma_study.md]
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from srflip_backtest import atr

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
HORIZONS = [10, 20, 50, 100]
TARGETS = [1, 1.5, 2, 3, 4, 5]


def first_passage(h, l, o, i0, d, entry, stop, tgt, max_bars=500):
    """+1 if target first, -1 if stop first, 0 if neither within max_bars. Returns (result, exit_px, bars)."""
    n = len(h)
    for j in range(i0 + 1, min(n, i0 + 1 + max_bars)):
        if (l[j] <= stop) if d == 1 else (h[j] >= stop):
            return -1, (min(o[j], stop) if d == 1 else max(o[j], stop)), j - i0
        if (h[j] >= tgt) if d == 1 else (l[j] <= tgt):
            return 1, (max(o[j], tgt) if d == 1 else min(o[j], tgt)), j - i0
    return 0, math.nan, max_bars


def find_events(df, N, K, side):
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    s50 = pd.Series(c).rolling(50).mean().to_numpy()
    s100 = pd.Series(c).rolling(100).mean().to_numpy()
    s200 = pd.Series(c).rolling(200).mean().to_numpy()
    a = atr(h, l, c, 14)
    d = side
    up = (s100 > s200) if d == 1 else (s100 < s200)
    run = np.zeros(len(c), int)                       # consecutive bars the trend condition held
    for i in range(1, len(c)):
        run[i] = run[i - 1] + 1 if up[i] else 0
    events = []
    last_touch_bar = -10 ** 9
    touches_in_trend = 0
    i = 201
    n = len(c)
    while i < n - 1:
        if run[i] == 0:
            touches_in_trend = 0
        if run[i - 1] >= N and not math.isnan(a[i]):
            from_side = c[i - 1] > s200[i - 1] if d == 1 else c[i - 1] < s200[i - 1]
            wick = l[i] < s200[i] if d == 1 else h[i] > s200[i]
            if from_side and wick:
                touches_in_trend += 1
                r = None
                for j in range(i, min(n, i + K + 1)):  # reclaim on the touch bar or within K bars
                    if (c[j] > s200[j]) if d == 1 else (c[j] < s200[j]):
                        r = j
                        break
                if r is not None:
                    ext = l[i:r + 1].min() if d == 1 else h[i:r + 1].max()
                    A = a[r]
                    events.append(dict(
                        touch=i, entry=r, d=d, e=c[r], ext=ext, A=A,
                        same_bar=r == i,
                        depth_atr=(s200[i] - ext) / A if d == 1 else (ext - s200[i]) / A,
                        white_crossed=(s50[i] < s100[i]) if d == 1 else (s50[i] > s100[i]),   # 50 crossed the 100
                        white_below_200=(s50[i] < s200[i]) if d == 1 else (s50[i] > s200[i]),
                        trend_bars=run[i - 1],
                        slope200_atr=d * (s200[i] - s200[i - 20]) / A,                       # 20-bar slope of the 200
                        gap100_200_atr=d * (s100[i] - s200[i]) / A,
                        first_touch=touches_in_trend == 1,
                        bars_since_touch=i - last_touch_bar))
                    last_touch_bar = i
                    i = r + 1
                    continue
        i += 1
    return events, (o, h, l, c, s200, a, run, up)


def outcomes(ev, arrs, bar_h):
    o, h, l, c, s200, a, run, up = arrs
    i0, d, e, A = ev["entry"], ev["d"], ev["e"], ev["A"]
    stop = ev["ext"] - d * 0.1 * A
    risk = abs(e - stop)
    res = dict(stop_atr=risk / A)
    for H in HORIZONS:
        j1 = min(len(c), i0 + 1 + H)
        if i0 + 1 >= j1:
            res[f"mfe{H}"] = res[f"mae{H}"] = math.nan
            continue
        if d == 1:
            res[f"mfe{H}"] = (h[i0 + 1:j1].max() - e) / A
            res[f"mae{H}"] = (e - l[i0 + 1:j1].min()) / A
        else:
            res[f"mfe{H}"] = (e - l[i0 + 1:j1].min()) / A
            res[f"mae{H}"] = (h[i0 + 1:j1].max() - e) / A
    for k in TARGETS:
        tgt = e + d * k * A
        hit, px, bars = first_passage(h, l, o, i0, d, e, stop, tgt)
        res[f"hit{k}"] = hit
        if hit == 0 or risk <= 0:
            res[f"r{k}"] = math.nan
        else:
            gross = d * (px - e) / risk
            res[f"r{k}"] = gross - S.cost_fraction(d, hit == 1, bars * bar_h) * e / risk
    return res


def baseline(arrs, N, side, stop_atr, bar_h, idx_range, step):
    """All regime bars (trend on for N bars, close on the trend side of SMA200), sampled every `step` bars."""
    o, h, l, c, s200, a, run, up = arrs
    d = side
    out = []
    for i in range(idx_range[0], idx_range[1], step):
        if run[i] < N or math.isnan(a[i]) or not ((c[i] > s200[i]) if d == 1 else (c[i] < s200[i])):
            continue
        ev = dict(entry=i, d=d, e=c[i], A=a[i], ext=c[i] - d * (stop_atr - 0.1) * a[i])
        out.append(outcomes(ev, arrs, bar_h))
    return pd.DataFrame(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("--out", default="results/ma_study.md")
    ap.add_argument("--csv", default="results/ma_study_events.csv")
    a = ap.parse_args(argv)
    S.FEE_MODEL = "futures"
    rows, base_rows = [], []
    for coin in COINS:
        S.DATA.clear()
        S.load(a.data_dir, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            k_split = int(len(df) * S.SPLIT)
            for side in (1, -1):
                for N in (50, 100):
                    for K in (0, 5):
                        evs, arrs = find_events(df, N, K, side)
                        for ev in evs:
                            r = outcomes(ev, arrs, bar_h)
                            rows.append(dict(coin=coin, tf=tf, side="long" if side == 1 else "short", N=N, K=K,
                                             period="IS" if ev["entry"] < k_split else "OOS",
                                             time=str(df.index[ev["entry"]]),
                                             **{k: v for k, v in ev.items() if k not in ("touch", "entry", "d", "e", "ext", "A")}, **r))
                    # baseline for this coin/tf/side, N=50 and N=100, stop distance ~ typical event stop (filled later)
            print(f"done {coin} {tf}", file=sys.stderr, flush=True)
    ev = pd.DataFrame(rows)
    ev.to_csv(a.csv, index=False)

    # baselines: same regime, stop at the median event stop distance for that coin/tf/side/N
    for coin in COINS:
        S.DATA.clear()
        S.load(a.data_dir, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            n = len(df)
            k_split = int(n * S.SPLIT)
            step = max(1, n // 4000)
            for side in (1, -1):
                for N in (50, 100):
                    sub = ev[(ev.coin == coin) & (ev.tf == tf) & (ev.side == ("long" if side == 1 else "short")) & (ev.N == N)]
                    st = float(sub.stop_atr.median()) if len(sub) else 1.0
                    _, arrs = find_events(df.iloc[:300], N, 0, side)  # cheap way to get the helper arrays shape
                    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
                    s100 = pd.Series(c).rolling(100).mean().to_numpy()
                    s200 = pd.Series(c).rolling(200).mean().to_numpy()
                    A = atr(h, l, c, 14)
                    up = (s100 > s200) if side == 1 else (s100 < s200)
                    run = np.zeros(n, int)
                    for i in range(1, n):
                        run[i] = run[i - 1] + 1 if up[i] else 0
                    arrs = (o, h, l, c, s200, A, run, up)
                    for per, rng in (("IS", (201, k_split)), ("OOS", (k_split, n - 1))):
                        b = baseline(arrs, N, side, st, bar_h, rng, step)
                        if len(b):
                            b["coin"], b["tf"], b["side"], b["N"], b["period"] = coin, tf, ("long" if side == 1 else "short"), N, per
                            base_rows.append(b)
            print(f"baseline {coin} {tf}", file=sys.stderr, flush=True)
    base = pd.concat(base_rows, ignore_index=True)
    base.to_csv(a.csv.replace("events", "baseline"), index=False)
    print(f"events: {len(ev)}  baseline samples: {len(base)}", file=sys.stderr)


if __name__ == "__main__":
    main()
