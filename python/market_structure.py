"""Python twin of structure() in pine/trend_finder.pine (swings, trend, market-structure breaks)."""
from __future__ import annotations

import math

import numpy as np

from dtdb_backtest import pivots


def structure(h, l, c, L, break_on=True):
    """Per bar (values after that bar's close): dict of arrays
    trend (1/-1/0), ms (structure bias), ev (break on this bar: 1 BOS up, 2 CHoCH up, -1 BOS down, -2 CHoCH down),
    lastH, lastL (latest swing high / low), hBrk, lBrk (already closed through), lastHb, lastLb (their bars),
    hiUp, loUp (latest vs previous: 1 / -1 / 0), newH, newL (a new or updated swing high / low was confirmed this bar)."""
    n = len(c)
    ph, pl = pivots(h, l, L)
    out = {k: np.zeros(n, int) for k in ("trend", "ms", "ev", "lastHb", "lastLb", "hiUp", "loUp")}
    out.update({k: np.full(n, np.nan) for k in ("lastH", "lastL")})
    out.update({k: np.zeros(n, bool) for k in ("hBrk", "lBrk", "newH", "newL")})
    lastH = prevH = lastL = prevL = math.nan
    lastHb = lastLb = -1
    lastT = trend = ms = 0
    hBrk = lBrk = False
    for i in range(n):
        changed = False
        if not math.isnan(ph[i]):
            if lastT == 1:
                if ph[i] > lastH:
                    lastH, lastHb, hBrk, changed = ph[i], i - L, False, True
                    out["newH"][i] = True
            else:
                prevH, lastH, lastHb, hBrk, lastT, changed = lastH, ph[i], i - L, False, 1, True
                out["newH"][i] = True
        if not math.isnan(pl[i]):
            if lastT == -1:
                if pl[i] < lastL:
                    lastL, lastLb, lBrk, changed = pl[i], i - L, False, True
                    out["newL"][i] = True
            else:
                prevL, lastL, lastLb, lBrk, lastT, changed = lastL, pl[i], i - L, False, -1, True
                out["newL"][i] = True
        if changed and not math.isnan(prevH) and not math.isnan(prevL):
            if lastH > prevH and lastL > prevL and c[i] > lastL:
                trend = 1
            elif lastH < prevH and lastL < prevL and c[i] < lastH:
                trend = -1
        if break_on:
            if trend == 1 and c[i] < lastL:
                trend = 0
            elif trend == -1 and c[i] > lastH:
                trend = 0
        ev = 0
        if not math.isnan(lastH) and not hBrk and c[i] > lastH:
            ev = 2 if ms == -1 else 1
            ms, hBrk = 1, True
        elif not math.isnan(lastL) and not lBrk and c[i] < lastL:
            ev = -2 if ms == 1 else -1
            ms, lBrk = -1, True
        out["trend"][i], out["ms"][i], out["ev"][i] = trend, ms, ev
        out["lastH"][i], out["lastL"][i], out["hBrk"][i], out["lBrk"][i] = lastH, lastL, hBrk, lBrk
        out["lastHb"][i], out["lastLb"][i] = lastHb, lastLb
        out["hiUp"][i] = 0 if math.isnan(prevH) or math.isnan(lastH) else (1 if lastH > prevH else -1)
        out["loUp"][i] = 0 if math.isnan(prevL) or math.isnan(lastL) else (1 if lastL > prevL else -1)
    return out


def resample(df, rule):
    import pandas as pd
    if rule == "1W":
        key = (df.index - pd.to_timedelta(df.index.weekday, unit="D")).floor("1D")
    else:
        key = df.index.floor(rule)
    g = df.groupby(key).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"))
    pos = np.searchsorted(g.index.values, key.values)          # HTF candle of every chart bar
    return g, pos
