"""
Grid test of the megaphone strategy over the daily universe, with a random-entry benchmark.

    python run_megaphone_experiments.py --cache /path/to/cache --out results/megaphone_daily.md
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

from dtdb_backtest import fetch_yahoo, max_dd_r, stats
from megaphone_backtest import MPParams, backtest
from run_experiments import UNIVERSE, fmt_table
from run_srflip_experiments import random_control

SETUPS = []
for entry in ("touch", "rejection"):
    for tgt, rr in (("rr", 1.0), ("rr", 2.0), ("rr", 3.0), ("midline", 2.0), ("opposite", 2.0)):
        name = f"Fade {entry} → " + (f"{rr:g}:1" if tgt == "rr" else tgt)
        SETUPS.append((name, dict(mode="fade", fade_entry=entry, target=tgt, rr=rr)))
for rr in (1.0, 2.0, 3.0):
    SETUPS.append((f"Breakout → {rr:g}:1", dict(mode="breakout", rr=rr)))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--out", default="results/megaphone_daily.md")
    a = ap.parse_args(argv)

    data = {}
    for sym in UNIVERSE:
        try:
            df = fetch_yahoo(sym, a.interval, a.range, a.cache)
            if len(df) > 300:
                data[sym] = df
        except Exception as e:  # noqa: BLE001
            print(f"skip {sym}: {e}", file=sys.stderr)

    rows = []
    for (name, kw) in SETUPS:
        for piv in (4, 5):
            for trend in ("off", "sma"):
                p = replace(MPParams(), min_pivots=piv, trend_filter=trend, **kw)
                trades, ctrl_l, ctrl_s, pats, sym_r = [], [], [], 0, []
                for sym, df in data.items():
                    res = backtest(df, p, sym)
                    trades += res.trades
                    pats += res.e2_fills
                    sym_r.append(sum(t.r for t in res.trades))
                    if trend == "off":
                        # random_control gives every random trade the same reward:risk as the trade it mirrors
                        cl = random_control(df, [t for t in res.trades if t.direction == 1], p.rr)
                        cs = random_control(df, [t for t in res.trades if t.direction == -1], p.rr)
                        ctrl_l += cl
                        ctrl_s += cs
                s = stats(trades)
                sl = stats([t for t in trades if t.direction == 1])
                ss = stats([t for t in trades if t.direction == -1])
                rows.append(dict(
                    setup=name, pivots=piv, trend="SMA200" if trend == "sma" else "off", patterns=pats,
                    trades=s["n"], win_rate=s["win_rate"], avg_r=s["avg_r"], net_r=s["net_r"], pf=s["pf"],
                    long_n=sl["n"], long_avg=sl["avg_r"], short_n=ss["n"], short_avg=ss["avg_r"],
                    ctrl_long=float(np.mean(ctrl_l)) if ctrl_l else math.nan,
                    ctrl_short=float(np.mean(ctrl_s)) if ctrl_s else math.nan,
                    pct_sym_profitable=np.mean([r > 0 for r in sym_r]) * 100, max_dd=max_dd_r(trades)))
                print(f"done {name} piv{piv} {trend}", file=sys.stderr)

    df_all = pd.DataFrame(rows)
    df_all["edge_long"] = df_all.long_avg - df_all.ctrl_long
    df_all["edge_short"] = df_all.short_avg - df_all.ctrl_short
    df_all.to_csv(a.out.replace(".md", ".csv"), index=False)
    cols = [("setup", "Setup", ""), ("pivots", "Swings", "{:.0f}"), ("trend", "Trend", ""), ("trades", "Trades", "{:.0f}"),
            ("win_rate", "Win %", "{:.1f}"), ("avg_r", "Avg R", "{:+.3f}"), ("net_r", "Net R", "{:+.1f}"), ("pf", "PF", "{:.2f}"),
            ("long_avg", "Long avg R", "{:+.3f}"), ("short_avg", "Short avg R", "{:+.3f}"),
            ("pct_sym_profitable", "% symbols +", "{:.0f}"), ("max_dd", "Max DD (R)", "{:.1f}")]
    ccols = [("setup", "Setup", ""), ("pivots", "Swings", "{:.0f}"), ("long_n", "Long trades", "{:.0f}"),
             ("long_avg", "Long avg R", "{:+.3f}"), ("ctrl_long", "Random long", "{:+.3f}"), ("edge_long", "Long edge", "{:+.3f}"),
             ("short_n", "Short trades", "{:.0f}"), ("short_avg", "Short avg R", "{:+.3f}"),
             ("ctrl_short", "Random short", "{:+.3f}"), ("edge_short", "Short edge", "{:+.3f}")]
    with open(a.out, "w") as fh:
        fh.write(f"# Megaphone experiments ({a.interval})\n\nUniverse: {len(data)} symbols — {', '.join(data)}\n\n")
        fh.write("No commissions/slippage. Stop and target touched in the same bar = loss. R = multiple of risk.\n"
                 "Random benchmark = same symbol, direction, stop distance and reward:risk as each real trade, random entry day.\n\n")
        fh.write("## Benchmark vs random entries (no trend filter)\n\n")
        fh.write(fmt_table(df_all[df_all.trend == "off"], ccols) + "\n\n")
        fh.write("## All configurations\n\n" + fmt_table(df_all, cols) + "\n")
    print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
