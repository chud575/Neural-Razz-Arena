# 1h break of structure — which entry conditions help (feature screen)

Rules in python/bos_features.py. 2,034 trades on four coins, after fees. Each reading is split into five equal groups (cut points from the first 70% only); the table shows the average R of the lowest and highest group in each period.

| Reading at the entry | IS lowest group | IS highest | OOS lowest | OOS highest | Same direction in both? |
|---|---|---|---|---|---|
| close_past_level_atr | -0.07 | +0.37 | +0.10 | +0.35 | yes |
| range_pos_100 | +0.01 | +0.35 | +0.20 | +0.10 | no |
| rsi_aligned | +0.01 | +0.30 | +0.06 | +0.19 | yes |
| body_in_atr | +0.09 | +0.35 | +0.08 | +0.24 | yes |
| di_aligned | +0.06 | +0.26 | +0.07 | +0.27 | yes |
| stop_in_atr | -0.01 | +0.19 | -0.04 | +0.28 | yes |
| ema200_dist_atr | +0.07 | +0.26 | +0.14 | +0.30 | yes |
| volatility_rank | +0.24 | +0.08 | +0.13 | +0.22 | no |
| ret_7d | +0.00 | +0.13 | +0.20 | +0.07 | no |
| cvd_100 | +0.09 | +0.21 | +0.16 | +0.15 | no |
| norm_volume | +0.12 | +0.24 | +0.08 | +0.16 | no |
| stop_pct | +0.14 | +0.04 | +0.24 | +0.03 | yes |
| ret_24h | +0.06 | +0.14 | +0.25 | -0.21 | no |
| ema50_over_200 | +0.07 | +0.15 | +0.09 | +0.12 | no |
| cvd_20 | +0.08 | +0.15 | +0.17 | +0.10 | no |
| bb_width_rank | +0.14 | +0.18 | +0.09 | +0.24 | no |
| adx | +0.07 | +0.09 | +0.05 | +0.22 | no |
| bars_since_swing | +0.14 | +0.15 | +0.02 | +0.29 | no |

## As filters (cut points from the first 70% only)

| Filter | Trades | IS | OOS |
|---|---|---|---|
| all trades | 2034 | +0.155 | +0.133 |
| close past level > 0.17 ATR (drop weakest 20%) | 1614 | +0.213 | +0.143 |
| close past level > 0.36 ATR (drop weakest 40%) | 1190 | +0.247 | +0.159 |
| stop > 2.92 ATR (drop tightest 20%) | 1593 | +0.198 | +0.193 |
| DI aligned > 11.6 | 1627 | +0.179 | +0.149 |
| RSI aligned > 63.3 | 1606 | +0.191 | +0.154 |
| close past + stop filters | 1323 | +0.234 | +0.153 |
| REJECTED by close past + stop | 711 | -0.004 | +0.102 |
| norm volume >= 150 | 1176 | +0.176 | +0.126 |
| norm volume < 75 | 234 | +0.137 | +0.201 |
