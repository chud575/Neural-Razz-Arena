"""
The Strat — "failed 2" reversal (Alex's Options: "if a bar fails one side of the range it is attempting to take the
other side"). Mirrors pine/strat_failed2.pine.

Signal (long; shorts are the mirror image), read at the close of bar i:
  prev    the bar took out the PREVIOUS bar's low and closed back above it (and still below the previous bar's high).
          Reference range = the previous bar. `green`: the bar must also close above its open.
  mother  the last `min_inside` (2) or more bars were all inside one earlier "mother" bar; this bar took out the mother
          bar's low and closed back above it (below the mother high). Reference range = the mother bar.
Higher-timeframe filter (optional): the higher-timeframe candle in progress has already traded below the previous
  higher-timeframe candle's low and this bar closes back above that low (and below that candle's high) — the same
  phenomenon one level up, entered with the lower-timeframe signal.
Entry at the close of the signal bar. Stop = the signal bar's low.
Exits   other     target = the other side of the reference range
        htf       target = the other side of the previous higher-timeframe candle (needs the filter)
        2R        target = 2 × risk
        t1trail   half off at the "other" target, then the stop trails under each previous bar's low
        trail     no target: the stop trails under each previous bar's low from the first bar after entry
        (stops only ever move toward price; max 200 bars; stop first if stop and target are in the same bar)
Costs: Bybit VIP 3 futures (taker entry, maker at a target, taker at a stop, funding). One trade at a time.
Baseline: the same entry/stop/exit rules on RANDOM bars (same reference range), so a row only matters if it beats it.
IS = first 70 % of history, OOS = last 30 %.

    python strat_failed2.py <data_dir>     -> results/strat_failed2_trades.csv (report: strat_failed2_report.py)
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd

import run_btc_sweep as S

COINS = ["btc", "eth", "avax", "xrp"]
TFS = ["15m", "1h", "4h", "1d"]
HTFS = {"15m": ["1h", "4h", "1D"], "1h": ["4h", "1D", "1W"], "4h": ["1D", "1W"], "1d": ["1W"]}
EXITS = ("other", "htf", "2R", "t1trail", "trail")
MAXBARS = 200
MIN_INSIDE = 2


def htf_levels(df, rule):
    """Per chart bar: previous HTF candle's high/low, and the running high/low of the HTF candle in progress."""
    idx = df.index
    key = (idx - pd.to_timedelta(idx.weekday, unit="D")).floor("1D") if rule == "1W" else idx.floor(rule)
    g = df.groupby(key)
    hi, lo = g["high"].max(), g["low"].min()
    ph = pd.Series(key).map(hi.shift(1)).to_numpy(float)
    pl = pd.Series(key).map(lo.shift(1)).to_numpy(float)
    return ph, pl, g["high"].cummax().to_numpy(float), g["low"].cummin().to_numpy(float)


def mother_levels(h, l):
    """State BEFORE each bar: mother bar high/low and how many bars have been inside it."""
    n = len(h)
    mh, ml, cnt = np.full(n, np.nan), np.full(n, np.nan), np.zeros(n, int)
    H, L, k = h[0], l[0], 0
    for i in range(1, n):
        mh[i], ml[i], cnt[i] = H, L, k
        if h[i] <= H and l[i] >= L:
            k += 1
        else:
            H, L, k = h[i], l[i], 0
    return mh, ml, cnt


def simulate(o, h, l, c, i, d, tgt, mode, bar_h):
    """Returns (net R, gross R, exit bar, hit target?). tgt = price target (nan for 'trail')."""
    e = c[i]
    stop = l[i] if d == 1 else h[i]
    risk = abs(e - stop)
    if risk <= 0:
        return None
    if mode == "2R":
        tgt = e + d * 2 * risk
    if mode != "trail" and (math.isnan(tgt) or (tgt - e) * d <= 0):
        return None
    trail = mode == "trail"
    half_done, r, cost = False, 0.0, 0.0
    size = 1.0
    end = min(len(c), i + 1 + MAXBARS)
    j = i + 1
    while j < end:
        if trail and j > i + 1:
            stop = max(stop, l[j - 1]) if d == 1 else min(stop, h[j - 1])
        if (l[j] <= stop) if d == 1 else (h[j] >= stop):
            px = min(o[j], stop) if d == 1 else max(o[j], stop)
            r += size * d * (px - e) / risk
            cost += size * S.cost_fraction(d, False, (j - i) * bar_h)
            return r - cost * e / risk, r, j, half_done
        if not trail and ((h[j] >= tgt) if d == 1 else (l[j] <= tgt)):
            px = max(o[j], tgt) if d == 1 else min(o[j], tgt)
            if mode == "t1trail":
                r += 0.5 * d * (px - e) / risk
                cost += 0.5 * S.cost_fraction(d, True, (j - i) * bar_h)
                size, half_done, trail = 0.5, True, True
            else:
                r += d * (px - e) / risk
                cost += S.cost_fraction(d, True, (j - i) * bar_h)
                return r - cost * e / risk, r, j, True
        j += 1
    j = end - 1
    r += size * d * (c[j] - e) / risk
    cost += size * S.cost_fraction(d, False, (j - i) * bar_h)
    return r - cost * e / risk, r, j, half_done


