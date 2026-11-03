"""
Analyze run_btc_sweep.py output: IS-ranked picks, their OOS results, overfitting diagnostics, random benchmark.

    python analyze_btc_sweep.py --data DIR --csv results/btc_sweep_all.csv [more csvs] --out results/btc_sweep.md
"""
from __future__ import annotations

import argparse
import math
import re

import numpy as np
import pandas as pd

import run_btc_sweep as S

TF_ORDER = ["15m", "1h", "4h", "1d"]
TF_NAME = {"15m": "15-minute", "1h": "1-hour", "4h": "4-hour", "1d": "Daily"}
STRAT_NAME = {"dtdb": "Double Top / Bottom", "srflip": "S/R Flip", "megaphone": "Megaphone"}


def config_kwargs(strat: str, tf: str, name: str) -> dict:
    for n, kw in S.STRATS[strat][2](tf):
        if n == name:
            return kw
    raise KeyError(name)


def finalist_control(strat, tf, name, direction):
    mod, P, _ = S.STRATS[strat]
    df = S.DATA[tf]
    split_t = df.index[int(len(df) * S.SPLIT)]
    res = mod.backtest(df, P(**config_kwargs(strat, tf, name)), "BTC")
    tr = [t for t in res.trades if t.signal_time >= split_t and
          (direction == "both" or (direction == "longs") == (t.direction == 1))]
    if not tr:
        return math.nan, 0

    def rr_of(t):
        risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
        tgt = getattr(t, "target", math.nan)
        if math.isnan(tgt) or risk <= 0:
            return 2.0
        return abs(tgt - (t.stop_px + t.direction * risk)) / risk

    return S.random_oos_control(tf, tr, rr_of), len(tr)


def buy_hold(tf):
    df = S.DATA[tf]
    k = int(len(df) * S.SPLIT)
    c = df["close"]
    return (c.iloc[k] / c.iloc[0] - 1) * 100, (c.iloc[-1] / c.iloc[k] - 1) * 100, df.index[0], df.index[k], df.index[-1]


def md_table(df, cols):
    out = ["| " + " | ".join(h for _, h, _ in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(S.fmt(r[k], f) if f else str(r[k]) for k, _, f in cols) + " |")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--csv", nargs="+", required=True)
    ap.add_argument("--out", default="results/btc_sweep.md")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args(argv)
    df = pd.concat([pd.read_csv(p) for p in a.csv], ignore_index=True)
    df = df.drop_duplicates(["strategy", "tf", "config", "direction"], keep="last")
    tfs = [tf for tf in TF_ORDER if tf in set(df.tf)]
    S.load(a.data, tfs)

    cols = [("config", "Settings", ""), ("direction", "Side", ""), ("is_n", "IS trades", "{:.0f}"),
            ("is_avg", "IS avg R (net)", "{:+.3f}"), ("is_t", "IS t-stat", "{:.2f}"),
            ("oos_n", "OOS trades", "{:.0f}"), ("oos_avg", "OOS avg R (net)", "{:+.3f}"), ("oos_sum", "OOS total R", "{:+.1f}"),
            ("oos_win", "OOS win %", "{:.0f}")]
    lines = ["# BTC strategy sweep — 15m / 1h / 4h / 1D\n",
             f"Costs: {S.COST_RT * 100:.2f}% round trip per trade (0.1% per side), charged in R. "
             f"In-sample (IS) = first {int(S.SPLIT * 100)}% of each timeframe's history, out-of-sample (OOS) = last "
             f"{100 - int(S.SPLIT * 100)}%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).\n"]
    summary = []
    for tf in tfs:
        bh_is, bh_oos, t0, tk, t1 = buy_hold(tf)
        lines.append(f"\n## {TF_NAME[tf]}  (IS {t0.date()} → {tk.date()}, OOS {tk.date()} → {t1.date()}; "
                     f"BTC buy & hold: IS {bh_is:+.0f}%, OOS {bh_oos:+.0f}%)\n")
        for strat in ("dtdb", "srflip", "megaphone"):
            sub = df[(df.tf == tf) & (df.strategy == strat)]
            if sub.empty:
                continue
            elig = sub[sub.is_n >= S.MIN_IS[tf]].copy()
            n_cfg = sub.config.nunique()
            if elig.empty:
                lines.append(f"### {STRAT_NAME[strat]}\n\nNo configuration reached {S.MIN_IS[tf]} IS trades.\n")
                continue
            top = elig.sort_values("is_t", ascending=False).head(a.top)
            both = elig.dropna(subset=["is_avg", "oos_avg"])
            both = both[both.oos_n >= 10]
            rho = both[["is_avg", "oos_avg"]].corr(method="spearman").iloc[0, 1] if len(both) > 10 else math.nan
            top20 = elig.sort_values("is_t", ascending=False).head(20)
            pos_is = (elig.is_avg > 0).mean() * 100
            ctrl, n_ctrl = finalist_control(strat, tf, top.iloc[0].config, top.iloc[0].direction)
            best = top.iloc[0]
            summary.append(dict(tf=tf, strategy=STRAT_NAME[strat], config=best.config, direction=best.direction,
                                is_n=best.is_n, is_avg=best.is_avg, oos_n=best.oos_n, oos_avg=best.oos_avg,
                                ctrl=ctrl, edge=best.oos_avg - ctrl if not math.isnan(best.oos_avg) else math.nan,
                                top20_oos=top20.oos_avg.mean(), rho=rho))
            lines.append(f"### {STRAT_NAME[strat]}\n")
            lines.append(f"{n_cfg} settings × 3 sides tested; {len(elig)} combinations had ≥{S.MIN_IS[tf]} IS trades, "
                         f"{pos_is:.0f}% of them were profitable in-sample after costs. "
                         f"IS→OOS rank correlation (Spearman): {S.fmt(rho, '{:+.2f}')}. "
                         f"Average OOS result of the top-20 IS picks: {S.fmt(top20.oos_avg.mean())} R/trade.\n")
            lines.append(f"Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): "
                         f"{S.fmt(ctrl)} R/trade over {n_ctrl} mirrored trades.\n")
            lines.append(md_table(top, cols) + "\n")
    sm = pd.DataFrame(summary)
    if not sm.empty:
        scols = [("tf", "TF", ""), ("strategy", "Strategy", ""), ("config", "Best IS settings", ""), ("direction", "Side", ""),
                 ("is_n", "IS n", "{:.0f}"), ("is_avg", "IS avg R", "{:+.3f}"), ("oos_n", "OOS n", "{:.0f}"),
                 ("oos_avg", "OOS avg R", "{:+.3f}"), ("ctrl", "Random OOS", "{:+.3f}"), ("edge", "OOS edge", "{:+.3f}"),
                 ("top20_oos", "Top-20 OOS avg", "{:+.3f}"), ("rho", "IS→OOS ρ", "{:+.2f}")]
        lines.insert(2, "\n## Summary — #1 in-sample pick per strategy and timeframe\n\n" + md_table(sm, scols) + "\n")
        sm.to_csv(a.out.replace(".md", "_summary.csv"), index=False)
    with open(a.out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
