"""
Cup & handle (and inverted cup & handle) backtester. Mirrors pine/cup_handle.pine.

Pattern (bullish; the inverted pattern is the mirror image and is traded short)
  The last four alternating swings (swing length L) are  A high (left rim) – B low (cup bottom) – C high (right rim)
  – D low (handle), with depth = C − B:
    * depth ≥ `min_depth_atr` × ATR(14)
    * the rims are level:            |A − C| ≤ `rim_tol` × depth
    * the handle is shallow:         `handle_min` ≤ (C − D) / depth ≤ `handle_max`
    * the cup is not lopsided:       bars A→B vs B→C within a factor `sym`
    * the handle is short:           bars C→D ≤ `handle_len` × bars A→C
    * prior advance (optional):      the lowest low in the bars before A (as many as the cup is wide) is at least
                                     `prior_min` × depth below the rim
  The pattern is known when D is confirmed (L bars after it). If price already closed above the rim, it is skipped.
Entry    first close above the rim C, within `wait_mult` × cup width bars. Dead on a close below the handle low D.
Stop     "handle" = the handle low D   |   "half" = half-way down the cup
Target   "measured" = rim + depth      |   "rr" = rr × risk
Same conservative simulation as the other testers (stop first, gaps at the open, one trade at a time, max 300 bars).

    python cup_handle_backtest.py <data_dir>     -> results/cup_handle.md
"""
from __future__ import annotations

import itertools
import math
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

import run_btc_sweep as S
from dtdb_backtest import pivots
from srflip_backtest import atr

__version__ = "1.0"


@dataclass
class CHParams:
    piv_len: int = 5
    min_depth_atr: float = 3.0
    rim_tol: float = 0.25
    handle_min: float = 0.1
    handle_max: float = 0.5
    sym: float = 3.0
    handle_len: float = 0.5
    prior_min: float = 0.0
    wait_mult: float = 0.5
    stop: str = "handle"         # handle | half
    target: str = "measured"     # measured | rr
    rr: float = 2.0
    max_bars: int = 300


