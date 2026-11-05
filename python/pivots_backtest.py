"""
Pivot-point strategy backtester. Mirrors pine/pivot_points.pine.

Levels
  From the previous COMPLETED pivot period (D / W / M, or the chart's own timeframe) high H, low L, close C:
    Traditional  P=(H+L+C)/3  R1=2P-L  S1=2P-H  R2=P+(H-L)  S2=P-(H-L)  R3=H+2(P-L)  S3=L-2(H-P)
    Fibonacci    P            R1/S1=P±0.382(H-L)  R2/S2=P±0.618(H-L)  R3/S3=P±(H-L)
    Camarilla    P            R1..R4 / S1..S4 = C ± 1.1(H-L)/12, /6, /4, /2
    Woodie       P=(H+L+2C)/4 then as Traditional
Trades (one per level per period)
  bounce   price comes to a support (S level) from above and holds -> long; resistance (R level) from below -> short
             entry "touch"     limit at the level (same-bar stop check)
             entry "rejection" bar trades through the level and CLOSES back on the bounce side -> enter at close
  breakout previous close on one side, bar CLOSES beyond the level by brk_atr x ATR -> trade the breakout
  stop     level -/+ stop_atr x ATR (ATR of the previous bar)
  target   "next": next pivot level in the trade direction (S1 -> P, S2 -> S1, R1 -> R2 for a breakout ...)
           "rr":   rr x risk.  TP1 / % at TP1 / breakeven via exits.py.
  exit_eop close any open trade at the first bar of the next pivot period (optional)

    python pivots_backtest.py BTC --csv btc_1h.csv --pivot-tf D --type traditional --mode bounce --level 1
"""
from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from dtdb_backtest import Result, Trade, _f, max_dd_r, stats
from exits import make_entry, scale_step
from srflip_backtest import atr

__version__ = "1.0"  # same version as pine/pivot_points.pine

PERIOD = {"D": "D", "W": "W-SUN", "M": "M"}   # weeks Mon–Sun (UTC), like TradingView's crypto weeks


@dataclass
class PVParams:
    pivot_tf: str = "D"            # D | W | M | chart (levels from the previous chart bar)
    pivot_type: str = "traditional"  # traditional | fibonacci | camarilla | woodie
    mode: str = "bounce"           # bounce | breakout | both
    entry: str = "rejection"       # bounce entry: touch | rejection
    levels: tuple = (1,)           # which level numbers to trade (1 = S1/R1, 2 = S2/R2, 3 = S3/R3, 4 = Camarilla S4/R4)
    atr_len: int = 14
    stop_atr: float = 0.5
    brk_atr: float = 0.1
    target: str = "next"           # next | rr
    rr: float = 2.0
    exit_eop: bool = False
    tp1_rr: float = 1.0
    tp1_pct: float = 0.0
    be_after_tp1: bool = True
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        return (f"{self.pivot_type} {self.pivot_tf} | {self.mode}" + (f"-{self.entry}" if self.mode != "breakout" else "")
                + f" | levels {','.join(map(str, self.levels))} | stop {self.stop_atr:g}ATR | target "
                + (self.target if self.target == "next" else f"{self.rr:g}R") + (" | exit at period end" if self.exit_eop else ""))


def pivot_levels(H, L, C, kind: str):
    """Returns dict of arrays: P, R1..R4, S1..S4 (R4/S4 only for camarilla, else NaN)."""
    R = H - L
    nan = np.full_like(H, np.nan)
    if kind == "woodie":
        P = (H + L + 2 * C) / 4
    else:
        P = (H + L + C) / 3
    if kind in ("traditional", "woodie"):
        lv = dict(R1=2 * P - L, S1=2 * P - H, R2=P + R, S2=P - R, R3=H + 2 * (P - L), S3=L - 2 * (H - P), R4=nan, S4=nan)
    elif kind == "fibonacci":
        lv = dict(R1=P + 0.382 * R, S1=P - 0.382 * R, R2=P + 0.618 * R, S2=P - 0.618 * R, R3=P + R, S3=P - R, R4=nan, S4=nan)
    elif kind == "camarilla":
        k = 1.1 * R
        lv = dict(R1=C + k / 12, S1=C - k / 12, R2=C + k / 6, S2=C - k / 6, R3=C + k / 4, S3=C - k / 4, R4=C + k / 2, S4=C - k / 2)
    else:
        raise ValueError(kind)
    lv["P"] = P
    return lv


