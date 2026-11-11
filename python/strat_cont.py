"""
The Strat — 2-2 continuation with Full Timeframe Continuity.

Setups (read on completed candle i, triggered on candle i+1 only):
  2-2 Cont     candle i is 2u  -> long when candle i+1 breaks its high (it becomes another 2u); 2d mirror -> short
  2-2-2 Cont   candles i-1 and i are both 2u -> long on the break of candle i's high; 2d mirror
  Baseline     any candle i -> break of its high (long) / low (short), same stops and targets
Stops:   candle   = other end of the trigger candle i (classic Strat stop)
         2candle  = lowest low (highest high) of candles i-1 and i
         1atr     = entry -/+ 1 × ATR(14) of candle i
Targets: 1R, 2R, 3R (stop first if both in one candle; trigger candle checked for the stop first; max 100 candles).
FTFC at entry vs the open of the current candle of each higher timeframe (15m: 1h/4h/D, 1h: 4h/D/W, 4h: D/W/M,
1D: W/M) — "with" = all agree with the trade, "against" = none, else "mixed".
Costs: Bybit VIP 3 futures (taker entry, maker target / taker stop, funding); "gross" = before costs.
IS = first 70% of history, OOS = last 30%.

    python strat_cont.py <data_dir>     -> results/strat_cont_trades.csv (+ report printed / results/strat_cont.md)
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from srflip_backtest import atr
from strat_study import HTFS, classify, htf_open

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
TARGETS = (1.0, 2.0, 3.0)
STOPS = ("candle", "2candle", "1atr")
MAXBARS = 100
CAP = 25000          # max setups per coin/timeframe/setup type (random sample beyond that, to keep run time sane)


def run_trade(o, h, l, c, i, d, stop_kind, a, bar_h):
    j = i + 1
    trig = h[i] if d == 1 else l[i]
    if not ((h[j] > trig) if d == 1 else (l[j] < trig)):
        return None
    e = max(o[j], trig) if d == 1 else min(o[j], trig)
    if stop_kind == "candle":
        stop = l[i] if d == 1 else h[i]
    elif stop_kind == "2candle":
        stop = min(l[i - 1], l[i]) if d == 1 else max(h[i - 1], h[i])
    else:
        if math.isnan(a[i]):
            return None
        stop = e - d * a[i]
    risk = abs(e - stop)
    if risk <= 0 or (e - stop) * d <= 0:
        return None
    out = {}
    tg = {k: e + d * k * risk for k in TARGETS}
    done = {k: None for k in TARGETS}            # (exit_px, at_target, bars)
    # trigger candle: stop first, then targets
    if (l[j] <= stop) if d == 1 else (h[j] >= stop):
        for k in TARGETS:
            done[k] = (stop, False, 0)
    else:
        for k in TARGETS:
            if (h[j] >= tg[k]) if d == 1 else (l[j] <= tg[k]):
                done[k] = (tg[k], True, 0)
        m = j + 1
        end = min(len(c), j + 1 + MAXBARS)
        while m < end and any(v is None for v in done.values()):
            stop_hit = (l[m] <= stop) if d == 1 else (h[m] >= stop)
            for k in TARGETS:
                if done[k] is not None:
                    continue
                if stop_hit:
                    done[k] = ((min(o[m], stop) if d == 1 else max(o[m], stop)), False, m - j)
                elif (h[m] >= tg[k]) if d == 1 else (l[m] <= tg[k]):
                    done[k] = ((max(o[m], tg[k]) if d == 1 else min(o[m], tg[k])), True, m - j)
            m += 1
        last = min(len(c) - 1, j + MAXBARS)
        for k in TARGETS:
            if done[k] is None:
                done[k] = (c[last], False, last - j)
    for k in TARGETS:
        px, at_t, bars = done[k]
        gross = d * (px - e) / risk
        out[f"g{k:g}"] = gross
        out[f"r{k:g}"] = gross - S.cost_fraction(d, at_t, bars * bar_h) * e / risk
        out[f"b{k:g}"] = bars
    out["risk_pct"] = risk / e * 100
    out["e"] = e
    return out


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rng = np.random.default_rng(5)
    rows = []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            t = classify(h, l)
            a = atr(h, l, c, 14)
            k_split = int(n * S.SPLIT)
            opens = np.vstack([htf_open(df, r) for r in HTFS[tf]])
            idx = np.arange(2, n - 1)
            groups = {
                "2-2 Cont": [(i, 1) for i in idx[t[idx] == "2u"]] + [(i, -1) for i in idx[t[idx] == "2d"]],
                "2-2-2 Cont": [(i, 1) for i in idx[(t[idx] == "2u") & (t[idx - 1] == "2u")]] +
                              [(i, -1) for i in idx[(t[idx] == "2d") & (t[idx - 1] == "2d")]],
                "Baseline (any candle)": [(i, d) for i in idx for d in (1, -1)],
            }
            for name, lst in groups.items():
                if len(lst) > CAP:
                    pick = rng.choice(len(lst), size=CAP, replace=False)
                    lst = [lst[p] for p in pick]
                for i, d in lst:
                    j = i + 1
                    for sk in STOPS:
                        r = run_trade(o, h, l, c, i, d, sk, a, bar_h)
                        if r is None:
                            continue
                        gs = [(r["e"] > op) if d == 1 else (r["e"] < op) for op in opens[:, j]]
                        ftfc = "with" if all(gs) else ("against" if not any(gs) else "mixed")
                        rows.append(dict(coin=coin, tf=tf, setup=name, d=d, stop=sk, ftfc=ftfc,
                                         period="IS" if j < k_split else "OOS", **{k: v for k, v in r.items() if k != "e"}))
            print(f"done {coin} {tf}", file=sys.stderr, flush=True)
    df = pd.DataFrame(rows)
    df.to_csv("results/strat_cont_trades.csv", index=False)
    print(f"trades {len(df)}", file=sys.stderr)


if __name__ == "__main__":
    main()
