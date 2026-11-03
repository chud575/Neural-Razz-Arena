"""Compare single-target exits with TP1/TP2 scale-outs for the DT/DB strategy (daily, 34 symbols).

Usage: python run_tp_compare.py <cache_dir>   (expects <cache_dir>/data, filled by run_experiments.py)
"""
import sys
from dataclasses import replace
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from dtdb_backtest import Params, backtest, fetch_yahoo, stats, max_dd_r
from run_experiments import UNIVERSE
data = {s: fetch_yahoo(s, '1d', 'max', sys.argv[1] + '/data') for s in UNIVERSE}
setups = [("Breakout + Midpoint", dict(use_entry1=True, entry2_mode="midpoint")),
          ("Breakout only", dict(use_entry1=True, entry2_mode="off"))]
exits = [("Single target 2R", dict(rr=2.0, tp1_pct=0)),
         ("Single target 3R", dict(rr=3.0, tp1_pct=0)),
         ("TP1 1R 50% / TP2 2R, BE", dict(rr=2.0, tp1_rr=1.0, tp1_pct=50, be_after_tp1=True)),
         ("TP1 1R 50% / TP2 2R, no BE", dict(rr=2.0, tp1_rr=1.0, tp1_pct=50, be_after_tp1=False)),
         ("TP1 1R 50% / TP2 3R, BE", dict(rr=3.0, tp1_rr=1.0, tp1_pct=50, be_after_tp1=True)),
         ("TP1 1.5R 50% / TP2 3R, BE", dict(rr=3.0, tp1_rr=1.5, tp1_pct=50, be_after_tp1=True))]
print(f"{'setup':22}{'exits':30}{'trades':>7}{'win%':>7}{'avgR':>8}{'netR':>8}{'maxDD':>7}{'longR':>8}{'shortR':>8}")
for sn, skw in setups:
    for en, ekw in exits:
        p = replace(Params(), **skw, **ekw)
        tr = []
        for sym, df in data.items():
            tr += backtest(df, p, sym).trades
        s = stats(tr)
        lr = np.mean([t.r for t in tr if t.direction == 1]); sr = np.mean([t.r for t in tr if t.direction == -1])
        print(f"{sn:22}{en:30}{s['n']:>7}{s['win_rate']:>7.1f}{s['avg_r']:>+8.3f}{s['net_r']:>+8.1f}{max_dd_r(tr):>7.1f}{lr:>+8.3f}{sr:>+8.3f}")
