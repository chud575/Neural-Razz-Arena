"""
1h break-of-structure strategy: after a stop-out, re-enter if price comes back to the ORIGINAL entry price.

Base trade: BOS at a 1h close, stop at the latest swing, 2R target, max 300 bars, one trade at a time.
Re-entry: after a base trade is stopped, a resting stop-order at the original entry price in the same direction
  (a gap fills at the open), valid for 300 bars and cancelled as soon as a new base trade starts. Same target price.
    stop "orig" = the original stop level       stop "low" = the furthest price reached since the stop-out
  A re-entry that stops out is not re-entered again ("once"), or is ("repeat").
Costs: Bybit VIP 3 futures (taker entry, maker target, taker stop, funding). R0 = the original trade's risk.

    python bos_reentry.py <data_dir>   -> results/bos_reentry.csv
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import structure

MAXB = 300


def simulate(o, h, l, c, st, mode, repeat):
    """mode: None (base only) | 'orig' | 'low'. Returns list of trades (bar, kind 'base'/'re', d, r in own R, r in R0, outcome)."""
    n = len(c)
    ev = st["ev"]
    out = []
    tr = None            # open trade
    pend = None          # resting re-entry order
    for i in range(n):
        if tr is not None and i > tr["bar"]:
            d = tr["d"]
            res = None
            if (l[i] <= tr["stop"]) if d == 1 else (h[i] >= tr["stop"]):
                px, res = (min(o[i], tr["stop"]) if d == 1 else max(o[i], tr["stop"])), "stop"
            elif (h[i] >= tr["tp"]) if d == 1 else (l[i] <= tr["tp"]):
                px, res = (max(o[i], tr["tp"]) if d == 1 else min(o[i], tr["tp"])), "target"
            elif i - tr["bar"] >= MAXB:
                px, res = c[i], "time"
            if res:
                risk = abs(tr["e"] - tr["stop"])
                r = d * (px - tr["e"]) / risk - (S.TAKER + (S.MAKER if res == "target" else S.TAKER) + d * S.FUNDING_8H * (i - tr["bar"]) / 8) * tr["e"] / risk
                out.append((tr["bar"], tr["kind"], d, r, r * risk / tr["R0"], res))
                if res == "stop" and mode and (tr["kind"] == "base" or repeat):
                    pend = dict(d=d, e=tr["e0"], stop0=tr["stop0"], tp=tr["tp"], R0=tr["R0"], ext=(l[i] if d == 1 else h[i]), until=i + MAXB, born=i)
                tr = None
                if res == "stop":
                    continue                           # nothing else on the stop-out candle
        if tr is None and pend is not None:
            d = pend["d"]
            if i > pend["until"]:
                pend = None
            elif i > pend["born"] and ((h[i] >= pend["e"]) if d == 1 else (l[i] <= pend["e"])):
                e = max(o[i], pend["e"]) if d == 1 else min(o[i], pend["e"])
                stop = pend["stop0"] if mode == "orig" else pend["ext"]
                if (e - stop) * d > 0 and (pend["tp"] - e) * d > 0:
                    tr = dict(bar=i, kind="re", d=d, e=e, stop=stop, tp=pend["tp"], R0=pend["R0"], e0=pend["e"], stop0=pend["stop0"])
                pend = None
            else:
                pend["ext"] = min(pend["ext"], l[i]) if d == 1 else max(pend["ext"], h[i])
        if tr is None and abs(ev[i]) == 1 and i < n - 1:
            d = int(ev[i])
            e = c[i]
            stop = st["lastL"][i] if d == 1 else st["lastH"][i]
            if not math.isnan(stop) and (e - stop) * d > 0:
                R0 = abs(e - stop)
                tr = dict(bar=i, kind="base", d=d, e=e, stop=stop, tp=e + d * 2 * R0, R0=R0, e0=e, stop0=stop)
                pend = None
    return out


rows = []
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(sys.argv[1], ["1h"], coin)
    df = S.DATA["1h"]
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    split = int(len(c) * S.SPLIT)
    st = structure(h, l, c, 5)
    for name, mode, rep in (("base", None, False), ("orig stop, once", "orig", False), ("orig stop, repeat", "orig", True),
                            ("low stop, once", "low", False), ("low stop, repeat", "low", True)):
        for bar, kind, d, r, r0, res in simulate(o, h, l, c, st, mode, rep):
            rows.append((coin, name, "IS" if bar < split else "OOS", kind, d, r, r0, res))
t = pd.DataFrame(rows, columns=["coin", "variant", "period", "kind", "d", "r", "r0", "res"])
t.to_csv("results/bos_reentry.csv", index=False)
pd.set_option("display.width", 220)
for v, g in t.groupby("variant", sort=False):
    b, re = g[g.kind == "base"], g[g.kind == "re"]
    def io(x, col):
        return f"{x[x.period == 'IS'][col].mean():+.3f} / {x[x.period == 'OOS'][col].mean():+.3f}"
    tot = g.groupby("period").r0.sum()
    print(f"{v:20} base n={len(b)} R {io(b, 'r')} | re n={len(re)} own R {io(re, 'r')} R0 {io(re, 'r0')} | total R0 IS {tot['IS']:.0f} OOS {tot['OOS']:.0f}"
          + (f" | re outcomes {re.res.value_counts(normalize=True).round(2).to_dict()}" if len(re) else ""))
x = t[(t.variant == "orig stop, once") & (t.kind == "re")]
print(x.groupby(["coin", "period"]).r.agg(["mean", "size"]).round(3).unstack())
print(x.groupby(["d", "period"]).r.agg(["mean", "size"]).round(3).unstack())
b = t[t.variant == "base"]
print("stop-outs in base:", (b.res == "stop").sum(), "re-entries filled:", len(x))
