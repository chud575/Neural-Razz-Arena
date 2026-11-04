# AVAX strategy sweep — 15m / 1h / 4h / 1D

Costs: 0.20% round trip per trade (0.1% per side), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase AVAX-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | within_n · target:opposite (shorts) | -0.270 | -0.208 | 9 | range96 max10ATR touches1 within_n sweepMax3 stop0.75ATR target:opposite exit:single | 244 | -0.181 | -0.120 |
| 1h | Range Sweep | within_n · target:3R (shorts) | -0.145 | -0.053 | 25 | range24 max6ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:single | 67 | -0.101 | -0.059 |
| 4h | Range Sweep | same_bar · target:opposite (shorts) | +0.071 | +0.054 | 65 | range24 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | 61 | +0.013 | +0.007 |
| 1d | Range Sweep | same_bar · target:opposite (longs) | +0.410 | -0.372 | 0 | range48 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:opposite exit:TP1 1R 50% BE | 6 | -0.095 | +0.092 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | range144 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | longs | 177 | +0.284 | 81 | -0.527 | -0.166 | -0.361 | -0.420 | +0.57 |
| 1h | Range Sweep | range48 max6ATR touches1 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | shorts | 157 | +0.269 | 80 | -0.057 | -0.078 | +0.022 | -0.054 | +0.14 |
| 4h | Range Sweep | range24 max6ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | both | 84 | +0.377 | 40 | +0.235 | +0.003 | +0.232 | -0.064 | +0.09 |
| 1d | Range Sweep | range48 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:2R exit:TP1 1R 50% BE | longs | 15 | +0.631 | 6 | -0.616 | -0.050 | -0.567 | -0.326 | -0.10 |


## 15-minute  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Range Sweep

2304 settings × 3 sides tested; 4327 combinations had ≥120 IS trades, 0% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.57. Average OOS result of the top-20 IS picks: -0.420 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.166 R/trade over 81 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range144 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | longs | 177 | +0.284 | 1.24 | 81 | -0.527 | -42.7 | 11 |
| range144 max15ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | longs | 210 | +0.327 | 1.21 | 94 | -0.690 | -64.9 | 9 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.25ATR target:opposite exit:single | longs | 197 | +0.306 | 1.08 | 81 | -0.740 | -59.9 | 7 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | longs | 165 | +0.248 | 1.03 | 68 | -0.535 | -36.4 | 10 |
| range144 max15ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | both | 378 | +0.089 | 0.47 | 154 | -0.461 | -71.0 | 11 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:opposite | shorts | 174 | -0.270 | -0.208 | 9 | 266 |
| same_bar · target:opposite | longs | 152 | -0.276 | -0.362 | 0 | 222 |
| within_n · target:3R | shorts | 173 | -0.277 | -0.251 | 3 | 264 |
| within_n · target:opposite | both | 227 | -0.285 | -0.248 | 2 | 329 |
| within_n · target:3R | both | 227 | -0.286 | -0.275 | 3 | 348 |
| within_n · target:2R | both | 228 | -0.289 | -0.270 | 4 | 355 |
| within_n · target:2R | shorts | 176 | -0.294 | -0.272 | 1 | 275 |
| same_bar · target:2R | longs | 152 | -0.295 | -0.383 | 0 | 228 |
| within_n · target:midline | shorts | 176 | -0.300 | -0.268 | 3 | 298 |
| same_bar · target:3R | shorts | 152 | -0.302 | -0.255 | 8 | 200 |
| same_bar · target:3R | longs | 152 | -0.304 | -0.404 | 0 | 216 |
| same_bar · target:opposite | shorts | 152 | -0.304 | -0.203 | 8 | 202 |
| within_n · target:2R | longs | 176 | -0.307 | -0.312 | 0 | 299 |
| within_n · target:opposite | longs | 176 | -0.309 | -0.297 | 0 | 284 |
| same_bar · target:midline | shorts | 152 | -0.311 | -0.264 | 4 | 210 |
| same_bar · target:opposite | both | 199 | -0.313 | -0.303 | 0 | 316 |
| within_n · target:midline | both | 228 | -0.313 | -0.273 | 2 | 356 |
| same_bar · target:3R | both | 198 | -0.322 | -0.346 | 0 | 326 |
| within_n · target:3R | longs | 175 | -0.322 | -0.325 | 0 | 284 |
| same_bar · target:midline | longs | 152 | -0.323 | -0.379 | 0 | 235 |
| same_bar · target:2R | both | 200 | -0.323 | -0.337 | 0 | 325 |
| same_bar · target:2R | shorts | 152 | -0.325 | -0.273 | 3 | 206 |
| same_bar · target:midline | both | 202 | -0.332 | -0.347 | 0 | 324 |
| within_n · target:midline | longs | 176 | -0.334 | -0.292 | 0 | 316 |


## 1-hour  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Range Sweep

