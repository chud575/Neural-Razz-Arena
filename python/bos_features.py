"""
Which conditions at the entry help the 1h break-of-structure strategy? (feature screen)

Base trade: BOS at a 1h close, stop at the latest swing, 2R target, after Bybit VIP 3 fees (python/ms_continuation.py).
For every trade a set of readings is taken AT THE ENTRY CANDLE'S CLOSE (nothing later), each turned so that a higher
value means "more in the trade's direction" where that makes sense. Trades are split into five equal groups by each
reading (cut points from the first 70 % of history only) and the average result of each group is compared in the
first 70 % (IS) and the last 30 % (OOS). A reading only counts if it sorts trades the same way in both.
Volume is Coinbase spot volume. "CVD" is an estimate from candles (volume × (close − open) / (high − low)), not true
trade-by-trade delta, which this data does not have.

    python bos_features.py <data_dir>   -> results/bos_features.csv, results/bos_features.md
"""
import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S
from market_structure import structure
from srflip_backtest import atr


def rsi(c, n=14):
    d = pd.Series(c).diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return (100 - 100 / (1 + up / dn)).to_numpy()


def adx(h, l, c, n=14):
    hs, ls, cs = pd.Series(h), pd.Series(l), pd.Series(c)
    up, dn = hs.diff(), -ls.diff()
    plus = np.where((up > dn) & (up > 0), up, 0.0)
    minus = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = pd.concat([hs - ls, (hs - cs.shift()).abs(), (ls - cs.shift()).abs()], axis=1).max(axis=1)
    a = tr.ewm(alpha=1 / n, adjust=False).mean()
    pdi = 100 * pd.Series(plus).ewm(alpha=1 / n, adjust=False).mean() / a
    mdi = 100 * pd.Series(minus).ewm(alpha=1 / n, adjust=False).mean() / a
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(alpha=1 / n, adjust=False).mean().to_numpy(), (pdi - mdi).to_numpy()


