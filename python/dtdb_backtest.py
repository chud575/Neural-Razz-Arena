"""
Python port of pine/double_top_bottom_2entry.pine.

Same pattern detection, same two-stage entry plan, same conservative bar-by-bar
trade simulation, so the numbers should match the TradingView table for the same
data and settings.

Usage:
    python dtdb_backtest.py SPY BTC-USD --interval 1d --range max
"""
from __future__ import annotations

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
    piv_len: int = 5
    tol_pct: float = 0.5
    min_sep: int = 10
    max_sep: int = 100
    min_depth: float = 1.0
    max_wait: int = 30
    trade_longs: bool = True
    trade_shorts: bool = True
    rr: float = 2.0
    tgt_mode: str = "per_entry"        # or "blended"
    stop_buf_pct: float = 0.0
    e2_expiry: int = 50                # 0 = never


# ───────────────────────────── Data ─────────────────────────────
def fetch_yahoo(symbol: str, interval: str = "1d", rng: str = "max", cache_dir: str | None = None) -> pd.DataFrame:
    cache = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        cache = os.path.join(cache_dir, f"{symbol.replace('=', '_')}_{interval}_{rng}.csv")
        if os.path.exists(cache):
            return pd.read_csv(cache, index_col=0, parse_dates=True)
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
    for attempt in range(4):
        if rng == "max":   # "range=max" makes Yahoo silently downsample; ask for explicit dates instead
            params = {"period1": 0, "period2": int(time.time()), "interval": interval}
        else:
            params = {"range": rng, "interval": interval}
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
    if cache:
        df.to_csv(cache)
    return df


# ───────────────────────────── Backtest ─────────────────────────────
@dataclass
class Trade:
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


@dataclass
class Result:
    trades: list[Trade] = field(default_factory=list)
    signals_long: int = 0
    signals_short: int = 0
    e2_fills: int = 0
    open_trade: str = "Flat"


def pivots(h: np.ndarray, l: np.ndarray, L: int):
    """Pine-style pivots, confirmed L bars after the pivot bar. Returns arrays indexed by confirmation bar."""
    n = len(h)
    ph = np.full(n, np.nan)
    pl = np.full(n, np.nan)
    for i in range(2 * L, n):
        c = i - L
        left_h, right_h = h[c - L:c], h[c + 1:i + 1]
        if h[c] > left_h.max() and h[c] >= right_h.max():
            ph[i] = h[c]
        left_l, right_l = l[c - L:c], l[c + 1:i + 1]
        if l[c] < left_l.min() and l[c] <= right_l.min():
            pl[i] = l[c]
    return ph, pl


