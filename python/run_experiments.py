"""
Run a grid of strategy toggles across a universe of symbols and write a markdown report.

    python run_experiments.py --cache /path/to/cache --out results/experiments_daily.md
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

from dtdb_backtest import Params, backtest, fetch_yahoo, max_dd_r, stats

UNIVERSE = [
    # US index ETFs + bonds
    "SPY", "QQQ", "IWM", "DIA", "TLT",
    # large-cap stocks across sectors
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "BAC", "XOM", "CVX",
    "JNJ", "PFE", "PG", "KO", "WMT", "HD", "DIS", "INTC", "CSCO", "T",
    # crypto
    "BTC-USD", "ETH-USD",
    # commodities futures
    "GC=F", "SI=F", "CL=F",
    # FX
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X",
]

ENTRY_SETUPS = [
    ("Breakout + Midpoint (original)", dict(use_entry1=True, entry2_mode="midpoint")),
    ("Breakout only", dict(use_entry1=True, entry2_mode="off")),
    ("Retest only (limit at neckline)", dict(use_entry1=False, entry2_mode="retest")),
    ("Retest only (confirmed close)", dict(use_entry1=False, entry2_mode="retest_confirm")),
    ("Breakout + Retest", dict(use_entry1=True, entry2_mode="retest")),
]
RRS = [1.0, 2.0, 3.0]
TRENDS = ["off", "sma"]
DIRECTIONS = [("Both", dict()), ("Longs only", dict(trade_shorts=False))]


def run_grid(data: dict[str, pd.DataFrame], base: Params):
    rows = []
    for (setup_name, setup), rr, trend, (dir_name, dirs) in itertools.product(ENTRY_SETUPS, RRS, TRENDS, DIRECTIONS):
        p = replace(base, rr=rr, trend_filter=trend, **setup, **dirs)
        trades, sym_r = [], []
        signals = fills = 0
        for sym, df in data.items():
            res = backtest(df, p, sym)
            trades += res.trades
            signals += res.signals_long + res.signals_short
            fills += res.e2_fills
            sym_r.append(sum(t.r for t in res.trades))
        s = stats(trades)
        rows.append(dict(
            setup=setup_name, rr=rr, trend="SMA200" if trend == "sma" else "off", direction=dir_name,
            signals=signals, trades=s["n"], win_rate=s["win_rate"], avg_r=s["avg_r"], net_r=s["net_r"],
            pf=s["pf"], long_r=sum(t.r for t in trades if t.direction == 1),
            short_r=sum(t.r for t in trades if t.direction == -1),
            pct_sym_profitable=np.mean([r > 0 for r in sym_r]) * 100,
            max_dd=max_dd_r(trades),
            breakeven_wr=100 / (1 + rr),
        ))
    return pd.DataFrame(rows)


def fmt_table(df: pd.DataFrame, cols: list[tuple[str, str, str]]) -> str:
    head = "| " + " | ".join(c[1] for c in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    lines = [head, sep]
    for _, r in df.iterrows():
        cells = []
        for key, _, fmt in cols:
            v = r[key]
            if isinstance(v, float) and math.isnan(v):
                cells.append("–")
            elif fmt:
                cells.append(fmt.format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


COLS = [
    ("setup", "Entry setup", ""), ("rr", "R:R", "{:g}:1"), ("trend", "Trend filter", ""),
    ("direction", "Direction", ""), ("trades", "Trades", "{:.0f}"), ("win_rate", "Win %", "{:.1f}"),
    ("breakeven_wr", "B/E win %", "{:.1f}"), ("avg_r", "Avg R", "{:+.3f}"), ("net_r", "Net R", "{:+.1f}"),
    ("pf", "PF", "{:.2f}"), ("long_r", "Long R", "{:+.1f}"), ("short_r", "Short R", "{:+.1f}"),
    ("pct_sym_profitable", "% symbols +", "{:.0f}"), ("max_dd", "Max DD (R)", "{:.1f}"),
]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--range", default="max")
    ap.add_argument("--out", default="results/experiments_daily.md")
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
    print(f"Loaded {len(data)} symbols, {sum(len(d) for d in data.values())} bars", file=sys.stderr)

    res = run_grid(data, Params())
    if a.csv:
        res.to_csv(a.csv, index=False)

    both = res[res.direction == "Both"]
    best = res[res.trades >= 100].sort_values("avg_r", ascending=False).head(10)
    req = res[(res.setup == "Retest only (limit at neckline)") & (res.trend == "off") & (res.direction == "Both")]

    with open(a.out, "w") as fh:
        fh.write(f"# Double Top / Bottom experiments ({a.interval})\n\n")
        fh.write(f"Universe: {len(data)} symbols — {', '.join(data)}\n\n")
        fh.write("No commissions/slippage. Stop and target touched in the same bar = loss. "
                 "R = multiple of risk. 'B/E win %' = win rate needed to break even at that R:R.\n\n")
        fh.write("## Requested test: no second entry, enter only on a retest of the breakout point\n\n")
        fh.write(fmt_table(req, COLS) + "\n\n")
        fh.write("## Top 10 configurations by avg R per trade (min 100 trades)\n\n")
        fh.write(fmt_table(best, COLS) + "\n\n")
        fh.write("## All configurations — both directions\n\n")
        fh.write(fmt_table(both, COLS) + "\n\n")
        fh.write("## All configurations — longs only\n\n")
        fh.write(fmt_table(res[res.direction == "Longs only"], COLS) + "\n")
    print(f"wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