rows = []
for coin in ("btc", "eth", "avax", "xrp"):
    df = pd.read_csv(f"{sys.argv[1]}/{coin}_1h.csv", index_col=0, parse_dates=True)
    df = df[(df[["open", "high", "low", "close"]] > 0).all(axis=1)]
    o, h, l, c, v = (df[k].to_numpy(float) for k in ("open", "high", "low", "close", "volume"))
    n = len(c)
    split = int(n * S.SPLIT)
    cs, vs = pd.Series(c), pd.Series(v)
    a14 = atr(h, l, c, 14)
    nv = v / vs.rolling(50).mean().to_numpy() * 100
    delta = v * (c - o) / np.where(h - l > 0, h - l, np.nan)
    cvd20 = (pd.Series(delta).rolling(20).sum() / vs.rolling(20).sum()).to_numpy()
    cvd100 = (pd.Series(delta).rolling(100).sum() / vs.rolling(100).sum()).to_numpy()
    r14 = rsi(c)
    adx14, di = adx(h, l, c)
    e50, e200 = cs.ewm(span=50, adjust=False).mean().to_numpy(), cs.ewm(span=200, adjust=False).mean().to_numpy()
    atrp = pd.Series(a14 / c)
    vol_rank = atrp.rolling(500).rank(pct=True).to_numpy()
    hi100, lo100 = pd.Series(h).rolling(100).max().to_numpy(), pd.Series(l).rolling(100).min().to_numpy()
    ret24, ret168 = (cs / cs.shift(24) - 1).to_numpy(), (cs / cs.shift(168) - 1).to_numpy()
    bbw = (cs.rolling(20).std() / cs.rolling(20).mean())
    bb_rank = bbw.rolling(500).rank(pct=True).to_numpy()
    st = structure(h, l, c, 5)
    busy, streak, last_d = -1, 0, 0
    for i in np.flatnonzero(np.abs(st["ev"]) >= 1):
        d = 1 if st["ev"][i] > 0 else -1
        if abs(st["ev"][i]) == 2:                      # CHoCH: structure flips, the BOS count restarts
            streak, last_d = 0, d
            continue
        streak = streak + 1 if d == last_d else 1
        last_d = d
        if i <= busy or i >= n - 1 or i < 520:
            continue
        e = c[i]
        stop = st["lastL"][i] if d == 1 else st["lastH"][i]
        lvl = st["lastH"][i - 1] if d == 1 else st["lastL"][i - 1]
        if math.isnan(stop) or (e - stop) * d <= 0 or math.isnan(a14[i]):
            continue
        R0 = abs(e - stop)
        tp = e + d * 2 * R0
        px, at_t, m = None, False, i + 1
        end = min(n, i + 301)
        while m < end:
            if (l[m] <= stop) if d == 1 else (h[m] >= stop):
                px = min(o[m], stop) if d == 1 else max(o[m], stop)
                break
            if (h[m] >= tp) if d == 1 else (l[m] <= tp):
                px, at_t = (max(o[m], tp) if d == 1 else min(o[m], tp)), True
                break
            m += 1
        if px is None:
            m = end - 1
            px = c[m]
        busy = m
        r = d * (px - e) / R0 - (S.TAKER + (S.MAKER if at_t else S.TAKER) + d * S.FUNDING_8H * (m - i) / 8) * e / R0
        A = a14[i]
        ts = df.index[i]
        rows.append(dict(coin=coin, period="IS" if i < split else "OOS", d=d, r=r,
                         norm_volume=nv[i], cvd_20=d * cvd20[i], cvd_100=d * cvd100[i],
                         rsi_aligned=r14[i] if d == 1 else 100 - r14[i], adx=adx14[i], di_aligned=d * di[i],
                         ema200_dist_atr=d * (e - e200[i]) / A, ema50_over_200=d * (e50[i] - e200[i]) / A,
                         volatility_rank=vol_rank[i], bb_width_rank=bb_rank[i],
                         stop_in_atr=R0 / A, stop_pct=R0 / e * 100, body_in_atr=abs(c[i] - o[i]) / A, close_past_level_atr=d * (e - lvl) / A,
                         range_pos_100=(e - lo100[i]) / (hi100[i] - lo100[i]) if d == 1 else (hi100[i] - e) / (hi100[i] - lo100[i]),
                         ret_24h=d * ret24[i] * 100, ret_7d=d * ret168[i] * 100, bos_in_a_row=streak,
                         hour_utc=ts.hour, weekday=ts.weekday(), bars_since_swing=i - (st["lastLb"][i] if d == 1 else st["lastHb"][i])))
t = pd.DataFrame(rows)
t.to_csv("results/bos_features.csv", index=False)
feats = [c for c in t.columns if c not in ("coin", "period", "d", "r", "hour_utc", "weekday")]
IS, OOS = t[t.period == "IS"], t[t.period == "OOS"]
out = []
for f in feats:
    q = np.unique(IS[f].quantile([0.2, 0.4, 0.6, 0.8]).to_numpy())
    bi, bo = np.digitize(IS[f], q), np.digitize(OOS[f], q)
    gi = IS.r.groupby(bi).mean().reindex(range(len(q) + 1))
    go = OOS.r.groupby(bo).mean().reindex(range(len(q) + 1))
    rho_i = IS[[f, "r"]].corr(method="spearman").iloc[0, 1]
    rho_o = OOS[[f, "r"]].corr(method="spearman").iloc[0, 1]
    out.append(dict(feature=f, IS_low=gi.iloc[0], IS_high=gi.iloc[-1], OOS_low=go.iloc[0], OOS_high=go.iloc[-1],
                    IS_spread=gi.iloc[-1] - gi.iloc[0], OOS_spread=go.iloc[-1] - go.iloc[0], rho_IS=rho_i, rho_OOS=rho_o,
                    IS_groups=" ".join(f"{x:+.2f}" for x in gi), OOS_groups=" ".join(f"{x:+.2f}" for x in go)))
res = pd.DataFrame(out).sort_values("IS_spread", key=abs, ascending=False)
pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 60)
print(len(t), "trades; base IS %.3f OOS %.3f" % (IS.r.mean(), OOS.r.mean()))
print(res.round(3).to_string(index=False))
for f in ("hour_utc", "weekday"):
    g = t.groupby([f, "period"]).r.mean().unstack().round(2)
    g["n"] = t.groupby(f).size()
    print(g.T.to_string())
res.to_csv("results/bos_features_summary.csv", index=False)
