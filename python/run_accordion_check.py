"""Accordion check: the plain 2:1 setup on every coin/timeframe (before and after fees, IS/OOS, random benchmark),
plus the strong-fan (≥5 ATR) family on BTC 1h. Usage: python run_accordion_check.py <data_dir>"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S

D = sys.argv[1]
S.FEE_MODEL = "futures"


def rr_of(t):
    risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
    return abs(t.target - (t.stop_px + t.direction * risk)) / risk


print("Plain setup: fan ≥3 ATR for 10 bars, fold ≤0.5, lookback 100, stop 1 ATR, 2:1 — both sides")
print(f"{'coin':5}{'tf':4}{'IS n':>6}{'IS gross':>9}{'IS net':>8}{'OOS n':>6}{'OOS gross':>10}{'OOS net':>8}{'random':>8}{'med stop':>9}")
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(D, ["15m", "1h", "4h", "1d"], coin)
    for tf in ("15m", "1h", "4h", "1d"):
        df = S.DATA[tf]
        split = df.index[int(len(df) * S.SPLIT)]
        tr = S.AC.backtest(df, S.AC.ACParams(), coin).trades
        ins = [t for t in tr if t.signal_time < split]
        oo = [t for t in tr if t.signal_time >= split]
        if len(ins) < 5 or len(oo) < 5:
            print(f"{coin:5}{tf:4} too few trades ({len(ins)}/{len(oo)})")
            continue
        c = S.random_oos_control(tf, oo, rr_of, reps=20, seed=4)
        sp = np.median([abs(t.entry_px - t.stop_px) / t.entry_px * 100 for t in tr])
        print(f"{coin:5}{tf:4}{len(ins):>6}{np.mean([t.r for t in ins]):>+9.3f}{np.mean([S.net_r(t) for t in ins]):>+8.3f}"
              f"{len(oo):>6}{np.mean([t.r for t in oo]):>+10.3f}{np.mean([S.net_r(t) for t in oo]):>+8.3f}{c:>+8.3f}{sp:>8.2f}%")

print("\nStrong fans on BTC 1h (fan ≥5 ATR), all variants: IS vs OOS net R")
d = pd.read_csv(f"{D}/ac_btc_all.csv")
s = d[(d.tf == "1h") & d.config.str.startswith("fan5ATR") & (d.direction == "both")]
print(f"variants {len(s)} | IS mean {s.is_avg.mean():+.3f} ({(s.is_avg > 0).mean() * 100:.0f}% > 0) | "
      f"OOS mean {s.oos_avg.mean():+.3f} ({(s.oos_avg > 0).mean() * 100:.0f}% > 0) | median trades IS {s.is_n.median():.0f} / OOS {s.oos_n.median():.0f}")
for coin in ("eth", "avax", "xrp"):
    d = pd.read_csv(f"{D}/ac_{coin}_all.csv")
    s = d[(d.tf == "1h") & d.config.str.startswith("fan5ATR") & (d.direction == "both")]
    if len(s):
        print(f"  {coin}: IS {s.is_avg.mean():+.3f}  OOS {s.oos_avg.mean():+.3f}  median trades {s.is_n.median():.0f}/{s.oos_n.median():.0f}")
