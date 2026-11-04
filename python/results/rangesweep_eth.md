# ETH strategy sweep — 15m / 1h / 4h / 1D

Costs: 0.20% round trip per trade (0.1% per side), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase ETH-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | within_n · target:3R (shorts) | -0.328 | -0.457 | 0 | range48 max15ATR touches3 within_n sweepMax3 stop0.75ATR target:3R exit:TP1 1R 50% BE | 60 | -0.378 | -0.272 |
| 1h | Range Sweep | within_n · target:3R (longs) | -0.143 | -0.156 | 7 | range144 max10ATR touches1 within_n sweepMax3 stop0.75ATR target:3R exit:single | 67 | -0.221 | +0.022 |
| 4h | Range Sweep | within_n · target:opposite (longs) | +0.050 | -0.053 | 45 | range24 max15ATR touches2 within_n sweepMax3 stop0.75ATR target:opposite exit:single | 36 | +0.241 | +0.107 |
| 1d | Range Sweep | within_n · target:opposite (longs) | +0.099 | -0.063 | 37 | range24 max15ATR touches1 within_n sweepMax3 stop0.75ATR target:opposite exit:TP1 1R 50% BE | 17 | -0.419 | +0.261 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | range144 max15ATR touches2 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | longs | 187 | +0.057 | 90 | -0.440 | -0.082 | -0.358 | -0.399 | +0.63 |
| 1h | Range Sweep | range48 max6ATR touches2 within_n sweepMax3 stop0.75ATR target:opposite exit:single | shorts | 84 | +0.355 | 79 | -0.241 | -0.252 | +0.011 | -0.253 | +0.15 |
| 4h | Range Sweep | range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 57 | +0.763 | 24 | +0.921 | +0.204 | +0.717 | +0.369 | +0.27 |
| 1d | Range Sweep | range24 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:2R exit:single | both | 29 | +0.526 | 21 | -0.187 | +0.076 | -0.263 | -0.275 | -0.01 |


## 15-minute  (IS 2020-01-01 → 2024-10-15, OOS 2024-10-15 → 2026-11-04; ETH buy & hold: IS +1915%, OOS -10%)

### Range Sweep

2304 settings × 3 sides tested; 4432 combinations had ≥120 IS trades, 0% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.63. Average OOS result of the top-20 IS picks: -0.399 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.082 R/trade over 90 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range144 max15ATR touches2 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | longs | 187 | +0.057 | 0.29 | 90 | -0.440 | -39.6 | 16 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.25ATR target:opposite exit:single | longs | 215 | +0.018 | 0.08 | 106 | -0.573 | -60.7 | 12 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | longs | 202 | +0.002 | 0.01 | 97 | -0.368 | -35.6 | 15 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | longs | 240 | -0.008 | -0.04 | 116 | -0.484 | -56.1 | 12 |
| range96 max15ATR touches3 within_n sweepMax3 stop0.75ATR target:opposite exit:single | both | 130 | -0.040 | -0.21 | 79 | -0.191 | -15.1 | 28 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:3R | shorts | 183 | -0.328 | -0.457 | 0 | 376 |
| within_n · target:opposite | shorts | 183 | -0.333 | -0.465 | 0 | 382 |
| within_n · target:2R | shorts | 183 | -0.338 | -0.467 | 0 | 420 |
| within_n · target:opposite | both | 221 | -0.348 | -0.413 | 0 | 545 |
| within_n · target:3R | both | 221 | -0.351 | -0.395 | 0 | 536 |
| within_n · target:midline | shorts | 184 | -0.359 | -0.451 | 0 | 453 |
| within_n · target:opposite | longs | 184 | -0.360 | -0.381 | 0 | 372 |
| within_n · target:2R | both | 222 | -0.369 | -0.403 | 0 | 572 |
| same_bar · target:opposite | longs | 168 | -0.376 | -0.434 | 0 | 340 |
| within_n · target:3R | longs | 184 | -0.378 | -0.350 | 1 | 359 |
| within_n · target:midline | both | 222 | -0.389 | -0.417 | 0 | 604 |
| same_bar · target:3R | shorts | 152 | -0.397 | -0.458 | 0 | 353 |
| same_bar · target:2R | shorts | 152 | -0.400 | -0.459 | 0 | 376 |
| same_bar · target:opposite | shorts | 152 | -0.401 | -0.484 | 0 | 352 |
| within_n · target:2R | longs | 184 | -0.402 | -0.361 | 0 | 408 |
| same_bar · target:3R | longs | 164 | -0.402 | -0.402 | 0 | 339 |
| same_bar · target:opposite | both | 203 | -0.404 | -0.487 | 0 | 531 |
| within_n · target:midline | longs | 184 | -0.415 | -0.411 | 0 | 434 |
| same_bar · target:3R | both | 204 | -0.416 | -0.457 | 0 | 533 |
| same_bar · target:midline | longs | 158 | -0.419 | -0.422 | 0 | 384 |
| same_bar · target:midline | shorts | 152 | -0.420 | -0.441 | 0 | 397 |
| same_bar · target:2R | longs | 166 | -0.427 | -0.416 | 0 | 353 |
| same_bar · target:2R | both | 204 | -0.433 | -0.471 | 0 | 550 |
| same_bar · target:midline | both | 202 | -0.443 | -0.479 | 0 | 564 |


