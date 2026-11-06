"""
"Reverse the worst strategy" test.

For every trade a strategy takes, simulate the OPPOSITE trade from the same entry bar and price:
  mirror  direction flipped, stop and target swapped (the old target becomes the stop and vice versa).
          Before costs this is close to the exact negative of the original trade, but a 2:1 trade becomes 1:2.
  flip    direction flipped, same stop distance and same reward:risk as the original (a 2:1 trade stays 2:1).
Conservative fills (stop first when stop and target share a bar, gaps fill at the open) and the futures cost
model from run_btc_sweep.py (Bybit VIP 3 by default). Uses trades whose entry bar is the signal bar (closes and
same-bar limit fills; Double/Triple Top second entries are skipped). The reversed trade is simulated from the bar
after entry. "random" = random entry bars in the same period with the reversed trade's direction, stop and target
distances (20 per trade), so drift alone is accounted for.

    python reverse_test.py <data_dir>
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S

CASES = [  # (strategy, coin, tf, settings name in the sweep grid, note)
    ("megaphone", "btc", "4h", "piv3 swings4 expand0.0 fade-touch midline trend:off exit:single", "bad in both periods"),
    ("pivots", "btc", "1d", "woodie pivots:chart bounce-touch level2 stop1ATR target:2R exitAtPeriodEnd:no", "bad in both periods"),
    ("ttb", "btc", "1h", "piv8 tol1.0 depth2.0 B+Retest 3R trend:off exit:single", "bad in both periods"),
    ("pivots", "btc", "1h", "traditional pivots:W bounce-rejection level1 stop0.5ATR target:next exitAtPeriodEnd:no", "bad in-sample, good OOS"),
    ("megaphone", "btc", "4h", "piv3 swings4 expand0.0 fade-rejection midline trend:off exit:single", "bad in both periods"),
    ("pivots", "btc", "1h", "traditional pivots:D bounce-rejection level1 stop1ATR target:next exitAtPeriodEnd:no", "typical losing family"),
    ("rangesweep", "eth", "1h", "range48 max10ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:single", "typical losing family"),
]


def simulate(df, i0, d, e, stop, tgt, bar_h):
    """Walk forward from the bar after i0. Returns net R (futures costs) or None if never resolved."""
    o, h, l = df["open"].to_numpy(float), df["high"].to_numpy(float), df["low"].to_numpy(float)
    risk = abs(e - stop)
    if risk <= 0:
        return None
    for j in range(i0 + 1, len(df)):
        if (l[j] <= stop) if d == 1 else (h[j] >= stop):
            px, at_tgt = (min(o[j], stop) if d == 1 else max(o[j], stop)), False
        elif (h[j] >= tgt) if d == 1 else (l[j] <= tgt):
            px, at_tgt = (max(o[j], tgt) if d == 1 else min(o[j], tgt)), True
        else:
            continue
        gross = d * (px - e) / risk
        return gross, gross - S.cost_fraction(d, at_tgt, (j - i0) * bar_h) * e / risk
    return None


def main():
    data_dir = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows = []
    for strat, coin, tf, name, note in CASES:
        S.DATA.clear()
        S.load(data_dir, [tf], coin)
        df = S.DATA[tf]
        split = df.index[int(len(df) * S.SPLIT)]
        bar_h = df.index.to_series().diff().median().total_seconds() / 3600
        mod, P, grid = S.STRATS[strat]
        kw = next(k for n, k in grid(tf) if n == name)
        trades = mod.backtest(df, P(**kw), coin).trades
        pos = df.index.get_indexer(pd.DatetimeIndex([t.signal_time for t in trades]))
        close = df["close"].to_numpy(float)
        out = {"IS": [], "OOS": []}
        rng = np.random.default_rng(7)
        n = len(df)
        k_split = int(n * S.SPLIT)
        for t, i0 in zip(trades, pos):
            if i0 < 0 or math.isnan(t.target) or (strat in ("dtdb", "ttb") and t.entry != 0):
                continue                                           # entry bar must be the signal bar
            d, e, st, tg = t.direction, t.entry_px, t.stop_px, t.target
            risk = abs(e - st)
            rr = abs(tg - e) / risk if risk > 0 else 0
            mir = simulate(df, i0, -d, e, tg, st, bar_h)                        # stop <-> target swapped
            flp = simulate(df, i0, -d, e, e + d * risk, e - d * rr * risk, bar_h)  # same distances, other way
            if mir is None or flp is None:
                continue
            per = "IS" if t.signal_time < split else "OOS"
            lo, hi = (200, k_split) if per == "IS" else (k_split, n - 2)
            rm, rf = [], []
            for _ in range(20):                                    # random entries with the reversed geometry
                j = int(rng.integers(lo, hi))
                ej = close[j]
                m = simulate(df, j, -d, ej, ej * tg / e, ej * st / e, bar_h)
                f = simulate(df, j, -d, ej, ej * (e + d * risk) / e, ej * (e - d * rr * risk) / e, bar_h)
                if m:
                    rm.append(m[1])
                if f:
                    rf.append(f[1])
            out[per].append((t.r, S.net_r(t), mir[0], mir[1], flp[0], flp[1],
                             np.mean(rm) if rm else np.nan, np.mean(rf) if rf else np.nan))
        for per in ("IS", "OOS"):
            a = np.array(out[per])
            if not len(a):
                continue
            rows.append(dict(strategy=strat, coin=coin, tf=tf, settings=name, note=note, period=per, n=len(a),
                             orig_gross=a[:, 0].mean(), orig_net=a[:, 1].mean(), mirror_gross=a[:, 2].mean(),
                             mirror_net=a[:, 3].mean(), mirror_random=np.nanmean(a[:, 6]),
                             flip_gross=a[:, 4].mean(), flip_net=a[:, 5].mean(), flip_random=np.nanmean(a[:, 7])))
    res = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 60)
    print(res.round(3).to_string(index=False))
    return res


if __name__ == "__main__":
    main()
