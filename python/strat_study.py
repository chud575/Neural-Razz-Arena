"""
The Strat — statistical study (mirrors the rules of pine/strat_study.pine).

Candle types (vs the previous candle):  1 = inside (no new high or low), 2u = new high only, 2d = new low only,
3 = outside (new high and new low).

Part A: how often each type occurs and what follows it (transition probabilities).
Part B: combos. A setup is read on a completed candle i; it triggers on candle i+1 only (Strat triggers are
next-bar only) when price breaks candle i's high (long) or low (short):
  2-1-2 Cont / Rev   2u|2d, 1         -> break of the inside bar either way (continuation = same way as the 2)
  3-1-2              3, 1             -> break of the inside bar either way
  1-2-2 RevStrat     1, 2d (2u)       -> long through the 2d high (short through the 2u low)
  3-2-2 Rev          3, 2d (2u)       -> long through the 2d high (short through the 2u low)
  2-2 Rev            2u|2d, 2d (2u)   -> long through the 2d high (short through the 2u low)
  Baseline (any)     any candle       -> a break of the previous candle's high/low (what every combo is compared to)
Entry: stop order at the trigger (gap fills at the open). Stop: the other end of the trigger candle i.
Targets: "magnitude" = the nearest earlier high (low) beyond the entry within the last 10 candles (Strat-style
previous-candle target; falls back to 2R if none), and fixed 1R / 2R / 3R. Max 100 candles in a trade, then exit at
the close. If candle i+1 breaks BOTH sides (it is a 3) the trade is counted as stopped out (conservative).
FTFC (Full Timeframe Continuity): for a long, the entry price is above the OPEN of the current candle of every higher
timeframe (all "green"); "against" = below all of them; otherwise "mixed".
Costs: Bybit VIP 3 futures (taker entry, maker target / taker stop, funding). IS = first 70% of history, OOS = last 30%.

    python strat_study.py <data_dir> [nofee]   -> results/strat_*.csv  (report: strat_study_report.py)
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
HTFS = {"15m": ["1h", "4h", "D"], "1h": ["4h", "D", "W"], "4h": ["D", "W", "M"], "1d": ["W", "M"]}
RULE = {"1h": "1h", "4h": "4h", "D": "D", "W": "W-SUN", "M": "M"}
TYPES = ["1", "2u", "2d", "3"]
MAXBARS = 100


def classify(h, l):
    t = np.full(len(h), "", dtype=object)
    up, dn = h[1:] > h[:-1], l[1:] < l[:-1]
    t[1:] = np.where(up & dn, "3", np.where(up, "2u", np.where(dn, "2d", "1")))
    return t


def htf_open(df, rule):
    """Open of the current higher-timeframe candle for every chart bar (known at that candle's start)."""
    per = df.index.to_period(RULE[rule]) if rule in ("W", "M", "D") else df.index.floor(rule)
    first = df["open"].groupby(per).transform("first")
    return first.to_numpy(float)


def setups(t, i):
    """Yield (combo, direction) for setups read on completed candle i."""
    a, b = t[i - 1], t[i]
    if b == "1":
        if a in ("2u", "2d"):
            for d in (1, -1):
                same = (d == 1) == (a == "2u")
                yield ("2-1-2 Cont" if same else "2-1-2 Rev"), d
        elif a == "3":
            yield "3-1-2", 1
            yield "3-1-2", -1
    elif b in ("2u", "2d"):
        d = 1 if b == "2d" else -1                       # reversal through the 2's opposite end
        if a == "1":
            yield "1-2-2 RevStrat", d
        elif a == "3":
            yield "3-2-2 Rev", d
        elif a in ("2u", "2d"):
            yield "2-2 Rev", d


def simulate(o, h, l, c, i, d, bar_h, ftfc_opens):
    """Trade triggered on candle i+1 through candle i's high (d=1) / low (d=-1). Returns dict or None."""
    j = i + 1
    if j >= len(c):
        return None
    trig = h[i] if d == 1 else l[i]
    stop = l[i] if d == 1 else h[i]
    if not ((h[j] > trig) if d == 1 else (l[j] < trig)):
        return None                                     # not triggered on the next candle
    e = max(o[j], trig) if d == 1 else min(o[j], trig)
    risk = abs(e - stop)
    if risk <= 0:
        return None
    # magnitude: nearest earlier high (low) beyond the entry within the last 10 candles before i
    lo_k = max(0, i - 10)
    if d == 1:
        cand = h[lo_k:i][h[lo_k:i] > e]
        mag = cand.min() if len(cand) else math.nan
    else:
        cand = l[lo_k:i][l[lo_k:i] < e]
        mag = cand.max() if len(cand) else math.nan
    mag_r = abs(mag - e) / risk if not math.isnan(mag) else 2.0
    # FTFC at entry
    gs = [(e > op) if d == 1 else (e < op) for op in ftfc_opens[:, j]]
    ftfc = "with" if all(gs) else ("against" if not any(gs) else "mixed")
    out = dict(entry_bar=j, d=d, risk_pct=risk / e * 100, mag_r=mag_r, ftfc=ftfc)
    both = (l[j] <= stop) if d == 1 else (h[j] >= stop)   # trigger candle took out the stop too (a 3)
    for name, k in (("mag", mag_r), ("1R", 1.0), ("2R", 2.0), ("3R", 3.0)):
        tgt = e + d * k * risk
        res, px, at_t, bars = None, None, False, 0
        if both:
            res, px = -1, stop
        else:
            if (h[j] >= tgt) if d == 1 else (l[j] <= tgt):
                res, px, at_t = 1, tgt, True
            else:
                for m in range(j + 1, min(len(c), j + 1 + MAXBARS)):
                    if (l[m] <= stop) if d == 1 else (h[m] >= stop):
                        res, px, bars = -1, (min(o[m], stop) if d == 1 else max(o[m], stop)), m - j
                        break
                    if (h[m] >= tgt) if d == 1 else (l[m] <= tgt):
                        res, px, at_t, bars = 1, (max(o[m], tgt) if d == 1 else min(o[m], tgt)), True, m - j
                        break
                if res is None:
                    m = min(len(c) - 1, j + MAXBARS)
                    res, px, bars = 0, c[m], m - j
        gross = d * (px - e) / risk
        out[f"r_{name}"] = gross - S.cost_fraction(d, at_t, bars * bar_h) * e / risk
        out[f"hit_{name}"] = res
    return out


def main():
    D = sys.argv[1]
    nofee = len(sys.argv) > 2 and sys.argv[2] == "nofee"       # before-cost run, for comparison
    S.FEE_MODEL = "flat" if nofee else "futures"
    S.COST_RT = 0.0 if nofee else S.COST_RT
    suffix = "_nofee" if nofee else ""
    trades, trans = [], []
    rng = np.random.default_rng(11)
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            t = classify(h, l)
            k_split = int(n * S.SPLIT)
            ftfc_opens = np.vstack([htf_open(df, r) for r in HTFS[tf]])
            # Part A: transitions (type of candle i -> type of candle i+1)
            for per, sl in (("IS", slice(2, k_split)), ("OOS", slice(k_split, n - 1))):
                a, b = t[sl], t[sl.start + 1: sl.stop + 1]
                tab = pd.crosstab(pd.Series(a, name="from"), pd.Series(b, name="to"))
                for fr in tab.index:
                    for to in tab.columns:
                        trans.append(dict(coin=coin, tf=tf, period=per, frm=fr, to=to, n=int(tab.loc[fr, to])))
            # Part B: combos + baseline (baseline sampled to keep the run fast)
            base_idx = set(rng.choice(np.arange(2, n - 1), size=min(n - 3, 15000), replace=False).tolist())
            for i in range(2, n - 1):
                per = "IS" if i + 1 < k_split else "OOS"
                for combo, d in setups(t, i):
                    r = simulate(o, h, l, c, i, d, bar_h, ftfc_opens)
                    if r:
                        trades.append(dict(coin=coin, tf=tf, period=per, combo=combo, setup=f"{t[i-1]}-{t[i]}", **r))
                if i in base_idx:
                    for d in (1, -1):
                        r = simulate(o, h, l, c, i, d, bar_h, ftfc_opens)
                        if r:
                            trades.append(dict(coin=coin, tf=tf, period=per, combo="Baseline (any candle)",
                                               setup=f"{t[i-1]}-{t[i]}", **r))
            print(f"done {coin} {tf}", file=sys.stderr, flush=True)
    pd.DataFrame(trades).to_csv(f"results/strat_trades{suffix}.csv", index=False)
    pd.DataFrame(trans).to_csv("results/strat_transitions.csv", index=False)
    print(f"trades {len(trades)}", file=sys.stderr)


if __name__ == "__main__":
    main()
