# XRP strategy sweep — 15m / 1h / 4h / 1D

Costs: 0.20% round trip per trade (0.1% per side), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase XRP-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | within_n · target:3R (shorts) | -0.296 | -0.364 | 0 | range96 max10ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:single | 76 | -0.255 | -0.122 |
| 1h | Range Sweep | within_n · target:midline (shorts) | -0.221 | -0.161 | 7 | range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:midline exit:single | 54 | -0.084 | -0.057 |
| 4h | Range Sweep | within_n · target:3R (both) | -0.258 | -0.086 | 23 | range24 max6ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | 26 | -0.490 | -0.166 |
| 1d | Range Sweep | within_n · target:midline (longs) | +0.368 | -0.169 | 6 | range24 max15ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:TP1 1R 50% BE | 15 | -0.039 | -0.174 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | range24 max6ATR touches3 within_n sweepMax3 stop0.75ATR target:3R exit:single | both | 170 | +0.003 | 85 | -0.747 | -0.346 | -0.401 | -0.362 | +0.65 |
| 1h | Range Sweep | range96 max15ATR touches1 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | longs | 99 | +0.247 | 45 | -0.083 | -0.399 | +0.315 | -0.066 | +0.45 |
| 4h | Range Sweep | range24 max6ATR touches1 within_n sweepMax3 stop0.25ATR target:3R exit:single | shorts | 61 | +0.102 | 15 | -0.063 | +0.045 | -0.108 | -0.181 | -0.10 |
| 1d | Range Sweep | range24 max15ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:TP1 1R 50% BE | longs | 19 | +0.460 | 15 | -0.039 | -0.174 | +0.136 | +0.032 | -0.22 |


## 15-minute  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +171%, OOS -42%)

### Range Sweep

2304 settings × 3 sides tested; 3779 combinations had ≥120 IS trades, 0% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.65. Average OOS result of the top-20 IS picks: -0.362 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.346 R/trade over 85 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max6ATR touches3 within_n sweepMax3 stop0.75ATR target:3R exit:single | both | 170 | +0.003 | 0.02 | 85 | -0.747 | -63.5 | 15 |
| range48 max6ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | shorts | 155 | -0.034 | -0.16 | 92 | -0.519 | -47.7 | 24 |
| range48 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | shorts | 145 | -0.035 | -0.22 | 81 | -0.413 | -33.4 | 30 |
| range96 max10ATR touches1 within_n sweepMax1 stop0.75ATR target:opposite exit:single | shorts | 305 | -0.036 | -0.26 | 168 | -0.546 | -91.8 | 15 |
| range96 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | shorts | 182 | -0.050 | -0.26 | 109 | -0.570 | -62.1 | 16 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:3R | shorts | 151 | -0.296 | -0.364 | 0 | 223 |
| within_n · target:opposite | shorts | 151 | -0.297 | -0.361 | 4 | 222 |
| within_n · target:2R | shorts | 151 | -0.330 | -0.414 | 0 | 242 |
| same_bar · target:opposite | shorts | 136 | -0.336 | -0.432 | 1 | 192 |
| within_n · target:midline | shorts | 151 | -0.338 | -0.415 | 0 | 265 |
| same_bar · target:3R | shorts | 137 | -0.352 | -0.454 | 0 | 194 |
| within_n · target:3R | both | 192 | -0.354 | -0.487 | 0 | 404 |
| same_bar · target:midline | shorts | 137 | -0.362 | -0.470 | 0 | 209 |
| within_n · target:opposite | both | 195 | -0.372 | -0.506 | 0 | 409 |
| within_n · target:2R | both | 195 | -0.380 | -0.501 | 0 | 428 |
| same_bar · target:2R | shorts | 137 | -0.381 | -0.472 | 0 | 197 |
| within_n · target:midline | both | 196 | -0.394 | -0.501 | 0 | 471 |
| within_n · target:3R | longs | 154 | -0.422 | -0.531 | 0 | 262 |
| same_bar · target:3R | both | 158 | -0.435 | -0.502 | 0 | 378 |
| within_n · target:opposite | longs | 154 | -0.436 | -0.582 | 0 | 260 |
| same_bar · target:opposite | both | 158 | -0.436 | -0.526 | 0 | 376 |
| within_n · target:2R | longs | 154 | -0.436 | -0.529 | 0 | 281 |
| same_bar · target:2R | both | 159 | -0.442 | -0.510 | 0 | 394 |
| same_bar · target:midline | both | 159 | -0.446 | -0.512 | 0 | 408 |
| within_n · target:midline | longs | 154 | -0.457 | -0.530 | 0 | 301 |
| same_bar · target:3R | longs | 149 | -0.503 | -0.561 | 0 | 204 |
| same_bar · target:2R | longs | 151 | -0.504 | -0.561 | 0 | 212 |
| same_bar · target:opposite | longs | 149 | -0.513 | -0.625 | 0 | 203 |
| same_bar · target:midline | longs | 151 | -0.516 | -0.569 | 0 | 218 |