2304 settings × 3 sides tested; 3228 combinations had ≥80 IS trades, 3% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.14. Average OOS result of the top-20 IS picks: -0.054 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.078 R/trade over 80 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max6ATR touches1 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | shorts | 157 | +0.269 | 1.30 | 80 | -0.057 | -4.5 | 24 |
| range24 max6ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:single | shorts | 165 | +0.188 | 1.29 | 67 | -0.101 | -6.8 | 25 |
| range24 max15ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:single | shorts | 173 | +0.174 | 1.23 | 69 | -0.128 | -8.8 | 25 |
| range24 max10ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:single | shorts | 173 | +0.174 | 1.22 | 69 | -0.128 | -8.8 | 25 |
| range48 max6ATR touches1 within_n sweepMax3 stop0.25ATR target:opposite exit:single | shorts | 200 | +0.210 | 1.20 | 94 | +0.227 | +21.4 | 31 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:3R | shorts | 136 | -0.145 | -0.053 | 25 | 87 |
| within_n · target:3R | both | 152 | -0.163 | -0.155 | 7 | 164 |
| within_n · target:3R | longs | 129 | -0.166 | -0.245 | 2 | 93 |
| same_bar · target:3R | shorts | 121 | -0.180 | -0.097 | 12 | 74 |
| same_bar · target:3R | longs | 117 | -0.192 | -0.265 | 1 | 75 |
| within_n · target:opposite | longs | 129 | -0.194 | -0.237 | 1 | 97 |
| same_bar · target:opposite | longs | 116 | -0.194 | -0.254 | 0 | 74 |
| within_n · target:2R | shorts | 138 | -0.197 | -0.069 | 17 | 91 |
| same_bar · target:3R | both | 152 | -0.204 | -0.207 | 0 | 122 |
| same_bar · target:opposite | shorts | 117 | -0.205 | +0.022 | 45 | 74 |
| within_n · target:opposite | shorts | 136 | -0.206 | +0.029 | 59 | 84 |
| within_n · target:2R | both | 152 | -0.211 | -0.149 | 7 | 174 |
| within_n · target:2R | longs | 129 | -0.212 | -0.219 | 3 | 101 |
| within_n · target:opposite | both | 152 | -0.213 | -0.114 | 12 | 170 |
| same_bar · target:2R | longs | 117 | -0.220 | -0.239 | 0 | 77 |
| within_n · target:midline | shorts | 137 | -0.224 | -0.007 | 39 | 94 |
| same_bar · target:opposite | both | 152 | -0.225 | -0.142 | 9 | 125 |
| same_bar · target:2R | shorts | 121 | -0.231 | -0.104 | 9 | 76 |
| same_bar · target:midline | longs | 118 | -0.234 | -0.246 | 0 | 78 |
| same_bar · target:2R | both | 152 | -0.239 | -0.197 | 1 | 126 |
| same_bar · target:midline | shorts | 122 | -0.240 | -0.049 | 25 | 76 |
| within_n · target:midline | longs | 129 | -0.242 | -0.207 | 2 | 105 |
| within_n · target:midline | both | 152 | -0.243 | -0.111 | 11 | 184 |
| same_bar · target:midline | both | 152 | -0.263 | -0.166 | 1 | 128 |


## 4-hour  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Range Sweep

2304 settings × 3 sides tested; 2001 combinations had ≥50 IS trades, 27% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.09. Average OOS result of the top-20 IS picks: -0.064 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.003 R/trade over 40 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max6ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | both | 84 | +0.377 | 1.79 | 40 | +0.235 | +9.4 | 32 |
| range24 max10ATR touches1 same_bar sweepMax3 stop0.75ATR target:3R exit:single | both | 214 | +0.227 | 1.78 | 71 | -0.264 | -18.8 | 20 |
| range24 max15ATR touches1 same_bar sweepMax3 stop0.75ATR target:3R exit:single | both | 214 | +0.227 | 1.78 | 72 | -0.275 | -19.8 | 19 |
| range24 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | both | 89 | +0.343 | 1.68 | 42 | +0.174 | +7.3 | 31 |
| range24 max15ATR touches1 same_bar sweepMax3 stop0.75ATR target:3R exit:single | shorts | 115 | +0.277 | 1.57 | 37 | -0.193 | -7.1 | 22 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| same_bar · target:opposite | shorts | 62 | +0.071 | +0.054 | 65 | 45 |
| same_bar · target:3R | shorts | 64 | +0.022 | -0.063 | 27 | 38 |
| same_bar · target:opposite | both | 112 | -0.000 | -0.087 | 26 | 48 |
| same_bar · target:3R | both | 112 | -0.004 | -0.126 | 16 | 49 |
| within_n · target:3R | longs | 73 | -0.015 | -0.085 | 23 | 38 |
| within_n · target:3R | both | 114 | -0.042 | -0.028 | 37 | 60 |
| within_n · target:opposite | longs | 71 | -0.042 | -0.141 | 24 | 45 |
| same_bar · target:2R | shorts | 64 | -0.056 | -0.039 | 34 | 47 |
| within_n · target:opposite | shorts | 73 | -0.058 | +0.004 | 45 | 38 |
| within_n · target:opposite | both | 113 | -0.060 | -0.038 | 35 | 58 |
| same_bar · target:midline | shorts | 64 | -0.061 | +0.015 | 61 | 54 |
| same_bar · target:opposite | longs | 56 | -0.073 | -0.263 | 4 | 48 |
| within_n · target:2R | longs | 73 | -0.074 | -0.103 | 10 | 51 |
| same_bar · target:3R | longs | 58 | -0.075 | -0.216 | 2 | 44 |
| same_bar · target:2R | both | 112 | -0.075 | -0.115 | 12 | 51 |
| within_n · target:3R | shorts | 76 | -0.076 | -0.046 | 37 | 42 |
| within_n · target:2R | both | 115 | -0.083 | -0.030 | 32 | 64 |
| within_n · target:midline | shorts | 81 | -0.097 | +0.023 | 56 | 53 |
| within_n · target:2R | shorts | 86 | -0.101 | -0.024 | 38 | 44 |
| within_n · target:midline | both | 115 | -0.126 | -0.018 | 47 | 66 |
| same_bar · target:midline | both | 112 | -0.127 | -0.099 | 13 | 52 |
| same_bar · target:2R | longs | 58 | -0.154 | -0.175 | 0 | 54 |
| within_n · target:midline | longs | 73 | -0.157 | -0.104 | 21 | 62 |
| same_bar · target:midline | longs | 64 | -0.199 | -0.176 | 19 | 62 |


