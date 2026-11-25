"""Download the full Coinbase 5-minute history for BTC and ETH from 2020-01-01 (one request per UTC day).

    python fetch_5m_all.py <data_dir>      -> <data_dir>/<coin>_5m.csv  (time index; open, high, low, close, volume)
"""
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import pandas as pd
import requests

URL = "https://api.exchange.coinbase.com/products/{}/candles"
D = sys.argv[1]


def one(args):
    product, day = args
    sess = requests.Session()
    sess.headers["User-Agent"] = "backtest-research/1.0"
    for attempt in range(8):
        try:
            r = sess.get(URL.format(product), params={"granularity": 300, "start": day.isoformat(), "end": (day + timedelta(hours=24) - timedelta(minutes=5)).isoformat()}, timeout=30)
            if r.status_code == 200:
                time.sleep(0.1)
                return r.json()
        except Exception:
            pass
        time.sleep(0.5 + 1.5 ** attempt)
    print("FAILED", product, day, flush=True)
    return []


end = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
days = [datetime(2020, 1, 1) + timedelta(days=k) for k in range((end - datetime(2020, 1, 1)).days)]
for coin, product in (("btc", "BTC-USD"), ("eth", "ETH-USD")):
    out = []
    with ThreadPoolExecutor(6) as ex:
        for k, res in enumerate(ex.map(one, [(product, d) for d in days])):
            out += res
            if k % 500 == 0:
                print(coin, k, len(days), flush=True)
    df = pd.DataFrame(out, columns=["time", "low", "high", "open", "close", "volume"]).drop_duplicates("time")
    df["time"] = pd.to_datetime(df.time, unit="s")
    df.sort_values("time").set_index("time")[["open", "high", "low", "close", "volume"]].to_csv(f"{D}/{coin}_5m.csv")
    print(coin, "rows", len(df), flush=True)
