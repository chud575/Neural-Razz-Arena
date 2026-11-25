"""
What the 5-minute chart looks like on days BTC / ETH moved 5 % or more (open to close, UTC day), against quiet days.

Data: fetch_5m_days.py (Coinbase 5m candles for every ±5 % day and a sample of quiet days, |move| < 2 %, each with the
12 hours before it). Everything is described relative to the day's direction ("with" = the way the day finished).

    python big_day_study.py <data_dir>   -> results/big_day_features.csv, results/big_day_harmonics.csv
"""
import math
import sys

import numpy as np
import pandas as pd

from dtdb_backtest import pivots
from impulse_study import find_legs
from market_structure import structure
from srflip_backtest import atr

WARM = 144          # 12 h of 5m candles before the day
N_RECLAIM = 6       # a sweep must close back within 30 minutes


def first_breach(h, l, c, level, low_side, start, end):
    """First candle in [start, end) that trades beyond `level`. Returns (bar, reclaimed within N_RECLAIM candles) or (None, False)."""
    seg = (l[start:end] < level) if low_side else (h[start:end] > level)
    idx = np.flatnonzero(seg)
    if not len(idx):
        return None, False
    i = start + int(idx[0])
    j = min(len(c), i + N_RECLAIM + 1)
    rec = bool((c[i:j] > level).any()) if low_side else bool((c[i:j] < level).any())
    return i, rec


def harmonics(h, l, c, L=3, min_xa=0.004):
    """XABCD patterns from alternating swings. Returns list of dict(name, d, bar(confirm), D, X, A, C)."""
    ph, pl = pivots(h, l, L)
    seq, out = [], []
    for i in range(len(c)):
        ch = False
        for tp, arr in ((1, ph), (-1, pl)):
            if not math.isnan(arr[i]):
                if seq and seq[-1][0] == tp:
                    if (tp == 1 and arr[i] > seq[-1][1]) or (tp == -1 and arr[i] < seq[-1][1]):
                        seq[-1] = (tp, arr[i], i - L)
                        ch = True
                else:
                    seq.append((tp, arr[i], i - L))
                    del seq[:-6]
                    ch = True
        if ch and len(seq) >= 5:
            (tx, X, _), (_, A, _), (_, B, _), (_, C, _), (td, Dp, db) = seq[-5:]
            d = 1 if td == -1 else -1                      # bullish when D is a low
            XA, AB, BC, AD = abs(A - X), abs(B - A), abs(C - B), abs(Dp - A)
            if XA <= 0 or AB <= 0 or XA / X < min_xa:
                continue
            ab, bc, ad = AB / XA, BC / AB, AD / XA
            if not 0.382 <= bc <= 0.886:
                continue
            name = None
            if abs(ab - 0.618) <= 0.05 and abs(ad - 0.786) <= 0.05:
                name = "Gartley"
            elif 0.382 <= ab <= 0.5 and abs(ad - 0.886) <= 0.05:
                name = "Bat"
            elif abs(ab - 0.786) <= 0.05 and abs(ad - 1.27) <= 0.07:
                name = "Butterfly"
            elif 0.382 <= ab <= 0.618 and abs(ad - 1.618) <= 0.1:
                name = "Crab"
            if name:
                out.append(dict(name=name, d=d, bar=i, D=Dp, A=A, X=X, XA=XA, AD=AD))
    return out


