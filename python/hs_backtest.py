"""
Head & Shoulders / Inverse Head & Shoulders backtester. Mirrors pine/head_shoulders.pine.

Pattern (top; the inverse is the mirror image)
  Swing points (pivots, `piv_len` bars each side) are kept as an alternating high/low sequence. The last five swings
  LS (high) – T1 (low) – H (high) – T2 (low) – RS (high) form a head & shoulders top when, with
  base = (T1 + T2) / 2 and height = H − base:
    * height ≥ `min_height_atr` × ATR
    * both shoulders stand at least `sh_min` × height above the base
    * the head is above the higher shoulder by at least `head_min` × height
    * the shoulders are level:   |LS − RS| ≤ `sh_tol` × height
    * the neckline is not steep: |T1 − T2| ≤ `neck_tol` × height
    * time symmetry: bars LS→H vs H→RS within a factor `sym`; LS→RS at most `max_width` bars
    * prior trend (`prior_min` > 0): in the bars before LS (as many as the pattern is wide) price was at least
      `prior_min` × height below the base — there is something to reverse.
  The pattern is known when RS is confirmed (piv_len bars after it). If price already closed through the neckline
  before that, the pattern is skipped (the breakout was missed).
Neckline   "sloped" = the line through T1 and T2, extended;  "flat" = the lower trough (higher peak for the inverse).
Entry      "breakout" = first close through the neckline (within `wait_mult` × pattern width bars)
           "retest"   = after that close, a limit order at the neckline for `retest_bars` bars (cancelled if the
                        target is reached first)
           "early"    = at the close of the bar that confirms the right shoulder (before any breakout)
Stop       beyond the right "shoulder" or the "head", plus `stop_atr` × ATR.
Target     "measured" = neckline ∓ `meas_mult` × (head − neckline at the head)  |  "rr" = rr × risk.
           TP1 / % at TP1 / breakeven as in the other scripts (exits.py).
The pattern dies on a close beyond the right shoulder, or when the wait runs out. One trade at a time.
Same conservative simulation rules as the other testers.

    python hs_backtest.py BTC-USD --interval 1h --range 730d
"""
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from dtdb_backtest import Result, Trade, _f, fetch_yahoo, max_dd_r, pivots, stats
from exits import make_entry, scale_step
from srflip_backtest import atr

__version__ = "1.0"  # same version as pine/head_shoulders.pine (costs: run_btc_sweep.py --fees)


@dataclass
class HSParams:
    piv_len: int = 5
    atr_len: int = 14
    sh_tol: float = 0.5
    sh_min: float = 0.3
    head_min: float = 0.15
    neck_tol: float = 0.5
    sym: float = 3.0
    max_width: int = 150
    min_height_atr: float = 2.0
    prior_min: float = 0.5          # 0 = no prior-trend requirement
    neck: str = "sloped"            # sloped | flat
    entry: str = "breakout"         # breakout | retest | early
    retest_bars: int = 10
    wait_mult: float = 1.0
    stop: str = "shoulder"          # shoulder | head
    stop_atr: float = 0.25
    target: str = "measured"        # measured | rr
    meas_mult: float = 1.0
    rr: float = 2.0
    tp1_rr: float = 1.0
    tp1_pct: float = 0.0            # 0 = single target (Pine defaults to 50)
    be_after_tp1: bool = True
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        s = (f"piv {self.piv_len} | shoulders ±{self.sh_tol:g} | {self.entry} | neck {self.neck} | stop {self.stop} | "
             f"target {self.target}" + (f" {self.rr:g}R" if self.target == "rr" else f" ×{self.meas_mult:g}"))
        if self.tp1_pct > 0:
            s += f" | TP1 {self.tp1_rr:g}R ({self.tp1_pct:g}%)" + (" BE" if self.be_after_tp1 else "")
        return s


