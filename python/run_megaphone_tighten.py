"""
Test the megaphone "tightening" toggles one at a time and in combination (daily, 34 symbols, random benchmark).

    python run_megaphone_tighten.py --cache /path/to/cache --out results/megaphone_tighten.md
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

BO = dict(mode="breakout", bo_entry="close", bo_target="rr", rr=3.0)
TESTS = [
    ("Baseline: breakout at close, 3:1", BO),
    ("#1  6 swings", {**BO, "min_pivots": 6}),
    ("#2  min expansion 0.5 ATR", {**BO, "min_expand_atr": 0.5}),
    ("#2  min expansion 1.0 ATR", {**BO, "min_expand_atr": 1.0}),
    ("#3  swings on lines (fit 1.0 ATR)", {**BO, "fit_atr": 1.0}),
    ("#3  swings on lines (fit 2.0 ATR)", {**BO, "fit_atr": 2.0}),
    ("#4  breakout + retest, 3:1", {**BO, "bo_entry": "retest"}),
    ("#6  breakout at close, measured move", {**BO, "bo_target": "measured"}),
    ("#4+#6  retest, measured move", {**BO, "bo_entry": "retest", "bo_target": "measured"}),
    ("#5  failed-breakout fade → 2:1", dict(mode="none", failed_bo=True, target="rr", rr=2.0)),
    ("#5  failed-breakout fade → midline", dict(mode="none", failed_bo=True, target="midline", rr=2.0)),
    ("#5  failed-breakout fade → opposite line", dict(mode="none", failed_bo=True, target="opposite", rr=2.0)),
    ("Combo: expand 0.5 + fit 2.0 + breakout close 3:1", {**BO, "min_expand_atr": 0.5, "fit_atr": 2.0}),
    ("Combo: expand 0.5 + fit 2.0 + retest + measured", {**BO, "min_expand_atr": 0.5, "fit_atr": 2.0,
                                                          "bo_entry": "retest", "bo_target": "measured"}),
    ("Combo: expand 0.5 + breakout close 3:1 + SMA200", {**BO, "min_expand_atr": 0.5, "trend_filter": "sma"}),
]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--out", default="results/megaphone_tighten.md")
    a = ap.parse_args(argv)
    data = {}
    for sym in UNIVERSE:
        try:
            df = fetch_yahoo(sym, "1d", "max", a.cache)
            if len(df) > 300:
                data[sym] = df
        except Exception as e:  # noqa: BLE001
            print(f"skip {sym}: {e}", file=sys.stderr)

    rows = []
    for name, kw in TESTS:
        for piv in ((4, 5) if "min_pivots" not in kw else (kw["min_pivots"],)):
            p = replace(MPParams(), **{**kw, "min_pivots": piv})
            trades, ctrl, pats, sym_r = [], [], 0, []
            for sym, df in data.items():
                res = backtest(df, p, sym)
                trades += res.trades
                pats += res.e2_fills
                sym_r.append(sum(t.r for t in res.trades))
                ctrl += random_control(df, res.trades, p.rr, reps=5)
            s = stats(trades)
            sl = stats([t for t in trades if t.direction == 1])
            ss = stats([t for t in trades if t.direction == -1])
            c = float(np.mean(ctrl)) if ctrl else math.nan
            rows.append(dict(test=name, swings=piv, patterns=pats, trades=s["n"], win_rate=s["win_rate"], avg_r=s["avg_r"],
                             ctrl=c, edge=s["avg_r"] - c if s["n"] else math.nan, net_r=s["net_r"], pf=s["pf"],
                             long_avg=sl["avg_r"], short_avg=ss["avg_r"],
                             pct_sym=np.mean([r > 0 for r in sym_r]) * 100, max_dd=max_dd_r(trades)))
            print(f"done {name} {piv}", file=sys.stderr)
    df = pd.DataFrame(rows)
    df.to_csv(a.out.replace(".md", ".csv"), index=False)
    cols = [("test", "Test", ""), ("swings", "Swings", "{:.0f}"), ("patterns", "Megaphones", "{:.0f}"),
            ("trades", "Trades", "{:.0f}"), ("win_rate", "Win %", "{:.1f}"), ("avg_r", "Avg R", "{:+.3f}"),
            ("ctrl", "Random avg R", "{:+.3f}"), ("edge", "Edge", "{:+.3f}"), ("pf", "PF", "{:.2f}"),
            ("long_avg", "Long avg R", "{:+.3f}"), ("short_avg", "Short avg R", "{:+.3f}"),
            ("pct_sym", "% symbols +", "{:.0f}"), ("max_dd", "Max DD (R)", "{:.1f}")]
    with open(a.out, "w") as fh:
        fh.write("# Megaphone tightening toggles (daily, 34 symbols)\n\nNo costs. Random benchmark = same symbols, "
                 "direction, stop distance and reward:risk, random entry day.\n\n" + fmt_table(df, cols) + "\n")
    print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
