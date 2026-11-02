"""
Grid test of the S/R flip strategy over the daily universe, plus a random-entry benchmark.

    python run_srflip_experiments.py --cache /path/to/cache --out results/srflip_daily.md
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

from dtdb_backtest import fetch_yahoo, max_dd_r, stats
from run_experiments import UNIVERSE, fmt_table
from srflip_backtest import SRParams, backtest

MODES = ["touch", "rejection", "sweep"]
RRS = [1.0, 2.0, 3.0]
TRIES = [1, 3]
TRENDS = ["off", "sma"]
DIRS = [("Both", {}), ("Longs only", dict(trade_shorts=False)), ("Shorts only", dict(trade_longs=False))]

rng = np.random.default_rng(0)


def random_control(df, trades, rr, reps=5):
    """Random entries on the same symbol: same direction, same stop distance (%), same R:R, same conservative rules."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    out = []
    for t in trades:
        dist = abs(t.entry_px - t.stop_px) / t.entry_px
        if dist <= 0:
            continue
        for _ in range(reps):
            i = int(rng.integers(200, n - 2))
            e, d = c[i], t.direction
            stop = e * (1 - d * dist)
            tgt = e + d * rr * abs(e - stop)
            for j in range(i + 1, n):
                if (l[j] <= stop) if d == 1 else (h[j] >= stop):
                    px = min(o[j], stop) if d == 1 else max(o[j], stop)
                    out.append(d * (px - e) / abs(e - stop)); break
                if (h[j] >= tgt) if d == 1 else (l[j] <= tgt):
                    px = max(o[j], tgt) if d == 1 else min(o[j], tgt)
                    out.append(d * (px - e) / abs(e - stop)); break
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--out", default="results/srflip_daily.md")
    ap.add_argument("--csv", default=None)
    a = ap.parse_args(argv)

    data = {}
    for sym in UNIVERSE:
        try:
            df = fetch_yahoo(sym, a.interval, a.range, a.cache)
            if len(df) > 300:
                data[sym] = df
        except Exception as e:  # noqa: BLE001
            print(f"skip {sym}: {e}", file=sys.stderr)

    rows, try_rows, ctrl_rows = [], [], []
    for mode, rr, tries, trend, (dname, dkw) in itertools.product(MODES, RRS, TRIES, TRENDS, DIRS):
        p = replace(SRParams(), entry_mode=mode, rr=rr, max_tries=tries, trend_filter=trend, **dkw)
        trades, sym_r, brk = [], [], 0
        per_sym = {}
        for sym, df in data.items():
            res = backtest(df, p, sym)
            trades += res.trades
            per_sym[sym] = res.trades
            brk += res.signals_long + res.signals_short
            sym_r.append(sum(t.r for t in res.trades))
        s = stats(trades)
        levels = {(t.symbol, t.signal_time) for t in trades}
        won = {(t.symbol, t.signal_time) for t in trades if t.r > 0}
        row = dict(mode=mode, rr=rr, tries=tries, trend="SMA200" if trend == "sma" else "off", direction=dname,
                   breakouts=brk, levels=len(levels), level_win=len(won) / len(levels) * 100 if levels else math.nan,
                   trades=s["n"], win_rate=s["win_rate"], breakeven_wr=100 / (1 + rr), avg_r=s["avg_r"],
                   net_r=s["net_r"], pf=s["pf"], pct_sym_profitable=np.mean([r > 0 for r in sym_r]) * 100,
                   max_dd=max_dd_r(trades))
        rows.append(row)
        if tries == 3 and trend == "off" and dname == "Both":
            for k, name in enumerate(["Try 1", "Try 2", "Try 3"]):
                st = stats([t for t in trades if t.entry == k])
                try_rows.append(dict(mode=mode, rr=rr, attempt=name, trades=st["n"], win_rate=st["win_rate"],
                                     avg_r=st["avg_r"], net_r=st["net_r"]))
        if tries == 3 and trend == "off" and dname != "Both":
            ctrl = []
            for sym, tr in per_sym.items():
                ctrl += random_control(data[sym], tr, rr)
            ctrl_rows.append(dict(mode=mode, rr=rr, direction=dname, trades=s["n"], avg_r=s["avg_r"],
                                  ctrl_avg_r=float(np.mean(ctrl)) if ctrl else math.nan,
                                  edge=s["avg_r"] - (float(np.mean(ctrl)) if ctrl else math.nan)))
        print(f"done {p.label()}", file=sys.stderr)

    df_all = pd.DataFrame(rows)
    if a.csv:
        df_all.to_csv(a.csv, index=False)
    cols = [("mode", "Entry", ""), ("rr", "R:R", "{:g}:1"), ("tries", "Max tries", "{:.0f}"), ("trend", "Trend", ""),
            ("direction", "Direction", ""), ("breakouts", "Breakouts", "{:.0f}"), ("level_win", "Levels that paid %", "{:.0f}"),
            ("trades", "Trades", "{:.0f}"), ("win_rate", "Win %", "{:.1f}"), ("breakeven_wr", "B/E win %", "{:.1f}"),
            ("avg_r", "Avg R", "{:+.3f}"), ("net_r", "Net R", "{:+.1f}"), ("pf", "PF", "{:.2f}"),
            ("pct_sym_profitable", "% symbols +", "{:.0f}"), ("max_dd", "Max DD (R)", "{:.1f}")]
    with open(a.out, "w") as fh:
        fh.write(f"# S/R flip experiments ({a.interval})\n\nUniverse: {len(data)} symbols — {', '.join(data)}\n\n")
        fh.write("No commissions/slippage. Stop and target touched in the same bar = loss. R = multiple of risk.\n\n")
        fh.write("## Benchmark vs random entries (max tries 3, no trend filter)\n\n")
        fh.write(fmt_table(pd.DataFrame(ctrl_rows), [("mode", "Entry", ""), ("rr", "R:R", "{:g}:1"), ("direction", "Direction", ""),
                 ("trades", "Trades", "{:.0f}"), ("avg_r", "Strategy avg R", "{:+.3f}"),
                 ("ctrl_avg_r", "Random avg R", "{:+.3f}"), ("edge", "Edge", "{:+.3f}")]) + "\n\n")
        fh.write("## Results by attempt (max tries 3, no trend filter, both directions)\n\n")
        fh.write(fmt_table(pd.DataFrame(try_rows), [("mode", "Entry", ""), ("rr", "R:R", "{:g}:1"), ("attempt", "Attempt", ""),
                 ("trades", "Trades", "{:.0f}"), ("win_rate", "Win %", "{:.1f}"), ("avg_r", "Avg R", "{:+.3f}"),
                 ("net_r", "Net R", "{:+.1f}")]) + "\n\n")
        fh.write("## All configurations\n\n" + fmt_table(df_all, cols) + "\n")
    pd.DataFrame(ctrl_rows).to_csv(a.out.replace(".md", "_control.csv"), index=False)
    pd.DataFrame(try_rows).to_csv(a.out.replace(".md", "_tries.csv"), index=False)
    print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