## 1-hour  (IS 2016-06-01 → 2023-09-19, OOS 2023-09-19 → 2026-11-04; ETH buy & hold: IS +11664%, OOS +41%)

### Range Sweep

2304 settings × 3 sides tested; 3532 combinations had ≥80 IS trades, 2% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.15. Average OOS result of the top-20 IS picks: -0.253 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.252 R/trade over 79 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max6ATR touches2 within_n sweepMax3 stop0.75ATR target:opposite exit:single | shorts | 84 | +0.355 | 1.76 | 79 | -0.241 | -19.0 | 27 |
| range48 max6ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | shorts | 94 | +0.261 | 1.09 | 92 | -0.378 | -34.8 | 20 |
| range48 max6ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | shorts | 84 | +0.252 | 0.95 | 82 | -0.398 | -32.6 | 17 |
| range48 max6ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | both | 165 | +0.152 | 0.83 | 125 | -0.219 | -27.4 | 26 |
| range144 max10ATR touches1 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 97 | +0.155 | 0.82 | 56 | -0.193 | -10.8 | 23 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:3R | longs | 149 | -0.143 | -0.156 | 7 | 145 |
| same_bar · target:3R | longs | 140 | -0.148 | -0.182 | 5 | 124 |
| same_bar · target:3R | both | 152 | -0.158 | -0.232 | 1 | 275 |
| within_n · target:3R | both | 166 | -0.159 | -0.203 | 2 | 310 |
| same_bar · target:3R | shorts | 129 | -0.161 | -0.277 | 1 | 170 |
| within_n · target:3R | shorts | 147 | -0.163 | -0.225 | 3 | 195 |
| within_n · target:2R | longs | 150 | -0.174 | -0.146 | 5 | 156 |
| within_n · target:2R | shorts | 148 | -0.178 | -0.190 | 6 | 210 |
| same_bar · target:2R | shorts | 130 | -0.179 | -0.247 | 0 | 182 |
| within_n · target:2R | both | 166 | -0.180 | -0.180 | 3 | 338 |
| same_bar · target:2R | longs | 140 | -0.188 | -0.173 | 4 | 132 |
| same_bar · target:2R | both | 152 | -0.188 | -0.208 | 3 | 280 |
| within_n · target:midline | longs | 149 | -0.193 | -0.165 | 4 | 175 |
| within_n · target:opposite | longs | 148 | -0.198 | -0.166 | 7 | 142 |
| same_bar · target:opposite | longs | 138 | -0.203 | -0.175 | 9 | 126 |
| within_n · target:midline | shorts | 148 | -0.209 | -0.208 | 3 | 218 |
| within_n · target:opposite | shorts | 146 | -0.210 | -0.249 | 1 | 194 |
| same_bar · target:opposite | shorts | 128 | -0.212 | -0.318 | 0 | 170 |
| within_n · target:midline | both | 166 | -0.212 | -0.198 | 1 | 358 |
| same_bar · target:midline | shorts | 130 | -0.214 | -0.259 | 0 | 178 |
| within_n · target:opposite | both | 166 | -0.217 | -0.229 | 2 | 310 |
| same_bar · target:opposite | both | 152 | -0.218 | -0.258 | 0 | 276 |
| same_bar · target:midline | longs | 140 | -0.222 | -0.193 | 4 | 140 |
| same_bar · target:midline | both | 152 | -0.224 | -0.226 | 0 | 299 |


