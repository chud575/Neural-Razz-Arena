"""
Cross-asset check for a sweep: settings chosen on ONE asset's in-sample period, evaluated on the other assets'
full history (none of which was used for the choice). Works on run_btc_sweep.py *_all.csv outputs.

    python analyze_crossasset.py --dir DIR --strategy rangesweep --pick btc --others eth,avax,xrp --out results/x.md
expects DIR/rs_<asset>_all.csv (override the pattern with --pattern)
"""
from __future__ import annotations

import argparse
import math

import pandas as pd

import run_btc_sweep as S
from analyze_btc_sweep import family

TF_ORDER = ["15m", "1h", "4h", "1d"]


def full(r):
    n = r.is_n + r.oos_n
    return (r.is_sum + r.oos_sum) / n if n else math.nan, n


def f(v, fmt="{:+.3f}"):
    return "–" if v is None or (isinstance(v, float) and math.isnan(v)) else fmt.format(v)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--strategy", default="rangesweep")
    ap.add_argument("--pick", default="btc")
    ap.add_argument("--others", default="eth,avax,xrp")
    ap.add_argument("--pattern", default="rs_{asset}_all.csv")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    others = a.others.split(",")
    dfs = {x: pd.read_csv(f"{a.dir}/{a.pattern.format(asset=x)}") for x in [a.pick] + others}
    for x, d in dfs.items():
        d["key"] = d.config + " | " + d.direction
        dfs[x] = d[d.strategy == a.strategy].set_index("key")

    L = [f"# Cross-asset check — {a.strategy}: settings picked on {a.pick.upper()} (in-sample only), "
         f"tested on {', '.join(o.upper() for o in others)}\n",
         f"Net of {S.COST_RT * 100:.2f}% round-trip costs. 'Full' = every trade in that asset's history "
         "(none of it was used to pick the settings). R = average net R per trade (n = trades).\n"]
    for tf in TF_ORDER:
        base = dfs[a.pick]
        base = base[base.tf == tf]
        if base.empty:
            continue
        elig = base[base.is_n >= S.MIN_IS[tf]].sort_values("is_t", ascending=False)
        elig = elig.drop_duplicates(["direction", "is_n", "is_avg", "oos_n", "oos_avg"])
        L.append(f"\n## {tf}\n")
        if elig.empty:
            L.append(f"No setting reached {S.MIN_IS[tf]} in-sample trades on {a.pick.upper()}.\n")
            continue
        hdr = ["Settings (top by " + a.pick.upper() + " IS t-stat)", a.pick.upper() + " IS", a.pick.upper() + " OOS"] + \
              [o.upper() + " full" for o in others] + ["Positive on"]
        L.append("| " + " | ".join(hdr) + " |\n|" + "|".join("---" for _ in hdr) + "|")
        agg = {o: [] for o in others}
        for key, r in elig.head(a.top).iterrows():
            cells = [key, f"{f(r.is_avg)} (n={r.is_n:.0f})", f"{f(r.oos_avg)} (n={r.oos_n:.0f})"]
            pos = int(r.oos_avg > 0) if not math.isnan(r.oos_avg) else 0
            cnt = 1
            for o in others:
                d = dfs[o]
                sub = d[(d.index == key) & (d.tf == tf)]
                if not len(sub):
                    cells.append("–")
                    continue
                v, n = full(sub.iloc[0])
                cells.append(f"{f(v)} (n={n:.0f})")
                agg[o].append(v)
                if n:
                    cnt += 1
                    pos += int(v > 0)
            cells.append(f"{pos}/{cnt}")
            L.append("| " + " | ".join(cells) + " |")
        L.append("")
        # family view across assets (all variants, full history, both sides)
        L.append(f"Entry families on {tf} (all variants averaged, full history, both sides):\n")
        fams = {}
        for x, d in dfs.items():
            sub = d[(d.tf == tf) & (d.direction == "both")].copy()
            sub = sub[(sub.is_n + sub.oos_n) >= 20]
            if sub.empty:
                continue
            sub["fam"] = [family(a.strategy, c) for c in sub.config]
            sub["full"] = (sub.is_sum + sub.oos_sum) / (sub.is_n + sub.oos_n)
            fams[x] = sub.groupby("fam").agg(avg=("full", "mean"), pos=("full", lambda s: (s > 0).mean() * 100))
        names = sorted(set().union(*[set(v.index) for v in fams.values()])) if fams else []
        hdr = ["Family"] + [f"{x.upper()} avg R (% variants > 0)" for x in fams]
        L.append("| " + " | ".join(hdr) + " |\n|" + "|".join("---" for _ in hdr) + "|")
        for nm in names:
            row = [nm]
            for x, fm in fams.items():
                row.append(f"{f(fm.loc[nm, 'avg'])} ({fm.loc[nm, 'pos']:.0f}%)" if nm in fm.index else "–")
            L.append("| " + " | ".join(row) + " |")
        L.append("")
    with open(a.out, "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
