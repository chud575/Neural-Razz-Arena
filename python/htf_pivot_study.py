"""
HTF pivot study — how price moves between higher-timeframe pivot lines (same lines as pine/htf_pivot_lines.pine).

Chart = 15m candles. Pivots = swing highs / lows of the 1h and 4h candles (3 candles each side, confirmed 3 candles
later, closed candles only). A line is active from its confirmation until a 15m candle CLOSES through it; at most
5 active lines per side per timeframe (oldest dropped), as in the indicator.

Events
  touch    first time a 15m candle's wick reaches an active line
  break    a 15m candle closes through an active line
  bounce   price touched a line, then reached the nearest opposite line before closing through the first one
Races (from the event price): which of two lines is reached first by a wick, within 2000 candles (~3 weeks).
  "expected" = what a coin flip with no memory would give from the two distances alone: P(far side A first) =
  distance to B / (distance to A + distance to B). A race only says something when "actual" differs from "expected".

    python htf_pivot_study.py <data_dir>     -> results/htf_pivot_study.md (+ results/htf_pivot_races.csv)
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

from dtdb_backtest import pivots

COINS = ["btc", "eth", "avax", "xrp"]
PIV, MAXL, HORIZON = 3, 5, 2000
TFS = {"1h": "1h", "4h": "4h"}


def htf_pivot_events(df, rule):
    """[(chart bar index where the line appears, +1 high / -1 low, price, pivot time)]"""
    g = df.resample(rule).agg({"high": "max", "low": "min"}).dropna()
    ph, pl = pivots(g["high"].to_numpy(float), g["low"].to_numpy(float), PIV)   # indexed by confirmation candle
    pos = df.index.searchsorted(g.index)                                         # first chart bar of each HTF candle
    out = []
    for k in range(len(g) - 1):
        for s, arr in ((1, ph), (-1, pl)):
            if not math.isnan(arr[k]):
                out.append((int(pos[k + 1]), s, float(arr[k]), int(pos[k - PIV])))
    return out


def race(h, l, i, up, dn):
    """First of up / dn reached by a wick after bar i. Returns 1 (up), -1 (down), 0 (neither / same candle)."""
    if up is None or dn is None:
        return None
    e = min(len(h), i + 1 + HORIZON)
    hu = np.flatnonzero(h[i + 1:e] >= up)
    hd = np.flatnonzero(l[i + 1:e] <= dn)
    a = hu[0] if len(hu) else 10 ** 9
    b = hd[0] if len(hd) else 10 ** 9
    return 0 if a == b else (1 if a < b else -1)


def run(coin, df, rows, bounces):
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    ev = {}
    for tf, rule in TFS.items():
        for bar, s, px, pb in htf_pivot_events(df, rule):
            ev.setdefault(bar, []).append((s, px, tf, pb))
    highs, lows = [], []                       # dicts: px, tf, touched
    pend = []                                  # bounces in progress

    def nxt(levels, ref, above, tf=None):
        xs = [x["px"] for x in levels if (tf is None or x["tf"] == tf) and ((x["px"] > ref) if above else (x["px"] < ref))]
        return (min(xs) if above else max(xs)) if xs else None

    def tf_of(levels, px):
        return next(x["tf"] for x in levels if x["px"] == px)

    def add_races(i, kind, s, tf, ref, extra=""):
        """s = +1: event at a high (looking up = continuation), -1: at a low. Races are stored 'continuation vs reversal'."""
        fw, bk = (highs, lows) if s == 1 else (lows, highs)
        for name, ftf, btf in (("next pivot ahead (any) vs nearest pivot behind (any)", None, None),
                               ("next 4h ahead vs nearest 1h behind", "4h", "1h"),
                               ("next 4h ahead vs nearest 4h behind", "4h", "4h"),
                               ("next 1h ahead vs nearest 1h behind", "1h", "1h")):
            A = nxt(fw, ref, s == 1, ftf)
            B = nxt(bk, ref, s != 1, btf)
            if A is None or B is None:
                continue
            r = race(h, l, i, A if s == 1 else B, B if s == 1 else A)
            if r is None:
                continue
            da, db = abs(A - ref), abs(B - ref)
            rows.append((coin, i / n, kind, tf, "high" if s == 1 else "low", name, extra,
                         int(r == s), int(r == -s), int(r == 0), db / (da + db), da / ref * 100, db / ref * 100))

    for i in range(n):
        for s, px, tf, pb in ev.get(i, []):
            closed = c[pb + 1:i]
            if len(closed) and ((closed.max() > px) if s == 1 else (closed.min() < px)):
                continue                                           # already closed through before it was confirmed
            lst = highs if s == 1 else lows
            lst.append(dict(px=px, tf=tf, touched=False))
            same = [x for x in lst if x["tf"] == tf]
            if len(same) > MAXL:
                lst.remove(same[0])
        # bounces in progress
        for b in pend[:]:
            s = b["s"]                                             # +1: touched a high, heading down to b["tgt"]
            if (l[i] <= b["tgt"]) if s == 1 else (h[i] >= b["tgt"]):
                pend.remove(b)
                bounces.append((coin, b["tf"], "high" if s == 1 else "low", b["ttf"], 1))
                add_races(i, "bounce complete", -s, b["ttf"], b["tgt"], extra=f"from {b['tf']} {'high' if s == 1 else 'low'}")
            elif (c[i] > b["px"]) if s == 1 else (c[i] < b["px"]):
                pend.remove(b)
                bounces.append((coin, b["tf"], "high" if s == 1 else "low", b["ttf"], 0))
            elif i - b["bar"] > HORIZON:
                pend.remove(b)
        # touches
        for s, lst, opp in ((1, highs, lows), (-1, lows, highs)):
            for x in lst:
                if not x["touched"] and ((h[i] >= x["px"]) if s == 1 else (l[i] <= x["px"])):
                    x["touched"] = True
                    add_races(i, "touch", s, x["tf"], x["px"])
                    tgt = nxt(opp, x["px"], s != 1)
                    if tgt is not None and not ((c[i] > x["px"]) if s == 1 else (c[i] < x["px"])):
                        pend.append(dict(s=s, px=x["px"], tf=x["tf"], tgt=tgt, ttf=tf_of(opp, tgt), bar=i))
        # breaks (close through) -> line removed
        for s, lst in ((1, highs), (-1, lows)):
            for x in lst[:]:
                if (c[i] > x["px"]) if s == 1 else (c[i] < x["px"]):
                    lst.remove(x)
                    add_races(i, "break", s, x["tf"], c[i])


def main():
    D = sys.argv[1]
    rows, bounces = [], []
    for coin in COINS:
        df = pd.read_csv(f"{D}/{coin}_15m.csv", index_col=0, parse_dates=True)[["open", "high", "low", "close"]]
        df = df[(df > 0).all(axis=1)]
        run(coin, df, rows, bounces)
        print("done", coin, file=sys.stderr, flush=True)
    R = pd.DataFrame(rows, columns=["coin", "pos", "event", "tf", "side", "race", "extra", "ahead", "behind", "none", "exp", "dA", "dB"])
    B = pd.DataFrame(bounces, columns=["coin", "tf", "side", "target_tf", "ok"])
    R.to_csv("results/htf_pivot_races.csv", index=False)
    B.to_csv("results/htf_pivot_bounces.csv", index=False)


if __name__ == "__main__":
    main()
