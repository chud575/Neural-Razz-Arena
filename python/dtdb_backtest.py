"""
Python port of pine/double_top_bottom_2entry.pine, with strategy toggles.

Same pattern detection and the same conservative bar-by-bar trade simulation as
the TradingView indicator, so numbers should match for the same data/settings.

Toggles (see Params):
  use_entry1     Entry 1 = market entry at the close of the breakout bar.
  entry2_mode    "off"            no second entry
                 "midpoint"       limit halfway between neckline and pattern extreme (original idea)
                 "retest"         limit at the neckline (retest of the breakout point)
                 "retest_confirm" a bar touches the neckline and CLOSES back on the breakout side; enter at that close
  rr             reward : risk of the final target (TP2)
  tp1_rr         reward : risk of TP1
  tp1_pct        % of each entry closed at TP1 (0 = single target at rr — the default here, so older results
                 reproduce; the Pine indicator defaults to 50)
  be_after_tp1   move the remainder's stop to breakeven after TP1 (remainder managed from the next bar)
  tgt_mode       "per_entry" (each entry its own RR target) or "blended" (one target off the average entry)
  trend_filter   "off" or "sma" (longs only above the N-period SMA, shorts only below)
  trade_longs / trade_shorts

Examples:
    python dtdb_backtest.py SPY BTC-USD
    python dtdb_backtest.py SPY --no-entry1 --entry2 retest --rr 3 --trend sma
"""
from __future__ import annotations

__version__ = "1.5"  # same version as pine/double_top_bottom_2entry.pine

import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import requests


# ───────────────────────────── Settings ─────────────────────────────
@dataclass
class Params:
    # pattern detection
    piv_len: int = 5
    tol_pct: float = 0.5
    min_sep: int = 10
    max_sep: int = 100
    min_depth: float = 1.0
    max_wait: int = 30
    # trade plan toggles
    trade_longs: bool = True
    trade_shorts: bool = True
    use_entry1: bool = True
    entry2_mode: str = "midpoint"      # off | midpoint | retest | retest_confirm
    rr: float = 2.0                    # TP2 (final target) as R multiple
    tp1_rr: float = 1.0                # TP1 as R multiple
    tp1_pct: float = 0.0               # % closed at TP1 (0 = single target)
    be_after_tp1: bool = True
    tgt_mode: str = "per_entry"        # per_entry | blended
    stop_buf_pct: float = 0.0
    e2_expiry: int = 50                # 0 = never
    trend_filter: str = "off"          # off | sma
    trend_len: int = 200

    def label(self) -> str:
        parts = []
        parts.append("Breakout" if self.use_entry1 else "")
        e2 = {"off": "", "midpoint": "Midpoint", "retest": "Retest", "retest_confirm": "Retest+Confirm"}[self.entry2_mode]
        parts.append(e2)
        name = " + ".join(x for x in parts if x) or "NONE"
        if self.trend_filter == "sma":
            name += f" | SMA{self.trend_len}"
        if not self.trade_shorts:
            name += " | longs only"
        if not self.trade_longs:
            name += " | shorts only"
        if self.tp1_pct > 0:
            return f"{name} | TP1 {self.tp1_rr:g}R ({self.tp1_pct:g}%) / TP2 {self.rr:g}R" + (" | BE" if self.be_after_tp1 else "")
        return f"{name} | {self.rr:g}:1"