def main():
    Dd = sys.argv[1]
    rows, hrows = [], []
    for coin in ("btc", "eth"):
        daily = pd.read_csv(f"{Dd}/{coin}_1d.csv", index_col=0, parse_dates=True)
        f = pd.read_csv(f"{Dd}/{coin}_5m_days.csv", parse_dates=["time"])
        for day, g in f.groupby("day"):
            t0 = pd.Timestamp(day)
            g = g.set_index("time").sort_index()
            g = g[~g.index.duplicated()]
            full = g.reindex(pd.date_range(t0 - pd.Timedelta(hours=12), t0 + pd.Timedelta(hours=24) - pd.Timedelta(minutes=5), freq="5min"))
            if full.close.loc[t0:].notna().sum() < 250 or full.close.loc[:t0 - pd.Timedelta(minutes=5)].notna().sum() < 100:
                continue
            full["close"] = full.close.ffill().bfill()
            for k in ("open", "high", "low"):
                full[k] = full[k].fillna(full.close)
            full["volume"] = full.volume.fillna(0.0)
            o, h, l, c, v = (full[k].to_numpy(float) for k in ("open", "high", "low", "close", "volume"))
            n = len(c)
            s = WARM
            O, C = o[s], c[-1]
            ret = (C / O - 1) * 100
            d = 1 if ret >= 0 else -1
            kind = g.kind.iloc[0]
            prev = daily.index.get_indexer([t0])[0] - 1
            pdh, pdl = (daily.high.iloc[prev], daily.low.iloc[prev]) if prev >= 0 else (np.nan, np.nan)
            ci, hi_, lo_ = c[s:], h[s:], l[s:]
            row = dict(coin=coin, day=day, kind=kind, ret=ret, d=d, year=t0.year)
            # A. time on the wrong side of the open
            wrong = (ci < O) if d == 1 else (ci > O)
            row["wrong_share"] = wrong.mean() * 100
            row["wrong_hours"] = wrong.sum() / 12
            row["last_wrong_hour"] = (np.flatnonzero(wrong)[-1] / 12) if wrong.any() else -1.0
            row["never_wrong"] = int(not wrong.any())
            row["adverse_pct"] = ((O - lo_.min()) / O if d == 1 else (hi_.max() - O) / O) * 100
            row["range_pct"] = (hi_.max() - lo_.min()) / O * 100
            row["close_in_range"] = ((C - lo_.min()) / (hi_.max() - lo_.min()) if d == 1 else (hi_.max() - C) / (hi_.max() - lo_.min())) * 100
            # B. timing
            row["start_ext_hour"] = (int(lo_.argmin()) if d == 1 else int(hi_.argmax())) / 12      # the extreme the move started from
            row["end_ext_hour"] = (int(hi_.argmax()) if d == 1 else int(lo_.argmin())) / 12
            hourly = c[s + 11::12][:24]
            hopen = np.r_[O, hourly[:-1]]
            hmove = d * (hourly - hopen) / O * 100
            row["big_hour"] = int(hmove.argmax())
            row["big_hour_pct"] = hmove.max()
            row["big_hour_share"] = hmove.max() / abs(ret) * 100 if abs(ret) > 0 else np.nan
            for hh in (1, 2, 4, 8, 12, 16, 20):
                row[f"done_{hh}h"] = d * (c[s + hh * 12 - 1] - O) / abs(C - O) * 100 if C != O else np.nan
                row[f"agree_{hh}h"] = int(d * (c[s + hh * 12 - 1] - O) > 0)
            # C. early tells
            row["range_1h"] = (hi_[:12].max() - lo_[:12].min()) / O * 100
            row["range_4h"] = (hi_[:48].max() - lo_[:48].min()) / O * 100
            pv = v[:s].mean()
            row["vol_1h_ratio"] = v[s:s + 12].mean() / pv if pv > 0 else np.nan
            row["vol_4h_ratio"] = v[s:s + 48].mean() / pv if pv > 0 else np.nan
            row["prior12_range"] = (h[:s].max() - l[:s].min()) / O * 100
            # D. liquidity sweeps. "against" side = the side the day did NOT finish on (lows on an up day)
            lv = {"pd": (pdl, pdh), "prior12h": (l[:s].min(), h[:s].max()), "asia": (lo_[:96].min(), hi_[:96].max())}
            for name, (lo_lv, hi_lv) in lv.items():
                st = s + 96 if name == "asia" else s
                for side, level, low_side in (("against", lo_lv if d == 1 else hi_lv, d == 1), ("with", hi_lv if d == 1 else lo_lv, d != 1)):
                    if np.isnan(level):
                        continue
                    i, rec = first_breach(h, l, c, level, low_side, st, n)
                    row[f"{name}_{side}_taken"] = int(i is not None)
                    row[f"{name}_{side}_swept"] = int(i is not None and rec)
                    row[f"{name}_{side}_hour"] = (i - s) / 12 if i is not None else np.nan
                    if side == "against" and i is not None:
                        ext = int(lo_.argmin()) if d == 1 else int(hi_.argmax())
                        row[f"{name}_sweep_is_extreme"] = int(rec and abs((i - s) - ext) <= 6)
            # E. patterns
            a50 = atr(h, l, c, 50)
            legs = [x for x in find_legs(h, l, c) if x[5] >= s]
            row["legs"] = len(legs)
            row["legs_with"] = sum(1 for x in legs if x[4] == d)
            row["first_leg_with"] = int(legs[0][4] == d) if legs else np.nan
            row["first_leg_hour"] = (legs[0][5] - s) / 12 if legs else np.nan
            cs = pd.Series(c)
            basis = cs.rolling(20).mean()
            dev = 2 * cs.rolling(20).std(ddof=0)
            pc = cs.shift(1)
            tr = pd.concat([pd.Series(h) - pd.Series(l), (pd.Series(h) - pc).abs(), (pd.Series(l) - pc).abs()], axis=1).max(axis=1)
            sq = ((dev < 1.5 * tr.rolling(20).mean())).to_numpy()
            row["squeeze_share"] = sq[s:].mean() * 100
            bh = s + row["big_hour"] * 12
            row["squeeze_before_big_hour"] = int(sq[max(0, bh - 12):bh].any())
            row["squeeze_at_open"] = int(sq[s - 6:s + 6].any())
            stt = structure(h, l, c, 5)
            ev = stt["ev"][s:]
            nz_ = np.flatnonzero(ev != 0)
            row["first_break_with"] = int(np.sign(ev[nz_[0]]) == d) if len(nz_) else np.nan
            row["bos_with"] = int(((np.sign(ev) == d) & (np.abs(ev) == 1)).sum())
            row["bos_against"] = int(((np.sign(ev) == -d) & (np.abs(ev) == 1)).sum())
            row["choch"] = int((np.abs(ev) == 2).sum())
            up_gap = (l[2:] > h[:-2])[s - 2:]
            dn_gap = (h[2:] < l[:-2])[s - 2:]
            row["fvg_with"] = int((up_gap if d == 1 else dn_gap).sum())
            row["fvg_against"] = int((dn_gap if d == 1 else up_gap).sum())
            hs = [x for x in harmonics(h, l, c) if x["bar"] >= s]
            row["harmonics"] = len(hs)
            row["harmonics_with"] = sum(1 for x in hs if x["d"] == d)
            for x in hs:
                # outcome: 38.2 % of AD back toward A before 25 % of XA beyond D (from the confirmation close)
                e = c[x["bar"]]
                tgt = x["D"] + x["d"] * 0.382 * x["AD"]
                stp = x["D"] - x["d"] * 0.25 * x["XA"]
                res = np.nan
                if (tgt - e) * x["d"] > 0 and (e - stp) * x["d"] > 0:
                    for m in range(x["bar"] + 1, n):
                        if (l[m] <= stp) if x["d"] == 1 else (h[m] >= stp):
                            res = 0
                            break
                        if (h[m] >= tgt) if x["d"] == 1 else (l[m] <= tgt):
                            res = 1
                            break
                    exp_ = abs(e - stp) / (abs(e - stp) + abs(tgt - e))
                else:
                    exp_ = np.nan
                hrows.append(dict(coin=coin, day=day, kind=kind, day_d=d, name=x["name"], d=x["d"], with_day=int(x["d"] == d), hour=(x["bar"] - s) / 12, win=res, exp=exp_))
            rows.append(row)
        print("done", coin, file=sys.stderr, flush=True)
    pd.DataFrame(rows).to_csv("results/big_day_features.csv", index=False)
    pd.DataFrame(hrows).to_csv("results/big_day_harmonics.csv", index=False)


if __name__ == "__main__":
    main()
