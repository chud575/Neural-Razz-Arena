"""
Range liquidity-sweep (stop-hunt reversal) backtester. Mirrors pine/range_sweep.pine.

Idea
  1. Tight range: over the previous `range_len` bars (current bar excluded) the highest high and lowest low are
     between `min_range_atr` and `max_range_atr` x ATR apart, and price visited each edge zone (within
     `touch_zone_atr` x ATR of the edge) at least `min_touches` separate times.
  2. Sweep: a bar wicks THROUGH an edge by at least `sweep_min_atr` x ATR (and by at most `sweep_max_atr`, deeper =
     treated as a real breakout) and CLOSES back inside the range.
        reclaim "same_bar"  -> the sweep bar itself closes back inside
        reclaim "within_n"  -> a bar that closed outside is followed, within `reclaim_bars` bars, by a close back inside
  3. Entry: fade the sweep at that close (sweep of the high -> short, sweep of the low -> long).
  4. Stop: beyond the sweep's extreme by `stop_atr` x ATR.
  5. Target (TP2): "opposite" side of the range | "midline" | "rr" (rr x risk). TP1 / % at TP1 / breakeven as in
     the other scripts (exits.py). ATR = Wilder ATR of the bar BEFORE the signal.

Same conservative simulation rules as the other testers; one trade at a time.

    python rangesweep_backtest.py BTC-USD --interval 1h --range 730d
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from dtdb_backtest import Result, Trade, _f, fetch_yahoo, max_dd_r, stats
from exits import make_entry, scale_step
from srflip_backtest import atr

__version__ = "1.2"  # same version as pine/range_sweep.pine (costs: run_btc_sweep.py --fees)


@dataclass
class RSParams:
    range_len: int = 120
    atr_len: int = 14
    min_range_atr: float = 2.0
    max_range_atr: float = 10.0
    min_touches: int = 2
    touch_zone_atr: float = 0.5
    sweep_min_atr: float = 0.1
    sweep_max_atr: float = 2.0      # 0 = no limit
    reclaim: str = "same_bar"       # same_bar | within_n
    reclaim_bars: int = 3
    stop_atr: float = 0.25
    target: str = "opposite"        # opposite | midline | rr
    rr: float = 2.0                 # TP2 when target == "rr"
    tp1_rr: float = 1.0
    tp1_pct: float = 0.0            # 0 = single target (Pine defaults to 50)
    be_after_tp1: bool = True
    trend_filter: str = "off"
    trend_len: int = 200
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        s = (f"range {self.range_len} bars ≤{self.max_range_atr:g}ATR touches≥{self.min_touches} | "
             f"{self.reclaim} | target {self.target}" + (f" {self.rr:g}R" if self.target == "rr" else ""))
        if self.tp1_pct > 0:
            s += f" | TP1 {self.tp1_rr:g}R ({self.tp1_pct:g}%)" + (" BE" if self.be_after_tp1 else "")
        if self.trend_filter == "sma":
            s += f" | SMA{self.trend_len}"
        return s


def count_visits(x: np.ndarray, lo_i: int, hi_i: int, thresh: float, above: bool) -> int:
    """Number of separate runs of bars in x[lo_i:hi_i] that are inside the edge zone."""
    zone = x[lo_i:hi_i] >= thresh if above else x[lo_i:hi_i] <= thresh
    if not zone.any():
        return 0
    return int(zone[0]) + int(np.count_nonzero(zone[1:] & ~zone[:-1]))


def backtest(df: pd.DataFrame, p: RSParams, symbol: str = "") -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    N = p.range_len
    a = atr(h, l, c, p.atr_len)
    rhi = pd.Series(h).rolling(N).max().shift(1).to_numpy()     # range of the N bars BEFORE bar i
    rlo = pd.Series(l).rolling(N).min().shift(1).to_numpy()
    sma = pd.Series(c).rolling(p.trend_len).mean().to_numpy() if p.trend_filter == "sma" else None
    p1 = p.tp1_pct / 100.0
    res = Result()

    in_tr = False
    tr: dict = {}
    pend = None          # within_n: dict(d, hi, lo, ext, bar, A)

    def range_ok(i):
        """Is the range ending at bar i-1 tight with enough visits to both edges? Returns (hi, lo, A) or None."""
        if i < N + 1 or math.isnan(rhi[i]) or math.isnan(a[i - 1]):
            return None
        hi, lo, A = rhi[i], rlo[i], a[i - 1]
        height = hi - lo
        if A <= 0 or not (p.min_range_atr * A <= height <= p.max_range_atr * A):
            return None
        z = p.touch_zone_atr * A
        if p.min_touches > 1:
            if count_visits(h, i - N, i, hi - z, True) < p.min_touches:
                return None
            if count_visits(l, i - N, i, lo + z, False) < p.min_touches:
                return None
        return hi, lo, A

    def trend_ok(d, i):
        if sma is None:
            return True
        return not math.isnan(sma[i]) and (c[i] > sma[i] if d == 1 else c[i] < sma[i])

    def try_enter(i, d, hi, lo, ext, A):
        nonlocal in_tr, tr
        if not ((p.trade_longs if d == 1 else p.trade_shorts) and trend_ok(d, i)):
            return False
        e = c[i]
        stop = ext - d * p.stop_atr * A            # long: below the sweep low; short: above the sweep high
        risk = abs(e - stop)
        if risk <= 0 or (e - stop) * d <= 0:
            return False
        if p.target == "opposite":
            tgt = hi if d == 1 else lo
        elif p.target == "midline":
            tgt = (hi + lo) / 2
        else:
            tgt = e + d * p.rr * risk
        if (tgt - e) * d <= 0:
            return False
        tr = dict(d=d, e=e, s=stop, t=tgt, risk=risk, bar=i,
                  en=make_entry(e, risk, stop, e + d * p.tp1_rr * risk, tgt, d, p1))
        in_tr = True
        if d == 1:
            res.signals_long += 1
        else:
            res.signals_short += 1
        return True

    for i in range(n):
        # 1) manage open trade
        if in_tr and i > tr["bar"]:
            closed, x_px, reason, _ = scale_step(o, h, l, i, tr["d"], tr["en"], p1, p.be_after_tp1)
            if closed:
                en = tr["en"]
                res.trades.append(Trade(symbol, tr["d"], 0, t[tr["bar"]], t[i], tr["e"], x_px, tr["s"],
                                        en["r"], en["pct"], reason, tr["risk"], tr["t"]))
                in_tr = False
        if in_tr:
            pend = None
            continue

        # 2) pending sweep (within_n): waiting for a close back inside
        if pend is not None:
            d = pend["d"]                                   # trade direction
            pend["ext"] = min(pend["ext"], l[i]) if d == 1 else max(pend["ext"], h[i])
            too_deep = p.sweep_max_atr > 0 and (
                (pend["lo"] - pend["ext"]) if d == 1 else (pend["ext"] - pend["hi"])) > p.sweep_max_atr * pend["A"]
            back_in = pend["lo"] < c[i] < pend["hi"]
            if too_deep or i - pend["bar"] > p.reclaim_bars:
                pend = None
            elif back_in:
                try_enter(i, d, pend["hi"], pend["lo"], pend["ext"], pend["A"])
                pend = None
                continue

        # 3) new sweep of a tight range
        rg = range_ok(i)
        if rg is None:
            continue
        hi, lo, A = rg
        for d, pierced, depth, ext in ((-1, h[i] > hi + p.sweep_min_atr * A, h[i] - hi, h[i]),
                                       (1, l[i] < lo - p.sweep_min_atr * A, lo - l[i], l[i])):
            if not pierced or (p.sweep_max_atr > 0 and depth > p.sweep_max_atr * A):
                continue
            if lo < c[i] < hi:                              # closed back inside on the same bar
                try_enter(i, d, hi, lo, ext, A)
                break
            if p.reclaim == "within_n" and pend is None:    # closed outside: wait for a reclaim
                pend = dict(d=d, hi=hi, lo=lo, ext=ext, bar=i, A=A)
                break

    if in_tr:
        res.open_trade = f"{'LONG' if tr['d'] == 1 else 'SHORT'} since {t[tr['bar']]}"
    return res


def summarize(symbol, df, res):
    tr = res.trades
    return dict(symbol=symbol, bars=len(df), start=str(df.index[0].date()), end=str(df.index[-1].date()),
                total=stats(tr), long=stats([x for x in tr if x.direction == 1]),
                short=stats([x for x in tr if x.direction == -1]), max_dd_r=max_dd_r(tr), open_trade=res.open_trade)


def print_summary(s):
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===   Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
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
    ap.add_argument("--range-len", type=int, default=120)
    ap.add_argument("--max-range-atr", type=float, default=10.0)
    ap.add_argument("--touches", type=int, default=2)
    ap.add_argument("--reclaim", default="same_bar", choices=["same_bar", "within_n"])
    ap.add_argument("--target", default="opposite", choices=["opposite", "midline", "rr"])
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--tp1-pct", type=float, default=0.0)
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    p = RSParams(range_len=a.range_len, max_range_atr=a.max_range_atr, min_touches=a.touches, reclaim=a.reclaim,
                 target=a.target, rr=a.rr, tp1_pct=a.tp1_pct)
    print("Config:", p.label())
    for sym in a.symbols:
        df = pd.read_csv(a.csv, index_col=0, parse_dates=True) if a.csv else fetch_yahoo(sym, a.interval, a.range, a.cache)
        print_summary(summarize(sym, df, backtest(df, p, sym)))


if __name__ == "__main__":
    main()