def main():
    D = sys.argv[1]
    S.FEE_MODEL = "futures"
    rng = np.random.default_rng(7)
    rows = []
    for coin in COINS:
        S.DATA.clear()
        S.load(D, TFS, coin)
        for tf in TFS:
            df = S.DATA[tf]
            o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
            n = len(c)
            bar_h = df.index.to_series().diff().median().total_seconds() / 3600
            split = int(n * S.SPLIT)
            ph1, pl1 = np.roll(h, 1), np.roll(l, 1)
            ph1[0] = pl1[0] = np.nan
            mh, ml, cnt = mother_levels(h, l)
            sig = {}
            for d in (1, -1):
                took = (l < pl1) if d == 1 else (h > ph1)
                back = ((c > pl1) & (c < ph1))
                sig[("prev", d)] = took & back
                sig[("prev green", d)] = took & back & ((c > o) if d == 1 else (c < o))
                tookm = (l < ml) if d == 1 else (h > mh)
                sig[("mother", d)] = (cnt >= MIN_INSIDE) & tookm & (c > ml) & (c < mh)
            base = np.zeros(n, bool)
            base[rng.choice(np.arange(2, n - 2), size=min(n - 4, 6000), replace=False)] = True
            sig[("Baseline (random bar)", 1)] = base & (c > pl1) & (c < ph1)
            sig[("Baseline (random bar)", -1)] = sig[("Baseline (random bar)", 1)]
            filt = {"none": None}
            for rule in HTFS[tf]:
                filt[rule] = htf_levels(df, rule)
            for name in ("prev", "prev green", "mother", "Baseline (random bar)"):
                for fname, F in filt.items():
                    ok = {}
                    for d in (1, -1):
                        s = sig[(name, d)].copy()
                        if F is not None:
                            pH, pL, rH, rL = F
                            s &= ((rL < pL) & (c > pL) & (c < pH)) if d == 1 else ((rH > pH) & (c < pH) & (c > pL))
                        ok[d] = s
                    idx = np.flatnonzero(ok[1] | ok[-1])
                    for mode in EXITS:
                        if mode == "htf" and F is None:
                            continue
                        busy_until = -1
                        for i in idx:
                            if i < 2 or i >= n - 1:
                                continue
                            for d in (1, -1):
                                if not ok[d][i]:
                                    continue
                                if name != "Baseline (random bar)" and i <= busy_until:
                                    continue
                                if mode == "htf":
                                    tgt = F[0][i] if d == 1 else F[1][i]
                                elif name == "mother":
                                    tgt = mh[i] if d == 1 else ml[i]
                                else:
                                    tgt = ph1[i] if d == 1 else pl1[i]
                                res = simulate(o, h, l, c, i, d, tgt, mode, bar_h)
                                if res is None:
                                    continue
                                net, gross, xb, hit = res
                                busy_until = xb
                                rows.append((coin, tf, name, fname, mode, d, "IS" if i < split else "OOS", net, gross, hit,
                                             xb - i, abs(c[i] - (l[i] if d == 1 else h[i])) / c[i] * 100))
            print("done", coin, tf, file=sys.stderr, flush=True)
    df = pd.DataFrame(rows, columns=["coin", "tf", "signal", "htf", "exit", "d", "period", "r", "gross", "hit", "bars", "risk_pct"])
    df.to_csv("results/strat_failed2_trades.csv", index=False)
    print("trades", len(df), file=sys.stderr)


if __name__ == "__main__":
    main()