def backtest(df: pd.DataFrame, p: Params) -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    L = p.piv_len
    ph, pl = pivots(h, l, L)
    res = Result()

    last_ph = last_ph_bar = None
    last_pl = last_pl_bar = None
    dt = None  # pending double top: dict(top, neck, set_bar)
    db = None

    # trade state
    t_dir = 0
    tE1 = tE2 = tE2fill = tStop = tT1 = tT2 = math.nan
    e1_open = e2_open = e2_pend = False
    sig_bar = -1

    def record(direction, entry, entry_px, exit_px, stop_px, i, reason):
        risk = abs(entry_px - stop_px)
        r = direction * (exit_px - entry_px) / risk if risk > 0 else 0.0
        pct = direction * (exit_px - entry_px) / entry_px * 100.0
        res.trades.append(Trade(direction, entry, t[sig_bar], t[i], entry_px, exit_px, stop_px, r, pct, reason))

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
            e2_just = False
            if e2_pend and ((t_dir == -1 and h[i] >= tE2) or (t_dir == 1 and l[i] <= tE2)):
                tE2fill = max(o[i], tE2) if t_dir == -1 else min(o[i], tE2)
                e2_pend, e2_open, e2_just = False, True, True
                res.e2_fills += 1
            stop_hit = h[i] >= tStop if t_dir == -1 else l[i] <= tStop
            stop_px = max(o[i], tStop) if t_dir == -1 else min(o[i], tStop)
            if e1_open:
                tp = l[i] <= tT1 if t_dir == -1 else h[i] >= tT1
                if stop_hit:
                    record(t_dir, 0, tE1, stop_px, tStop, i, "SL"); e1_open = False
                elif tp:
                    px = min(o[i], tT1) if t_dir == -1 else max(o[i], tT1)
                    record(t_dir, 0, tE1, px, tStop, i, "TP"); e1_open = False
            if e2_open:
                tp = (not e2_just) and (l[i] <= tT2 if t_dir == -1 else h[i] >= tT2)
                if stop_hit:
                    record(t_dir, 1, tE2fill, stop_px, tStop, i, "SL"); e2_open = False
                elif tp:
                    px = min(o[i], tT2) if t_dir == -1 else max(o[i], tT2)
                    record(t_dir, 1, tE2fill, px, tStop, i, "TP"); e2_open = False
            if e2_pend and (not e1_open or (p.e2_expiry > 0 and i - sig_bar >= p.e2_expiry)):
                e2_pend = False
            if not (e1_open or e2_open or e2_pend):
                t_dir = 0

        # ── New entries
        if dt and t_dir == 0 and c[i] < dt["neck"]:
            H = dt["top"] - dt["neck"]
            tStop = dt["top"] + H * p.stop_buf_pct / 100
            tE1, tE2 = c[i], dt["neck"] + H / 2
            avg = (tE1 + tE2) / 2
            if p.tgt_mode == "per_entry":
                tT1 = tE1 - p.rr * (tStop - tE1)
                tT2 = tE2 - p.rr * (tStop - tE2)
            else:
                tT1 = tT2 = avg - p.rr * (tStop - avg)
            t_dir, e1_open, e2_open, e2_pend, sig_bar = -1, True, False, True, i
            res.signals_short += 1
            dt = db = None

        if db and t_dir == 0 and c[i] > db["neck"]:
            H = db["neck"] - db["bot"]
            tStop = db["bot"] - H * p.stop_buf_pct / 100
            tE1, tE2 = c[i], db["neck"] - H / 2
            avg = (tE1 + tE2) / 2
            if p.tgt_mode == "per_entry":
                tT1 = tE1 + p.rr * (tE1 - tStop)
                tT2 = tE2 + p.rr * (tE2 - tStop)
            else:
                tT1 = tT2 = avg + p.rr * (avg - tStop)
            t_dir, e1_open, e2_open, e2_pend, sig_bar = 1, True, False, True, i
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
    out = dict(
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
    return out


def print_summary(s: dict) -> None:
    def f(v, fmt="{:.2f}"):
        return "–" if v is None or (isinstance(v, float) and math.isnan(v)) else ("∞" if v == float("inf") else fmt.format(v))
    print(f"\n=== {s['symbol']}  ({s['start']} → {s['end']}, {s['bars']} bars) ===")
    print(f"Signals: {s['signals']} (long {s['signals_long']} / short {s['signals_short']})   "
          f"Entry-2 fill rate: {f(s['e2_fill_rate'], '{:.1f}%')}   Max DD: {s['max_dd_r']:.2f}R   Now: {s['open_trade']}")
    print(f"{'':16}{'Entry 1':>12}{'Entry 2':>12}{'Total':>12}{'Longs':>12}{'Shorts':>12}")
    cols = [s["e1"], s["e2"], s["total"], s["long"], s["short"]]
    rows = [("Closed trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Net R", "net_r", "{:+.2f}"),
            ("Avg R/trade", "avg_r", "{:+.3f}"), ("Profit factor", "pf", "{:.2f}"), ("Net % (sum)", "net_pct", "{:+.1f}%")]
    for name, key, fmt in rows:
        print(f"{name:16}" + "".join(f"{f(cl[key], fmt):>12}" for cl in cols))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("symbols", nargs="+")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--blended", action="store_true")
    ap.add_argument("--cache", default=None)
    ap.add_argument("--json", default=None, help="write summaries to this JSON file")
    a = ap.parse_args(argv)
    p = Params(rr=a.rr, tgt_mode="blended" if a.blended else "per_entry")
    summaries = []
    for sym in a.symbols:
        try:
            df = fetch_yahoo(sym, a.interval, a.range, a.cache)
        except Exception as e:  # noqa: BLE001
            print(f"{sym}: data error {e}", file=sys.stderr)
            continue
        s = summarize(sym, df, backtest(df, p))
        print_summary(s)
        summaries.append(s)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(summaries, fh, indent=2, default=str)


if __name__ == "__main__":
    main()