## 1-hour  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +185%, OOS -42%)

### Range Sweep

2304 settings × 3 sides tested; 2639 combinations had ≥80 IS trades, 1% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.45. Average OOS result of the top-20 IS picks: -0.066 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.399 R/trade over 45 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range96 max15ATR touches1 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | longs | 99 | +0.247 | 0.99 | 45 | -0.083 | -3.8 | 18 |
| range96 max15ATR touches1 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | longs | 121 | +0.167 | 0.65 | 70 | -0.159 | -11.2 | 13 |
| range96 max10ATR touches1 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | longs | 80 | +0.149 | 0.60 | 52 | -0.148 | -7.7 | 17 |
| range96 max15ATR touches1 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | longs | 102 | +0.126 | 0.52 | 43 | -0.036 | -1.5 | 19 |
| range96 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:midline exit:single | both | 108 | +0.091 | 0.47 | 70 | -0.473 | -33.1 | 27 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:midline | shorts | 104 | -0.221 | -0.161 | 7 | 65 |
| same_bar · target:opposite | shorts | 90 | -0.238 | -0.072 | 31 | 47 |
| same_bar · target:midline | shorts | 95 | -0.244 | -0.169 | 9 | 64 |
| within_n · target:opposite | shorts | 99 | -0.246 | -0.005 | 33 | 58 |
| same_bar · target:opposite | longs | 93 | -0.246 | -0.453 | 0 | 69 |
| within_n · target:3R | shorts | 101 | -0.249 | -0.154 | 24 | 59 |
| within_n · target:2R | shorts | 102 | -0.258 | -0.185 | 11 | 62 |
| within_n · target:3R | both | 135 | -0.260 | -0.251 | 10 | 132 |
| within_n · target:midline | both | 137 | -0.262 | -0.252 | 3 | 148 |
| within_n · target:3R | longs | 108 | -0.262 | -0.307 | 9 | 87 |
| same_bar · target:3R | longs | 97 | -0.265 | -0.323 | 11 | 77 |
| same_bar · target:opposite | both | 123 | -0.266 | -0.285 | 11 | 103 |
| within_n · target:opposite | both | 133 | -0.268 | -0.250 | 9 | 129 |
| same_bar · target:midline | longs | 100 | -0.271 | -0.334 | 2 | 86 |
| same_bar · target:2R | shorts | 93 | -0.271 | -0.245 | 3 | 54 |
| same_bar · target:midline | both | 125 | -0.272 | -0.281 | 2 | 114 |
| same_bar · target:3R | shorts | 89 | -0.272 | -0.225 | 11 | 58 |
| within_n · target:opposite | longs | 107 | -0.273 | -0.402 | 5 | 83 |
| same_bar · target:3R | both | 121 | -0.277 | -0.281 | 9 | 109 |
| within_n · target:2R | both | 137 | -0.290 | -0.244 | 1 | 136 |
| within_n · target:midline | longs | 114 | -0.297 | -0.298 | 3 | 95 |
| same_bar · target:2R | both | 122 | -0.302 | -0.291 | 1 | 113 |
| same_bar · target:2R | longs | 100 | -0.304 | -0.297 | 7 | 76 |
| within_n · target:2R | longs | 114 | -0.313 | -0.280 | 5 | 90 |


## 4-hour  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +182%, OOS -42%)

### Range Sweep