def backtest(df: pd.DataFrame, p: HSParams, symbol: str = "") -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    L = p.piv_len
    ph, pl = pivots(h, l, L)
    a = atr(h, l, c, p.atr_len)
    p1 = p.tp1_pct / 100.0
    res = Result()
    res.patterns = 0

    seq: list[tuple[int, float, int]] = []     # (type 1 high / -1 low, price, bar)
    pat = None
    last_head = -1
    in_tr = False
    tr: dict = {}

    def push(tp, price, bar):
        if seq and seq[-1][0] == tp:
            if (tp == 1 and price > seq[-1][1]) or (tp == -1 and price < seq[-1][1]):
                seq[-1] = (tp, price, bar)
                return True
            return False
        seq.append((tp, price, bar))
        if len(seq) > 8:
            del seq[0]
        return True

    def detect(i):
        """Pattern from the last five swings (the last one = right shoulder, just confirmed on bar i)."""
        (_, ls, lsb), (_, t1, t1b), (_, hd, hb), (_, t2, t2b), (tp, rs, rsb) = seq[-5:]
        s = tp                                   # 1 = top (short), -1 = inverse (long)
        A = a[i]
        if math.isnan(A) or A <= 0:
            return None
        base = (t1 + t2) / 2
        ht = s * (hd - base)
        if ht <= 0 or ht < p.min_height_atr * A:
            return None
        if s * (ls - base) < p.sh_min * ht or s * (rs - base) < p.sh_min * ht:
            return None
        if s * (hd - (max(ls, rs) if s == 1 else min(ls, rs))) < p.head_min * ht:
            return None
        if abs(ls - rs) > p.sh_tol * ht or abs(t1 - t2) > p.neck_tol * ht:
            return None
        w1, w2, W = hb - lsb, rsb - hb, rsb - lsb
        if W > p.max_width or w1 > p.sym * w2 or w2 > p.sym * w1:
            return None
        if p.prior_min > 0:
            lo_i = max(0, lsb - W)
            if lo_i >= lsb:
                return None
            ext = l[lo_i:lsb].min() if s == 1 else h[lo_i:lsb].max()
            if s * (base - ext) < p.prior_min * ht:
                return None
        if p.neck == "sloped":
            slope = (t2 - t1) / (t2b - t1b)
            n0, nb = t1, t1b
        else:
            slope = 0.0
            n0, nb = (min(t1, t2) if s == 1 else max(t1, t2)), t1b
        hgt = s * (hd - (n0 + slope * (hb - nb)))          # head to neckline, used for the measured move
        if hgt <= 0:
            return None
        for k in range(rsb + 1, i):                         # closed through the neckline before confirmation = missed
            if s * (c[k] - (n0 + slope * (k - nb))) < 0:
                return None
        return dict(d=-s, n0=n0, nb=nb, slope=slope, hgt=hgt, rs=rs, hd=hd, hb=hb, A=A, conf=i,
                    expiry=i + max(5, int(round(p.wait_mult * W))), brk=None, tgt=None,
                    stop=(rs if p.stop == "shoulder" else hd) + s * p.stop_atr * A)

    def open_trade(i, d, e, ref, stop, tgt, limit_fill=False):
        """ref = planned entry (the limit price for limit fills, else e)."""
        nonlocal in_tr, tr
        risk = abs(ref - stop)
        if risk <= 0 or (ref - stop) * d <= 0 or (tgt - e) * d <= 0 or (e - stop) * d <= 0:
            return False
        if not (p.trade_longs if d == 1 else p.trade_shorts):
            return False
        tr = dict(d=d, e=e, s=stop, t=tgt, risk=risk, bar=i,
                  en=make_entry(e, risk, stop, ref + d * p.tp1_rr * risk, tgt, d, p1))
        in_tr = True
        if d == 1:
            res.signals_long += 1
        else:
            res.signals_short += 1
        if limit_fill and (l[i] <= stop if d == 1 else h[i] >= stop):
            res.trades.append(Trade(symbol, d, 0, t[i], t[i], e, stop, stop, d * (stop - e) / risk,
                                    d * (stop - e) / e * 100, "SL", risk, tgt))
            in_tr = False
        return True

    for i in range(n):
        # 1) manage the open trade
        if in_tr and i > tr["bar"]:
            closed, x_px, reason, _ = scale_step(o, h, l, i, tr["d"], tr["en"], p1, p.be_after_tp1)
            if closed:
                en = tr["en"]
                res.trades.append(Trade(symbol, tr["d"], 0, t[tr["bar"]], t[i], tr["e"], x_px, tr["s"],
                                        en["r"], en["pct"], reason, tr["risk"], tr["t"]))
                in_tr = False

        # 2) swings -> pattern
        changed = False
        if not math.isnan(ph[i]):
            changed |= push(1, ph[i], i - L)
        if not math.isnan(pl[i]):
            changed |= push(-1, pl[i], i - L)
        if changed and len(seq) >= 5:
            cand = detect(i)
            if cand is not None:
                pat = cand
                if cand["hb"] != last_head:
                    res.patterns += 1
                    last_head = cand["hb"]

        # 3) act on the pattern
        if pat is None:
            continue
        d = pat["d"]
        nk = pat["n0"] + pat["slope"] * (i - pat["nb"])
        if (c[i] - pat["rs"]) * d < 0:                       # close beyond the right shoulder: pattern failed
            pat = None
            continue
        if in_tr:                                            # busy: a breakout now is simply missed
            if pat["brk"] is not None or (c[i] - nk) * d > 0 or i > pat["expiry"]:
                pat = None
            continue
        if pat["brk"] is None:
            if p.entry == "early":
                if i == pat["conf"]:
                    tgt = nk + d * p.meas_mult * pat["hgt"] if p.target == "measured" else \
                        c[i] + d * p.rr * abs(c[i] - pat["stop"])
                    open_trade(i, d, c[i], c[i], pat["stop"], tgt)
                pat = None
                continue
            if (c[i] - nk) * d > 0:                          # close through the neckline
                if p.entry == "breakout":
                    tgt = nk + d * p.meas_mult * pat["hgt"] if p.target == "measured" else \
                        c[i] + d * p.rr * abs(c[i] - pat["stop"])
                    open_trade(i, d, c[i], c[i], pat["stop"], tgt)
                    pat = None
                else:
                    pat["brk"] = i
                    pat["tgt"] = nk + d * p.meas_mult * pat["hgt"]   # run-away check (and target when measured)
            elif i > pat["expiry"]:
                pat = None
        else:                                                # waiting for the retest of the neckline
            if i - pat["brk"] > p.retest_bars:
                pat = None
            elif (l[i] <= nk) if d == 1 else (h[i] >= nk):
                e = min(o[i], nk) if d == 1 else max(o[i], nk)
                tgt = pat["tgt"] if p.target == "measured" else nk + d * p.rr * abs(nk - pat["stop"])
                open_trade(i, d, e, nk, pat["stop"], tgt, limit_fill=True)
                pat = None
            elif (h[i] >= pat["tgt"]) if d == 1 else (l[i] <= pat["tgt"]):
                pat = None                                   # ran to the target without a retest

    if in_tr:
        res.open_trade = f"{'LONG' if tr['d'] == 1 else 'SHORT'} since {t[tr['bar']]}"
    return res


