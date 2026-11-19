"""
Impulse legs and the golden pocket (the 61.8 %–65 % Fibonacci retracement of the leg).

Legs = pine/impulse_legs.pine defaults (python/impulse_study.find_legs), on 15m, 1h and 4h. For a leg UP from S to E
(legs down mirrored), after the extreme E:
  * does price come back to the golden pocket (61.8 % retracement) before making a new extreme?
  * how deep does that pullback go (turns inside the pocket / goes through it / through 78.6 % / whole leg)?
  * entering at 61.8 %:
        A  stop at the leg start (100 %), target the extreme           no-edge win rate 38 %
        B  stop at 78.6 %, target the extreme                          no-edge win rate 21 %
        C  stop at 78.6 %, target the 38.2 % level (a bounce)          no-edge win rate 42 %
    R after Bybit VIP 3 fees (maker entry and target, taker stop) and funding.
Higher timeframes (two above each chart): at the moment the pocket is touched —
  * is there a LIVE higher-timeframe impulse leg (finished, extreme not exceeded, start not broken) and does this
    trade go WITH it or AGAINST it?
  * does the chart pocket overlap that leg's own golden pocket (61.8–65 %), or its wider 50–78.6 % zone?
  * is a higher-timeframe swing high / low (swing length 3, last 100 candles) sitting inside the 60–67 % band?
  * is there a fair value gap of the chart leg inside the 60–67 % band?

    python golden_pocket_study.py <data_dir>   -> results/golden_pocket.csv / .md
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from dtdb_backtest import pivots
from impulse_study import HOLD, find_legs, race

COINS = ["btc", "eth", "avax", "xrp"]
HTFS = {"15m": ("1h", "4h"), "1h": ("4h", "1d"), "4h": ("1d", "1w")}
DUR = {"15m": 900, "1h": 3600, "4h": 14400, "1d": 86400, "1w": 604800}


def htf_context(df, tf):
    """Finished legs with the time they became known and the time they stopped being live; confirmed swing levels."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    ts = df.index.values.astype("datetime64[s]").astype(np.int64)
    n = len(c)
    legs = []
    for sB, eB, sP, eP, d, fin in find_legs(h, l, c):
        dead = n
        for m in range(eB + 1, n):
            if ((h[m] > eP) or (l[m] < sP)) if d == 1 else ((l[m] < eP) or (h[m] > sP)):
                dead = m
                break
        known = ts[fin] + DUR[tf]
        dead_t = ts[dead] if dead < n else 2 ** 62
        if dead_t > known:
            legs.append((known, dead_t, d, sP, eP))
    ph, pl = pivots(h, l, 3)
    piv = [(ts[i] + DUR[tf], float(v)) for arr in (ph, pl) for i, v in enumerate(arr) if not math.isnan(v)]
    piv.sort()
    return legs, piv, 100 * DUR[tf]


def main():
    Dd = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    for coin in COINS:
        S.DATA.clear()
        S.load(Dd, ["15m", "1h", "4h", "1d"], coin)
        data = dict(S.DATA)
        data["1w"] = data["1d"].resample("W-MON", label="left", closed="left").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
        ctx = {tf: htf_context(data[tf], tf) for tf in ("1h", "4h", "1d", "1w")}
        for tf in ("15m", "1h", "4h"):
            df = data[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            ts = df.index.values.astype("datetime64[s]").astype(np.int64)
            n = len(c)
            bar_h = DUR[tf] / 3600
            split = int(n * S.SPLIT)
            for sB, eB, sP, eP, d, fin in find_legs(h, l, c):
                if eB >= n - 3:
                    continue
                leg = abs(eP - sP)
                lv = lambda f: eP - d * f * leg                       # price at retracement f
                per = "IS" if eB < split else "OOS"
                touch, dep = None, 0.0
                outcome = "open"
                for m in range(eB + 1, min(n, eB + 1 + HOLD)):
                    pb = (eP - l[m]) / leg if d == 1 else (h[m] - eP) / leg
                    if touch is None and pb >= 0.618:
                        touch = m
                    if pb >= 1:
                        dep, outcome = 1.0, "full retrace"
                        break
                    dep = max(dep, pb)
                    if (h[m] > eP) if d == 1 else (l[m] < eP):
                        outcome = "new extreme"
                        break
                row = dict(coin=coin, tf=tf, period=per, d=d, leg_pct=leg / sP * 100, touched=int(touch is not None), outcome=outcome, depth=dep)
                if touch is not None:
                    e = lv(0.618)
                    if not ((o[touch] >= e) if d == 1 else (o[touch] <= e)):
                        e = o[touch]
                    for name, stop, tgt in (("A", sP, eP), ("B", lv(0.786), eP), ("C", lv(0.786), lv(0.382))):
                        if (e - stop) * d <= 0 or (tgt - e) * d <= 0:
                            continue
                        res, g, r = race(o, h, l, c, touch, d, e, stop, tgt, bar_h)
                        row[name + "_win"], row[name + "_gross"], row[name + "_r"] = int(res == 1), g, r
                        row[name + "_exp"] = abs(e - stop) / (abs(e - stop) + abs(tgt - e))
                    t = ts[touch]
                    band_lo, band_hi = sorted((lv(0.60), lv(0.67)))
                    # fair value gap of this leg inside the band
                    fv = 0
                    for i in range(sB + 1, eB + 1):
                        if i + 1 < n:
                            glo, ghi = (h[i - 1], l[i + 1]) if d == 1 else (h[i + 1], l[i - 1])
                            if ghi > glo and glo <= band_hi and ghi >= band_lo:
                                fv = 1
                                break
                    row["fvg_in_pocket"] = fv
                    for k, htf in enumerate(HTFS[tf], 1):
                        legs, piv, look = ctx[htf]
                        live = [x for x in legs if x[0] <= t < x[1]]
                        tag = f"htf{k}"
                        row[tag + "_dir"] = 0
                        row[tag + "_gp"] = 0
                        row[tag + "_zone"] = 0
                        if live:
                            _, _, hd, hs, he = live[-1]
                            hl = abs(he - hs)
                            row[tag + "_dir"] = 1 if hd == d else -1
                            if hd == d:
                                g1, g2 = sorted((he - hd * 0.618 * hl, he - hd * 0.65 * hl))
                                z1, z2 = sorted((he - hd * 0.5 * hl, he - hd * 0.786 * hl))
                                row[tag + "_gp"] = int(g1 <= band_hi and g2 >= band_lo)
                                row[tag + "_zone"] = int(z1 <= band_hi and z2 >= band_lo)
                        row[tag + "_pivot"] = int(any(band_lo <= p <= band_hi for (kt, p) in piv if t - look <= kt <= t))
                rows.append(row)
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows).to_csv("results/golden_pocket.csv", index=False)


if __name__ == "__main__":
    main()
