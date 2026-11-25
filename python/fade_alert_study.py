"""
Fade the first move on alert days, on 5-minute candles. BTC and ETH, 2020 ->.

Alert day (known at 00:00 UTC): previous day's range AND its last 12 hours' range both in the widest third of the
trailing 365 days (no hindsight; the 15m studies ranked over the whole sample).
Signal: price first reaches open +/- X %. Entry: limit order at that level AGAINST the move (maker).
Stop S % / target T % from the entry, else out at 24:00 UTC. Entry candle: stop can be hit, target cannot (pessimistic).
Fill rule "through": the limit only counts as filled if price trades 0.05 % beyond it.
Fees: Bybit VIP 3 futures. P&L in % of price. In-sample = first 70 % of days.

    python fade_alert_study.py <data_dir>   -> results/fade_alert_study.md
"""
import sys

import numpy as np
import pandas as pd

TAKER, MAKER = 0.035, 0.014
XS = (0.75, 1, 1.25, 1.5, 2)
SS = (0.75, 1, 1.5, 2, 3, None)
TS = (0.75, 1, 1.5, 2, 3, 4, None)
BIG = 10 ** 9
D = sys.argv[1]


def sim(o, h, l, c, idx, e, d, pess=True):
    hh, ll, oo = h[idx:], l[idx:], o[idx:]
    fav = d * ((hh if d == 1 else ll) - e) / e * 100
    adv = -d * ((ll if d == 1 else hh) - e) / e * 100
    out = np.empty((len(SS), len(TS)))
    close_pnl = d * (c[-1] - e) / e * 100
    sk, sp, tk = [], [], []
    for S in SS:
        hit = (adv >= S) if S is not None else np.zeros(len(adv), bool)
        if not pess:
            hit = hit.copy(); hit[0] = False
        if hit.any():
            k = int(np.argmax(hit))
            sk.append(k); sp.append(-max(S, -d * (oo[k] - e) / e * 100 if k > 0 else 0.0))
        else:
            sk.append(BIG); sp.append(0.0)
    for T in TS:
        hit = (fav >= T) if T is not None else np.zeros(len(fav), bool)
        hit = hit.copy(); hit[0] = False
        tk.append(int(np.argmax(hit)) if hit.any() else BIG)
    for a in range(len(SS)):
        for b in range(len(TS)):
            out[a, b] = (sp[a] - TAKER) if (sk[a] != BIG and sk[a] <= tk[b]) else ((TS[b] - MAKER) if tk[b] != BIG else close_pnl - TAKER)
    return out


