"""
Grid search around the "first X % move from the daily open" signal. 15m candles, BTC and ETH, 2020 ->.

Signal: price first reaches open +/- X % (X = 0.5, 1, 1.5, 2, 3).
Entry modes:
    follow   enter at the trigger, with the move (stop order, taker)
    fade     enter at the trigger, against the move (limit order, maker)
    reclaim  wait for price to come back to the open, then enter AGAINST the first move (stop order, taker)
    retest   wait for price to come back to the open, then enter WITH the first move (limit order, maker)
Stop S % and target T % measured from the entry (S: 0.5, 1, 1.5, 2, 3, none; T: 1, 2, 3, 4, 6, none); otherwise out at 24:00 UTC.
Day filter: all / alert (previous day's range and last 12 h both in the widest third) / quiet (the rest).
Entry candle: the stop can be hit, the target cannot ("pessimistic"); the second pass ignores the entry candle for the stop ("optimistic").
Fees: Bybit VIP 3 futures; maker at a target, taker at a stop or the close. P&L in % of price.
In-sample = first 70 % of days, out-of-sample = last 30 %. t-statistics use one number per day (BTC and ETH averaged).

    python first_move_grid.py <data_dir>   -> results/first_move_grid.md
"""
import sys

import numpy as np
import pandas as pd

TAKER, MAKER = 0.035, 0.014
XS = (0.5, 1, 1.5, 2, 3)
SS = (0.5, 1, 1.5, 2, 3, None)
TS = (1, 2, 3, 4, 6, None)
MODES = ("follow", "fade", "reclaim", "retest")
D = sys.argv[1]
BIG = 10 ** 9


def sim(o, h, l, c, idx, e, d, pess):
    """P&L matrix [S, T] for an entry at bar idx, price e, direction d."""
    hh, ll, oo = h[idx:], l[idx:], o[idx:]
    fav = (d * ((hh if d == 1 else ll) - e) / e * 100)
    adv = (-d * ((ll if d == 1 else hh) - e) / e * 100)
    out = np.empty((len(SS), len(TS)))
    close_pnl = d * (c[-1] - e) / e * 100
    sk, sp = [], []
    for S in SS:
        if S is None:
            sk.append(BIG); sp.append(0.0); continue
        hit = adv >= S
        if not pess:
            hit = hit.copy(); hit[0] = False
        if hit.any():
            k = int(np.argmax(hit))
            gap = -d * (oo[k] - e) / e * 100 if k > 0 else 0.0
            sk.append(k); sp.append(-max(S, gap))
        else:
            sk.append(BIG); sp.append(0.0)
    tk = []
    for T in TS:
        if T is None:
            tk.append(BIG); continue
        hit = fav >= T
        hit = hit.copy(); hit[0] = False
        tk.append(int(np.argmax(hit)) if hit.any() else BIG)
    for a in range(len(SS)):
        for b in range(len(TS)):
            if sk[a] != BIG and sk[a] <= tk[b]:
                out[a, b] = sp[a] - TAKER
            elif tk[b] != BIG:
                out[a, b] = TS[b] - MAKER
            else:
                out[a, b] = close_pnl - TAKER
    return out


