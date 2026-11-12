"""Typical head & shoulders settings on several coins: IS/OOS net R (futures fees), random benchmark, 25x liquidation share.

    python run_hs_finalists.py <data_dir>
"""
import math
import sys

import numpy as np

import run_btc_sweep as S

D = sys.argv[1]
S.FEE_MODEL = "futures"
LIQ = 100 / 25 - 0.5
SETS = ["piv3 tol0.5 breakout neck:sloped stop:shoulder target:2R prior:0.5 exit:single",
        "piv3 tol0.5 breakout neck:sloped stop:shoulder target:measured prior:0.5 exit:single",
        "piv3 tol0.5 retest neck:sloped stop:shoulder target:3R prior:0.5 exit:single",
        "piv5 tol0.5 breakout neck:sloped stop:shoulder target:2R prior:0.5 exit:single",
        "piv3 tol0.5 early neck:sloped stop:shoulder target:2R prior:0.5 exit:single"]
TFS = ["15m", "1h", "4h", "1d"]


def rr_of(t):
    risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
    tg = getattr(t, "target", math.nan)
    return 2.0 if math.isnan(tg) else abs(tg - (t.stop_px + t.direction * risk)) / risk


print(f"{'coin':5}{'tf':4}{'settings':86}{'side':7}{'IS n':>5}{'IS R':>8}{'OOS n':>6}{'OOS R':>8}{'random':>8}{'med stop':>9}{'liq@25x':>8}")
pool = {}
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(D, TFS, coin)
    for tf in TFS:
        for name in SETS:
            kw = next(k for n, k in S.grid_hs(tf) if n == name)
            df = S.DATA[tf]
            split = df.index[int(len(df) * S.SPLIT)]
            tr = S.HS.backtest(df, S.HS.HSParams(**kw), coin).trades
            for side, sel in (("both", lambda t: True), ("longs", lambda t: t.direction == 1), ("shorts", lambda t: t.direction == -1)):
                a = [t for t in tr if sel(t)]
                ins = [S.net_r(t) for t in a if t.signal_time < split]
                oo = [t for t in a if t.signal_time >= split]
                oos = [S.net_r(t) for t in oo]
                p = pool.setdefault((tf, name, side), dict(i=[], o=[], c=[], sp=[]))
                p["i"] += ins
                p["o"] += oos
                sp = [abs(t.entry_px - t.stop_px) / t.entry_px * 100 for t in a]
                p["sp"] += sp
                c = S.random_oos_control(tf, oo, rr_of, reps=20, seed=2) if oo else math.nan
                if oo:
                    p["c"] += [c] * len(oo)
                if side != "both" or not a:
                    continue
                print(f"{coin:5}{tf:4}{name:86}{side:7}{len(ins):>5}{(np.mean(ins) if ins else math.nan):>+8.3f}{len(oo):>6}"
                      f"{(np.mean(oos) if oos else math.nan):>+8.3f}{c:>+8.3f}{np.median(sp):>8.2f}%{(np.array(sp) > LIQ).mean() * 100:>7.0f}%")
print("\nPOOLED (all four coins)")
for (tf, name, side), p in pool.items():
    if not p["i"] and not p["o"]:
        continue
    m = lambda x: np.mean(x) if x else math.nan
    print(f"{'all':5}{tf:4}{name:86}{side:7}{len(p['i']):>5}{m(p['i']):>+8.3f}{len(p['o']):>6}{m(p['o']):>+8.3f}{m(p['c']):>+8.3f}"
          f"{np.median(p['sp']):>8.2f}%{(np.array(p['sp']) > LIQ).mean() * 100:>7.0f}%")
