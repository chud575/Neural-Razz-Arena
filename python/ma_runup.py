"""How many ATR does price run in your favour before the stop (under the wick) is hit? Idea-1 longs vs baseline.

    python ma_runup.py <data_dir>
"""
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from ma_study import find_events

D = sys.argv[1]
rows = []
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(D, ["15m", "1h", "4h", "1d"], coin)
    for tf in ("15m", "1h", "4h", "1d"):
        df = S.DATA[tf]
        evs, (o, h, l, c, s200, a, run, up) = find_events(df, 50, 0, 1)
        n = len(c)
        rng = np.random.default_rng(3)
        stops = []
        for ev in evs:
            i0, e, A = ev["entry"], ev["e"], ev["A"]
            stop = ev["ext"] - 0.1 * A
            stops.append((e - stop) / A)
            best = e
            for j in range(i0 + 1, min(n, i0 + 500)):
                if l[j] <= stop:
                    break
                best = max(best, h[j])
            rows.append(dict(coin=coin, tf=tf, kind="event", runup=(best - e) / A))
        med_stop = float(np.median(stops)) if stops else 0.7
        cand = np.where((run >= 50) & (c > s200))[0]
        for i0 in rng.choice(cand, size=min(len(cand), 3000), replace=False) if len(cand) else []:
            e, A = c[i0], a[i0]
            if np.isnan(A):
                continue
            stop = e - med_stop * A
            best = e
            for j in range(i0 + 1, min(n, i0 + 500)):
                if l[j] <= stop:
                    break
                best = max(best, h[j])
            rows.append(dict(coin=coin, tf=tf, kind="baseline", runup=(best - e) / A))
r = pd.DataFrame(rows)
q = r.groupby(["tf", "kind"]).runup.describe(percentiles=[.25, .5, .75, .9])[["count", "25%", "50%", "75%", "90%"]]
print(q.round(2).to_string())