# ───────────────────────────── Data ─────────────────────────────
def fetch_yahoo(symbol: str, interval: str = "1d", rng: str = "max", cache_dir: str | None = None) -> pd.DataFrame:
    cache = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        cache = os.path.join(cache_dir, f"{symbol.replace('=', '_')}_{interval}_{rng}.csv")
        if os.path.exists(cache):
            return pd.read_csv(cache, index_col=0, parse_dates=True)
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
    if rng == "max":   # "range=max" makes Yahoo silently downsample; ask for explicit dates instead
        params = {"period1": 0, "period2": int(time.time()), "interval": interval}
    else:
        params = {"range": rng, "interval": interval}
    r = None
    for attempt in range(4):
        r = requests.get(url, params={**params, "includePrePost": "false"},
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code == 200:
            break
        time.sleep(2 ** attempt)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({k: q[k] for k in ("open", "high", "low", "close")},
                      index=pd.to_datetime(res["timestamp"], unit="s"))
    df = df.dropna()
    df = df[(df[["open", "high", "low", "close"]] > 0).all(axis=1)]
    if cache:
        df.to_csv(cache)
    return df


# ───────────────────────────── Backtest ─────────────────────────────
@dataclass
class Trade:
    symbol: str
    direction: int          # 1 long, -1 short
    entry: int              # 0 = Entry 1, 1 = Entry 2
    signal_time: object
    exit_time: object
    entry_px: float
    exit_px: float
    stop_px: float
    r: float
    pct: float
    reason: str
    risk: float = float("nan")   # risk per unit used for R (planned risk for limit fills)
    target: float = float("nan")  # take-profit price (when the strategy records it)


@dataclass
class Result:
    trades: list[Trade] = field(default_factory=list)
    signals_long: int = 0
    signals_short: int = 0
    e2_fills: int = 0
    open_trade: str = "Flat"


def pivots(h: np.ndarray, l: np.ndarray, L: int):
    """Pine-style pivots, confirmed L bars after the pivot bar. Arrays are indexed by confirmation bar."""
    n = len(h)
    ph = np.full(n, np.nan)
    pl = np.full(n, np.nan)
    if n <= 2 * L:
        return ph, pl
    win = np.lib.stride_tricks.sliding_window_view
    hw, lw = win(h, 2 * L + 1), win(l, 2 * L + 1)     # row k covers bars k .. k+2L, centre k+L
    cen_h, cen_l = hw[:, L], lw[:, L]
    is_ph = (cen_h > hw[:, :L].max(axis=1)) & (cen_h >= hw[:, L + 1:].max(axis=1))
    is_pl = (cen_l < lw[:, :L].min(axis=1)) & (cen_l <= lw[:, L + 1:].min(axis=1))
    idx = np.arange(2 * L, n)
    ph[idx[is_ph]] = cen_h[is_ph]
    pl[idx[is_pl]] = cen_l[is_pl]
    return ph, pl


def backtest(df: pd.DataFrame, p: Params, symbol: str = "") -> Result:
    if not p.use_entry1 and p.entry2_mode == "off":
        raise ValueError("At least one entry must be enabled")
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    L = p.piv_len
    ph, pl = pivots(h, l, L)
    sma = pd.Series(c).rolling(p.trend_len).mean().to_numpy() if p.trend_filter == "sma" else None
    res = Result()
    use_e2 = p.entry2_mode != "off"
    confirm = p.entry2_mode == "retest_confirm"
    retest_like = p.entry2_mode in ("retest", "retest_confirm")

    last_ph = last_ph_bar = None
    last_pl = last_pl_bar = None
    dt = None  # pending double top
    db = None  # pending double bottom

    t_dir = 0
    tE1 = tE2 = tE2fill = tStop = tT2plan = math.nan
    e1_open = e2_open = e2_pend = False
    sig_bar = -1
    p1 = p.tp1_pct / 100.0
    # per-entry exit state: e = entry price, risk = risk unit (planned for limit fills), stop (moves to BE),
    # tp1 / tp2, done1 = TP1 taken, r / pct = running totals
    ent = [dict(), dict()]

    def tgt(direction, entry_px, stop_px, mult=None):
        return entry_px + direction * (p.rr if mult is None else mult) * abs(entry_px - stop_px)

    def new_ent(e, risk, stop, tp1, tp2):
        if (tp1 - tp2) * t_dir > 0:            # TP1 never beyond TP2
            tp1 = tp2
        return dict(e=e, risk=risk, stop=stop, tp1=tp1, tp2=tp2, done1=p1 <= 0, r=0.0, pct=0.0)

    def step(k, i, d, stop_only):
        """Advance entry k one bar (mirrors stepEntry in the Pine script). Returns True when it is fully closed."""
        en = ent[k]
        rem = 1.0 if (p1 <= 0 or not en["done1"]) else 1.0 - p1
        x_px, reason = None, ""
        if (l[i] <= en["stop"]) if d == 1 else (h[i] >= en["stop"]):
            x_px = min(o[i], en["stop"]) if d == 1 else max(o[i], en["stop"])
            reason = "BE" if (en["done1"] and p.be_after_tp1 and p1 > 0) else "SL"
        elif not stop_only:
            if not en["done1"] and ((h[i] >= en["tp1"]) if d == 1 else (l[i] <= en["tp1"])):
                px = max(o[i], en["tp1"]) if d == 1 else min(o[i], en["tp1"])
                en["r"] += p1 * d * (px - en["e"]) / en["risk"]
                en["pct"] += p1 * d * (px - en["e"]) / en["e"] * 100
                en["done1"] = True
                if p1 >= 1:
                    finish(k, i, d, px, "TP1")
                    return True
                if p.be_after_tp1:
                    en["stop"] = en["e"]          # remainder managed from the next bar
            elif en["done1"] and ((h[i] >= en["tp2"]) if d == 1 else (l[i] <= en["tp2"])):
                x_px = max(o[i], en["tp2"]) if d == 1 else min(o[i], en["tp2"])
                reason = "TP"
        if x_px is None:
            return False
        en["r"] += rem * d * (x_px - en["e"]) / en["risk"] if en["risk"] > 0 else 0.0
        en["pct"] += rem * d * (x_px - en["e"]) / en["e"] * 100
        finish(k, i, d, x_px, reason)
        return True

    def finish(k, i, d, x_px, reason):
        en = ent[k]
        res.trades.append(Trade(symbol, d, k, t[sig_bar], t[i], en["e"], x_px, tStop, en["r"], en["pct"], reason,
                                en["risk"], en["tp2"]))

    def trend_ok(direction, i):
        if sma is None:
            return True
        if math.isnan(sma[i]):
            return False
        return c[i] > sma[i] if direction == 1 else c[i] < sma[i]

    for i in range(n):
        # ── Double top detection
        if not math.isnan(ph[i]):
            b2, p2 = i - L, ph[i]
            if p.trade_shorts and last_ph is not None:
                sep = b2 - last_ph_bar
                diff = abs(p2 - last_ph) / last_ph * 100
                if p.min_sep <= sep <= p.max_sep and diff <= p.tol_pct:
                    top = max(p2, last_ph)
                    seg = slice(last_ph_bar + 1, b2)          # bars strictly between peaks
                    neck = l[seg].min()
                    hi_mid = h[seg].max()
                    stale = any(c[k] < neck or c[k] > top for k in range(b2 + 1, i))
                    if hi_mid <= top and (top - neck) / top * 100 >= p.min_depth and not stale:
                        dt = dict(top=top, neck=neck, set_bar=i)
            last_ph, last_ph_bar = p2, b2

        # ── Double bottom detection
        if not math.isnan(pl[i]):
            b2, p2 = i - L, pl[i]
            if p.trade_longs and last_pl is not None:
                sep = b2 - last_pl_bar
                diff = abs(p2 - last_pl) / last_pl * 100
                if p.min_sep <= sep <= p.max_sep and diff <= p.tol_pct:
                    bot = min(p2, last_pl)
                    seg = slice(last_pl_bar + 1, b2)
                    neck = h[seg].max()
                    lo_mid = l[seg].min()
                    stale = any(c[k] > neck or c[k] < bot for k in range(b2 + 1, i))
                    if lo_mid >= bot and (neck - bot) / bot * 100 >= p.min_depth and not stale:
                        db = dict(bot=bot, neck=neck, set_bar=i)
            last_pl, last_pl_bar = p2, b2

        # ── Pending invalidation
        if dt and (c[i] > dt["top"] or i - dt["set_bar"] > p.max_wait):
            dt = None
        if db and (c[i] < db["bot"] or i - db["set_bar"] > p.max_wait):
            db = None

        # ── Simulate open trade
        if t_dir != 0 and i > sig_bar:
            d = t_dir
            e2_just = False
            if e2_pend:
                touched = h[i] >= tE2 if d == -1 else l[i] <= tE2
                if confirm:
                    filled = touched and (c[i] < tE2 if d == -1 else c[i] > tE2)
                    fill_px = c[i]
                else:
                    filled = touched
                    fill_px = max(o[i], tE2) if d == -1 else min(o[i], tE2)
                # never fill beyond the stop (gap through the whole pattern)
                if filled and (fill_px < tStop if d == -1 else fill_px > tStop):
                    tE2fill = fill_px
                    # confirm entries are at a known close -> risk/targets from the fill; limit fills keep the plan
                    e2 = ent[1]
                    e2.update(e=fill_px, stop=tStop, done1=p1 <= 0, r=0.0, pct=0.0)
                    if confirm:
                        e2["risk"] = abs(fill_px - tStop)
                        if p.tgt_mode == "per_entry" or not p.use_entry1:
                            e2["tp1"] = tgt(d, fill_px, tStop, p.tp1_rr)
                            e2["tp2"] = tgt(d, fill_px, tStop)
                            if (e2["tp1"] - e2["tp2"]) * d > 0:
                                e2["tp1"] = e2["tp2"]
                    e2_pend, e2_open, e2_just = False, True, True
                    res.e2_fills += 1
            if e1_open and step(0, i, d, stop_only=False):
                e1_open = False
            # limit fills: only the stop can hit on the fill bar; confirm fills enter at the close -> nothing on that bar
            if e2_open and not (e2_just and confirm) and step(1, i, d, stop_only=e2_just):
                e2_open = False
            if e2_pend:
                cancel = p.use_entry1 and not e1_open                       # entry 1 finished
                cancel |= p.e2_expiry > 0 and i - sig_bar >= p.e2_expiry    # expired
                if retest_like:                                             # ran to target / stop without a retest
                    cancel |= (l[i] <= tT2plan) if d == -1 else (h[i] >= tT2plan)
                    cancel |= (h[i] >= tStop) if d == -1 else (l[i] <= tStop)
                if cancel:
                    e2_pend = False
            if not (e1_open or e2_open or e2_pend):
                t_dir = 0

        # ── New entries
        def open_trade(d, extreme, neck):
            nonlocal t_dir, tE1, tE2, tStop, tT2plan, e1_open, e2_open, e2_pend, sig_bar
            H = abs(extreme - neck)
            tStop = extreme - d * H * p.stop_buf_pct / 100
            tE1 = c[i]
            if p.entry2_mode == "midpoint":
                tE2 = neck - d * H / 2
            else:
                tE2 = neck
            if p.tgt_mode == "blended" and p.use_entry1 and use_e2:
                avg = (tE1 + tE2) / 2
                a1, a2 = tgt(d, avg, tStop, p.tp1_rr), tgt(d, avg, tStop)
                b1, b2 = a1, a2
            else:
                a1, a2 = tgt(d, tE1, tStop, p.tp1_rr), tgt(d, tE1, tStop)
                b1, b2 = tgt(d, tE2, tStop, p.tp1_rr), tgt(d, tE2, tStop)
            t_dir = d
            ent[0] = new_ent(tE1, abs(tE1 - tStop), tStop, a1, a2)
            ent[1] = new_ent(tE2, abs(tE2 - tStop), tStop, b1, b2)
            tT2plan = b2
            t_dir, sig_bar = d, i
            e1_open, e2_open, e2_pend = p.use_entry1, False, use_e2

        if dt and t_dir == 0 and c[i] < dt["neck"]:
            if trend_ok(-1, i):
                open_trade(-1, dt["top"], dt["neck"])
                res.signals_short += 1
            dt = db = None

        if db and t_dir == 0 and c[i] > db["neck"]:
            if trend_ok(1, i):
                open_trade(1, db["bot"], db["neck"])
                res.signals_long += 1
            db = dt = None

    if t_dir != 0:
        res.open_trade = f"{'LONG' if t_dir == 1 else 'SHORT'} since {t[sig_bar].date()}"
    return res


# ───────────────────────────── Reporting ─────────────────────────────
def stats(trades: list[Trade]) -> dict:
    if not trades:
        return dict(n=0, wins=0, losses=0, win_rate=float("nan"), net_r=0.0, avg_r=float("nan"),
                    pf=float("nan"), net_pct=0.0)
    r = np.array([x.r for x in trades])
    gw, gl = r[r > 0].sum(), -r[r <= 0].sum()
    return dict(n=len(r), wins=int((r > 0).sum()), losses=int((r <= 0).sum()),
                win_rate=(r > 0).mean() * 100, net_r=r.sum(), avg_r=r.mean(),
                pf=gw / gl if gl > 0 else float("inf"), net_pct=sum(x.pct for x in trades))


def max_dd_r(trades: list[Trade]) -> float:
    cum = np.cumsum([x.r for x in sorted(trades, key=lambda x: x.exit_time)])
    if len(cum) == 0:
        return 0.0
    peak = np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]
    return float((peak - cum).max())


