"""
"Impulse leg + pullback" strategy study (the tracker in pine/impulse_legs.pine v1.6).

Leg = pine/impulse_legs.pine defaults. When a leg is declared finished: limit order in its pullback half at
`depth` % (0 = the midline, 100 = the leg's start), stop at the leg's start, targets as multiples of the risk.
Skipped if price already traded through the stop since the extreme; taken at that close if price is already at or
beyond the entry; cancelled if price breaks beyond the leg's extreme before the fill. Stop first in a shared candle.
Costs: Bybit VIP 3 futures (maker limit entry and targets, taker stop / market entry, funding). R = units × risk.
Trend filter (optional): EMA 50 above EMA 200 on the leg's own timeframe for longs (below for shorts).

    python leg_pullback_study.py <data_dir>   -> results/leg_pullback.csv / .md
"""
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from impulse_study import find_legs

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h"]
DEPTHS = (0, 25, 50, 75)
TSETS = {"1R/2R/3R split": ((1, .34), (2, .33), (3, .33)), "1R only": ((1, 1.0),), "2R only": ((2, 1.0),), "3R only": ((3, 1.0),)}
MAXB = 3000


def trade(o, h, l, c, fin, eB, d, sP, eP, depth, tset, bar_h):
    n = len(c)
    eq = (sP + eP) / 2
    px = eq + (sP - eq) * depth / 100
    seg_l, seg_h = l[eB + 1:fin + 1], h[eB + 1:fin + 1]
    if len(seg_l) and ((seg_l.min() <= sP) if d == 1 else (seg_h.max() >= sP)):
        return None, "dead"
    entry_fee = S.MAKER
    if (c[fin] <= px) if d == 1 else (c[fin] >= px):
        e, f, entry_fee = c[fin], fin, S.TAKER
    else:
        f = None
        for m in range(fin + 1, min(n, fin + 1 + MAXB)):
            if (l[m] <= px) if d == 1 else (h[m] >= px):
                e, f = (min(o[m], px) if d == 1 else max(o[m], px)), m
                break
            if (h[m] > eP) if d == 1 else (l[m] < eP):
                return None, "cancelled"
        if f is None:
            return None, "cancelled"
    risk = abs(e - sP)
    if risk <= 0 or (e - sP) * d <= 0:
        return None, "dead"
    pnl = cost = 0.0
    rem, k, hits = 1.0, 0, 0
    fund = lambda m: d * S.FUNDING_8H * (m - f) * bar_h / 8
    cost += entry_fee
    m = f if f != fin else fin + 1
    if f != fin and ((l[f] <= sP) if d == 1 else (h[f] >= sP)):            # filled and stopped in the same candle
        return dict(r=-1 - (cost + S.TAKER) * e / risk, hits=0, bars=0, risk=risk / e * 100), "filled"
    m = f + 1
    end = min(n, f + 1 + MAXB)
    while m < end and rem > 1e-9:
        if (l[m] <= sP) if d == 1 else (h[m] >= sP):
            xp = min(o[m], sP) if d == 1 else max(o[m], sP)
            pnl += rem * d * (xp - e) / risk
            cost += rem * (S.TAKER + fund(m))
            rem = 0
            break
        while k < len(tset) and rem > 1e-9:
            tp = e + d * tset[k][0] * risk
            if (h[m] >= tp) if d == 1 else (l[m] <= tp):
                xp = max(o[m], tp) if d == 1 else min(o[m], tp)
                sh = min(tset[k][1], rem)
                pnl += sh * d * (xp - e) / risk
                cost += sh * (S.MAKER + fund(m))
                rem -= sh
                hits += 1
                k += 1
            else:
                break
        m += 1
    if rem > 1e-9:
        m = min(end - 1, m)
        pnl += rem * d * (c[m] - e) / risk
        cost += rem * (S.TAKER + fund(m))
    return dict(r=pnl - cost * e / risk, gross=pnl, hits=hits, bars=m - f, risk=risk / e * 100, e=e, usd=(pnl - cost * e / risk) * risk), "filled"


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows, counts = [], []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(n * S.SPLIT)
            cs = pd.Series(c)
            up = (cs.ewm(span=50, adjust=False).mean() > cs.ewm(span=200, adjust=False).mean()).to_numpy()
            legs = [x for x in find_legs(h, l, c) if x[5] < n - 3]
            for depth in DEPTHS:
                st = {"filled": 0, "cancelled": 0, "dead": 0}
                for sB, eB, sP, eP, d, fin in legs:
                    with_trend = bool(up[fin]) == (d == 1)
                    for name, tset in TSETS.items():
                        res, why = trade(o, h, l, c, fin, eB, d, sP, eP, depth, tset, bar_h)
                        if name == "1R/2R/3R split":
                            st[why] += 1
                        if res:
                            rows.append((coin, tf, depth, name, d, "IS" if fin < split else "OOS", int(with_trend), res["r"], res.get("gross", -1.0), res["hits"],
                                         res["risk"], res.get("usd", np.nan), str(df.index[fin])[:10]))
                counts.append((coin, tf, depth, len(legs), st["filled"], st["cancelled"], st["dead"]))
        print("done", coin, file=sys.stderr, flush=True)
    t = pd.DataFrame(rows, columns=["coin", "tf", "depth", "targets", "d", "period", "trend", "r", "gross", "hits", "risk", "usd", "date"])
    t.to_csv("results/leg_pullback.csv", index=False)
    pd.DataFrame(counts, columns=["coin", "tf", "depth", "legs", "filled", "cancelled", "dead"]).to_csv("results/leg_pullback_counts.csv", index=False)


if __name__ == "__main__":
    main()
