# Cup & handle — test summary (BTC, ETH, AVAX, XRP)

Rules: python/cup_handle_backtest.py = pine/cup_handle.pine (v1.0). 144 settings per coin and timeframe. Net of Bybit VIP 3 futures fees and funding, average R per trade, IS / OOS (trade rows across all settings).

| TF | All settings | Swing 5 | Swing 10 | Swing 20 | Longs | Shorts | Win % | Break-even win % |
|---|---|---|---|---|---|---|---|---|
| 15m | -0.11 / -0.07 (26488) | -0.12 / +0.03 (14905) | -0.09 / -0.15 (7472) | -0.12 / -0.29 (4111) | -0.14 / -0.08 (14477) | -0.08 / -0.06 (12011) | 27 | 31 |
| 1h | +0.02 / -0.21 (10135) | -0.01 / -0.42 (5424) | +0.02 / -0.00 (2917) | +0.14 / -0.05 (1794) | +0.03 / -0.47 (5454) | +0.02 / -0.02 (4681) | 28 | 32 |
| 4h | -0.07 / +0.05 (2607) | -0.25 / -0.27 (1856) | -0.05 / +1.04 (573) | +1.15 / +2.08 (178) | +0.07 / -0.10 (1004) | -0.16 / +0.14 (1603) | 32 | 32 |
| 1d | +0.29 / +1.07 (476) | -0.02 / +2.02 (228) | +0.06 / -0.58 (104) | +0.79 / +nan (144) | +1.89 / +1.49 (160) | -0.42 / +0.73 (316) | 44 | 32 |

## Indicator defaults (swing 10, rims within 0.3, handle up to 0.5, stop at the handle low, measured-move target)

| TF | IS / OOS (trades) | Median stop |
|---|---|---|
| 15m | +0.05 / -0.11 (328) | 1.6% |
| 1h | +0.01 / +0.11 (125) | 3.6% |
| 4h | +0.05 / +0.41 (26) | 8.6% |
| 1d | +0.35 / -0.23 (4) | 18.8% |

1h defaults by coin: AVAX +0.20 / -1.00 (20); BTC +0.10 / +0.60 (42); ETH -0.09 / -0.11 (40); XRP -0.18 / +0.19 (23).