def summarize(symbol: str, df: pd.DataFrame, res: Result) -> dict:
    tr = res.trades
    sig = res.signals_long + res.signals_short
    return dict(
        symbol=symbol, bars=len(df), start=str(df.index[0].date()), end=str(df.index[-1].date()),
        signals=sig, signals_long=res.signals_long, signals_short=res.signals_short,
        e2_fill_rate=res.e2_fills / sig * 100 if sig else float("nan"),
        e1=stats([x for x in tr if x.entry == 0]),
        e2=stats([x for x in tr if x.entry == 1]),
        total=stats(tr),
        long=stats([x for x in tr if x.direction == 1]),
        short=stats([x for x in tr if x.direction == -1]),
        max_dd_r=max_dd_r(tr), open_trade=res.open_trade,
    )


def _f(v, fmt="{:.2f}"):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "–"
    return "∞" if v == float("inf") else fmt.format(v)


def print_summary(s: dict) -> None:
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===")
    print(f"Signals: {s['signals']} (long {s['signals_long']} / short {s['signals_short']})   "
          f"Entry-2 fill rate: {_f(s['e2_fill_rate'], '{:.1f}%')}   Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
    print(f"{'':16}{'Entry 1':>12}{'Entry 2':>12}{'Total':>12}{'Longs':>12}{'Shorts':>12}")
    cols = [s["e1"], s["e2"], s["total"], s["long"], s["short"]]
    rows = [("Closed trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Net R", "net_r", "{:+.2f}"),
            ("Avg R/trade", "avg_r", "{:+.3f}"), ("Profit factor", "pf", "{:.2f}"), ("Net % (sum)", "net_pct", "{:+.1f}%")]
    for name, key, fmt in rows:
        print(f"{name:16}" + "".join(f"{_f(cl[key], fmt):>12}" for cl in cols))


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbols", nargs="+")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--rr", type=float, default=2.0, help="TP2 / final target as R multiple")
    ap.add_argument("--tp1", type=float, default=1.0, help="TP1 as R multiple")
    ap.add_argument("--tp1-pct", type=float, default=0.0, help="%% of each entry closed at TP1 (0 = single target)")
    ap.add_argument("--no-be", action="store_true", help="do not move the stop to breakeven after TP1")
    ap.add_argument("--blended", action="store_true", help="shared target off the average entry")
    ap.add_argument("--no-entry1", action="store_true", help="disable the breakout entry")
    ap.add_argument("--entry2", default="midpoint", choices=["off", "midpoint", "retest", "retest_confirm"])
    ap.add_argument("--trend", default="off", choices=["off", "sma"])
    ap.add_argument("--trend-len", type=int, default=200)
    ap.add_argument("--longs-only", action="store_true")
    ap.add_argument("--shorts-only", action="store_true")
    ap.add_argument("--cache", default=None)
    ap.add_argument("--json", default=None, help="write summaries to this JSON file")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    p = Params(rr=a.rr, tp1_rr=a.tp1, tp1_pct=a.tp1_pct, be_after_tp1=not a.no_be, tgt_mode="blended" if a.blended else "per_entry", use_entry1=not a.no_entry1,
               entry2_mode=a.entry2, trend_filter=a.trend, trend_len=a.trend_len,
               trade_longs=not a.shorts_only, trade_shorts=not a.longs_only)
    print(f"Config: {p.label()}")
    summaries = []
    for sym in a.symbols:
        try:
            df = fetch_yahoo(sym, a.interval, a.range, a.cache)
        except Exception as e:  # noqa: BLE001
            print(f"{sym}: data error {e}", file=sys.stderr)
            continue
        s = summarize(sym, df, backtest(df, p, sym))
        print_summary(s)
        summaries.append(s)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(summaries, fh, indent=2, default=str)


if __name__ == "__main__":
    main()
