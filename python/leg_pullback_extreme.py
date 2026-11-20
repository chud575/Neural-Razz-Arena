"""
Impulse leg + pullback, with the target tied to the first leg instead of a fixed R multiple.

Same orders as python/leg_pullback_study.py (limit in the pullback half at `depth` %, stop at the leg's start, skipped /
taken at the close / cancelled the same way). One unit, one target:
    "extreme"        the first leg's extreme (its high for a leg up)
    "extreme +25%"   a quarter of the leg beyond the extreme
    "extreme +50%"   half the leg beyond the extreme (where an equal second leg from a 50 % pullback would end)
Reward : risk follows from the depth. Break-even win rate = 1 / (1 + reward:risk), before fees.
Costs: Bybit VIP 3 futures. IS = first 70 %, OOS = last 30 %.

    python leg_pullback_extreme.py <data_dir>   -> results/leg_pullback_extreme.csv / .md
"""
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from impulse_study import find_legs

MAXB = 3000
DEPTHS = (0, 25, 50, 75, 90)
EXTS = {"extreme": 0.0, "extreme +25%": 0.25, "extreme +50%": 0.5}


def trade(o, h, l, c, fin, eB, d, sP, eP, depth, ext, bar_h):
    n = len(c)
    L = abs(eP - sP)
    eq = (sP + eP) / 2
    px = eq + (sP - eq) * depth / 100
    tp = eP + d * ext * L
    if len(l[eB + 1:fin + 1]) and ((l[eB + 1:fin + 1].min() <= sP) if d == 1 else (h[eB + 1:fin + 1].max() >= sP)):
        return None
    fee_in = S.MAKER
    if (c[fin] <= px) if d == 1 else (c[fin] >= px):
        e, f, fee_in = c[fin], fin, S.TAKER
    else:
        f = None
        for m in range(fin + 1, min(n, fin + 1 + MAXB)):
            if (l[m] <= px) if d == 1 else (h[m] >= px):
                e, f = (min(o[m], px) if d == 1 else max(o[m], px)), m
                break
            if (h[m] > eP) if d == 1 else (l[m] < eP):
                return None
        if f is None:
            return None
        if (l[f] <= sP) if d == 1 else (h[f] >= sP):
            risk = abs(e - sP)
            return dict(r=-1 - (fee_in + S.TAKER) * e / risk, win=0, rr=abs(tp - e) / risk, risk=risk / e * 100) if risk > 0 else None
    risk = abs(e - sP)
    if risk <= 0 or (e - sP) * d <= 0 or (tp - e) * d <= 0:
        return None
    px_x, win, m = None, 0, f + 1
    end = min(n, f + 1 + MAXB)
    while m < end:
        if (l[m] <= sP) if d == 1 else (h[m] >= sP):
            px_x = min(o[m], sP) if d == 1 else max(o[m], sP)
            break
        if (h[m] >= tp) if d == 1 else (l[m] <= tp):
            px_x, win = (max(o[m], tp) if d == 1 else min(o[m], tp)), 1
            break
        m += 1
    if px_x is None:
        m = end - 1
        px_x = c[m]
    cost = fee_in + (S.MAKER if win else S.TAKER) + d * S.FUNDING_8H * (m - f) * bar_h / 8
    return dict(r=d * (px_x - e) / risk - cost * e / risk, win=win, rr=abs(tp - e) / risk, risk=risk / e * 100)


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rows, cnt = [], []
    for coin in ("btc", "eth", "avax", "xrp"):
        S.DATA.clear()
        S.load(D, ["15m", "1h", "4h"], coin)
        for tf in ("15m", "1h", "4h"):
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(n * S.SPLIT)
            legs = [x for x in find_legs(h, l, c) if x[5] < n - 3]
            cnt.append((coin, tf, len(legs)))
            for sB, eB, sP, eP, d, fin in legs:
                for depth in DEPTHS:
                    for name, ext in EXTS.items():
                        r = trade(o, h, l, c, fin, eB, d, sP, eP, depth, ext, bar_h)
                        if r:
                            rows.append((coin, tf, depth, name, d, "IS" if fin < split else "OOS", r["r"], r["win"], r["rr"], r["risk"]))
        print("done", coin, file=sys.stderr, flush=True)
    t = pd.DataFrame(rows, columns=["coin", "tf", "depth", "target", "d", "period", "r", "win", "rr", "risk"])
    t.to_csv("results/leg_pullback_extreme.csv", index=False)
    k = pd.DataFrame(cnt, columns=["coin", "tf", "legs"])
    L = ["# Impulse leg + pullback with the target at the first leg's extreme — study\n",
         "Rules in python/leg_pullback_extreme.py. After Bybit VIP 3 fees. Win rate against the break-even rate for that reward:risk; average R per trade IS / OOS.\n"]
    for coins, title in ((["btc"], "BTC"), (["btc", "eth", "avax", "xrp"], "All four coins")):
        for tf in ("15m", "1h", "4h"):
            legs = k[k.coin.isin(coins) & (k.tf == tf)].legs.sum()
            L.append(f"\n## {title} · {tf} ({legs} legs)\n\n| Entry depth | Target | Reward : risk | Trades (share of legs) | Win rate | Break-even | R per trade IS / OOS | Total R |\n|---|---|---|---|---|---|---|---|")
            for depth in DEPTHS:
                for name in EXTS:
                    x = t[t.coin.isin(coins) & (t.tf == tf) & (t.depth == depth) & (t.target == name)]
                    if len(x) == 0:
                        continue
                    L.append(f"| {depth}% | {name} | {x.rr.median():.1f} | {len(x)} ({len(x)/legs*100:.0f}%) | {x.win.mean()*100:.0f}% | {(1/(1+x.rr)).mean()*100:.0f}% | "
                             f"{x[x.period=='IS'].r.mean():+.2f} / {x[x.period=='OOS'].r.mean():+.2f} | {x.r.sum():+.0f} |")
    open("results/leg_pullback_extreme.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[2:]))


if __name__ == "__main__":
    main()
