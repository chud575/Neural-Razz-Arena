"""Compare single-target exits with TP1/TP2 scale-outs for S/R flip and megaphone (daily, 34 symbols).

Usage: python run_tp_compare_other.py <cache_dir>   (expects <cache_dir>/data, filled by run_experiments.py)
"""
import sys
from dataclasses import replace
sys.path.insert(0, __import__('os').path.dirname(__file__))
from dtdb_backtest import fetch_yahoo, stats, max_dd_r
from run_experiments import UNIVERSE
import srflip_backtest as SR, megaphone_backtest as MP
data = {s: fetch_yahoo(s, '1d', 'max', sys.argv[1] + '/data') for s in UNIVERSE}
cases = [("S/R flip, monthly levels, rejection", SR, SR.SRParams(entry_mode="rejection", level_src="htf", htf="ME", htf_max_age=60, max_tries=3)),
         ("S/R flip, daily levels, touch (baseline)", SR, SR.SRParams(entry_mode="touch", max_tries=3)),
         ("Megaphone 5 swings, expand 0.5 ATR, BO close", MP, MP.MPParams(mode="breakout", min_pivots=5, min_expand_atr=0.5)),
         ("Megaphone 4 swings, BO close", MP, MP.MPParams(mode="breakout", min_pivots=4))]
exits = [("Single 2R", dict(rr=2.0, tp1_pct=0)), ("Single 3R", dict(rr=3.0, tp1_pct=0)),
         ("TP1 1R 50% / TP2 2R, BE", dict(rr=2.0, tp1_rr=1.0, tp1_pct=50, be_after_tp1=True)),
         ("TP1 1R 50% / TP2 2R, no BE", dict(rr=2.0, tp1_rr=1.0, tp1_pct=50, be_after_tp1=False)),
         ("TP1 1R 50% / TP2 3R, BE", dict(rr=3.0, tp1_rr=1.0, tp1_pct=50, be_after_tp1=True))]
print(f"{'strategy':46}{'exits':28}{'trades':>7}{'win%':>7}{'avgR':>8}{'netR':>8}{'maxDD':>7}")
for name, mod, base in cases:
    for en, kw in exits:
        p = replace(base, **kw); tr = []
        for sym, df in data.items():
            tr += mod.backtest(df, p, sym).trades
        s = stats(tr)
        print(f"{name:46}{en:28}{s['n']:>7}{s['win_rate']:>7.1f}{s['avg_r']:>+8.3f}{s['net_r']:>+8.1f}{max_dd_r(tr):>7.1f}")
