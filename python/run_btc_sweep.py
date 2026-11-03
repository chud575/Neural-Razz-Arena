"""
BTC parameter sweep for all three strategies on 15m / 1h / 4h / 1D, with an in-sample / out-of-sample split.

Method
  * Each timeframe's history is split by time: first 70 % = in-sample (IS), last 30 % = out-of-sample (OOS).
  * Every configuration is backtested once over the full history; trades are assigned to IS/OOS by signal time.
  * Costs: COST_RT (default 0.2 % round trip = 0.1 % per side) is charged on every trade, converted to R
    (cost_R = COST_RT * entry / risk), so tight stops pay proportionally more.
  * Configurations are ranked ONLY on IS (t-stat of net R per trade, minimum trade count). The OOS columns show
    how those picks did on data the ranking never saw. Direction (both / longs / shorts) is split from the same
    run (approximation: a longs-only run could also take trades skipped while a short was open).
  * Finalists get a random-entry benchmark inside the OOS window (same direction mix, stop distance, R:R, costs).

    python run_btc_sweep.py --data DIR --out results/btc_sweep [--tfs 1d,4h,1h,15m] [--strategies dtdb,srflip,megaphone]
DIR must contain btc_1d.csv, btc_1h.csv, btc_15m.csv (fetch_coinbase.py); 4h is resampled from 1h.
"""
from __future__ import annotations

import argparse
import itertools
import math
import multiprocessing as mp
import os
import sys
import time

import numpy as np
import pandas as pd

import dtdb_backtest as DT
import megaphone_backtest as MP
import srflip_backtest as SR

COST_RT = 0.002
SPLIT = 0.70
MIN_IS = {"1d": 15, "4h": 50, "1h": 80, "15m": 120}
HTF_FOR = {"15m": ("4h", "D"), "1h": ("D", "W"), "4h": ("D", "W"), "1d": ("W", "ME")}
SR.HTF_SECONDS.update({"4h": 4 * 3600, "h": 3600, "1h": 3600})

DATA: dict[str, pd.DataFrame] = {}


def load(data_dir: str, tfs):
    for tf in tfs:
        if tf == "4h":
            h = pd.read_csv(os.path.join(data_dir, "btc_1h.csv"), index_col=0, parse_dates=True)
            df = h.resample("4h").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
        else:
            df = pd.read_csv(os.path.join(data_dir, f"btc_{tf}.csv"), index_col=0, parse_dates=True)
        df = df[["open", "high", "low", "close"]]
        DATA[tf] = df[(df > 0).all(axis=1)]


# ───────────────────────────── grids ─────────────────────────────
EXITS = [("single", dict(tp1_pct=0.0)), ("TP1 1R 50% BE", dict(tp1_pct=50.0, tp1_rr=1.0, be_after_tp1=True))]


def grid_dtdb(tf):
    setups = [("B+Mid", dict(use_entry1=True, entry2_mode="midpoint")), ("B", dict(use_entry1=True, entry2_mode="off")),
              ("Retest", dict(use_entry1=False, entry2_mode="retest")),
              ("RetestConf", dict(use_entry1=False, entry2_mode="retest_confirm")),
              ("B+Retest", dict(use_entry1=True, entry2_mode="retest"))]
    for piv, tol, depth, (sn, s), rr, trend, (en, e) in itertools.product(
            (3, 5, 8), (0.3, 0.6, 1.0), (0.5, 1.0, 2.0), setups, (1.5, 2.0, 3.0), ("off", "sma"), EXITS):
        yield (f"piv{piv} tol{tol} depth{depth} {sn} {rr:g}R trend:{trend} exit:{en}",
               dict(piv_len=piv, tol_pct=tol, min_depth=depth, rr=rr, trend_filter=trend, **s, **e))


def grid_srflip(tf):
    ha, hb = HTF_FOR[tf]
    levels = [("chart", dict(level_src="chart")), (f"htf:{ha}", dict(level_src="htf", htf=ha)),
              (f"htf:{hb}", dict(level_src="htf", htf=hb)),
              (f"chart+{ha} merged>=2", dict(level_src="both", htf=ha, merge_pct=0.5, min_touches=2))]
    for piv, mode, rr, tries, (ln, lv), trend, (en, e) in itertools.product(
            (3, 5, 8), ("touch", "rejection", "sweep"), (1.5, 2.0, 3.0), (1, 3), levels, ("off", "sma"), EXITS):
        yield (f"piv{piv} {mode} {rr:g}R tries{tries} levels:{ln} trend:{trend} exit:{en}",
               dict(piv_len=piv, entry_mode=mode, rr=rr, max_tries=tries, trend_filter=trend, **lv, **e))


