"""
"Take the first 1 %": from the 00:00 UTC open, enter in whichever direction price moves 1 % first, aiming for 4 % more
(5 % from the open). Tested on every day and on "alert" days (wide previous day and wide last 12 hours).

15-minute candles, BTC and ETH, 2020 →. Entry by stop order at open ± 1 %. Target = open ± 5 %. Exits tried:
    A  no stop: target, or the 24:00 UTC close
    B  stop back at the open (risk 1 %): stop, target, or the close
    C  stop at the opposite 1 % level (risk 2 %): stop, target, or the close
A candle that touches both the entry and the stop counts as stopped; a candle that touches both entry levels is skipped.
Costs: Bybit VIP 3 futures (taker entry; maker at the target, taker at a stop or at the close). P&L in % of price.
Alert day = previous day's range AND last 12 hours' range both in their widest third (known at 00:00 UTC).

    python first_move_trade.py <data_dir>   -> results/first_move_trade.csv / .md
"""
import sys

import numpy as np
import pandas as pd

TAKER, MAKER = 0.035, 0.014            # % of price
D = sys.argv[1]
rows = []
for coin in ("btc", "eth"):
    m = pd.read_csv(f"{D}/{coin}_15m.csv", index_col=0, parse_dates=True)
    m = m[(m[["open", "high", "low", "close"]] > 0).all(axis=1)]
    day = m.index.floor("1D")
    dd = m.groupby(day).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), n=("open", "size"))
    dd["rng"] = (dd.high - dd.low) / dd.open * 100
    dd["ret"] = (dd.close / dd.open - 1) * 100
    last12 = m[m.index.hour >= 12].groupby(m[m.index.hour >= 12].index.floor("1D")).agg(h=("high", "max"), l=("low", "min"))
    last4 = m[m.index.hour >= 20].groupby(m[m.index.hour >= 20].index.floor("1D")).agg(h=("high", "max"), l=("low", "min"))
    dd["r12"] = (last12.h - last12.l) / dd.open * 100
    dd["r4"] = (last4.h - last4.l) / dd.open * 100
    feat = dd[["rng", "r12", "r4", "ret"]].shift(1)                       # yesterday's readings, known at today's open
    q_rng, q_r12 = feat.rng.rank(pct=True), feat.r12.rank(pct=True)       # (ranked over the whole sample: thresholds only)
    for t, g in m.groupby(day):
        if len(g) < 92 or t not in feat.index or np.isnan(feat.rng.get(t, np.nan)):
            continue
        o, h, l, c = (g[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        O = o[0]
        up, dn = O * 1.01, O * 0.99
        iu = np.flatnonzero(h >= up)
        idn = np.flatnonzero(l <= dn)
        a = iu[0] if len(iu) else 10 ** 9
        b = idn[0] if len(idn) else 10 ** 9
        base = dict(coin=coin, day=t, year=t.year, alert=int(q_rng[t] >= 2 / 3 and q_r12[t] >= 2 / 3), prev_rng_q=q_rng[t], r12_q=q_r12[t], r4_q=feat.r4.rank(pct=True)[t],
                    day_ret=dd.ret[t], big=int(abs(dd.ret[t]) >= 5))
        if a == b:
            rows.append(dict(base, variant="-", outcome="no trigger" if a == 10 ** 9 else "both in one candle", pnl=0.0, traded=0))
            continue
        d = 1 if a < b else -1
        i = min(a, b)
        e = up if d == 1 else dn
        e = max(o[i], e) if d == 1 else min(o[i], e)                      # a gap fills at the open
        tgt = O * (1 + 0.05 * d)
        for variant, stop in (("A no stop", None), ("B stop at the open", O), ("C stop at the opposite 1%", O * (1 - 0.01 * d))):
            px, why = None, None
            for k in range(i, len(c)):
                if stop is not None and ((l[k] <= stop) if d == 1 else (h[k] >= stop)):
                    px, why = ((min(o[k], stop) if d == 1 else max(o[k], stop)) if k > i else stop), "stop"
                    break
                if k > i and ((h[k] >= tgt) if d == 1 else (l[k] <= tgt)):
                    px, why = tgt, "target"
                    break
            if px is None:
                px, why = c[-1], "close"
            pnl = d * (px - e) / e * 100 - TAKER - (MAKER if why == "target" else TAKER)
            rows.append(dict(base, variant=variant, outcome=why, pnl=pnl, traded=1, d=d, with_day=int(d == np.sign(dd.ret[t]))))
t = pd.DataFrame(rows)
t.to_csv("results/first_move_trade.csv", index=False)
days = t.drop_duplicates(["coin", "day"])
L = ["# \"Take the first 1%\" — enter the first 1% move from the daily open, aim for 4% more (python/first_move_trade.py)\n",
     f"15m candles, BTC and ETH, {days.day.min().date()} → {days.day.max().date()}: {len(days)} days. P&L in % of price per trade, after Bybit VIP 3 fees. "
     "Alert day = previous day's range and last 12 hours' range both in their widest third.\n"]
tr = t[t.traded == 1]


def block(x, title):
    n_days = x.drop_duplicates(["coin", "day"]).shape[0]
    L.append(f"\n## {title}\n")
    L.append("| Exit | Days | Trades | Hit +4% target | Stopped | Out at the close | Average P&L per trade | Total P&L | 2020–2022 avg | 2023–2026 avg | BTC avg | ETH avg |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for v, g in x[x.traded == 1].groupby("variant"):
        oc = g.outcome.value_counts(normalize=True) * 100
        L.append(f"| {v} | {n_days} | {len(g)} | {oc.get('target', 0):.0f}% | {oc.get('stop', 0):.0f}% | {oc.get('close', 0):.0f}% | {g.pnl.mean():+.2f}% | {g.pnl.sum():+.0f}% | "
                 f"{g[g.year <= 2022].pnl.mean():+.2f}% | {g[g.year > 2022].pnl.mean():+.2f}% | {g[g.coin == 'btc'].pnl.mean():+.2f}% | {g[g.coin == 'eth'].pnl.mean():+.2f}% |")


block(t, "Every day")
block(t[t.alert == 1], "Alert days only")
block(t[t.alert == 0], "Non-alert days")
block(t[(t.prev_rng_q >= 0.8)], "Previous day's range in its widest fifth")
block(t[(t.r4_q >= 0.8)], "Last 4 hours' range in its widest fifth")
a = t[(t.alert == 1)]
ad = a.drop_duplicates(["coin", "day"])
g = a[a.variant == "A no stop"]
L.append(f"\n## Alert days in detail\n\nAlert days: {len(ad)}; a 1% move triggered on {len(g)} ({len(g)/len(ad)*100:.0f}%). The day ended as a ±5% day on {ad.big.mean()*100:.0f}% of alert days "
         f"({days.big.mean()*100:.0f}% of all days). The first 1% move pointed the way the day finished on {g.with_day.mean()*100:.0f}% of triggered alert days "
         f"({tr[tr.variant=='A no stop'].with_day.mean()*100:.0f}% on all days).\n")
L.append("No-stop version on alert days, by how the day ended:\n\n| Day ended | Trades | Average P&L |\n|---|---|---|")
for nm, x in (("as a ±5% day, the trade's way", g[(g.big == 1) & (g.with_day == 1)]), ("as a ±5% day, against the trade", g[(g.big == 1) & (g.with_day == 0)]), ("under 5%", g[g.big == 0])):
    L.append(f"| {nm} | {len(x)} | {x.pnl.mean():+.2f}% |")
gb = a[a.variant == "B stop at the open"]
L.append(f"\nStop-at-the-open version on alert days, in R (1R = the 1% risked): average {gb.pnl.mean():+.2f}R per trade, largest losing streak "
         f"{max((sum(1 for _ in grp) for k, grp in __import__('itertools').groupby(gb.sort_values('day').pnl < 0) if k), default=0)} trades.")
open("results/first_move_trade.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[2:]))
