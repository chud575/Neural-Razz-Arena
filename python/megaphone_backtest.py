"""
Megaphone (broadening formation) backtester. Mirrors pine/megaphone.pine.

Pattern
  Swing points (pivots) are kept as an alternating high/low sequence. A megaphone exists when the last
  `min_pivots` swings make HIGHER highs and LOWER lows (each new extreme beyond the previous one by at
  least `min_expand_pct` %). Upper line = through the last two swing highs, lower line = through the last
  two swing lows; the lines diverge. The pattern stays live until a breakout close or `max_len` bars.

Trades (toggle with `mode`)
  fade      price returns to an edge and reverses -> trade back into the pattern
              fade_entry "touch"     limit order at the line (minus a small zone)
              fade_entry "rejection" bar touches the line and CLOSES back inside -> enter at the close
              stop   = line +/- stop_atr x ATR
              target = "rr" (R:R x risk) | "midline" | "opposite" (opposite line at entry time)
  breakout  a bar CLOSES beyond a line by brk_atr x ATR -> trade the breakout at the close
              stop   = back inside the line by stop_atr x ATR, target = R:R x risk. The pattern ends.

Simulation rules match the other testers: stop wins if stop and target are touched in the same bar,
limit fills only check the stop on the fill bar, gaps fill at the open, one trade at a time, limit
entries measure R from the planned price.

    python megaphone_backtest.py SPY GC=F --mode fade --fade-entry rejection --target opposite
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from dtdb_backtest import Result, Trade, _f, fetch_yahoo, max_dd_r, pivots, stats
from srflip_backtest import atr


@dataclass
class MPParams:
    piv_len: int = 5
    min_pivots: int = 4          # 4 = 2 highs + 2 lows, 5 = the "5-touch" megaphone
    min_expand_pct: float = 0.0  # each new high/low must exceed the previous one by this % of price
    max_len: int = 200           # bars from the first pivot until the pattern expires
    atr_len: int = 14
    mode: str = "both"           # fade | breakout | both
    fade_entry: str = "rejection"  # touch | rejection
    zone_atr: float = 0.1
    stop_atr: float = 0.5
    brk_atr: float = 0.2
    target: str = "rr"           # rr | midline | opposite  (fades only; breakouts always use rr)
    rr: float = 2.0
    trend_filter: str = "off"    # off | sma
    trend_len: int = 200
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        parts = [self.mode]
        if self.mode != "breakout":
            parts.append(f"fade {self.fade_entry} -> {self.target}")
        parts.append(f"{self.rr:g}:1")
        parts.append(f"{self.min_pivots} pivots")
        if self.trend_filter == "sma":
            parts.append(f"SMA{self.trend_len}")
        return " | ".join(parts)


def find_megaphone(seq, p: MPParams):
    """seq: alternating list of (type, price, bar), type 1 = high, -1 = low. Returns pattern dict or None."""
    n = p.min_pivots
    if len(seq) < n:
        return None
    last = seq[-n:]
    highs = [x for x in last if x[0] == 1]
    lows = [x for x in last if x[0] == -1]
    if len(highs) < 2 or len(lows) < 2:
        return None
    for a, b in zip(highs, highs[1:]):
        if b[1] <= a[1] * (1 + p.min_expand_pct / 100):
            return None
    for a, b in zip(lows, lows[1:]):
        if b[1] >= a[1] * (1 - p.min_expand_pct / 100):
            return None
    h1, h2 = highs[-2], highs[-1]
    l1, l2 = lows[-2], lows[-1]
    su = (h2[1] - h1[1]) / (h2[2] - h1[2])
    sl = (l2[1] - l1[1]) / (l2[2] - l1[2])
    return dict(bu=h2[2], pu=h2[1], su=su, bl=l2[2], pl=l2[1], sl=sl, start=last[0][2],
                h1=h1, l1=l1, conf=None)


def backtest(df: pd.DataFrame, p: MPParams, symbol: str = "") -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    L = p.piv_len
    ph, pl = pivots(h, l, L)
    a = atr(h, l, c, p.atr_len)
    sma = pd.Series(c).rolling(p.trend_len).mean().to_numpy() if p.trend_filter == "sma" else None
    res = Result()
    do_fade = p.mode in ("fade", "both")
    do_brk = p.mode in ("breakout", "both")

    seq: list[tuple[int, float, int]] = []
    pat = None
    in_tr = False
    tr = {}

    def push(tp, price, bar):
        """Append a pivot keeping the sequence alternating (same-type pivots: keep the more extreme)."""
        if seq and seq[-1][0] == tp:
            if (tp == 1 and price > seq[-1][1]) or (tp == -1 and price < seq[-1][1]):
                seq[-1] = (tp, price, bar)
                return True
            return False
        seq.append((tp, price, bar))
        if len(seq) > 12:
            del seq[0]
        return True

    def record(i, exit_px, reason):
        r = tr["d"] * (exit_px - tr["e"]) / tr["risk"] if tr["risk"] > 0 else 0.0
        pct = tr["d"] * (exit_px - tr["e"]) / tr["e"] * 100
        res.trades.append(Trade(symbol, tr["d"], tr["kind"], t[tr["sig"]], t[i], tr["e"], exit_px, tr["s"], r, pct,
                                reason, tr["risk"], tr["t"]))

    def trend_ok(d, i):
        if sma is None:
            return True
        return not math.isnan(sma[i]) and (c[i] > sma[i] if d == 1 else c[i] < sma[i])

    def side_ok(d):
        return p.trade_longs if d == 1 else p.trade_shorts

    for i in range(n):
        # 1) pivots -> pattern detection
        changed = False
        if not math.isnan(ph[i]):
            changed |= push(1, ph[i], i - L)
        if not math.isnan(pl[i]):
            changed |= push(-1, pl[i], i - L)
        if changed:
            found = find_megaphone(seq, p)
            if found:
                found["conf"] = i
                pat = found
                res.e2_fills += 1      # reuse: number of megaphones detected

        # 2) manage open trade
        exited = False
        if in_tr and i > tr["bar"]:
            d = tr["d"]
            stop_hit = l[i] <= tr["s"] if d == 1 else h[i] >= tr["s"]
            tp_hit = h[i] >= tr["t"] if d == 1 else l[i] <= tr["t"]
            if stop_hit:
                record(i, min(o[i], tr["s"]) if d == 1 else max(o[i], tr["s"]), "SL")
                in_tr, exited = False, True
            elif tp_hit:
                record(i, max(o[i], tr["t"]) if d == 1 else min(o[i], tr["t"]), "TP")
                in_tr, exited = False, True

        if pat is None or math.isnan(a[i]):
            continue
        if i - pat["start"] > p.max_len:
            pat = None
            continue
        up = pat["pu"] + pat["su"] * (i - pat["bu"])
        lo = pat["pl"] + pat["sl"] * (i - pat["bl"])
        A = a[i]

        # 3) fade at the edges (only after the pattern was confirmed).
        #    Checked BEFORE the breakout: a touch limit order fills intrabar, before we know how the bar closes.
        if do_fade and not in_tr and not exited and i > pat["conf"]:
            for d, line in ((-1, up), (1, lo)):          # d = trade direction: short at the top, long at the bottom
                if not side_ok(d) or not trend_ok(d, i):
                    continue
                edge = line + d * p.zone_atr * A           # zone just inside the line
                touched = h[i] >= edge if d == -1 else l[i] <= edge
                if not touched:
                    continue
                stop = line - d * p.stop_atr * A
                plan = None
                if p.fade_entry == "touch":
                    e = max(o[i], edge) if d == -1 else min(o[i], edge)
                    plan = edge
                else:
                    if not (c[i] < line if d == -1 else c[i] > line):
                        continue
                    e = c[i]
                ref = plan if plan is not None else e
                if (ref - stop) * d <= 0 or (e - stop) * d <= 0:
                    continue
                risk = abs(ref - stop)
                if p.target == "rr":
                    tgt = ref + d * p.rr * risk
                elif p.target == "midline":
                    tgt = (up + lo) / 2
                else:
                    tgt = lo if d == -1 else up
                if (tgt - ref) * d <= 0:
                    continue
                tr = dict(d=d, kind=0, e=e, s=stop, t=tgt, risk=risk, bar=i, sig=i)
                in_tr = True
                if plan is not None and (h[i] >= stop if d == -1 else l[i] <= stop):
                    record(i, stop, "SL")   # limit filled, then stopped in the same bar
                    in_tr = False
                break

        # 4) breakout close (ends the pattern; only traded if flat)
        brk = 1 if c[i] > up + p.brk_atr * A else -1 if c[i] < lo - p.brk_atr * A else 0
        if brk:
            if do_brk and not in_tr and side_ok(brk) and trend_ok(brk, i):
                line = up if brk == 1 else lo
                stop = line - brk * p.stop_atr * A
                e = c[i]
                risk = abs(e - stop)
                if (e - stop) * brk > 0:
                    tr = dict(d=brk, kind=1, e=e, s=stop, t=e + brk * p.rr * risk, risk=risk, bar=i, sig=i)
                    in_tr = True
                    if brk == 1:
                        res.signals_long += 1
                    else:
                        res.signals_short += 1
            pat = None

    if in_tr:
        res.open_trade = f"{'LONG' if tr['d'] == 1 else 'SHORT'} since {t[tr['bar']].date()}"
    return res


def summarize(symbol, df, res):
    tr = res.trades
    return dict(symbol=symbol, bars=len(df), start=str(df.index[0].date()), end=str(df.index[-1].date()),
                patterns=res.e2_fills,
                fade=stats([x for x in tr if x.entry == 0]), brk=stats([x for x in tr if x.entry == 1]),
                total=stats(tr), long=stats([x for x in tr if x.direction == 1]),
                short=stats([x for x in tr if x.direction == -1]), max_dd_r=max_dd_r(tr), open_trade=res.open_trade)


def print_summary(s):
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===")
    print(f"Megaphones detected: {s['patterns']}   Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
    print(f"{'':16}{'Fade':>10}{'Breakout':>10}{'Total':>10}{'Longs':>10}{'Shorts':>10}")
    cols = [s["fade"], s["brk"], s["total"], s["long"], s["short"]]
    for name, key, fmt in [("Trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Net R", "net_r", "{:+.2f}"),
                           ("Avg R/trade", "avg_r", "{:+.3f}"), ("Profit factor", "pf", "{:.2f}")]:
        print(f"{name:16}" + "".join(f"{_f(x[key], fmt):>10}" for x in cols))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbols", nargs="+")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--mode", default="both", choices=["fade", "breakout", "both"])
    ap.add_argument("--fade-entry", default="rejection", choices=["touch", "rejection"])
    ap.add_argument("--target", default="rr", choices=["rr", "midline", "opposite"])
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--pivots", type=int, default=4, choices=[4, 5, 6])
    ap.add_argument("--trend", default="off", choices=["off", "sma"])
    ap.add_argument("--longs-only", action="store_true")
    ap.add_argument("--shorts-only", action="store_true")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    p = MPParams(mode=a.mode, fade_entry=a.fade_entry, target=a.target, rr=a.rr, min_pivots=a.pivots,
                 trend_filter=a.trend, trade_longs=not a.shorts_only, trade_shorts=not a.longs_only)
    print("Config:", p.label())
    for sym in a.symbols:
        try:
            df = fetch_yahoo(sym, a.interval, a.range, a.cache)
        except Exception as e:  # noqa: BLE001
            print(f"{sym}: data error {e}", file=sys.stderr)
            continue
        print_summary(summarize(sym, df, backtest(df, p, sym)))


if __name__ == "__main__":
    main()
