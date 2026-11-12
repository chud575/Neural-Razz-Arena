# Pullback to a pivot in the direction of the bigger candle — test summary

Rules in python/pivot_ftfc.py. 15m candles, BTC/ETH/AVAX/XRP since 2020, net of Bybit VIP 3 futures fees and funding, R per trade (trades). 'Expected win %' = the win rate that gives zero before fees for that stop and target.

| Context candle | Pivot TF | Filter | Target | IS | OOS | Before fees | Win % | Expected win % | Median stop |
|---|---|---|---|---|---|---|---|---|---|
| 1D | 1h | all | 2R | -0.96 (2494) | -0.67 (977) | -0.11 | 28 | 33 | 0.64% |
| 1D | 1h | all | pivot | -1.03 (2494) | -0.59 (977) | -0.12 | 25 | 27 | 0.64% |
| 1D | 1h | pivot above the context open | 2R | -0.07 (1435) | -0.24 (562) | -0.05 | 31 | 33 | 1.15% |
| 1D | 1h | pivot above the context open | pivot | -0.10 (1435) | -0.21 (562) | -0.06 | 35 | 37 | 1.15% |
| 1D | 4h | all | 2R | -0.39 (76) | -1.21 (28) | -0.00 | 20 | 33 | 0.23% |
| 1D | 4h | all | pivot | -0.42 (76) | -1.73 (28) | -0.12 | 8 | 6 | 0.23% |
| 1M | 1D | all | 2R | -0.06 (81) | +0.10 (41) | +0.01 | 12 | 33 | 9.37% |
| 1M | 1D | all | pivot | +0.06 (81) | -0.04 (41) | +0.04 | 33 | 42 | 9.37% |
| 1M | 1D | pivot above the context open | 2R | -0.06 (67) | +0.01 (39) | -0.03 | 10 | 33 | 10.40% |
| 1M | 1D | pivot above the context open | pivot | -0.00 (67) | -0.12 (39) | -0.03 | 34 | 45 | 10.40% |
| 1W | 4h | all | 2R | -0.10 (900) | -0.05 (379) | -0.03 | 27 | 33 | 4.27% |
| 1W | 4h | all | pivot | -0.14 (900) | -0.19 (379) | -0.10 | 44 | 46 | 4.27% |
| 1W | 4h | pivot above the context open | 2R | -0.06 (735) | +0.06 (304) | -0.01 | 27 | 33 | 5.12% |
| 1W | 4h | pivot above the context open | pivot | -0.10 (735) | +0.03 (304) | -0.05 | 49 | 52 | 5.12% |

Weekly context with DAILY pivots (the original example) produced only 4 trades: a daily pivot needs 3 more days to confirm, so one is almost never sitting between the week's low and the price.