rows, P = [], {}
for coin in ("btc", "eth"):
    m = pd.read_csv(f"{D}/{coin}_5m.csv", index_col=0, parse_dates=True)
    m = m[(m[["open", "high", "low", "close"]] > 0).all(axis=1)]
    day = m.index.floor("1D")
    dd = m.groupby(day).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"))
    dd["rng"] = (dd.high - dd.low) / dd.open * 100
    pm = m[m.index.hour >= 12]
    l12 = pm.groupby(pm.index.floor("1D")).agg(h=("high", "max"), l=("low", "min"))
    dd["r12"] = (l12.h - l12.l) / dd.open * 100
    f = dd[["rng", "r12"]].shift(1)
    q = f.rolling(365, min_periods=120).rank(pct=True)                    # trailing percentile: no hindsight
    for t, g in m.groupby(day):
        if len(g) < 280 or t not in q.index or np.isnan(q.rng[t]) or np.isnan(q.r12[t]):
            continue
        o, h, l, c = (g[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        O = o[0]
        for x in XS:
            for thru in (0, 1):
                up, dn = O * (1 + x / 100), O * (1 - x / 100)
                k_ = 1.0005 if thru else 1.0
                iu, idn = np.flatnonzero(h >= up * k_), np.flatnonzero(l <= dn / k_)
                a = iu[0] if len(iu) else BIG
                b = idn[0] if len(idn) else BIG
                if a == b or min(a, b) >= len(c) - 1:
                    continue
                mv = 1 if a < b else -1
                i = min(a, b)
                lvl = up if mv == 1 else dn
                e = max(o[i], lvl) if mv == 1 else min(o[i], lvl)
                key = len(rows)
                rows.append(dict(coin=coin, day=t, year=t.year, x=x, thru=thru, mv=mv, hour=g.index[i].hour, q_rng=q.rng[t], q_r12=q.r12[t], key=key))
                P[key] = (sim(o, h, l, c, i, e, -mv, True) - MAKER, sim(o, h, l, c, i, e, -mv, False) - MAKER)
T = pd.DataFrame(rows)
T["alert"] = (T.q_rng >= 2 / 3) & (T.q_r12 >= 2 / 3)
pes = np.array([P[k][0] for k in T.key])
opt = np.array([P[k][1] for k in T.key])
days = np.sort(T.day.unique())
cut = pd.Timestamp(days[int(len(days) * 0.7)])
si = lambda S: SS.index(S)
ti = lambda t: TS.index(t)
nm = lambda v: "none" if v is None or v != v else f"{v}%"


def st(mask, S, Tg, arr=pes):
    s = pd.Series(arr[mask.values, si(S), ti(Tg)], index=T.day[mask].values)
    bd = s.groupby(level=0).mean()
    tt = lambda v: v.mean() / v.std() * np.sqrt(len(v)) if len(v) > 5 and v.std() > 0 else np.nan
    return dict(n=len(s), win=(s > 0).mean() * 100, avg=s.mean(), is_avg=s[s.index < cut].mean(), oos_avg=s[s.index >= cut].mean(), t=tt(bd), is_t=tt(bd[bd.index < cut]), oos_t=tt(bd[bd.index >= cut]), total=s.sum(), s=s, bd=bd)


L = [f"# Fading the first move on alert days — 5-minute candles (python/fade_alert_study.py)\n",
     f"BTC and ETH, {pd.Timestamp(days[0]).date()} → {pd.Timestamp(days[-1]).date()}; in-sample before {cut.date()}. Alert day = previous day's range and last 12 h range both in the widest third of the trailing 365 days. "
     "Limit entry against the first move of X % from the 00:00 UTC open; P&L in % of price after Bybit VIP 3 fees.\n"]
base = (T.thru == 0)
A = base & T.alert
L.append("## Grid on alert days (touch fill, pessimistic entry candle)\n\n| Trigger | Stop | Target | Trades | Profitable | Avg | In-sample | Out-of-sample | IS t | OOS t | Total |\n|---|---|---|---|---|---|---|---|---|---|---|")
G = []
for x in XS:
    for S in SS:
        for Tg in TS:
            r = st(A & (T.x == x), S, Tg)
            G.append(dict(x=x, S=S, T=Tg, **{k: v for k, v in r.items() if k not in ("s", "bd")}))
G = pd.DataFrame(G)
G["mt"] = G[["is_t", "oos_t"]].min(axis=1)
for _, r in G.sort_values("mt", ascending=False).head(15).iterrows():
    L.append(f"| {r.x}% | {nm(r.S)} | {nm(r['T']).replace('none', 'close')} | {int(r.n)} | {r.win:.0f}% | {r.avg:+.3f}% | {r.is_avg:+.3f}% | {r.oos_avg:+.3f}% | {r.is_t:+.1f} | {r.oos_t:+.1f} | {r.total:+.0f}% |")
L.append(f"\n{len(G)} combinations: {((G.is_avg > 0) & (G.oos_avg > 0)).sum()} positive in both halves, {((G.is_t > 2) & (G.oos_t > 2)).sum()} with t > 2 in both, {((G.is_avg < 0) & (G.oos_avg < 0)).sum()} negative in both.\n")
L.append("Average P&L (all alert-day trades) by stop and target, trigger 1 %:\n\n| Stop \\ Target | " + " | ".join(nm(t) if t else "close" for t in TS) + " |\n|" + "---|" * (len(TS) + 1))
for S in SS:
    L.append(f"| {nm(S)} | " + " | ".join(f"{st(A & (T.x == 1), S, t)['avg']:+.3f}%" for t in TS) + " |")

S0, T0, X0 = 1.5, 2, 1
H = A & (T.x == X0)
h = st(H, S0, T0)
L.append(f"\n## The version picked from the 15m search: trigger {X0} %, stop {S0} %, target {T0} %\n")
L.append("| Cut | Trades | Profitable | Avg per trade | t | Total |\n|---|---|---|---|---|---|")


def line(nm_, mask, arr=pes):
    r = st(mask, S0, T0, arr)
    L.append(f"| {nm_} | {r['n']} | {r['win']:.0f}% | {r['avg']:+.3f}% | {r['t']:+.1f} | {r['total']:+.0f}% |")


line("All alert days", H)
line("In-sample", H & (T.day < cut))
line("Out-of-sample", H & (T.day >= cut))
line("Optimistic entry candle", H, opt)
line("Fill only if traded 0.05 % through", (T.thru == 1) & T.alert & (T.x == X0))
line("BTC", H & (T.coin == "btc"))
line("ETH", H & (T.coin == "eth"))
line("First move up (short it)", H & (T.mv == 1))
line("First move down (buy it)", H & (T.mv == -1))
for y in sorted(T.year.unique()):
    line(str(y), H & (T.year == y))
for a, b in ((0, 2), (2, 6), (6, 12), (12, 18), (18, 24)):
    line(f"Trigger at {a:02d}–{b:02d} UTC", H & (T.hour >= a) & (T.hour < b))
line("Stricter alert (both in widest fifth)", base & (T.x == X0) & (T.q_rng >= 0.8) & (T.q_r12 >= 0.8))
line("Looser alert (both in widest half)", base & (T.x == X0) & (T.q_rng >= 0.5) & (T.q_r12 >= 0.5))
line("Previous day wide only (widest third)", base & (T.x == X0) & (T.q_rng >= 2 / 3))
line("Non-alert days (same rules)", base & (T.x == X0) & ~T.alert)
line("Every day (same rules)", base & (T.x == X0))
s = h["s"]
out = pd.Series(np.where(np.isclose(s, T0 - 2 * MAKER), "target", np.where(s <= -S0, "stop", "close")), index=s.index).value_counts(normalize=True) * 100
bd = h["bd"]
eq = bd.cumsum()
dd_ = (eq - eq.cummax()).min()
streak = max((sum(1 for _ in grp) for k, grp in __import__("itertools").groupby(bd < 0) if k), default=0)
rng = np.random.default_rng(1)
boot = np.array([rng.choice(bd.values, len(bd)).mean() for _ in range(5000)])
L.append(f"\nOutcomes: target {out.get('target', 0):.0f}%, stop {out.get('stop', 0):.0f}%, out at the close {out.get('close', 0):.0f}%. "
         f"Trading days: {len(bd)} ({len(bd) / ((pd.Timestamp(days[-1]) - pd.Timestamp(days[0])).days / 365.25):.0f} per year). Per-day average {bd.mean():+.3f}% "
         f"(bootstrap 95% range {np.percentile(boot, 2.5):+.3f}% to {np.percentile(boot, 97.5):+.3f}%; share of resamples above zero {np.mean(boot > 0) * 100:.0f}%). "
         f"Deepest drawdown {dd_:.1f}% of price, longest run of losing days {streak}.")
open("results/fade_alert_study.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