## 4-hour  (IS 2016-06-01 → 2023-09-18, OOS 2023-09-18 → 2026-11-04; ETH buy & hold: IS +11307%, OOS +42%)

### Range Sweep

2304 settings × 3 sides tested; 2670 combinations had ≥50 IS trades, 28% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.27. Average OOS result of the top-20 IS picks: +0.369 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.204 R/trade over 24 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 57 | +0.763 | 2.86 | 24 | +0.921 | +22.1 | 50 |
| range24 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 64 | +0.691 | 2.76 | 27 | +0.702 | +19.0 | 44 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | both | 102 | +0.507 | 2.61 | 51 | +0.566 | +28.9 | 41 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.25ATR target:3R exit:single | longs | 63 | +0.618 | 2.45 | 26 | +0.419 | +10.9 | 38 |
| range24 max6ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | longs | 97 | +0.485 | 2.43 | 34 | +0.422 | +14.3 | 38 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:opposite | longs | 101 | +0.050 | -0.053 | 45 | 44 |
| same_bar · target:opposite | longs | 81 | +0.049 | +0.026 | 53 | 53 |
| within_n · target:3R | longs | 103 | +0.033 | -0.065 | 31 | 50 |
| same_bar · target:3R | longs | 87 | +0.023 | +0.001 | 34 | 61 |
| same_bar · target:opposite | both | 126 | -0.010 | -0.094 | 30 | 75 |
| within_n · target:midline | longs | 106 | -0.010 | -0.110 | 24 | 50 |
| within_n · target:2R | longs | 105 | -0.023 | -0.077 | 25 | 50 |
| same_bar · target:2R | longs | 87 | -0.054 | +0.002 | 37 | 72 |
| same_bar · target:3R | both | 127 | -0.055 | -0.089 | 24 | 75 |
| within_n · target:opposite | both | 139 | -0.068 | -0.079 | 27 | 88 |
| same_bar · target:midline | longs | 88 | -0.078 | -0.048 | 27 | 66 |
| same_bar · target:2R | both | 127 | -0.084 | -0.087 | 29 | 77 |
| same_bar · target:opposite | shorts | 86 | -0.086 | -0.025 | 35 | 72 |
| within_n · target:3R | both | 138 | -0.090 | -0.088 | 20 | 89 |
| within_n · target:opposite | shorts | 119 | -0.091 | -0.025 | 35 | 58 |
| same_bar · target:midline | both | 127 | -0.091 | -0.097 | 27 | 79 |
| within_n · target:midline | both | 142 | -0.104 | -0.099 | 22 | 94 |
| within_n · target:2R | both | 141 | -0.104 | -0.092 | 25 | 92 |
| same_bar · target:midline | shorts | 98 | -0.121 | -0.039 | 28 | 73 |
| same_bar · target:2R | shorts | 93 | -0.123 | -0.087 | 18 | 88 |
| within_n · target:3R | shorts | 119 | -0.126 | -0.009 | 42 | 61 |
| within_n · target:2R | shorts | 121 | -0.128 | -0.036 | 37 | 61 |
| within_n · target:midline | shorts | 121 | -0.132 | -0.022 | 40 | 61 |
| same_bar · target:3R | shorts | 88 | -0.133 | -0.063 | 25 | 78 |