def summarize(symbol, df, res):
    tr = res.trades
    return dict(symbol=symbol, bars=len(df), start=str(df.index[0].date()), end=str(df.index[-1].date()),
                total=stats(tr), long=stats([x for x in tr if x.direction == 1]),
                short=stats([x for x in tr if x.direction == -1]), max_dd_r=max_dd_r(tr), open_trade=res.open_trade,
                patterns=res.patterns)


def print_summary(s):
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===   Patterns: {s['patterns']}   "
          f"Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
    print(f"{'':16}{'Total':>10}{'Longs':>10}{'Shorts':>10}")
    for name, key, fmt in [("Trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Net R", "net_r", "{:+.2f}"),
                           ("Avg R/trade", "avg_r", "{:+.3f}"), ("Profit factor", "pf", "{:.2f}")]:
        print(f"{name:16}" + "".join(f"{_f(x[key], fmt):>10}" for x in (s["total"], s["long"], s["short"])))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbols", nargs="+")
    ap.add_argument("--interval", default="1h")
    ap.add_argument("--range", default="730d")
    ap.add_argument("--csv", default=None, help="read OHLC from this CSV instead of downloading (one symbol)")
    ap.add_argument("--piv", type=int, default=5)
    ap.add_argument("--sh-tol", type=float, default=0.5)
    ap.add_argument("--prior", type=float, default=0.5)
    ap.add_argument("--neck", default="sloped", choices=["sloped", "flat"])
    ap.add_argument("--entry", default="breakout", choices=["breakout", "retest", "early"])
    ap.add_argument("--stop", default="shoulder", choices=["shoulder", "head"])
    ap.add_argument("--target", default="measured", choices=["measured", "rr"])
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--tp1-pct", type=float, default=0.0)
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    p = HSParams(piv_len=a.piv, sh_tol=a.sh_tol, prior_min=a.prior, neck=a.neck, entry=a.entry, stop=a.stop,
                 target=a.target, rr=a.rr, tp1_pct=a.tp1_pct)
    print("Config:", p.label())
    for sym in a.symbols:
        df = pd.read_csv(a.csv, index_col=0, parse_dates=True) if a.csv else fetch_yahoo(sym, a.interval, a.range, a.cache)
        print_summary(summarize(sym, df, backtest(df, p, sym)))


if __name__ == "__main__":
    main()