res = {(p, x, m): [] for p in (1, 0) for x in XS for m in MODES}
meta = {(x, m): [] for x in XS for m in MODES}
for coin in ("btc", "eth"):
    m15 = pd.read_csv(f"{D}/{coin}_15m.csv", index_col=0, parse_dates=True)
    m15 = m15[(m15[["open", "high", "low", "close"]] > 0).all(axis=1)]
    day = m15.index.floor("1D")
    dd = m15.groupby(day).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"))
    dd["rng"] = (dd.high - dd.low) / dd.open * 100
    pm = m15[m15.index.hour >= 12]
    l12 = pm.groupby(pm.index.floor("1D")).agg(h=("high", "max"), l=("low", "min"))
    dd["r12"] = (l12.h - l12.l) / dd.open * 100
    f = dd[["rng", "r12"]].shift(1)
    alert = (f.rng.rank(pct=True) >= 2 / 3) & (f.r12.rank(pct=True) >= 2 / 3)
    for t, g in m15.groupby(day):
        if len(g) < 92 or np.isnan(f.rng.get(t, np.nan)):
            continue
        o, h, l, c = (g[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        O = o[0]
        for x in XS:
            up, dn = O * (1 + x / 100), O * (1 - x / 100)
            iu, idn = np.flatnonzero(h >= up), np.flatnonzero(l <= dn)
            a = iu[0] if len(iu) else BIG
            b = idn[0] if len(idn) else BIG
            if a == b:
                continue
            mv = 1 if a < b else -1
            i = min(a, b)
            lvl = up if mv == 1 else dn
            e_stop = max(o[i], lvl) if mv == 1 else min(o[i], lvl)          # stop order: gap fills at the (worse) open
            back = np.flatnonzero((l[i + 1:] <= O) if mv == 1 else (h[i + 1:] >= O))
            j = i + 1 + back[0] if len(back) else None
            for mode in MODES:
                if mode == "follow":
                    idx, e, d, fee = i, e_stop, mv, TAKER
                elif mode == "fade":
                    idx, e, d, fee = i, e_stop, -mv, MAKER                  # limit order: a gap through fills at the (better) open
                elif j is None:
                    continue
                elif mode == "reclaim":
                    idx, e, d, fee = j, (min(o[j], O) if mv == 1 else max(o[j], O)), -mv, TAKER
                else:
                    idx, e, d, fee = j, (min(o[j], O) if mv == 1 else max(o[j], O)), mv, MAKER
                if idx >= len(c) - 1:
                    continue
                meta[(x, mode)].append((coin, t, bool(alert[t])))
                for p in (1, 0):
                    res[(p, x, mode)].append(sim(o, h, l, c, idx, e, d, bool(p)) - fee)

alld = sorted({t for v in meta.values() for _, t, _ in v})
cut = alld[int(len(alld) * 0.7)]
rows = []
for (x, mode), mt in meta.items():
    md = pd.DataFrame(mt, columns=["coin", "day", "alert"])
    for p in (1, 0):
        P = np.array(res[(p, x, mode)])
        for filt, mask in (("all", np.ones(len(md), bool)), ("alert", md.alert.values), ("quiet", ~md.alert.values)):
            for a, S in enumerate(SS):
                for b, T in enumerate(TS):
                    s = pd.Series(P[mask, a, b], index=md.day[mask].values)
                    byday = s.groupby(level=0).mean()
                    i_, o_ = byday[byday.index < cut], byday[byday.index >= cut]
                    if len(i_) < 50 or len(o_) < 30:
                        continue
                    ts = lambda v: v.mean() / v.std() * np.sqrt(len(v))
                    sc = s[md.coin[mask].values == "btc"].mean(), s[md.coin[mask].values == "eth"].mean()
                    rows.append(dict(pess=p, X=x, mode=mode, days=filt, S=S if S else "none", T=T if T else "close", n=len(s), win=(s > 0).mean() * 100,
                                     is_avg=s[s.index < cut].mean(), oos_avg=s[s.index >= cut].mean(), is_t=ts(i_), oos_t=ts(o_), total=s.sum(), btc=sc[0], eth=sc[1],
                                     n_oos=int((s.index >= cut).sum())))
R = pd.DataFrame(rows)
R.to_csv("results/first_move_grid.csv", index=False)
pe = R[R.pess == 1].reset_index(drop=True)
op = R[R.pess == 0].set_index(["X", "mode", "days", "S", "T"])
L = [f"# Grid search around the first-move-from-the-open signal (python/first_move_grid.py)\n",
     f"BTC and ETH, 15m candles, {alld[0].date()} → {alld[-1].date()}. In-sample before {cut.date()}, out-of-sample after. {len(pe)} rule combinations tested. "
     "P&L in % of price per trade after Bybit VIP 3 fees. 'Pessimistic' = the stop can be hit on the entry candle; 'optimistic' = it cannot.\n"]
both = pe[(pe.is_avg > 0) & (pe.oos_avg > 0)]
strong = pe[(pe.is_t > 2) & (pe.oos_t > 2)]
L.append(f"- Positive in both halves: {len(both)} of {len(pe)} ({len(both)/len(pe)*100:.0f}%). With t > 2 in both halves: {len(strong)}.\n")
L.append("## Share of combinations positive in both halves, by entry mode and day type\n\n| Mode | all days | alert days | quiet days |\n|---|---|---|---|")
for mode in MODES:
    L.append(f"| {mode} | " + " | ".join(f"{((pe[(pe['mode']==mode)&(pe.days==f)].is_avg>0)&(pe[(pe['mode']==mode)&(pe.days==f)].oos_avg>0)).mean()*100:.0f}%" for f in ("all", "alert", "quiet")) + " |")


def table(x, title, k=20):
    L.append(f"\n## {title}\n\n| Mode | Trigger | Days | Stop | Target | Trades | Profitable | In-sample avg | Out-of-sample avg | IS t | OOS t | BTC | ETH | Total | Optimistic IS / OOS |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in x.head(k).iterrows():
        q = op.loc[(r.X, r["mode"], r.days, r.S, r["T"])]
        L.append(f"| {r['mode']} | {r.X}% | {r.days} | {r.S} | {r['T']} | {r.n} | {r.win:.0f}% | {r.is_avg:+.3f}% | {r.oos_avg:+.3f}% | {r.is_t:+.1f} | {r.oos_t:+.1f} | {r.btc:+.3f}% | {r.eth:+.3f}% | {r.total:+.0f}% | {q.is_avg:+.3f}% / {q.oos_avg:+.3f}% |")


table(pe.sort_values("is_t", ascending=False), "Top 20 by in-sample t — and what they did out-of-sample")
pe["mt"] = pe[["is_t", "oos_t"]].min(axis=1)
table(pe.sort_values("mt", ascending=False), "Top 20 by the weaker of the two halves")
table(pe[pe.days == "all"].sort_values("mt", ascending=False), "Top 10 using every day (no day filter)", 10)
table(pe[(pe['mode'] == "follow") & (pe.X == 1) & (pe.S == 1) & (pe['T'] == 4)], "The original idea (follow 1%, stop 1%, target 4%)")
open("results/first_move_grid.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
