# The Strat — sweep-and-reclaim reversal after a big 2d / 2u candle (2-2 / 2-3 reversal)

Rules in python/strat_sweep.py. Setup candle on 1h or 4h, entries timed on 15m candles, BTC/ETH/AVAX/XRP since 2020. Net of Bybit VIP 3 futures fees and funding, R per trade, IS (first 70%) / OOS (last 30%). Entry within the next setup-timeframe candle. Stop = sweep low (high). Target 'high' = the far end of the setup candle.

A first version that assumed the fill at the setup close always came after the low of the same 15m candle showed about +0.7R per trade; that was look-ahead and is not reported here.


## Entry at the first 15m close back through the setup candle's close

| Setup TF | Min move | Target high IS | OOS | Target 1R IS | OOS | Win % (high) | Median stop | Gross R (high) |
|---|---|---|---|---|---|---|---|---|
| 1h | 0.5% | -0.13 (12359) | -0.18 (4190) | -0.14 (12506) | -0.20 (4222) | 40 | 0.63% | -0.02 |
| 1h | 1% | -0.12 (6095) | -0.14 (1643) | -0.11 (6137) | -0.15 (1650) | 36 | 0.84% | -0.03 |
| 1h | 2% | -0.14 (1794) | -0.01 (347) | -0.07 (1804) | -0.15 (348) | 32 | 1.24% | -0.05 |
| 1h | 3% | -0.15 (641) | -0.12 (99) | -0.08 (645) | -0.09 (100) | 31 | 1.73% | -0.10 |
| 4h | 0.5% | -0.07 (4904) | -0.16 (1930) | -0.05 (4924) | -0.13 (1947) | 35 | 0.90% | -0.00 |
| 4h | 1% | -0.07 (3628) | -0.11 (1220) | -0.05 (3637) | -0.09 (1226) | 32 | 1.01% | -0.00 |
| 4h | 2% | -0.08 (1884) | -0.16 (509) | -0.06 (1886) | -0.10 (511) | 28 | 1.22% | -0.03 |
| 4h | 3% | -0.04 (954) | -0.30 (233) | -0.02 (956) | -0.12 (234) | 25 | 1.51% | -0.04 |

## Resting stop order at the setup candle's close (ambiguous 15m candles counted as losses)

| Setup TF | Min move | Target high IS | OOS | Target 1R IS | OOS | Win % (high) | Median stop | Gross R (high) |
|---|---|---|---|---|---|---|---|---|
| 1h | 0.5% | -0.21 (14812) | -0.28 (5167) | -0.22 (14894) | -0.31 (5183) | 32 | 0.54% | -0.08 |
| 1h | 1% | -0.18 (7246) | -0.23 (2023) | -0.19 (7273) | -0.27 (2027) | 29 | 0.72% | -0.08 |
| 1h | 2% | -0.18 (2151) | -0.08 (413) | -0.14 (2158) | -0.27 (414) | 26 | 1.05% | -0.09 |
| 1h | 3% | -0.21 (756) | -0.19 (111) | -0.15 (760) | -0.20 (112) | 25 | 1.46% | -0.15 |
| 4h | 0.5% | -0.10 (5494) | -0.24 (2215) | -0.09 (5496) | -0.18 (2219) | 30 | 0.76% | -0.02 |
| 4h | 1% | -0.10 (4018) | -0.19 (1381) | -0.07 (4019) | -0.15 (1383) | 27 | 0.85% | -0.03 |
| 4h | 2% | -0.10 (2076) | -0.26 (574) | -0.08 (2076) | -0.18 (574) | 23 | 1.03% | -0.06 |
| 4h | 3% | -0.05 (1050) | -0.36 (259) | -0.02 (1050) | -0.16 (259) | 21 | 1.26% | -0.05 |

## 1h, move ≥ 1%, close entry, target high — by coin

| Coin | IS | OOS |
|---|---|---|
| AVAX | -0.07 (2023) | -0.12 (574) |
| BTC | -0.14 (1268) | -0.25 (267) |
| ETH | -0.15 (1844) | -0.09 (493) |
| XRP | -0.15 (960) | -0.19 (309) |
