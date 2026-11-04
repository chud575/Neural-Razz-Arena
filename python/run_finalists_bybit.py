"""Typical-settings check for the BTC finalists with Bybit futures fees: IS/OOS net R, random benchmark,
stop-distance distribution and how many trades would be liquidated before the stop at a given leverage.

    python run_finalists_bybit.py <data_dir> [leverage] [mmr_pct]
"""
import math
import sys

import numpy as np

import run_btc_sweep as S

D = sys.argv[1]
LEV = float(sys.argv[2]) if len(sys.argv) > 2 else 25.0
MMR = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
LIQ = 100.0 / LEV - MMR
S.FEE_MODEL = "futures"
S.load(D, ["4h", "1d", "1h"], "btc")
CASES = [
    ("dtdb", "4h", "piv5 tol0.6 depth1.0 B+Retest 2R trend:off exit:single"),
    ("dtdb", "4h", "piv5 tol0.6 depth1.0 B 2R trend:off exit:single"),
    ("dtdb", "4h", "piv5 tol0.6 depth1.0 B+Mid 2R trend:off exit:single"),
    ("ttb", "4h", "piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single"),
    ("ttb", "4h", "piv5 tol2.0 depth1.0 B 2R trend:off exit:single"),
    ("megaphone", "4h", "piv5 swings4 expand0.0 BO-close 2R trend:off exit:single"),
    ("megaphone", "4h", "piv5 swings4 expand0.0 BO-close 3R trend:off exit:single"),
    ("megaphone", "1d", "piv3 swings4 expand0.0 BO-close 2R trend:off exit:single"),
    ("ttb", "1h", "piv5 tol2.0 depth0.5 B 1.5R trend:sma exit:TP1 1R 50% BE"),
]


def rr_of(t):
    risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
    tg = getattr(t, "target", math.nan)
    return 2.0 if math.isnan(tg) else abs(tg - (t.stop_px + t.direction * risk)) / risk


print(f"Bybit futures fees, liquidation distance at {LEV:g}x ≈ {LIQ:.2f}% (isolated, MMR {MMR}%)\n")
print(f"{'strategy':10}{'tf':4}{'settings':58}{'side':7}{'IS n':>5}{'IS R':>8}{'OOS n':>6}{'OOS R':>8}{'random':>8}"
      f"{'med stop%':>10}{'max stop%':>10}{'liq-first':>10}")
for strat, tf, name in CASES:
    mod, P, g = S.STRATS[strat]
    kw = next(k for n, k in g(tf) if n == name)
    df = S.DATA[tf]
    split = df.index[int(len(df) * S.SPLIT)]
    tr = mod.backtest(df, P(**kw), "BTC").trades
    for side, sel in (("both", lambda t: True), ("longs", lambda t: t.direction == 1), ("shorts", lambda t: t.direction == -1)):
        a = [t for t in tr if sel(t)]
        ins = [S.net_r(t) for t in a if t.signal_time < split]
        oo = [t for t in a if t.signal_time >= split]
        if len(oo) < 3:
            continue
        stop_pct = np.array([abs(t.entry_px - t.stop_px) / t.entry_px * 100 for t in a])
        ctrl = S.random_oos_control(tf, oo, rr_of, reps=40, seed=1)
        print(f"{strat:10}{tf:4}{name:58}{side:7}{len(ins):>5}{np.mean(ins):>+8.3f}{len(oo):>6}"
              f"{np.mean([S.net_r(t) for t in oo]):>+8.3f}{ctrl:>+8.3f}{np.median(stop_pct):>9.2f}%{stop_pct.max():>9.2f}%"
              f"{(stop_pct > LIQ).mean() * 100:>9.0f}%")
