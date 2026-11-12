# The Strat — sweep-and-reclaim reversal after a 2d / 2u candle (2-2 / 2-3 reversal)

Rules in python/strat_sweep.py. Setup candle = any 2d (any size) on 1h or 4h; 'lower low' = its low is the lowest of at least N earlier candles. Next candle must sweep below that low, then entry at the first 15m close back above the 2d's close. Stop = sweep low, target = the 2d's high. Shorts mirror on 2u candles. BTC/ETH/AVAX/XRP since 2020, net of Bybit VIP 3 futures fees and funding, R per trade, IS (first 70%) / OOS (last 30%).

An earlier version that assumed the fill always came after the low of the same 15m candle showed about +0.7R per trade; that was look-ahead and is not reported.

| Setup TF | Lowest low of ≥ N candles | Target high IS | OOS | Target 1R IS | OOS | Win % (high) | Median stop | Gross R (high) |
|---|---|---|---|---|---|---|---|---|
| 1h | 1 | -0.17 (22965) | -0.23 (9432) | -0.18 (24075) | -0.24 (9870) | 47 | 0.47% | -0.01 |
| 1h | 5 | -0.15 (11172) | -0.21 (4583) | -0.15 (11583) | -0.20 (4721) | 45 | 0.55% | -0.02 |
| 1h | 10 | -0.14 (7334) | -0.18 (3143) | -0.13 (7575) | -0.17 (3218) | 44 | 0.61% | -0.02 |
| 1h | 20 | -0.14 (4774) | -0.14 (2010) | -0.12 (4904) | -0.13 (2047) | 44 | 0.67% | -0.02 |
| 1h | 50 | -0.12 (2703) | -0.16 (1177) | -0.11 (2771) | -0.14 (1200) | 43 | 0.74% | -0.03 |
| 1h | 100 | -0.10 (1770) | -0.10 (736) | -0.10 (1810) | -0.14 (751) | 44 | 0.79% | -0.00 |
| 4h | 1 | -0.08 (6283) | -0.16 (2723) | -0.06 (6426) | -0.12 (2813) | 41 | 0.85% | -0.00 |
| 4h | 5 | -0.05 (3051) | -0.15 (1247) | -0.05 (3092) | -0.09 (1282) | 38 | 0.97% | +0.01 |
| 4h | 10 | -0.09 (2073) | -0.11 (856) | -0.06 (2095) | -0.05 (880) | 37 | 1.02% | -0.02 |
| 4h | 20 | -0.10 (1387) | -0.08 (554) | -0.08 (1401) | -0.05 (568) | 36 | 1.09% | -0.02 |
| 4h | 50 | -0.19 (807) | -0.06 (325) | -0.13 (815) | -0.06 (333) | 34 | 1.17% | -0.08 |
| 4h | 100 | -0.19 (523) | -0.17 (225) | -0.15 (529) | -0.11 (229) | 33 | 1.20% | -0.12 |

A resting stop order at the 2d's close (ambiguous 15m candles counted as losses) tested worse: 1h −0.16 to −0.35R, 4h −0.08 to −0.23R.

## Structure from the weekly DIA example

Setup candle = a red 2d whose low is below the low of the last red candle before it (green candles in between don't matter); mirror for shorts. Next candle sweeps the low; entry at the first 15m close back above the setup candle's close; stop = sweep low; target = the setup candle's high. Max hold 10 setup candles (48 h on 1h).

| Setup TF | Target high IS | OOS | Target 2R IS | OOS | Win % (high) | Median stop | Gross R (high) | Next candle sweeps the low | ...and also reaches the high |
|---|---|---|---|---|---|---|---|---|---|
| 1h | -0.17 (18972) | -0.22 (7720) | -0.20 (19616) | -0.22 (7984) | 46 | 0.48% | -0.01 | 58% | 14% of those |
| 4h | -0.08 (5125) | -0.17 (2192) | -0.07 (5178) | -0.14 (2229) | 39 | 0.86% | -0.00 | 57% | 16% of those |
| 1D | -0.04 (930) | +0.06 (400) | +0.03 (936) | +0.02 (403) | 35 | 1.99% | +0.03 | 58% | 15% of those |
| 1W | -0.12 (132) | +0.03 (54) | +0.02 (132) | -0.17 (54) | 27 | 4.53% | -0.06 | 57% | 14% of those |

Daily, target high, by coin (IS / OOS): AVAX -0.24 (246) / -0.14 (98); BTC +0.03 (274) / +0.12 (115); ETH +0.06 (282) / +0.19 (109); XRP -0.03 (128) / +0.02 (78).