def backtest(df, p: CHParams):
    """Returns (trades, patterns). trade = dict(bar, exit_bar, d, e, stop, tp, px, at_target)."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    L = p.piv_len
    ph, pl = pivots(h, l, L)
    a = atr(h, l, c, 14)
    seq, trades = [], []
    pat, tr, n_pat, last_c = None, None, 0, -1
    for i in range(n):
        if tr is not None and i > tr["bar"]:
            d = tr["d"]
            px, at_t = None, False
            if (l[i] <= tr["stop"]) if d == 1 else (h[i] >= tr["stop"]):
                px = min(o[i], tr["stop"]) if d == 1 else max(o[i], tr["stop"])
            elif (h[i] >= tr["tp"]) if d == 1 else (l[i] <= tr["tp"]):
                px, at_t = (max(o[i], tr["tp"]) if d == 1 else min(o[i], tr["tp"])), True
            elif i - tr["bar"] >= p.max_bars:
                px = c[i]
            if px is not None:
                tr.update(exit_bar=i, px=px, at_target=at_t)
                trades.append(tr)
                tr = None
        changed = False
        for tp_, arr in ((1, ph), (-1, pl)):
            if not math.isnan(arr[i]):
                if seq and seq[-1][0] == tp_:
                    if (tp_ == 1 and arr[i] > seq[-1][1]) or (tp_ == -1 and arr[i] < seq[-1][1]):
                        seq[-1] = (tp_, arr[i], i - L)
                        changed = True
                else:
                    seq.append((tp_, arr[i], i - L))
                    del seq[:-8]
                    changed = True
        if changed and len(seq) >= 4 and not math.isnan(a[i]):
            (tA, A, Ab), (_, B, Bb), (_, C, Cb), (tD, Dp, Db) = seq[-4:]
            s = tA                                           # +1: A is a high -> bullish cup; -1: inverted
            if tD == -s and Cb != last_c:
                depth = s * (C - B)
                ok = depth > 0 and depth >= p.min_depth_atr * a[i]
                ok = ok and abs(A - C) <= p.rim_tol * depth
                hd = s * (C - Dp) / depth if depth > 0 else 9
                ok = ok and p.handle_min <= hd <= p.handle_max
                w1, w2, W = Bb - Ab, Cb - Bb, Cb - Ab
                ok = ok and w1 <= p.sym * w2 and w2 <= p.sym * w1 and (Db - Cb) <= p.handle_len * W
                if ok and p.prior_min > 0:
                    lo = max(0, Ab - W)
                    ext = (l[lo:Ab].min() if s == 1 else h[lo:Ab].max()) if lo < Ab else (A)
                    ok = s * (C - ext) >= p.prior_min * depth
                if ok:
                    seg = c[Cb + 1:i + 1]
                    if len(seg) and ((seg.max() > C) if s == 1 else (seg.min() < C)):
                        ok = False                            # already closed through the rim
                if ok:
                    n_pat += 1
                    last_c = Cb
                    pat = dict(d=s, rim=C, depth=depth, hl=Dp, bot=B, expiry=i + max(5, int(round(p.wait_mult * W))), pts=(Ab, A, Bb, B, Cb, C, Db, Dp))
        if pat is not None:
            d = pat["d"]
            if (c[i] - pat["hl"]) * d < 0 or i > pat["expiry"]:
                pat = None
            elif (c[i] - pat["rim"]) * d > 0:
                if tr is None and i < n - 1:
                    e = c[i]
                    stop = pat["hl"] if p.stop == "handle" else pat["rim"] - d * 0.5 * pat["depth"]
                    risk = abs(e - stop)
                    tp = pat["rim"] + d * pat["depth"] if p.target == "measured" else e + d * p.rr * risk
                    if risk > 0 and (e - stop) * d > 0 and (tp - e) * d > 0:
                        tr = dict(bar=i, d=d, e=e, stop=stop, tp=tp, pts=pat["pts"])
                pat = None
    return trades, n_pat


def net_r(t, bar_h):
    risk = abs(t["e"] - t["stop"])
    d = t["d"]
    return d * (t["px"] - t["e"]) / risk - S.cost_fraction(d, t["at_target"], (t["exit_bar"] - t["bar"]) * bar_h) * t["e"] / risk


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    TFS = ["15m", "1h", "4h", "1d"]
    grid = list(itertools.product((5, 10, 20), (0.15, 0.3), (0.38, 0.5), ("handle", "half"), ("measured", "2R", "3R"), (0.0, 0.5)))
    rows = []
    for coin in ("btc", "eth", "avax", "xrp"):
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(len(df) * S.SPLIT)
            for L, rt, hm, stp, tg, pr in grid:
                p = CHParams(piv_len=L, rim_tol=rt, handle_max=hm, stop=stp, prior_min=pr,
                             target="measured" if tg == "measured" else "rr", rr=2.0 if tg != "3R" else 3.0)
                trades, npat = backtest(df, p)
                for t in trades:
                    rows.append((coin, tf, L, rt, hm, stp, tg, pr, "IS" if t["bar"] < split else "OOS", t["d"], net_r(t, bar_h),
                                 t["d"] * (t["px"] - t["e"]) / abs(t["e"] - t["stop"]), int(t["at_target"]), abs(t["e"] - t["stop"]) / t["e"] * 100,
                                 abs(t["tp"] - t["e"]) / abs(t["e"] - t["stop"])))
        print("done", coin, file=sys.stderr, flush=True)
    t = pd.DataFrame(rows, columns=["coin", "tf", "L", "rim", "hmax", "stop", "target", "prior", "period", "d", "r", "gross", "win", "risk_pct", "rr"])
    t.to_csv("results/cup_handle_trades.csv", index=False)


if __name__ == "__main__":
    main()
