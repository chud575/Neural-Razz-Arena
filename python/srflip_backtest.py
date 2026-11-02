"""
S/R flip (break-and-retest / liquidity sweep) backtester. Mirrors pine/sr_flip.pine.

Idea
  1. Resistance = an unbroken swing high (pivot) that is at least `min_age` bars old.
  2. Breakout   = a bar CLOSES above it by at least `brk_atr` x ATR. The level is now "flipped" (expected support).
  3. Retest     = within `window` bars price comes back to the level. Entry modes:
        touch      limit order at level + zone (fills as soon as price trades into the zone)
        rejection  a bar trades into the zone and CLOSES back above the level -> enter at that close
        sweep      a bar wicks BELOW the level by >= sweep_atr x ATR (stop-hunt) and CLOSES back above -> enter at close
  4. Stop       = level - stop_atr x ATR (sweep mode: also below the sweep wick).
     Target     = rr x risk.
  5. Multiple tries: after a stop-out the level stays live (up to `max_tries`) unless a bar CLOSES
     beyond the stop level, the window expires, or a target is hit.
  Shorts are the mirror image (support breaks, retest from below).

Simulation (same conservative rules as the DT/DB tester): stop wins if stop and target are touched in
the same bar; limit fills only check the stop on the fill bar; gaps fill at the open; one trade at a time.

    python srflip_backtest.py SPY BTC-USD --mode rejection --rr 3 --tries 3
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from dtdb_backtest import Result, Trade, fetch_yahoo, max_dd_r, pivots, stats, _f


@dataclass
class SRParams:
    piv_len: int = 5
    max_age: int = 250          # candidate level expires this many bars after its pivot
    min_age: int = 10           # level must be at least this old when broken ("old" resistance)
    atr_len: int = 14
    brk_atr: float = 0.2        # breakout close must clear the level by this x ATR
    window: int = 30            # bars after the breakout during which retests are traded
    min_bars_after: int = 1     # earliest retest bar after the breakout
    entry_mode: str = "touch"   # touch | rejection | sweep
    zone_atr: float = 0.1       # entry zone on the breakout side of the level
    sweep_atr: float = 0.1      # sweep: wick must pierce the level by this x ATR
    stop_atr: float = 0.5       # stop (and close-invalidation) distance beyond the level
    max_tries: int = 3
    rr: float = 2.0
    trend_filter: str = "off"   # off | sma
    trend_len: int = 200
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        s = f"{self.entry_mode} | tries {self.max_tries} | {self.rr:g}:1"
        if self.trend_filter == "sma":
            s += f" | SMA{self.trend_len}"
        if not self.trade_shorts:
            s += " | longs only"
        if not self.trade_longs:
            s += " | shorts only"
        return s


def atr(h, l, c, n):
    prev = np.concatenate([[c[0]], c[:-1]])
    tr = np.maximum(h - l, np.maximum(abs(h - prev), abs(l - prev)))
    out = np.full(len(tr), np.nan)
    if len(tr) < n:
        return out
    out[n - 1] = tr[:n].mean()
    for i in range(n, len(tr)):                     # Wilder / Pine ta.rma
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def backtest(df: pd.DataFrame, p: SRParams, symbol: str = "") -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    L = p.piv_len
    ph, pl = pivots(h, l, L)
    a = atr(h, l, c, p.atr_len)
    sma = pd.Series(c).rolling(p.trend_len).mean().to_numpy() if p.trend_filter == "sma" else None
    res = Result()

    res_lv: list[tuple[float, int]] = []   # unbroken resistance (price, pivot bar)
    sup_lv: list[tuple[float, int]] = []   # unbroken support

    # active flipped level
    act = None   # dict(d, lvl, brk_bar, atr, tries)
    # open trade
    in_tr = False
    tr_d = 0
    tr_e = tr_s = tr_t = tr_risk = math.nan
    tr_bar = -1
    tr_try = 0

    def record(i, exit_px, reason):
        r = tr_d * (exit_px - tr_e) / tr_risk if tr_risk > 0 else 0.0
        pct = tr_d * (exit_px - tr_e) / tr_e * 100
        res.trades.append(Trade(symbol, tr_d, min(tr_try, 2), t[act_brk_bar], t[i], tr_e, exit_px, tr_s, r, pct, reason,
                                tr_risk))

    act_brk_bar = 0
    for i in range(n):
        if not math.isnan(ph[i]):
            res_lv.append((ph[i], i - L))
        if not math.isnan(pl[i]):
            sup_lv.append((pl[i], i - L))
        res_lv = [x for x in res_lv if i - x[1] <= p.max_age]
        sup_lv = [x for x in sup_lv if i - x[1] <= p.max_age]

        # 1) manage open trade
        exited = False
        if in_tr and i > tr_bar:
            d = tr_d
            stop_hit = l[i] <= tr_s if d == 1 else h[i] >= tr_s
            tp_hit = h[i] >= tr_t if d == 1 else l[i] <= tr_t
            if stop_hit:
                record(i, min(o[i], tr_s) if d == 1 else max(o[i], tr_s), "SL")
                in_tr, exited = False, True
                act["tries"] += 1
                if act["tries"] >= p.max_tries:
                    act = None
            elif tp_hit:
                record(i, max(o[i], tr_t) if d == 1 else min(o[i], tr_t), "TP")
                in_tr, exited = False, True
                act = None

        # 2) entry on a retest of the active level
        if act and not in_tr and not exited and i >= act["brk_bar"] + p.min_bars_after:
            d, lvl, A = act["d"], act["lvl"], act["atr"]
            zone = lvl + d * p.zone_atr * A
            base_stop = lvl - d * p.stop_atr * A
            in_zone = l[i] <= zone if d == 1 else h[i] >= zone
            entry = None
            plan = None          # planned entry price (limit level) used for risk/target
            stop = base_stop
            same_bar_stop_check = False
            if p.entry_mode == "touch":
                if in_zone:
                    entry = min(o[i], zone) if d == 1 else max(o[i], zone)
                    plan = zone
                    same_bar_stop_check = True
            elif p.entry_mode == "rejection":
                if in_zone and (c[i] > lvl if d == 1 else c[i] < lvl):
                    entry = c[i]
            elif p.entry_mode == "sweep":
                pierced = l[i] <= lvl - p.sweep_atr * A if d == 1 else h[i] >= lvl + p.sweep_atr * A
                if pierced and (c[i] > lvl if d == 1 else c[i] < lvl):
                    entry = c[i]
                    wick_stop = l[i] - 0.1 * A if d == 1 else h[i] + 0.1 * A
                    stop = min(base_stop, wick_stop) if d == 1 else max(base_stop, wick_stop)
            if entry is not None and (entry > stop if d == 1 else entry < stop):
                in_tr, tr_d, tr_e, tr_s, tr_bar, tr_try = True, d, entry, stop, i, act["tries"]
                ref = plan if plan is not None else entry
                tr_risk = abs(ref - stop)
                tr_t = ref + d * p.rr * tr_risk
                act_brk_bar = act["brk_bar"]
                if same_bar_stop_check and (l[i] <= stop if d == 1 else h[i] >= stop):
                    record(i, stop, "SL")      # filled then stopped in the same bar
                    in_tr = False
                    act["tries"] += 1
                    if act["tries"] >= p.max_tries:
                        act = None

        # 3) invalidation / expiry of the active level (only while flat)
        if act and not in_tr:
            d, lvl, A = act["d"], act["lvl"], act["atr"]
            inval = lvl - d * p.stop_atr * A
            if (c[i] < inval if d == 1 else c[i] > inval) or i - act["brk_bar"] > p.window:
                act = None

        # 4) breakouts
        if math.isnan(a[i]):
            continue
        new = None
        broken = [x for x in res_lv if c[i] > x[0]]
        if broken:
            res_lv = [x for x in res_lv if c[i] <= x[0]]
            ok = [x for x in broken if c[i] >= x[0] + p.brk_atr * a[i] and i - x[1] >= p.min_age]
            if ok and p.trade_longs:
                new = (1, max(ok)[0])
        broken = [x for x in sup_lv if c[i] < x[0]]
        if broken:
            sup_lv = [x for x in sup_lv if c[i] >= x[0]]
            ok = [x for x in broken if c[i] <= x[0] - p.brk_atr * a[i] and i - x[1] >= p.min_age]
            if ok and p.trade_shorts and new is None:
                new = (-1, min(ok)[0])
        if new and not in_tr:
            d, lvl = new
            if sma is None or (not math.isnan(sma[i]) and (c[i] > sma[i] if d == 1 else c[i] < sma[i])):
                act = dict(d=d, lvl=lvl, brk_bar=i, atr=a[i], tries=0)
                if d == 1:
                    res.signals_long += 1
                else:
                    res.signals_short += 1

    if in_tr:
        res.open_trade = f"{'LONG' if tr_d == 1 else 'SHORT'} since {t[tr_bar].date()}"
    return res


def summarize(symbol, df, res):
    tr = res.trades
    sig = res.signals_long + res.signals_short
    levels_won = len({(x.signal_time, x.direction) for x in tr if x.r > 0})
    levels_traded = len({(x.signal_time, x.direction) for x in tr})
    return dict(symbol=symbol, bars=len(df), start=str(df.index[0].date()), end=str(df.index[-1].date()),
                breakouts=sig, levels_traded=levels_traded, levels_won=levels_won,
                t1=stats([x for x in tr if x.entry == 0]), t2=stats([x for x in tr if x.entry == 1]),
                t3=stats([x for x in tr if x.entry == 2]), total=stats(tr),
                long=stats([x for x in tr if x.direction == 1]), short=stats([x for x in tr if x.direction == -1]),
                max_dd_r=max_dd_r(tr), open_trade=res.open_trade)


def print_summary(s):
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===")
    print(f"Breakouts: {s['breakouts']}   Levels traded: {s['levels_traded']}   Levels that paid: {s['levels_won']}   "
          f"Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
    print(f"{'':16}{'Try 1':>10}{'Try 2':>10}{'Try 3+':>10}{'Total':>10}{'Longs':>10}{'Shorts':>10}")
    cols = [s["t1"], s["t2"], s["t3"], s["total"], s["long"], s["short"]]
    for name, key, fmt in [("Trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Net R", "net_r", "{:+.2f}"),
                           ("Avg R/trade", "avg_r", "{:+.3f}"), ("Profit factor", "pf", "{:.2f}")]:
        print(f"{name:16}" + "".join(f"{_f(x[key], fmt):>10}" for x in cols))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbols", nargs="+")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--mode", default="touch", choices=["touch", "rejection", "sweep"])
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--tries", type=int, default=3)
    ap.add_argument("--trend", default="off", choices=["off", "sma"])
    ap.add_argument("--longs-only", action="store_true")
    ap.add_argument("--shorts-only", action="store_true")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    p = SRParams(entry_mode=a.mode, rr=a.rr, max_tries=a.tries, trend_filter=a.trend,
                 trade_longs=not a.shorts_only, trade_shorts=not a.longs_only)
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
