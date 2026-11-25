"""Download Coinbase 5-minute candles for selected days: every day BTC / ETH moved ±5 % open-to-close, plus a random
sample of quiet days (|move| < 2 %). Each day is stored with the 12 hours before it (warm-up for indicators).

    python fetch_5m_days.py <data_dir>      -> <data_dir>/<coin>_5m_days.csv  (columns: day, kind, time, open, high, low, close, volume)
"""
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import numpy as np
import pandas as pd
import requests

URL = "https://api.exchange.coinbase.com/products/{}/candles"
D = sys.argv[1]
rng = np.random.default_rng(42)


def get(sess, product, t0, t1):
    for attempt in range(7):
        try:
            r = sess.get(URL.format(product), params={"granularity": 300, "start": t0.isoformat(), "end": t1.isoformat()}, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(0.5 + 1.5 ** attempt)
    return []


def one(args):
    product, day, kind = args
    sess = requests.Session()
    sess.headers["User-Agent"] = "backtest-research/1.0"
    t0 = day - timedelta(hours=12)
    rows = get(sess, product, t0, day + timedelta(hours=12) - timedelta(minutes=5)) + get(sess, product, day + timedelta(hours=12), day + timedelta(hours=24) - timedelta(minutes=5))
    time.sleep(0.15)
    return [(str(day.date()), kind) + tuple(x) for x in rows]


for coin, product in (("btc", "BTC-USD"), ("eth", "ETH-USD")):
    d = pd.read_csv(f"{D}/{coin}_1d.csv", index_col=0, parse_dates=True)
    d = d.iloc[30:-1]
    ret = (d.close / d.open - 1) * 100
    big = list(d.index[ret.abs() >= 5])
    quiet = list(d.index[ret.abs() < 2])
    quiet = [quiet[i] for i in sorted(rng.choice(len(quiet), size=min(450, len(quiet)), replace=False))]
    jobs = [(product, x.to_pydatetime(), "big") for x in big] + [(product, x.to_pydatetime(), "quiet") for x in quiet]
    out = []
    with ThreadPoolExecutor(5) as ex:
        for k, res in enumerate(ex.map(one, jobs)):
            out += res
            if k % 200 == 0:
                print(coin, k, len(jobs), flush=True)
    df = pd.DataFrame(out, columns=["day", "kind", "time", "low", "high", "open", "close", "volume"]).drop_duplicates(["day", "time"])
    df["time"] = pd.to_datetime(df.time, unit="s")
    df.sort_values(["day", "time"])[["day", "kind", "time", "open", "high", "low", "close", "volume"]].to_csv(f"{D}/{coin}_5m_days.csv", index=False)
    print(coin, "days", df.day.nunique(), "rows", len(df), flush=True)
