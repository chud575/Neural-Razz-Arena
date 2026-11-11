"""2-2 / 2-2-2 continuation with FTFC, traded as ONE account (no overlapping trades): a new trade is only taken once
the previous one has closed. 2-candle stop, 1R / 2R / 3R targets, Bybit costs. Usage: python strat_cont_single.py <data_dir>"""
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from srflip_backtest import atr
from strat_cont import run_trade
from strat_study import HTFS, classify, htf_open

D = sys.argv[1]
S.FEE_MODEL = "futures"
print(f"{'coin':5}{'tf':4}{'setup':12}{'tgt':4}{'IS n':>6}{'IS R':>8}{'OOS n':>6}{'OOS R':>8}{'IS total':>10}{'OOS total':>10}{'trades/yr':>10}")
for coin in ("btc", "eth", "avax", "xrp"):
    S.DATA.clear()
    S.load(D, ["4h", "1d"], coin)
    for tf in ("4h", "1d"):
        df = S.DATA[tf]
        o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        n = len(c)
        bar_h = df.index.to_series().diff().median().total_seconds() / 3600
        years = (df.index[-1] - df.index[0]).days / 365.25
        t = classify(h, l)
        a = atr(h, l, c, 14)
        k_split = int(n * S.SPLIT)
        opens = np.vstack([htf_open(df, r) for r in HTFS[tf]])
        for setup in ("2-2 Cont", "2-2-2 Cont"):
            for k in (2, 3):
                busy_until = -1
                res = {"IS": [], "OOS": []}
                for i in range(2, n - 1):
                    if i + 1 <= busy_until:
                        continue
                    for d in (1, -1):
                        want = "2u" if d == 1 else "2d"
                        if t[i] != want or (setup == "2-2-2 Cont" and t[i - 1] != want):
                            continue
                        r = run_trade(o, h, l, c, i, d, "2candle", a, bar_h)
                        if r is None:
                            continue
                        gs = [(r["e"] > op) if d == 1 else (r["e"] < op) for op in opens[:, i + 1]]
                        if not all(gs):
                            continue
                        res["IS" if i + 1 < k_split else "OOS"].append(r[f"r{k}"])
                        busy_until = i + 1 + int(r[f"b{k}"])
                        break
                a_, b_ = np.array(res["IS"]), np.array(res["OOS"])
                print(f"{coin:5}{tf:4}{setup:12}{k}R  {len(a_):>6}{a_.mean() if len(a_) else np.nan:>+8.3f}{len(b_):>6}"
                      f"{b_.mean() if len(b_) else np.nan:>+8.3f}{a_.sum():>+10.1f}{b_.sum():>+10.1f}{(len(a_) + len(b_)) / years:>10.0f}")
