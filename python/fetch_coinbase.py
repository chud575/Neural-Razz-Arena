"""Download Coinbase BTC-USD (or any product) candles to CSV, paginating 300 candles per request.

    python fetch_coinbase.py BTC-USD 900 2020-01-01 out.csv      # 15-minute candles since 2020
Granularity in seconds: 60, 300, 900, 3600, 21600, 86400.
"""
import sys
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests

URL = "https://api.exchange.coinbase.com/products/{}/candles"


def fetch(product: str, gran: int, start: str, end: str | None = None) -> pd.DataFrame:
    t0 = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    t_end = datetime.now(timezone.utc) if end is None else datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
    step = timedelta(seconds=gran * 300)
    rows = []
    s = requests.Session()
    s.headers["User-Agent"] = "backtest-research/1.0"
    while t0 < t_end:
        t1 = min(t0 + step, t_end)
        for attempt in range(6):
            r = s.get(URL.format(product), params={"granularity": gran, "start": t0.isoformat(), "end": t1.isoformat()}, timeout=30)
            if r.status_code == 200:
                break
            time.sleep(1 + 2 ** attempt)
        r.raise_for_status()
        rows += r.json()
        t0 = t1
        time.sleep(0.12)
    df = pd.DataFrame(rows, columns=["time", "low", "high", "open", "close", "volume"]).drop_duplicates("time")
    df.index = pd.to_datetime(df.pop("time"), unit="s")
    return df.sort_index()[["open", "high", "low", "close", "volume"]]


if __name__ == "__main__":
    product, gran, start, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    df = fetch(product, gran, start)
    df.to_csv(out)
    print(out, len(df), df.index[0], df.index[-1])