def grid_megaphone(tf):
    combos = []
    for entry in ("rejection", "touch"):
        for rr in (1.5, 2.0, 3.0):
            combos.append((f"fade-{entry} {rr:g}R", dict(mode="fade", fade_entry=entry, target="rr", rr=rr)))
        for tg in ("midline", "opposite"):
            combos.append((f"fade-{entry} {tg}", dict(mode="fade", fade_entry=entry, target=tg)))
    for be in ("close", "retest"):
        for rr in (1.5, 2.0, 3.0):
            combos.append((f"BO-{be} {rr:g}R", dict(mode="breakout", bo_entry=be, bo_target="rr", rr=rr)))
        combos.append((f"BO-{be} measured", dict(mode="breakout", bo_entry=be, bo_target="measured")))
    for rr in (1.5, 2.0, 3.0):
        combos.append((f"failedBO {rr:g}R", dict(mode="none", failed_bo=True, target="rr", rr=rr)))
    combos.append(("failedBO midline", dict(mode="none", failed_bo=True, target="midline")))
    for piv, npv, exp, (cn, c), trend, (en, e) in itertools.product(
            (3, 5, 8), (4, 5), (0.0, 0.5), combos, ("off", "sma"), EXITS):
        yield (f"piv{piv} swings{npv} expand{exp} {cn} trend:{trend} exit:{en}",
               dict(piv_len=piv, min_pivots=npv, min_expand_atr=exp, trend_filter=trend, **c, **e))


STRATS = {"dtdb": (DT, DT.Params, grid_dtdb), "srflip": (SR, SR.SRParams, grid_srflip),
          "megaphone": (MP, MP.MPParams, grid_megaphone)}


# ───────────────────────────── evaluation ─────────────────────────────
def net_r(t) -> float:
    risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
    return t.r - (COST_RT * t.entry_px / risk if risk > 0 else 0.0)


def summ(rs: list[float]) -> dict:
    n = len(rs)
    if n == 0:
        return dict(n=0, avg=math.nan, sum=0.0, win=math.nan, t=math.nan)
    a = np.array(rs)
    sd = a.std(ddof=1) if n > 1 else math.nan
    return dict(n=n, avg=a.mean(), sum=a.sum(), win=(a > 0).mean() * 100,
                t=a.mean() / sd * math.sqrt(n) if sd and sd > 0 else math.nan)


def run_one(job):
    strat, tf, name, kw = job
    mod, P, _ = STRATS[strat]
    df = DATA[tf]
    split_t = df.index[int(len(df) * SPLIT)]
    res = mod.backtest(df, P(**kw), "BTC")
    out = []
    for dname, sel in (("both", lambda t: True), ("longs", lambda t: t.direction == 1), ("shorts", lambda t: t.direction == -1)):
        tr = [t for t in res.trades if sel(t)]
        is_ = summ([net_r(t) for t in tr if t.signal_time < split_t])
        oos = summ([net_r(t) for t in tr if t.signal_time >= split_t])
        gross_is = np.mean([t.r for t in tr if t.signal_time < split_t]) if is_["n"] else math.nan
        out.append(dict(strategy=strat, tf=tf, config=name, direction=dname,
                        is_n=is_["n"], is_avg=is_["avg"], is_sum=is_["sum"], is_win=is_["win"], is_t=is_["t"], is_gross=gross_is,
                        oos_n=oos["n"], oos_avg=oos["avg"], oos_sum=oos["sum"], oos_win=oos["win"], oos_t=oos["t"]))
    return out


def random_oos_control(tf, trades, rr_of, reps=20, seed=0):
    """Random entries inside the OOS window: same direction, stop distance (%), reward:risk, costs."""
    rng = np.random.default_rng(seed)
    df = DATA[tf]
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    n = len(c)
    start = int(n * SPLIT)
    out = []
    for t in trades:
        risk = t.risk if not math.isnan(t.risk) and t.risk > 0 else abs(t.entry_px - t.stop_px)
        dist = risk / t.entry_px
        rr = rr_of(t)
        for _ in range(reps):
            i = int(rng.integers(start, n - 2))
            e, d = c[i], t.direction
            stop = e * (1 - d * dist)
            tgt = e + d * rr * abs(e - stop)
            for j in range(i + 1, n):
                if (l[j] <= stop) if d == 1 else (h[j] >= stop):
                    px = min(o[j], stop) if d == 1 else max(o[j], stop)
                    out.append(d * (px - e) / abs(e - stop) - COST_RT / dist); break
                if (h[j] >= tgt) if d == 1 else (l[j] <= tgt):
                    px = max(o[j], tgt) if d == 1 else min(o[j], tgt)
                    out.append(d * (px - e) / abs(e - stop) - COST_RT / dist); break
    return float(np.mean(out)) if out else math.nan


def fmt(v, f="{:+.3f}"):
    return "–" if v is None or (isinstance(v, float) and math.isnan(v)) else f.format(v)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="results/btc_sweep")
    ap.add_argument("--tfs", default="1d,4h,1h,15m")
    ap.add_argument("--strategies", default="dtdb,srflip,megaphone")
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    a = ap.parse_args(argv)
    tfs = a.tfs.split(",")
    load(a.data, tfs)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)

    rows = []
    for strat in a.strategies.split(","):
        for tf in tfs:
            jobs = [(strat, tf, name, kw) for name, kw in STRATS[strat][2](tf)]
            t0 = time.time()
            with mp.Pool(a.procs) as pool:
                for r in pool.imap_unordered(run_one, jobs, chunksize=4):
                    rows += r
            print(f"{strat} {tf}: {len(jobs)} configs in {time.time() - t0:.0f}s", file=sys.stderr, flush=True)
            pd.DataFrame(rows).to_csv(a.out + "_all.csv", index=False)
    df = pd.DataFrame(rows)
    df.to_csv(a.out + "_all.csv", index=False)
    print(f"wrote {a.out}_all.csv ({len(df)} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
