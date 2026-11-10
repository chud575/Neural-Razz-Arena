"""
Accordion / Moving-Average Fan backtester (EMA 8, 13, 21, 34, 55). Mirrors pine/accordion_fan.pine.

Long setup (shorts are the mirror image):
  1. Fan:     EMA8 > EMA13 > EMA21 > EMA34 > EMA55 for at least `stacked_bars` bars in a row, and the gap
              EMA8 − EMA55 reaches at least `fan_min_atr` × ATR. The widest gap of the fan is remembered.
  2. Folding: the gap has shrunk to at most `fold_frac` × the widest gap (the fan "closes"), and the last
              fully-stacked bar was no more than `lookback` bars ago.
  3. Entry:   limit at the PREVIOUS bar's EMA55 (known at the open, no repainting); filled when price, coming
              from above (previous close above EMA55), trades down through it. Gaps fill at the open.
  4. Stop:    entry − `stop_atr` × ATR.  Target: `rr` × risk (2:1 default). TP1 / % at TP1 / breakeven via exits.py.
  5. One trade per fan: after a trade the setup needs a new fan.
Simulation: stop first when stop and target share a bar; the fill bar only checks the stop; one trade at a time.

    python accordion_backtest.py BTC --csv btc_1h.csv
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

__version__ = "1.0"  # same version as pine/accordion_fan.pine

LENS = (8, 13, 21, 34, 55)


def ema(x: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(x).ewm(span=n, adjust=False).mean().to_numpy()


@dataclass
class ACParams:
    fan_min_atr: float = 3.0
    stacked_bars: int = 10
    lookback: int = 100
    fold_frac: float = 0.5
    stop_atr: float = 1.0
    rr: float = 2.0
    atr_len: int = 14
    tp1_rr: float = 1.0
    tp1_pct: float = 0.0
    be_after_tp1: bool = True
    trade_longs: bool = True
    trade_shorts: bool = True

    def label(self) -> str:
        return (f"fan ≥{self.fan_min_atr:g} ATR for {self.stacked_bars} bars | fold ≤{self.fold_frac:g} of peak within "
                f"{self.lookback} bars | stop {self.stop_atr:g} ATR | {self.rr:g}:1")


def backtest(df: pd.DataFrame, p: ACParams, symbol: str = "") -> Result:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    t = df.index
    n = len(df)
    E = [ema(c, k) for k in LENS]
    e8, e55 = E[0], E[4]
    a = atr(h, l, c, p.atr_len)
    stacked = {1: np.all([E[j] > E[j + 1] for j in range(4)], axis=0),
               -1: np.all([E[j] < E[j + 1] for j in range(4)], axis=0)}
    p1 = p.tp1_pct / 100.0
    res = Result()
    in_tr = False
    tr: dict = {}
    # per-direction fan state
    st = {d: dict(run=0, armed=False, peak=0.0, last_stacked=-10 ** 9) for d in (1, -1)}

    def finish(i, x_px, reason):
        nonlocal in_tr
        en = tr["en"]
        res.trades.append(Trade(symbol, tr["d"], 0, t[tr["bar"]], t[i], tr["e"], x_px, tr["s"], en["r"], en["pct"],
                                reason, tr["risk"], tr["t"]))
        in_tr = False

    for i in range(1, n):
        # 1) fan state from the PREVIOUS bar (everything used for the entry decision is known at this bar's open)
        k = i - 1
        if not math.isnan(a[k]) and k >= 55:
            for d in (1, -1):
                s = st[d]
                gap = d * (e8[k] - e55[k]) / a[k]
                s["run"] = s["run"] + 1 if stacked[d][k] else 0
                if stacked[d][k]:
                    s["last_stacked"] = k
                if s["run"] >= p.stacked_bars and gap >= p.fan_min_atr:
                    if not s["armed"]:
                        s["armed"], s["peak"] = True, gap
                if s["armed"]:
                    if stacked[d][k]:
                        s["peak"] = max(s["peak"], gap)
                    if k - s["last_stacked"] > p.lookback:
                        s["armed"] = False
                s["gap"] = gap

        # 2) manage the open trade
        if in_tr and i > tr["bar"]:
            closed, x_px, reason, _ = scale_step(o, h, l, i, tr["d"], tr["en"], p1, p.be_after_tp1)
            if closed:
                finish(i, x_px, reason)
        if in_tr or math.isnan(a[k]):
            continue

        # 3) entry: folded fan + price crossing the previous bar's EMA55 from the trend side
        for d in (1, -1):
            s = st[d]
            if not s["armed"] or not (p.trade_longs if d == 1 else p.trade_shorts):
                continue
            folded = s.get("gap", 1e9) <= p.fold_frac * s["peak"]
            lvl = e55[k]
            from_side = c[k] > lvl if d == 1 else c[k] < lvl
            crossed = l[i] <= lvl if d == 1 else h[i] >= lvl
            if not (folded and from_side and crossed):
                continue
            A = a[k]
            e = min(o[i], lvl) if d == 1 else max(o[i], lvl)
            stop = lvl - d * p.stop_atr * A
            risk = abs(lvl - stop)                       # planned risk (limit price), so gap fills can't shrink it
            if (e - stop) * d <= 0:
                s["armed"] = False
                continue
            tgt = lvl + d * p.rr * risk
            tr = dict(d=d, e=e, s=stop, t=tgt, risk=risk, bar=i,
                      en=make_entry(e, risk, stop, lvl + d * p.tp1_rr * risk, tgt, d, p1))
            in_tr = True
            s["armed"] = False                           # one trade per fan
            if d == 1:
                res.signals_long += 1
            else:
                res.signals_short += 1
            if (l[i] <= stop) if d == 1 else (h[i] >= stop):        # filled, then stopped in the same bar
                en = tr["en"]
                en["r"] = d * (stop - e) / risk
                en["pct"] = d * (stop - e) / e * 100
                finish(i, stop, "SL")
            break

    if in_tr:
        res.open_trade = f"{'LONG' if tr['d'] == 1 else 'SHORT'} since {t[tr['bar']]}"
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--fan", type=float, default=3.0)
    ap.add_argument("--stacked", type=int, default=10)
    ap.add_argument("--lookback", type=int, default=100)
    ap.add_argument("--fold", type=float, default=0.5)
    ap.add_argument("--stop-atr", type=float, default=1.0)
    ap.add_argument("--rr", type=float, default=2.0)
    a = ap.parse_args(argv)
    p = ACParams(fan_min_atr=a.fan, stacked_bars=a.stacked, lookback=a.lookback, fold_frac=a.fold,
                 stop_atr=a.stop_atr, rr=a.rr)
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