2304 settings × 3 sides tested; 1130 combinations had ≥50 IS trades, 0% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.10. Average OOS result of the top-20 IS picks: -0.181 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.045 R/trade over 15 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max6ATR touches1 within_n sweepMax3 stop0.25ATR target:3R exit:single | shorts | 61 | +0.102 | 0.43 | 15 | -0.063 | -0.9 | 27 |
| range96 max15ATR touches1 within_n sweepMax3 stop0.25ATR target:midline exit:single | longs | 55 | +0.023 | 0.10 | 53 | -0.395 | -20.9 | 17 |
| range48 max10ATR touches1 within_n sweepMax3 stop0.75ATR target:opposite exit:TP1 1R 50% BE | longs | 58 | +0.009 | 0.06 | 51 | -0.217 | -11.1 | 47 |
| range48 max15ATR touches1 within_n sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | 67 | +0.007 | 0.05 | 53 | -0.112 | -5.9 | 49 |
| range24 max6ATR touches1 within_n sweepMax3 stop0.25ATR target:3R exit:TP1 1R 50% BE | shorts | 73 | +0.003 | 0.02 | 23 | -0.011 | -0.3 | 48 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:3R | both | 71 | -0.258 | -0.086 | 23 | 37 |
| within_n · target:2R | both | 77 | -0.260 | -0.131 | 12 | 56 |
| same_bar · target:2R | longs | 40 | -0.261 | -0.125 | 5 | 56 |
| within_n · target:3R | shorts | 31 | -0.265 | +0.266 | 61 | 13 |
| same_bar · target:3R | longs | 35 | -0.266 | -0.172 | 6 | 48 |
| same_bar · target:2R | both | 57 | -0.270 | -0.095 | 16 | 60 |
| same_bar · target:3R | both | 53 | -0.272 | -0.077 | 21 | 48 |
| within_n · target:opposite | longs | 36 | -0.280 | -0.142 | 19 | 58 |
| within_n · target:2R | longs | 42 | -0.281 | -0.101 | 12 | 64 |
| same_bar · target:opposite | longs | 37 | -0.291 | -0.111 | 27 | 44 |
| within_n · target:3R | longs | 30 | -0.292 | -0.173 | 3 | 54 |
| same_bar · target:midline | shorts | 41 | -0.298 | +0.041 | 56 | 20 |
| within_n · target:midline | both | 80 | -0.305 | -0.209 | 1 | 68 |
| same_bar · target:midline | both | 58 | -0.313 | -0.143 | 2 | 72 |
| same_bar · target:midline | longs | 42 | -0.313 | -0.172 | 0 | 60 |
| within_n · target:midline | longs | 42 | -0.313 | -0.185 | 0 | 74 |
| within_n · target:2R | shorts | 45 | -0.316 | +0.040 | 53 | 21 |
| within_n · target:opposite | both | 74 | -0.319 | -0.054 | 27 | 38 |
| same_bar · target:opposite | both | 51 | -0.325 | +0.037 | 39 | 53 |
| same_bar · target:3R | shorts | 27 | -0.331 | +0.040 | 48 | 12 |
| within_n · target:midline | shorts | 46 | -0.333 | -0.007 | 59 | 26 |
| same_bar · target:2R | shorts | 41 | -0.343 | +0.039 | 54 | 17 |
| within_n · target:opposite | shorts | 39 | -0.354 | +0.616 | 85 | 17 |
| same_bar · target:opposite | shorts | 35 | -0.362 | +0.484 | 80 | 15 |


## Daily  (IS 2023-07-14 → 2025-11-07, OOS 2025-11-07 → 2026-11-04; XRP buy & hold: IS +222%, OOS -44%)

### Range Sweep

2304 settings × 3 sides tested; 353 combinations had ≥15 IS trades, 53% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.22. Average OOS result of the top-20 IS picks: +0.032 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.174 R/trade over 15 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max15ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:TP1 1R 50% BE | longs | 19 | +0.460 | 2.36 | 15 | -0.039 | -0.6 | 53 |
| range24 max10ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:single | longs | 19 | +0.423 | 2.25 | 14 | -0.235 | -3.3 | 36 |
| range24 max6ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:TP1 1R 50% BE | longs | 18 | +0.445 | 2.16 | 11 | -0.062 | -0.7 | 45 |
| range24 max6ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:single | longs | 18 | +0.416 | 2.09 | 8 | +0.123 | +1.0 | 50 |
| range24 max15ATR touches1 within_n sweepMax3 stop0.25ATR target:2R exit:TP1 1R 50% BE | both | 34 | +0.388 | 2.05 | 12 | +0.342 | +4.1 | 58 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:opposite | longs | 2 | +0.472 | +0.314 | 100 | 9 |
| within_n · target:midline | longs | 18 | +0.368 | -0.169 | 6 | 15 |
| same_bar · target:midline | longs | 6 | +0.362 | -0.223 | 0 | 16 |
| within_n · target:2R | both | 30 | +0.180 | +0.444 | 87 | 12 |
| within_n · target:opposite | both | 31 | +0.142 | +0.575 | 94 | 11 |
| same_bar · target:3R | both | 20 | +0.088 | +0.790 | 100 | 10 |
| same_bar · target:2R | both | 26 | +0.037 | +0.456 | 100 | 11 |
| within_n · target:midline | both | 40 | +0.024 | +0.289 | 78 | 18 |
| same_bar · target:opposite | both | 25 | +0.019 | +0.640 | 100 | 11 |
| within_n · target:3R | both | 19 | +0.014 | +0.549 | 100 | 9 |
| same_bar · target:3R | shorts | 4 | +0.007 | +0.457 | 100 | 2 |
| within_n · target:2R | shorts | 11 | -0.034 | +0.321 | 64 | 2 |
| same_bar · target:midline | both | 40 | -0.051 | +0.236 | 60 | 16 |
| within_n · target:3R | shorts | 4 | -0.065 | +0.457 | 100 | 2 |
| same_bar · target:2R | shorts | 10 | -0.112 | +0.223 | 60 | 3 |
| within_n · target:opposite | shorts | 14 | -0.144 | +1.199 | 100 | 3 |
| within_n · target:midline | shorts | 26 | -0.198 | +0.619 | 100 | 6 |
| same_bar · target:opposite | shorts | 7 | -0.201 | +1.010 | 100 | 3 |
| same_bar · target:midline | shorts | 20 | -0.262 | +0.367 | 100 | 6 |

