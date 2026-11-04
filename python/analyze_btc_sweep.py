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
STRAT_NAME = {"rangesweep": "Range Sweep", "dtdb": "Double Top / Bottom", "ttb": "Triple Top / Bottom", "srflip": "S/R Flip", "megaphone": "Megaphone"}


def config_kwargs(strat: str, tf: str, name: str) -> dict:
    for n, kw in S.STRATS[strat][2](tf):
        if n == name:
            return kw
    raise KeyError(name)


def finalist_control(strat, tf, name, direction):
    mod, P, _ = S.STRATS[strat]
    df = S.DATA[tf]
    split_t = df.index[int(len(df) * S.SPLIT)]
    res = mod.backtest(df, P(**config_kwargs(strat, tf, name)), S.PREFIX.upper())
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


def family(strat: str, cfg: str) -> str:
    """Entry-type family of a configuration (used to average over the fine-tuning knobs)."""
    tok = cfg.split()
    if strat in ("dtdb", "ttb"):
        return tok[3]                                   # B+Mid / B / Retest / RetestConf / B+Retest
    if strat == "rangesweep":
        return f"{tok[3]} · {tok[6]}"                 # reclaim mode · target
    if strat == "srflip":
        lv = re.search(r"levels:(\S+)", cfg).group(1)
        return f"{tok[1]} · levels {lv}"
    m = re.search(r"(fade-\w+|BO-\w+|failedBO)", cfg).group(1)
    return m


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
    ap.add_argument("--prefix", default="btc")
    S.add_fee_args(ap)
    a = ap.parse_args(argv)
    S.apply_fee_args(a)
    df = pd.concat([pd.read_csv(p) for p in a.csv], ignore_index=True)
    df = df.drop_duplicates(["strategy", "tf", "config", "direction"], keep="last")
    tfs = [tf for tf in TF_ORDER if tf in set(df.tf)]
    S.load(a.data, tfs, a.prefix)

    cols = [("config", "Settings", ""), ("direction", "Side", ""), ("is_n", "IS trades", "{:.0f}"),
            ("is_avg", "IS avg R (net)", "{:+.3f}"), ("is_t", "IS t-stat", "{:.2f}"),
            ("oos_n", "OOS trades", "{:.0f}"), ("oos_avg", "OOS avg R (net)", "{:+.3f}"), ("oos_sum", "OOS total R", "{:+.1f}"),
            ("oos_win", "OOS win %", "{:.0f}")]
    lines = [f"# {a.prefix.upper()} strategy sweep — 15m / 1h / 4h / 1D\n",
             f"Costs: {S.fee_label()}, charged in R. "
             f"In-sample (IS) = first {int(S.SPLIT * 100)}% of each timeframe's history, out-of-sample (OOS) = last "
             f"{100 - int(S.SPLIT * 100)}%. Rankings use IS only. Data: Coinbase {a.prefix.upper()}-USD (4h resampled from 1h).\n"]
    summary = []
    for tf in tfs:
        bh_is, bh_oos, t0, tk, t1 = buy_hold(tf)
        lines.append(f"\n## {TF_NAME[tf]}  (IS {t0.date()} → {tk.date()}, OOS {tk.date()} → {t1.date()}; "
                     f"{a.prefix.upper()} buy & hold: IS {bh_is:+.0f}%, OOS {bh_oos:+.0f}%)\n")
        for strat in ("rangesweep", "dtdb", "ttb", "srflip", "megaphone"):
            sub = df[(df.tf == tf) & (df.strategy == strat)]
            if sub.empty:
                continue
            elig = sub[sub.is_n >= S.MIN_IS[tf]].copy()
            n_cfg = sub.config.nunique()
            if elig.empty:
                lines.append(f"### {STRAT_NAME[strat]}\n\nNo configuration reached {S.MIN_IS[tf]} IS trades.\n")
                continue
            # identical results (e.g. a knob that has no effect) collapse to one row
            ranked = elig.sort_values("is_t", ascending=False).drop_duplicates(
                ["direction", "is_n", "is_avg", "oos_n", "oos_avg"])
            top = ranked.head(a.top)
            both = elig.dropna(subset=["is_avg", "oos_avg"])
            both = both[both.oos_n >= 10]
            rho = both[["is_avg", "oos_avg"]].corr(method="spearman").iloc[0, 1] if len(both) > 10 else math.nan
            top20 = ranked.head(20)
            fam = elig.assign(family=[family(strat, c) for c in elig.config])
            fam = fam.groupby(["family", "direction"]).agg(
                configs=("config", "size"), is_avg=("is_avg", "mean"), oos_avg=("oos_avg", "mean"),
                oos_pos=("oos_avg", lambda x: (x > 0).mean() * 100), oos_n=("oos_n", "median")).reset_index()
            fam = fam.sort_values("is_avg", ascending=False)
            fam_ok = fam[fam.configs >= 5]
            fb = fam_ok.iloc[0] if len(fam_ok) else None
            fb_cfg = None
            if fb is not None:
                inside = ranked[np.array([family(strat, c) == fb.family for c in ranked.config]) & (ranked.direction == fb.direction).to_numpy()]
                fb_cfg = inside.iloc[0] if len(inside) else None
            fctrl, _ = finalist_control(strat, tf, fb_cfg.config, fb_cfg.direction) if fb_cfg is not None else (math.nan, 0)
            pos_is = (elig.is_avg > 0).mean() * 100
            ctrl, n_ctrl = finalist_control(strat, tf, top.iloc[0].config, top.iloc[0].direction)
            best = top.iloc[0]
            summary.append(dict(tf=tf, strategy=STRAT_NAME[strat], config=best.config, direction=best.direction,
                                is_n=best.is_n, is_avg=best.is_avg, oos_n=best.oos_n, oos_avg=best.oos_avg,
                                ctrl=ctrl, edge=best.oos_avg - ctrl if not math.isnan(best.oos_avg) else math.nan,
                                top20_oos=top20.oos_avg.mean(), rho=rho,
                                fam=f"{fb.family} ({fb.direction})" if fb is not None else "–",
                                fam_is=fb.is_avg if fb is not None else math.nan, fam_oos=fb.oos_avg if fb is not None else math.nan,
                                fam_pos=fb.oos_pos if fb is not None else math.nan,
                                fam_cfg=fb_cfg.config if fb_cfg is not None else "–",
                                fam_cfg_oos=fb_cfg.oos_avg if fb_cfg is not None else math.nan,
                                fam_cfg_n=fb_cfg.oos_n if fb_cfg is not None else math.nan, fam_ctrl=fctrl))
            lines.append(f"### {STRAT_NAME[strat]}\n")
            lines.append(f"{n_cfg} settings × 3 sides tested; {len(elig)} combinations had ≥{S.MIN_IS[tf]} IS trades, "
                         f"{pos_is:.0f}% of them were profitable in-sample after costs. "
                         f"IS→OOS rank correlation (Spearman): {S.fmt(rho, '{:+.2f}')}. "
                         f"Average OOS result of the top-20 IS picks: {S.fmt(top20.oos_avg.mean())} R/trade.\n")
            lines.append(f"Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): "
                         f"{S.fmt(ctrl)} R/trade over {n_ctrl} mirrored trades.\n")
            lines.append(md_table(top, cols) + "\n")
            lines.append("Families (all eligible variants of each entry type averaged — less prone to luck than the single best):\n")
            lines.append(md_table(fam, [("family", "Family", ""), ("direction", "Side", ""), ("configs", "Variants", "{:.0f}"),
                                        ("is_avg", "IS avg R", "{:+.3f}"), ("oos_avg", "OOS avg R", "{:+.3f}"),
                                        ("oos_pos", "% variants OOS > 0", "{:.0f}"), ("oos_n", "Median OOS trades", "{:.0f}")]) + "\n")
    sm = pd.DataFrame(summary)
    if not sm.empty:
        scols = [("tf", "TF", ""), ("strategy", "Strategy", ""), ("config", "Best IS settings", ""), ("direction", "Side", ""),
                 ("is_n", "IS n", "{:.0f}"), ("is_avg", "IS avg R", "{:+.3f}"), ("oos_n", "OOS n", "{:.0f}"),
                 ("oos_avg", "OOS avg R", "{:+.3f}"), ("ctrl", "Random OOS", "{:+.3f}"), ("edge", "OOS edge", "{:+.3f}"),
                 ("top20_oos", "Top-20 OOS avg", "{:+.3f}"), ("rho", "IS→OOS ρ", "{:+.2f}")]
        fcols = [("tf", "TF", ""), ("strategy", "Strategy", ""), ("fam", "Best family (by IS)", ""),
                 ("fam_is", "Family IS avg R", "{:+.3f}"), ("fam_oos", "Family OOS avg R", "{:+.3f}"),
                 ("fam_pos", "% variants OOS > 0", "{:.0f}"), ("fam_cfg", "Top IS settings in that family", ""),
                 ("fam_cfg_n", "OOS n", "{:.0f}"), ("fam_cfg_oos", "OOS avg R", "{:+.3f}"), ("fam_ctrl", "Random OOS", "{:+.3f}")]
        lines.insert(2, "\n## Summary A — best entry family per strategy and timeframe (chosen on IS only)\n\n"
                     + md_table(sm, fcols) + "\n\n## Summary B — single #1 in-sample settings (more prone to luck)\n\n"
                     + md_table(sm, scols) + "\n")
        sm.to_csv(a.out.replace(".md", "_summary.csv"), index=False)
    with open(a.out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
