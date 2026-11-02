"""Benchmark: compare pattern trades with random entries (same symbol, direction, stop % and R:R).

Usage: python random_control.py <cache_dir>   (expects <cache_dir>/data, filled by run_experiments.py)
Output columns: avgR = pattern trades, ctrlR = random entries, edge = difference; then a pre/post-2015 split.
"""
import sys, numpy as np, pandas as pd
from dataclasses import replace
sys.path.insert(0, __import__('os').path.dirname(__file__))
from dtdb_backtest import Params, backtest, fetch_yahoo, stats
from run_experiments import UNIVERSE
S = sys.argv[1]
data = {s: fetch_yahoo(s, '1d', 'max', S + '/data') for s in UNIVERSE}
rng = np.random.default_rng(0)

def random_control(df, trades, reps=20):
    """Same symbol, same direction, same stop distance (%), same RR, random entry bar; conservative same-bar rule."""
    o,h,l,c = (df[k].to_numpy(float) for k in ('open','high','low','close'))
    out=[]
    n=len(c)
    for t in trades:
        dist = abs(t.entry_px - t.stop_px)/t.entry_px
        rr = None
        for _ in range(reps):
            i = rng.integers(200, n-2)
            e = c[i]; d=t.direction
            stop = e*(1-d*dist); tgt = e + d*RR*abs(e-stop)
            r = None
            for j in range(i+1, n):
                sh = l[j] <= stop if d==1 else h[j] >= stop
                th = h[j] >= tgt if d==1 else l[j] <= tgt
                if sh: px = min(o[j],stop) if d==1 else max(o[j],stop); r = d*(px-e)/abs(e-stop); break
                if th: px = max(o[j],tgt) if d==1 else min(o[j],tgt); r = d*(px-e)/abs(e-stop); break
            if r is not None: out.append(r)
    return np.array(out)

configs = [
  ("Breakout only, longs", dict(use_entry1=True, entry2_mode='off', trade_shorts=False)),
  ("Breakout+Retest, longs", dict(use_entry1=True, entry2_mode='retest', trade_shorts=False)),
  ("Retest only, longs", dict(use_entry1=False, entry2_mode='retest', trade_shorts=False)),
  ("Breakout+Midpoint, longs", dict(use_entry1=True, entry2_mode='midpoint', trade_shorts=False)),
  ("Breakout only, shorts", dict(use_entry1=True, entry2_mode='off', trade_longs=False)),
]
print(f"{'config':28}{'RR':>4}{'trades':>8}{'avgR':>8}{'ctrlR':>8}{'edge':>8} | {'<2015 n':>8}{'avgR':>7} | {'>=2015 n':>8}{'avgR':>7}")
for name, kw in configs:
    for RR in (1.0, 2.0, 3.0):
        p = replace(Params(), rr=RR, **kw)
        allt=[]; ctrl=[]
        for s, df in data.items():
            tr = backtest(df, p, s).trades
            allt += tr
            ctrl.append(random_control(df, tr, reps=10))
        ctrl=np.concatenate(ctrl)
        r=np.array([t.r for t in allt])
        pre=np.array([t.r for t in allt if pd.Timestamp(t.signal_time).year<2015])
        post=np.array([t.r for t in allt if pd.Timestamp(t.signal_time).year>=2015])
        print(f"{name:28}{RR:>4g}{len(r):>8}{r.mean():>+8.3f}{ctrl.mean():>+8.3f}{r.mean()-ctrl.mean():>+8.3f} | {len(pre):>8}{pre.mean():>+7.3f} | {len(post):>8}{post.mean():>+7.3f}")
