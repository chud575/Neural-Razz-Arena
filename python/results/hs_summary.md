# Head & Shoulders — test summary (BTC, ETH, AVAX, XRP · 15m / 1h / 4h / 1D)

Rules: python/hs_backtest.py = pine/head_shoulders.pine (v1.0). 1,152 settings per coin and timeframe. Net of Bybit VIP 3
futures fees and funding, in R per trade. IS = first 70% of each history, OOS = last 30%. Data: Coinbase.

## All settings pooled (four coins, both sides)

| TF | Avg R IS | Avg R OOS | Read |
|---|---|---|---|
| 15m | -0.096 | -0.062 | loses after fees |
| 1h | -0.026 | -0.036 | flat overall; retest entries are the only positive group |
| 4h | -0.043 | -0.203 | loses; breakout and retest entries about -0.3R OOS |
| 1D | +0.038 | +0.088 | positive, but only about 5 trades per setting per coin — not evidence |

## 1h by entry and stop, 3R target (all variants pooled)

| Entry · stop | IS | OOS |
|---|---|---|
| Retest · right shoulder | +0.065 | +0.043 |
| Breakout · right shoulder | +0.049 | -0.002 |
| Retest · head | -0.038 | 0.000 |
| Breakout · head | -0.016 | -0.026 |
| Early · right shoulder | -0.056 | -0.067 |
| Early · head | -0.040 | -0.043 |

Taking half off at 1R and moving the stop to breakeven lowered the result of the retest entries.

## Default settings (1h, swing 5, retest, sloped neckline, stop beyond right shoulder, single 3R, prior trend 0.5)

| Coin | IS trades | IS avg R | OOS trades | OOS avg R | Random OOS | Median stop | Stop beyond 25x liquidation |
|---|---|---|---|---|---|---|---|
| BTC | 73 | +0.044 | 23 | -0.353 | -0.001 | 1.63% | 21% |
| ETH | 61 | +0.251 | 27 | +0.146 | +0.025 | 2.66% | 41% |
| AVAX | 31 | +0.133 | 12 | +0.978 | -0.094 | 3.32% | 40% |
| XRP | 31 | +0.271 | 11 | +0.055 | -0.066 | 3.21% | 43% |
| All four | 196 | +0.158 | 73 | +0.112 | -0.016 | 2.48% | 34% |

Pooled t-stat over all 269 trades: 1.2 (not statistically significant). BTC makes about 9 trades a year with these settings.

Per-coin detail: hs_btc.md, hs_eth.md, hs_avax.md, hs_xrp.md. Cross-asset: hs_crossasset.md. Main settings with random
benchmark: hs_finalists_bybit.txt.