## Daily  (IS 2016-06-01 → 2023-09-19, OOS 2023-09-19 → 2026-11-04; ETH buy & hold: IS +11698%, OOS +41%)

### Range Sweep

2304 settings × 3 sides tested; 1751 combinations had ≥15 IS trades, 17% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.01. Average OOS result of the top-20 IS picks: -0.275 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.076 R/trade over 21 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:2R exit:single | both | 29 | +0.526 | 1.85 | 21 | -0.187 | -3.9 | 29 |
| range24 max6ATR touches2 within_n sweepMax3 stop0.25ATR target:2R exit:single | both | 27 | +0.528 | 1.79 | 20 | -0.143 | -2.9 | 30 |
| range24 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:2R exit:single | both | 25 | +0.527 | 1.72 | 19 | -0.099 | -1.9 | 32 |
| range24 max6ATR touches2 within_n sweepMax1 stop0.25ATR target:2R exit:single | both | 23 | +0.531 | 1.66 | 18 | -0.045 | -0.8 | 33 |
| range24 max6ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | both | 20 | +0.734 | 1.53 | 18 | +0.228 | +4.1 | 28 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:opposite | longs | 46 | +0.099 | -0.063 | 37 | 15 |
| within_n · target:2R | longs | 47 | +0.055 | -0.266 | 4 | 18 |
| within_n · target:3R | longs | 40 | -0.026 | -0.232 | 8 | 18 |
| within_n · target:midline | longs | 52 | -0.035 | -0.191 | 6 | 19 |
| same_bar · target:2R | longs | 40 | -0.041 | -0.297 | 2 | 18 |
| same_bar · target:opposite | longs | 37 | -0.055 | -0.034 | 41 | 17 |
| within_n · target:2R | both | 105 | -0.059 | -0.246 | 5 | 21 |
| within_n · target:opposite | both | 109 | -0.068 | -0.074 | 47 | 20 |
| same_bar · target:3R | longs | 40 | -0.082 | -0.207 | 10 | 17 |
| same_bar · target:midline | longs | 40 | -0.085 | -0.215 | 5 | 19 |
| within_n · target:3R | both | 103 | -0.099 | -0.289 | 10 | 21 |
| same_bar · target:2R | both | 99 | -0.131 | -0.235 | 6 | 19 |
| within_n · target:midline | both | 112 | -0.153 | -0.146 | 33 | 21 |
| same_bar · target:opposite | both | 99 | -0.170 | -0.181 | 24 | 19 |
| same_bar · target:3R | both | 95 | -0.183 | -0.228 | 13 | 22 |
| within_n · target:2R | shorts | 76 | -0.211 | -0.156 | 25 | 20 |
| same_bar · target:midline | both | 100 | -0.225 | -0.181 | 24 | 20 |
| within_n · target:midline | shorts | 84 | -0.247 | -0.110 | 38 | 20 |
| within_n · target:opposite | shorts | 78 | -0.248 | -0.113 | 40 | 17 |
| same_bar · target:2R | shorts | 69 | -0.254 | -0.077 | 38 | 20 |
| same_bar · target:opposite | shorts | 69 | -0.282 | -0.257 | 29 | 18 |
| within_n · target:3R | shorts | 72 | -0.304 | -0.228 | 18 | 19 |
| same_bar · target:midline | shorts | 70 | -0.308 | -0.169 | 36 | 20 |
| same_bar · target:3R | shorts | 69 | -0.313 | -0.131 | 36 | 19 |

