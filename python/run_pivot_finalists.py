"""Typical pivot settings on several coins: IS/OOS net R (futures fees), random benchmark, 25x liquidation share.

    python run_pivot_finalists.py <data_dir>
"""
import math
import sys

import numpy as np

import run_btc_sweep as S

D = sys.argv[1]
S.FEE_MODEL = "futures"
LIQ = 100 / 25 - 0.5
CASES = [("1h", "traditional pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no"),
         ("4h", "traditional pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no"),
         ("4h", "traditional pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no"),
         ("4h", "traditional pivots:M breakout level1 stop1ATR target:2R exitAtPeriodEnd:no"),
         ("1h", "traditional pivots:D bounce-rejection level1 stop1ATR target:next exitAtPeriodEnd:no")]


def rr_of(t):
    risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
    tg = getattr(t, "target", math.nan)
    return 2.0 if math.isnan(tg) else abs(tg - (t.stop_px + t.direction * risk)) / risk


print(f"{'coin':5}{'tf':4}{'settings':80}{'side':7}{'IS n':>5}{'IS R':>8}{'OOS n':>6}{'OOS R':>8}{'random':>8}{'med stop':>9}{'liq@25x':>8}")
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(D, ["1h", "4h"], coin)
    for tf, name in CASES:
        kw = next(k for n, k in S.grid_pivots(tf) if n == name)
        df = S.DATA[tf]
        split = df.index[int(len(df) * S.SPLIT)]
        tr = S.PV.backtest(df, S.PV.PVParams(**kw), coin).trades
        for side, sel in (("both", lambda t: True), ("longs", lambda t: t.direction == 1), ("shorts", lambda t: t.direction == -1)):
            a = [t for t in tr if sel(t)]
            ins = [S.net_r(t) for t in a if t.signal_time < split]
            oo = [t for t in a if t.signal_time >= split]
            if len(oo) < 5 or not ins:
                continue
            sp = np.array([abs(t.entry_px - t.stop_px) / t.entry_px * 100 for t in a])
            c = S.random_oos_control(tf, oo, rr_of, reps=20, seed=2)
            print(f"{coin:5}{tf:4}{name:80}{side:7}{len(ins):>5}{np.mean(ins):>+8.3f}{len(oo):>6}"
                  f"{np.mean([S.net_r(t) for t in oo]):>+8.3f}{c:>+8.3f}{np.median(sp):>8.2f}%{(sp > LIQ).mean() * 100:>7.0f}%")
