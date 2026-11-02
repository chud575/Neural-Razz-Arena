"""
Megaphone (broadening formation) backtester. Mirrors pine/megaphone.pine.

Pattern
  Swing points (pivots) are kept as an alternating high/low sequence. A megaphone exists when the last
  `min_pivots` swings (4, 5 or 6) make HIGHER highs and LOWER lows. Upper line = through the last two swing
  highs, lower line = through the last two swing lows; the lines diverge.
  Tightening toggles:
    min_expand_pct / min_expand_atr  each new extreme must beyond the previous one by this % / x ATR
    fit_atr                          (5+ swings) older swings must sit within this x ATR of the trendlines

Trades
  Edge fade (kind 0)    price returns to an edge and reverses -> trade back into the pattern
                          fade_entry "touch" (limit at the line) | "rejection" (touch + close back inside)
                          stop = line +/- stop_atr x ATR, target = target ("rr" | "midline" | "opposite")
  Breakout (kind 1)     a bar CLOSES beyond a line by brk_atr x ATR
                          bo_entry "close"  -> enter at that close
                          bo_entry "retest" -> limit at the broken line within retest_window bars (one try)
                          stop = back inside the line by stop_atr x ATR
                          bo_target "rr" (R:R x risk) | "measured" (pattern height at the breakout)
  Failed-breakout fade (kind 2, failed_bo=True)
                          after a breakout close, price CLOSES back inside within fb_window bars ->
                          fade at that close; stop beyond the breakout's extreme (+0.2 ATR); target = target

Simulation rules match the other testers: stop wins if stop and target are touched in the same bar,
limit fills only check the stop on the fill bar, gaps fill at the open, one trade at a time, limit
entries measure R from the planned price.

    python megaphone_backtest.py SPY GC=F --mode breakout --bo-entry retest --bo-target measured --pivots 6
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

KINDS = ("Fade", "Breakout", "Failed BO")


@dataclass
class MPParams:
    piv_len: int = 5
    min_pivots: int = 4          # 4 = 2 highs + 2 lows, 5 = the "5-touch" megaphone, 6 = 3 + 3
    min_expand_pct: float = 0.0  # each new high/low must exceed the previous one by this % of price
    min_expand_atr: float = 0.0  # ... and by this x ATR
    fit_atr: float = 0.0         # 5+ swings: older swings must lie within this x ATR of the lines (0 = off)
    max_len: int = 200           # bars from the first pivot until the pattern expires
    atr_len: int = 14
    mode: str = "both"           # fade | breakout | both   (edge fades / breakouts)
    fade_entry: str = "rejection"  # touch | rejection
    zone_atr: float = 0.1
    stop_atr: float = 0.5
    brk_atr: float = 0.2
    target: str = "rr"           # fades: rr | midline | opposite
    bo_entry: str = "close"      # close | retest
    bo_target: str = "rr"        # rr | measured
    retest_window: int = 10
    failed_bo: bool = False
    fb_window: int = 5
    rr: float = 2.0
    trend_filter: str = "off"    # off | sma
    trend_len: int = 200
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        parts = [f"{self.min_pivots} swings"]
        if self.min_expand_atr or self.min_expand_pct:
            parts.append(f"expand {self.min_expand_atr:g}ATR/{self.min_expand_pct:g}%")
        if self.fit_atr:
            parts.append(f"fit {self.fit_atr:g}ATR")
        if self.mode in ("fade", "both"):
            parts.append(f"fade {self.fade_entry}->{self.target}")
        if self.mode in ("breakout", "both"):
            parts.append(f"BO {self.bo_entry}->{self.bo_target}")
        if self.failed_bo:
            parts.append(f"failed-BO fade->{self.target}")
        parts.append(f"{self.rr:g}:1")
        if self.trend_filter == "sma":
            parts.append(f"SMA{self.trend_len}")
        return " | ".join(parts)


def find_megaphone(seq, p: MPParams, atr_now: float):
    """seq: alternating list of (type, price, bar), type 1 = high, -1 = low. Returns pattern dict or None."""
    n = p.min_pivots
    if len(seq) < n:
        return None
    if (p.min_expand_atr > 0 or p.fit_atr > 0) and (atr_now is None or math.isnan(atr_now)):
        return None
    last = seq[-n:]
    highs = [x for x in last if x[0] == 1]
    lows = [x for x in last if x[0] == -1]
    if len(highs) < 2 or len(lows) < 2:
        return None
    for a, b in zip(highs, highs[1:]):
        if b[1] <= a[1] * (1 + p.min_expand_pct / 100) or b[1] - a[1] < p.min_expand_atr * (atr_now or 0):
            return None
    for a, b in zip(lows, lows[1:]):
        if b[1] >= a[1] * (1 - p.min_expand_pct / 100) or a[1] - b[1] < p.min_expand_atr * (atr_now or 0):
            return None
    h1, h2 = highs[-2], highs[-1]
    l1, l2 = lows[-2], lows[-1]
    su = (h2[1] - h1[1]) / (h2[2] - h1[2])
    sl = (l2[1] - l1[1]) / (l2[2] - l1[2])
    if p.fit_atr > 0:
        for x in highs[:-2]:
            if abs(x[1] - (h2[1] + su * (x[2] - h2[2]))) > p.fit_atr * atr_now:
                return None
        for x in lows[:-2]:
            if abs(x[1] - (l2[1] + sl * (x[2] - l2[2]))) > p.fit_atr * atr_now:
                return None
    return dict(bu=h2[2], pu=h2[1], su=su, bl=l2[2], pl=l2[1], sl=sl, start=last[0][2], conf=None, state="live")


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

    def ok(d, i):
        return (p.trade_longs if d == 1 else p.trade_shorts) and trend_ok(d, i)

    def fade_target(d, ref, risk, up, lo):
        if p.target == "rr":
            return ref + d * p.rr * risk
        if p.target == "midline":
            return (up + lo) / 2
        return lo if d == -1 else up

    def open_trade(i, d, kind, e, stop, tgt, risk, limit_fill=False):
        """Open a trade if it makes sense; limit fills are checked against the stop on the same bar."""
        nonlocal in_tr, tr
        if risk <= 0 or (e - stop) * d <= 0 or (tgt - e) * d <= 0:
            return False
        tr = dict(d=d, kind=kind, e=e, s=stop, t=tgt, risk=risk, bar=i, sig=i)
        in_tr = True
        if limit_fill and (l[i] <= stop if d == 1 else h[i] >= stop):
            record(i, stop, "SL")
            in_tr = False
        return True

    for i in range(n):
        # 1) pivots -> pattern detection
        changed = False
        if not math.isnan(ph[i]):
            changed |= push(1, ph[i], i - L)
        if not math.isnan(pl[i]):
            changed |= push(-1, pl[i], i - L)
        if changed:
            found = find_megaphone(seq, p, a[i])
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
        up = pat["pu"] + pat["su"] * (i - pat["bu"])
        lo = pat["pl"] + pat["sl"] * (i - pat["bl"])
        A = a[i]
        can_enter = not in_tr and not exited      # limit/touch entries: not on a bar where a trade just closed
        close_ok = not in_tr                       # entries at the close are fine after an intrabar exit

        if pat["state"] == "live":
            if i - pat["start"] > p.max_len:
                pat = None
                continue
            # 3) edge fades — checked BEFORE the breakout close (a touch limit fills before the close is known)
            if do_fade and can_enter and i > pat["conf"]:
                faded = False
                for d, line in ((-1, up), (1, lo)):          # short at the top edge, long at the bottom edge
                    if not ok(d, i):
                        continue
                    edge = line + d * p.zone_atr * A
                    if not (h[i] >= edge if d == -1 else l[i] <= edge):
                        continue
                    stop = line - d * p.stop_atr * A
                    if p.fade_entry == "touch":
                        e = max(o[i], edge) if d == -1 else min(o[i], edge)
                        ref, limit = edge, True
                    else:
                        if not (c[i] < line if d == -1 else c[i] > line):
                            continue
                        e, ref, limit = c[i], c[i], False
                    if (ref - stop) * d <= 0:
                        continue
                    risk = abs(ref - stop)
                    if open_trade(i, d, 0, e, stop, fade_target(d, ref, risk, up, lo), risk, limit):
                        faded = True
                        break
                close_ok = close_ok and not faded

            # 4) breakout close
            d = 1 if c[i] > up + p.brk_atr * A else -1 if c[i] < lo - p.brk_atr * A else 0
            if d:
                line = up if d == 1 else lo
                height = up - lo
                if do_brk and p.bo_entry == "close" and close_ok and ok(d, i):
                    stop = line - d * p.stop_atr * A
                    risk = abs(c[i] - stop)
                    tgt = c[i] + d * (p.rr * risk if p.bo_target == "rr" else height)
                    open_trade(i, d, 1, c[i], stop, tgt, risk)
                pat.update(state="broken", bo_dir=d, bo_bar=i, ext=h[i] if d == 1 else l[i], height=height,
                           retest=do_brk and p.bo_entry == "retest", fb=p.failed_bo)
            continue

        # ── broken pattern: retest entry and/or failed-breakout fade
        d = pat["bo_dir"]
        line = up if d == 1 else lo
        age = i - pat["bo_bar"]
        pat["ext"] = max(pat["ext"], h[i]) if d == 1 else min(pat["ext"], l[i])
        entered = False
        if pat["retest"]:
            if age > p.retest_window:
                pat["retest"] = False
            elif can_enter:
                zone = line + d * p.zone_atr * A
                stop = line - d * p.stop_atr * A
                if l[i] <= zone if d == 1 else h[i] >= zone:
                    pat["retest"] = False                 # one try
                    if ok(d, i):
                        e = min(o[i], zone) if d == 1 else max(o[i], zone)
                        risk = abs(zone - stop)
                        tgt = zone + d * (p.rr * risk if p.bo_target == "rr" else pat["height"])
                        entered = open_trade(i, d, 1, e, stop, tgt, risk, limit_fill=True)
            if pat["retest"] and (c[i] - (line - d * p.stop_atr * A)) * d < 0:
                pat["retest"] = False                     # closed back through the stop level: breakout failed
        if pat["fb"]:
            if age > p.fb_window:
                pat["fb"] = False
            elif c[i] < line if d == 1 else c[i] > line:  # closed back inside the megaphone
                pat["fb"] = False
                fd = -d
                if close_ok and not in_tr and not entered and ok(fd, i):
                    stop = pat["ext"] + d * 0.2 * A
                    risk = abs(c[i] - stop)
                    open_trade(i, fd, 2, c[i], stop, fade_target(fd, c[i], risk, up, lo), risk)
        if not pat["retest"] and not pat["fb"]:
            pat = None

    if in_tr:
        res.open_trade = f"{'LONG' if tr['d'] == 1 else 'SHORT'} since {t[tr['bar']].date()}"
    return res


def summarize(symbol, df, res):
    tr = res.trades
    return dict(symbol=symbol, bars=len(df), start=str(df.index[0].date()), end=str(df.index[-1].date()),
                patterns=res.e2_fills,
                kinds=[stats([x for x in tr if x.entry == k]) for k in range(3)],
                total=stats(tr), long=stats([x for x in tr if x.direction == 1]),
                short=stats([x for x in tr if x.direction == -1]), max_dd_r=max_dd_r(tr), open_trade=res.open_trade)


def print_summary(s):
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===")
    print(f"Megaphones detected: {s['patterns']}   Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
    print(f"{'':16}" + "".join(f"{k:>11}" for k in KINDS) + f"{'Total':>11}{'Longs':>11}{'Shorts':>11}")
    cols = s["kinds"] + [s["total"], s["long"], s["short"]]
    for name, key, fmt in [("Trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Net R", "net_r", "{:+.2f}"),
                           ("Avg R/trade", "avg_r", "{:+.3f}"), ("Profit factor", "pf", "{:.2f}")]:
        print(f"{name:16}" + "".join(f"{_f(x[key], fmt):>11}" for x in cols))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbols", nargs="+")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--mode", default="both", choices=["fade", "breakout", "both", "none"],
                    help="edge fades / breakouts ('none' = only the failed-breakout fade)")
    ap.add_argument("--fade-entry", default="rejection", choices=["touch", "rejection"])
    ap.add_argument("--target", default="rr", choices=["rr", "midline", "opposite"])
    ap.add_argument("--bo-entry", default="close", choices=["close", "retest"])
    ap.add_argument("--bo-target", default="rr", choices=["rr", "measured"])
    ap.add_argument("--failed-bo", action="store_true")
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--pivots", type=int, default=4, choices=[4, 5, 6])
    ap.add_argument("--expand-atr", type=float, default=0.0)
    ap.add_argument("--fit-atr", type=float, default=0.0)
    ap.add_argument("--trend", default="off", choices=["off", "sma"])
    ap.add_argument("--longs-only", action="store_true")
    ap.add_argument("--shorts-only", action="store_true")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    p = MPParams(mode=a.mode, fade_entry=a.fade_entry, target=a.target, rr=a.rr, min_pivots=a.pivots,
                 min_expand_atr=a.expand_atr, fit_atr=a.fit_atr, bo_entry=a.bo_entry, bo_target=a.bo_target,
                 failed_bo=a.failed_bo, trend_filter=a.trend, trade_longs=not a.shorts_only, trade_shorts=not a.longs_only)
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
