"""
What happens after an impulse leg — and do the fair value gaps inside it "work"?

Impulse leg = pine/impulse_legs.pine defaults: a move of ≥ 4 × ATR(50) within 12 bars with net move ≥ 70 % of the
distance travelled; it extends while it makes new extremes and ends on a close back of 38 % or 8 bars without a new
extreme. Leg = start price S → extreme E. Everything below is for a leg UP (legs down are mirrored).

Part 1 — retracements. After the extreme, when price first pulls back to 38 / 50 / 62 / 79 % of the leg: does it make
  a NEW extreme beyond E before it retraces the whole leg (back to S)?  "Expected" = what the two distances alone
  give if the leg meant nothing (at a 50 % pullback: 50 %).
Part 2 — fair value gaps (FVG): three candles inside the leg where candle 3's low is above candle 1's high.
  Zone = [candle 1 high, candle 3 low]. After the extreme, the first time price trades back into the zone:
    A  stop at the leg start S, target E         (the gap as an entry area for continuation)
    B  stop just beyond the far side of the gap, target E   (the gap itself must hold)
  "Expected" win rate again comes from the distances alone. R per trade is net of Bybit VIP 3 futures fees
  (maker entry and target, taker stop) and funding. Also: how many gaps are revisited at all.
Part 3 — the same trades at the 50 % level in legs with and without a gap, to see what the gap adds.

    python impulse_study.py <data_dir>   -> results/impulse_*.csv
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from srflip_backtest import atr

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h"]
SIZE, MAXN, EFF, RETR, STALL, ATRL, HOLD = 4.0, 12, 0.70, 0.38, 8, 50, 500


def find_legs(h, l, c):
    n = len(c)
    a = atr(h, l, c, ATRL)
    out = []
    st, last_end = 0, -1
    d = sB = eB = 0
    sP = eP = 0.0
    for i in range(n):
        if st == 1:
            if (h[i] > eP) if d == 1 else (l[i] < eP):
                eP, eB = (h[i] if d == 1 else l[i]), i
            sz = abs(eP - sP)
            if ((c[i] < eP - RETR * sz) if d == 1 else (c[i] > eP + RETR * sz)) or i - eB >= STALL:
                out.append((sB, eB, sP, eP, d, i))
                st, last_end = 0, eB
        if st == 0:
            best, bN, bD, path = 0.0, 0, 0, 0.0
            for k in range(1, MAXN + 1):
                if i - k < last_end or i - k < 0:
                    break
                path += abs(c[i - k + 1] - c[i - k])
                ar = a[i - k]
                if math.isnan(ar) or ar <= 0 or path <= 0:
                    continue
                net = c[i] - c[i - k]
                size = abs(net) / ar
                if size >= SIZE and abs(net) / path >= EFF and size > best:
                    best, bN, bD = size, k, (1 if net > 0 else -1)
            if bN > 0:
                w = slice(i - bN, i + 1)
                ks = (i - bN) + (int(np.argmin(l[w][::-1])) if False else 0)
                seg = l[w] if bD == 1 else h[w]
                # the LATEST bar holding the window's lowest low (highest high), as in the Pine script (k from 0 upward, <=)
                ext = seg.min() if bD == 1 else seg.max()
                idx = np.flatnonzero(seg == ext)
                s_bar = i - bN + int(idx[0])
                if s_bar < i:
                    seg2 = h[s_bar + 1:i + 1] if bD == 1 else l[s_bar + 1:i + 1]
                    e_val = seg2.max() if bD == 1 else seg2.min()
                    e_bar = s_bar + 1 + int(np.flatnonzero(seg2 == e_val)[-1])
                    if (e_val - ext) * bD > 0:
                        st, d, sP, sB, eP, eB = 1, bD, ext, s_bar, e_val, e_bar
    return out


def race(o, h, l, c, start, d, entry, stop, tgt, bar_h, same_bar_stop=True):
    """Limit entry at `entry` filled on bar `start`. Returns (win, gross R, net R)."""
    risk = abs(entry - stop)
    n = len(c)
    res, px, m = 0, None, start
    end = min(n, start + 1 + HOLD)
    while m < end:
        if (m > start or same_bar_stop) and ((l[m] <= stop) if d == 1 else (h[m] >= stop)):
            res, px = -1, stop if m == start else (min(o[m], stop) if d == 1 else max(o[m], stop))
            break
        if m > start and ((h[m] >= tgt) if d == 1 else (l[m] <= tgt)):
            res, px = 1, tgt
            break
        m += 1
    if px is None:
        m = end - 1
        px = c[m]
    gross = d * (px - entry) / risk
    cost = S.MAKER + (S.MAKER if res == 1 else S.TAKER) + d * S.FUNDING_8H * (m - start) * bar_h / 8
    return res, gross, gross - cost * entry / risk


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    legs_rows, lvl_rows, fvg_rows = [], [], []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(n * S.SPLIT)
            for sB, eB, sP, eP, d, fin in find_legs(h, l, c):
                if eB >= n - 3:
                    continue
                leg = abs(eP - sP)
                per = "IS" if eB < split else "OOS"
                # fair value gaps inside the leg (middle candle between the start and the extreme)
                gaps = []
                for i in range(sB + 1, eB + 1):
                    if i + 1 >= n:
                        break
                    lo, hi = (h[i - 1], l[i + 1]) if d == 1 else (h[i + 1], l[i - 1])
                    if hi > lo:
                        gaps.append((i, lo, hi))
                # max pullback before a new extreme / a full retrace
                dep, outcome = 0.0, "open"
                for m in range(eB + 1, min(n, eB + 1 + HOLD)):
                    pb = (eP - l[m]) / leg if d == 1 else (h[m] - eP) / leg
                    if pb >= 1:
                        outcome = "full retrace"
                        dep = 1.0
                        break
                    dep = max(dep, pb)
                    if (h[m] > eP) if d == 1 else (l[m] < eP):
                        outcome = "new extreme"
                        break
                legs_rows.append((coin, tf, per, d, leg / sP * 100, eB - sB, len(gaps), outcome, dep))
                # Part 1 / 3: pullback levels
                for f in (0.382, 0.5, 0.618, 0.786):
                    lvl = eP - d * f * leg
                    for m in range(eB + 1, min(n, eB + 1 + HOLD)):
                        if (h[m] > eP) if d == 1 else (l[m] < eP):
                            break                                    # ran away before reaching the level
                        if (l[m] <= lvl) if d == 1 else (h[m] >= lvl):
                            e = lvl if ((o[m] >= lvl) if d == 1 else (o[m] <= lvl)) else o[m]
                            res, g, r = race(o, h, l, c, m, d, e, sP, eP, bar_h)
                            lvl_rows.append((coin, tf, per, d, f, len(gaps) > 0, int(res == 1), int(res == -1), abs(e - sP) / leg, g, r))
                            break
                # Part 2: each gap
                for i, lo, hi in gaps:
                    near, far = (hi, lo) if d == 1 else (lo, hi)      # near = the side price reaches first on a pullback
                    f = abs(eP - near) / leg
                    touched, m_t = False, None
                    for m in range(max(eB + 1, i + 2), min(n, eB + 1 + HOLD)):
                        if (l[m] <= near) if d == 1 else (h[m] >= near):
                            touched, m_t = True, m
                            break
                        if (h[m] > eP) if d == 1 else (l[m] < eP):
                            break
                    if not touched:
                        fvg_rows.append((coin, tf, per, d, f, abs(hi - lo) / leg, 0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0))
                        continue
                    e = near if ((o[m_t] >= near) if d == 1 else (o[m_t] <= near)) else o[m_t]
                    if abs(eP - e) <= 0 or (eP - e) * d <= 0:
                        continue
                    rA, gA, nA = race(o, h, l, c, m_t, d, e, sP, eP, bar_h)
                    stopB = far - d * 0.0
                    if (e - stopB) * d <= 0:
                        continue
                    rB, gB, nB = race(o, h, l, c, m_t, d, e, stopB, eP, bar_h)
                    expA = abs(e - sP) / leg
                    expB = abs(e - stopB) / (abs(e - stopB) + abs(eP - e))
                    # filled completely (price traded through the whole gap) before the new extreme?
                    filled = 0
                    for m in range(m_t, min(n, m_t + 1 + HOLD)):
                        if (l[m] <= far) if d == 1 else (h[m] >= far):
                            filled = 1
                            break
                        if m > m_t and ((h[m] > eP) if d == 1 else (l[m] < eP)):
                            break
                    fvg_rows.append((coin, tf, per, d, f, abs(hi - lo) / leg, 1, int(rA == 1), expA, gA, nA, int(rB == 1), expB, gB, nB, filled))
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(legs_rows, columns=["coin", "tf", "period", "d", "leg_pct", "bars", "gaps", "outcome", "depth"]).to_csv("results/impulse_legs.csv", index=False)
    pd.DataFrame(lvl_rows, columns=["coin", "tf", "period", "d", "level", "has_gap", "win", "loss", "exp", "gross", "r"]).to_csv("results/impulse_levels.csv", index=False)
    pd.DataFrame(fvg_rows, columns=["coin", "tf", "period", "d", "pos", "size", "touched", "winA", "expA", "grossA", "rA", "winB", "expB", "grossB", "rB",
                                    "filled"]).to_csv("results/impulse_fvg.csv", index=False)


if __name__ == "__main__":
    main()