def prior_period_hlc(df: pd.DataFrame, pivot_tf: str):
    """Per bar: previous completed period's H, L, C and a 'first bar of a new period' flag."""
    if pivot_tf == "chart":
        H, L, C = (df[k].shift(1).to_numpy(float) for k in ("high", "low", "close"))
        newp = np.ones(len(df), bool)
        return H, L, C, newp
    per = df.index.to_period(PERIOD[pivot_tf])
    g = df.groupby(per).agg(high=("high", "max"), low=("low", "min"), close=("close", "last"))
    prev = g.shift(1)
    H = prev["high"].reindex(per).to_numpy(float)
    L = prev["low"].reindex(per).to_numpy(float)
    C = prev["close"].reindex(per).to_numpy(float)
    pv = np.asarray(per.asi8)
    newp = np.concatenate([[True], pv[1:] != pv[:-1]])
    return H, L, C, newp


def backtest(df: pd.DataFrame, p: PVParams, symbol: str = "") -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    a = atr(h, l, c, p.atr_len)
    H, L, C, newp = prior_period_hlc(df, p.pivot_tf)
    lv = pivot_levels(H, L, C, p.pivot_type)
    top = 4 if p.pivot_type == "camarilla" else 3
    # ordered ladder S_top .. S1, P, R1 .. R_top for "next level" targets
    ladder_names = [f"S{k}" for k in range(top, 0, -1)] + ["P"] + [f"R{k}" for k in range(1, top + 1)]
    ladder = np.vstack([lv[nm] for nm in ladder_names])          # rows = levels low -> high
    idx = {nm: j for j, nm in enumerate(ladder_names)}
    p1 = p.tp1_pct / 100.0
    res = Result()
    do_bounce = p.mode in ("bounce", "both")
    do_brk = p.mode in ("breakout", "both")

    in_tr = False
    tr: dict = {}
    used: set = set()

    def finish(i, x_px, reason):
        nonlocal in_tr
        en = tr["en"]
        res.trades.append(Trade(symbol, tr["d"], tr["lvl"], t[tr["bar"]], t[i], tr["e"], x_px, tr["s"], en["r"],
                                en["pct"], reason, tr["risk"], tr["t"]))
        in_tr = False

    def open_trade(i, d, e, stop, tgt, lvl_no, limit):
        nonlocal in_tr, tr
        risk = abs(e - stop) if not limit else abs(limit - stop)
        ref = limit if limit else e
        if risk <= 0 or (e - stop) * d <= 0 or (tgt - ref) * d <= 0:
            return False
        tr = dict(d=d, e=e, s=stop, t=tgt, risk=risk, bar=i, lvl=lvl_no,
                  en=make_entry(e, risk, stop, ref + d * p.tp1_rr * risk, tgt, d, p1))
        in_tr = True
        if d == 1:
            res.signals_long += 1
        else:
            res.signals_short += 1
        if limit and ((l[i] <= stop) if d == 1 else (h[i] >= stop)):     # limit filled, stopped in the same bar
            en = tr["en"]
            en["r"] = d * (stop - e) / risk
            en["pct"] = d * (stop - e) / e * 100
            finish(i, stop, "SL")
        return True

    for i in range(1, n):
        if newp[i]:
            used = set()
            if in_tr and p.exit_eop and p.pivot_tf != "chart":
                d = tr["d"]
                en = tr["en"]
                rem = 1.0 if (p1 <= 0 or not en["done1"]) else 1.0 - p1
                en["r"] += rem * d * (o[i] - en["e"]) / tr["risk"]
                en["pct"] += rem * d * (o[i] - en["e"]) / en["e"] * 100
                finish(i, o[i], "EOP")
        if in_tr and i > tr["bar"]:
            closed, x_px, reason, _ = scale_step(o, h, l, i, tr["d"], tr["en"], p1, p.be_after_tp1)
            if closed:
                finish(i, x_px, reason)
        if in_tr or math.isnan(a[i - 1]) or math.isnan(lv["P"][i]):
            continue
        A = a[i - 1]
        col = ladder[:, i]

        def nxt(name, d):
            j = idx[name] + d
            return col[j] if 0 <= j < len(col) and not math.isnan(col[j]) else math.nan

        done = False
        for k in p.levels:
            if k > top or done:
                continue
            for d, name in ((1, f"S{k}"), (-1, f"R{k}")):         # bounce: long at S, short at R
                if done or not do_bounce or (name, "b") in used or not (p.trade_longs if d == 1 else p.trade_shorts):
                    continue
                lvl = col[idx[name]]
                if not (c[i - 1] > lvl if d == 1 else c[i - 1] < lvl):    # must approach from the bounce side
                    continue
                if not ((l[i] <= lvl) if d == 1 else (h[i] >= lvl)):
                    continue
                stop = lvl - d * p.stop_atr * A
                if p.entry == "touch":
                    e, limit = (min(o[i], lvl) if d == 1 else max(o[i], lvl)), lvl
                else:
                    if not (c[i] > lvl if d == 1 else c[i] < lvl):
                        continue
                    e, limit = c[i], None
                ref = limit if limit else e
                tgt = nxt(name, d) if p.target == "next" else ref + d * p.rr * abs(ref - stop)
                if math.isnan(tgt):
                    tgt = ref + d * p.rr * abs(ref - stop)
                used.add((name, "b"))
                done = open_trade(i, d, e, stop, tgt, k, limit)
            for d, name in ((1, f"R{k}"), (-1, f"S{k}")):         # breakout: long through R, short through S
                if done or not do_brk or (name, "x") in used or not (p.trade_longs if d == 1 else p.trade_shorts):
                    continue
                lvl = col[idx[name]]
                if not ((c[i - 1] <= lvl and c[i] > lvl + p.brk_atr * A) if d == 1 else (c[i - 1] >= lvl and c[i] < lvl - p.brk_atr * A)):
                    continue
                stop = lvl - d * p.stop_atr * A
                e = c[i]
                tgt = nxt(name, d) if p.target == "next" else e + d * p.rr * abs(e - stop)
                if math.isnan(tgt) or (tgt - e) * d <= 0:
                    tgt = e + d * p.rr * abs(e - stop)
                used.add((name, "x"))
                done = open_trade(i, d, e, stop, tgt, k, None)

    if in_tr:
        res.open_trade = f"{'LONG' if tr['d'] == 1 else 'SHORT'} since {t[tr['bar']]}"
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--pivot-tf", default="D", choices=["D", "W", "M", "chart"])
    ap.add_argument("--type", default="traditional", choices=["traditional", "fibonacci", "camarilla", "woodie"])
    ap.add_argument("--mode", default="bounce", choices=["bounce", "breakout", "both"])
    ap.add_argument("--entry", default="rejection", choices=["touch", "rejection"])
    ap.add_argument("--levels", default="1")
    ap.add_argument("--target", default="next", choices=["next", "rr"])
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--stop-atr", type=float, default=0.5)
    ap.add_argument("--exit-eop", action="store_true")
    a = ap.parse_args(argv)
    p = PVParams(pivot_tf=a.pivot_tf, pivot_type=a.type, mode=a.mode, entry=a.entry,
                 levels=tuple(int(x) for x in a.levels.split(",")), target=a.target, rr=a.rr, stop_atr=a.stop_atr,
                 exit_eop=a.exit_eop)
    df = pd.read_csv(a.csv, index_col=0, parse_dates=True)
    r = backtest(df, p, a.symbol)
    tr = r.trades
    print("Config:", p.label())
    print(f"{'':14}{'Total':>10}{'Longs':>10}{'Shorts':>10}")
    for name, key, fmt in [("Trades", "n", "{:.0f}"), ("Win rate", "win_rate", "{:.1f}%"), ("Avg R (gross)", "avg_r", "{:+.3f}"),
                           ("Profit factor", "pf", "{:.2f}")]:
        cols = [stats(tr), stats([x for x in tr if x.direction == 1]), stats([x for x in tr if x.direction == -1])]
        print(f"{name:14}" + "".join(f"{_f(x[key], fmt):>10}" for x in cols))
    print(f"Max DD {max_dd_r(tr):.1f}R   Now: {r.open_trade}")


if __name__ == "__main__":
    main()