## Daily  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -67%, OOS -61%)

### Range Sweep

2304 settings × 3 sides tested; 1200 combinations had ≥15 IS trades, 51% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.10. Average OOS result of the top-20 IS picks: -0.326 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.050 R/trade over 6 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:2R exit:TP1 1R 50% BE | longs | 15 | +0.631 | 2.17 | 6 | -0.616 | -3.7 | 17 |
| range48 max10ATR touches1 within_n sweepMax1 stop0.25ATR target:2R exit:TP1 1R 50% BE | longs | 15 | +0.563 | 1.98 | 8 | -0.218 | -1.7 | 38 |
| range48 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:midline exit:TP1 1R 50% BE | longs | 15 | +0.593 | 1.94 | 6 | -0.446 | -2.7 | 17 |
| range48 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:3R exit:TP1 1R 50% BE | longs | 15 | +0.572 | 1.84 | 6 | -0.533 | -3.2 | 17 |
| range48 max10ATR touches1 within_n sweepMax1 stop0.25ATR target:midline exit:TP1 1R 50% BE | longs | 15 | +0.503 | 1.72 | 8 | -0.215 | -1.7 | 38 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| same_bar · target:opposite | longs | 31 | +0.410 | -0.372 | 0 | 11 |
| same_bar · target:opposite | both | 56 | +0.199 | -0.166 | 52 | 12 |
| same_bar · target:opposite | shorts | 38 | +0.190 | +0.128 | 79 | 8 |
| within_n · target:opposite | longs | 34 | +0.124 | -0.327 | 9 | 13 |
| same_bar · target:3R | shorts | 42 | +0.109 | +0.326 | 76 | 10 |
| same_bar · target:3R | longs | 32 | +0.105 | -0.442 | 0 | 12 |
| same_bar · target:midline | longs | 34 | +0.094 | -0.436 | 0 | 12 |
| within_n · target:midline | shorts | 50 | +0.045 | +0.205 | 80 | 12 |
| same_bar · target:midline | shorts | 44 | +0.045 | +0.253 | 73 | 11 |
| within_n · target:opposite | shorts | 46 | +0.044 | -0.015 | 59 | 8 |
| same_bar · target:3R | both | 60 | +0.031 | -0.117 | 37 | 14 |
| same_bar · target:2R | longs | 34 | +0.031 | -0.394 | 0 | 12 |
| within_n · target:opposite | both | 76 | +0.030 | -0.211 | 24 | 13 |
| within_n · target:3R | shorts | 49 | +0.018 | +0.178 | 49 | 11 |
| within_n · target:midline | longs | 37 | +0.013 | -0.413 | 0 | 15 |
| same_bar · target:2R | shorts | 44 | +0.005 | +0.204 | 82 | 11 |
| same_bar · target:midline | both | 60 | +0.005 | -0.040 | 37 | 18 |
| within_n · target:2R | longs | 37 | -0.016 | -0.357 | 0 | 14 |
| within_n · target:3R | longs | 35 | -0.018 | -0.393 | 0 | 13 |
| same_bar · target:2R | both | 60 | -0.041 | -0.093 | 30 | 18 |
| within_n · target:2R | shorts | 49 | -0.050 | +0.100 | 67 | 12 |
| within_n · target:3R | both | 84 | -0.062 | -0.093 | 30 | 14 |
| within_n · target:midline | both | 84 | -0.077 | -0.050 | 19 | 14 |
| within_n · target:2R | both | 84 | -0.106 | -0.089 | 26 | 14 |

