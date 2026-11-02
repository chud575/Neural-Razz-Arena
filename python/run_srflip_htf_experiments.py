"""
Does using higher-timeframe and/or "major" (multi-swing) levels improve the S/R flip strategy?

    python run_srflip_htf_experiments.py --cache /path/to/cache --out results/srflip_htf.md
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

from dtdb_backtest import fetch_yahoo, stats
from run_experiments import UNIVERSE, fmt_table
from run_srflip_experiments import random_control
from srflip_backtest import SRParams, backtest

LEVELS = {
    "1d": [
        ("Chart (daily) levels — baseline", dict(level_src="chart")),
        ("Daily levels, merged 0.5%, ≥2 swings", dict(level_src="chart", merge_pct=0.5, min_touches=2)),
        ("Weekly levels", dict(level_src="htf", htf="W")),
        ("Weekly levels, merged 0.5%, ≥2 swings", dict(level_src="htf", htf="W", merge_pct=0.5, min_touches=2)),
        ("Daily + weekly, merged 0.5%, ≥2 swings", dict(level_src="both", htf="W", merge_pct=0.5, min_touches=2)),
        ("Monthly levels", dict(level_src="htf", htf="ME", htf_max_age=60)),
        ("Monthly levels, merged 1%, ≥2 swings", dict(level_src="htf", htf="ME", htf_max_age=60, merge_pct=1.0, min_touches=2)),
    ],
    "1h": [
        ("Chart (hourly) levels — baseline", dict(level_src="chart")),
        ("Hourly levels, merged 0.3%, ≥2 swings", dict(level_src="chart", merge_pct=0.3, min_touches=2)),
        ("Daily levels", dict(level_src="htf", htf="D", htf_max_age=120)),
        ("Daily levels, merged 0.5%, ≥2 swings", dict(level_src="htf", htf="D", htf_max_age=120, merge_pct=0.5, min_touches=2)),
        ("Hourly + daily, merged 0.5%, ≥2 swings", dict(level_src="both", htf="D", htf_max_age=120, merge_pct=0.5, min_touches=2)),
        ("Weekly levels", dict(level_src="htf", htf="W", htf_max_age=52)),
    ],
}
ENTRIES = [("touch", 2.0), ("touch", 3.0), ("rejection", 2.0), ("rejection", 3.0)]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--out", default="results/srflip_htf.md")
    ap.add_argument("--intervals", default="1d,1h")
    a = ap.parse_args(argv)

    rows = []
    for interval in a.intervals.split(","):
        rng = "max" if interval == "1d" else "730d"
        data = {}
        for sym in UNIVERSE:
            try:
                df = fetch_yahoo(sym, interval, rng, a.cache)
                if len(df) > 500:
                    data[sym] = df
            except Exception as e:  # noqa: BLE001
                print(f"skip {sym} {interval}: {e}", file=sys.stderr)
        print(f"{interval}: {len(data)} symbols", file=sys.stderr)
        for (lname, lkw), (mode, rr) in itertools.product(LEVELS[interval], ENTRIES):
            p = replace(SRParams(), entry_mode=mode, rr=rr, max_tries=3, **lkw)
            trades, ctrl_l, ctrl_s, brk = [], [], [], 0
            for sym, df in data.items():
                res = backtest(df, p, sym)
                trades += res.trades
                brk += res.signals_long + res.signals_short
                ctrl_l += random_control(df, [t for t in res.trades if t.direction == 1], rr, reps=3)
                ctrl_s += random_control(df, [t for t in res.trades if t.direction == -1], rr, reps=3)
            s = stats(trades)
            sl = stats([t for t in trades if t.direction == 1])
            ss = stats([t for t in trades if t.direction == -1])
            cl = float(np.mean(ctrl_l)) if ctrl_l else math.nan
            cs = float(np.mean(ctrl_s)) if ctrl_s else math.nan
            nl, ns = sl["n"], ss["n"]
            blended_ctrl = (cl * nl + cs * ns) / (nl + ns) if nl + ns else math.nan
            rows.append(dict(chart=interval, levels=lname, entry=mode, rr=rr, breakouts=brk, trades=s["n"],
                             win_rate=s["win_rate"], avg_r=s["avg_r"], ctrl=blended_ctrl, edge=s["avg_r"] - blended_ctrl,
                             long_avg=sl["avg_r"], long_edge=sl["avg_r"] - cl, short_avg=ss["avg_r"], short_edge=ss["avg_r"] - cs))
            print(f"done {interval} {lname} {mode} {rr}", file=sys.stderr)

    df = pd.DataFrame(rows)
    df.to_csv(a.out.replace(".md", ".csv"), index=False)
    cols = [("levels", "Levels", ""), ("entry", "Entry", ""), ("rr", "R:R", "{:g}:1"), ("breakouts", "Breakouts", "{:.0f}"),
            ("trades", "Trades", "{:.0f}"), ("win_rate", "Win %", "{:.1f}"), ("avg_r", "Avg R", "{:+.3f}"),
            ("ctrl", "Random avg R", "{:+.3f}"), ("edge", "Edge vs random", "{:+.3f}"),
            ("long_edge", "Long edge", "{:+.3f}"), ("short_edge", "Short edge", "{:+.3f}")]
    with open(a.out, "w") as fh:
        fh.write("# S/R flip — higher-timeframe and major-level tests\n\n")
        fh.write("34-symbol universe. Max 3 tries per level, no trend filter, no costs. 'Random avg R' = random entries on the "
                 "same symbols with the same direction mix, stop distance and R:R.\n\n")
        for interval, title in (("1d", "Daily chart (full history)"), ("1h", "Hourly chart (~2 years)")):
            sub = df[df.chart == interval]
            if len(sub):
                fh.write(f"## {title}\n\n" + fmt_table(sub, cols) + "\n\n")
    print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
