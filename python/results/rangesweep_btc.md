# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: 0.20% round trip per trade (0.1% per side), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | within_n · target:opposite (longs) | -0.444 | -0.540 | 0 | range144 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | 129 | -0.402 | -0.365 |
| 1h | Range Sweep | same_bar · target:3R (longs) | -0.143 | -0.243 | 1 | range48 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | 60 | -0.166 | -0.208 |
| 4h | Range Sweep | same_bar · target:opposite (shorts) | +0.056 | -0.220 | 4 | range96 max10ATR touches1 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | 39 | -0.156 | -0.198 |
| 1d | Range Sweep | within_n · target:3R (longs) | +0.072 | +0.166 | 81 | range24 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | 10 | +0.538 | +0.223 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | range144 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | shorts | 219 | -0.097 | 96 | -0.412 | -0.399 | -0.013 | -0.440 | +0.82 |
| 1h | Range Sweep | range48 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 85 | +0.335 | 60 | -0.166 | -0.208 | +0.042 | -0.179 | +0.12 |
| 4h | Range Sweep | range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | 50 | +0.343 | 32 | -0.376 | -0.074 | -0.302 | -0.231 | +0.02 |
| 1d | Range Sweep | range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | 23 | +1.217 | 12 | +0.119 | +0.055 | +0.064 | +0.383 | +0.21 |


## 15-minute  (IS 2020-01-01 → 2024-10-14, OOS 2024-10-14 → 2026-11-03; BTC buy & hold: IS +817%, OOS +17%)

### Range Sweep

2304 settings × 3 sides tested; 4462 combinations had ≥120 IS trades, 0% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.82. Average OOS result of the top-20 IS picks: -0.440 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.399 R/trade over 96 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range144 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | shorts | 219 | -0.097 | -0.56 | 96 | -0.412 | -39.5 | 15 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | shorts | 229 | -0.131 | -0.78 | 101 | -0.469 | -47.4 | 16 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | shorts | 192 | -0.151 | -0.81 | 88 | -0.350 | -30.8 | 15 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | longs | 223 | -0.149 | -0.83 | 129 | -0.402 | -51.8 | 17 |
| range144 max15ATR touches2 within_n sweepMax3 stop0.75ATR target:opposite exit:single | shorts | 285 | -0.127 | -0.89 | 132 | -0.404 | -53.3 | 19 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:opposite | longs | 196 | -0.444 | -0.540 | 0 | 384 |
| within_n · target:2R | shorts | 186 | -0.445 | -0.581 | 0 | 416 |
| within_n · target:3R | shorts | 185 | -0.445 | -0.561 | 0 | 365 |
| within_n · target:opposite | both | 220 | -0.446 | -0.561 | 0 | 596 |
| within_n · target:opposite | shorts | 185 | -0.447 | -0.596 | 0 | 390 |
| within_n · target:3R | both | 220 | -0.449 | -0.543 | 0 | 590 |
| within_n · target:3R | longs | 190 | -0.458 | -0.542 | 0 | 374 |
| within_n · target:2R | both | 220 | -0.461 | -0.566 | 0 | 643 |
| within_n · target:2R | longs | 196 | -0.471 | -0.563 | 0 | 400 |
| same_bar · target:opposite | shorts | 152 | -0.471 | -0.647 | 0 | 354 |
| within_n · target:midline | shorts | 182 | -0.472 | -0.625 | 0 | 464 |
| same_bar · target:opposite | longs | 160 | -0.473 | -0.612 | 0 | 364 |
| same_bar · target:2R | shorts | 152 | -0.479 | -0.657 | 0 | 367 |
| same_bar · target:3R | shorts | 152 | -0.481 | -0.666 | 0 | 346 |
| within_n · target:midline | both | 220 | -0.483 | -0.614 | 0 | 661 |
| within_n · target:midline | longs | 190 | -0.487 | -0.620 | 0 | 463 |
| same_bar · target:midline | shorts | 152 | -0.494 | -0.677 | 0 | 382 |
| same_bar · target:3R | longs | 160 | -0.502 | -0.631 | 0 | 367 |
| same_bar · target:2R | longs | 160 | -0.516 | -0.641 | 0 | 396 |
| same_bar · target:midline | longs | 160 | -0.517 | -0.670 | 0 | 400 |
| same_bar · target:opposite | both | 206 | -0.518 | -0.644 | 0 | 520 |
| same_bar · target:3R | both | 206 | -0.533 | -0.661 | 0 | 524 |
| same_bar · target:2R | both | 206 | -0.535 | -0.665 | 0 | 536 |
| same_bar · target:midline | both | 206 | -0.548 | -0.700 | 0 | 543 |


## 1-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6684%, OOS +163%)

### Range Sweep

2304 settings × 3 sides tested; 3416 combinations had ≥80 IS trades, 4% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.12. Average OOS result of the top-20 IS picks: -0.179 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.208 R/trade over 60 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 85 | +0.335 | 1.60 | 60 | -0.166 | -10.0 | 27 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | longs | 153 | +0.221 | 1.42 | 110 | +0.107 | +11.8 | 33 |
| range48 max6ATR touches2 same_bar sweepMax3 stop0.25ATR target:3R exit:single | longs | 91 | +0.284 | 1.38 | 65 | -0.314 | -20.4 | 26 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | 177 | +0.185 | 1.27 | 129 | -0.067 | -8.7 | 31 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | longs | 156 | +0.196 | 1.27 | 113 | +0.109 | +12.3 | 33 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| same_bar · target:3R | longs | 139 | -0.143 | -0.243 | 1 | 147 |
| same_bar · target:opposite | shorts | 120 | -0.144 | -0.241 | 2 | 164 |
| within_n · target:3R | longs | 150 | -0.146 | -0.201 | 5 | 170 |
| same_bar · target:opposite | both | 152 | -0.171 | -0.226 | 9 | 292 |
| within_n · target:3R | both | 164 | -0.173 | -0.192 | 5 | 322 |
| same_bar · target:3R | both | 152 | -0.175 | -0.237 | 0 | 282 |
| within_n · target:opposite | longs | 148 | -0.182 | -0.225 | 6 | 172 |
| same_bar · target:2R | longs | 139 | -0.184 | -0.296 | 0 | 155 |
| within_n · target:2R | longs | 150 | -0.190 | -0.238 | 1 | 182 |
| same_bar · target:3R | shorts | 120 | -0.194 | -0.239 | 0 | 164 |
| same_bar · target:opposite | longs | 138 | -0.197 | -0.268 | 7 | 152 |
| within_n · target:opposite | both | 164 | -0.198 | -0.202 | 4 | 342 |
| within_n · target:2R | both | 164 | -0.201 | -0.218 | 0 | 356 |
| same_bar · target:midline | shorts | 120 | -0.202 | -0.245 | 1 | 177 |
| same_bar · target:2R | both | 152 | -0.203 | -0.268 | 0 | 298 |
| within_n · target:midline | longs | 152 | -0.205 | -0.248 | 1 | 202 |
| within_n · target:opposite | shorts | 128 | -0.207 | -0.202 | 5 | 199 |
| within_n · target:3R | shorts | 128 | -0.210 | -0.203 | 7 | 198 |
| within_n · target:2R | shorts | 129 | -0.211 | -0.210 | 3 | 211 |
| same_bar · target:2R | shorts | 120 | -0.211 | -0.239 | 3 | 174 |
| within_n · target:midline | shorts | 132 | -0.215 | -0.218 | 2 | 221 |
| same_bar · target:midline | longs | 139 | -0.215 | -0.279 | 1 | 160 |
| within_n · target:midline | both | 164 | -0.218 | -0.236 | 0 | 386 |
| same_bar · target:midline | both | 152 | -0.221 | -0.249 | 0 | 305 |


## 4-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6640%, OOS +164%)

### Range Sweep

2304 settings × 3 sides tested; 2734 combinations had ≥50 IS trades, 25% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.02. Average OOS result of the top-20 IS picks: -0.231 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.074 R/trade over 32 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | 50 | +0.343 | 2.15 | 32 | -0.376 | -12.0 | 38 |
| range24 max10ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | 51 | +0.315 | 1.98 | 33 | -0.302 | -10.0 | 42 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | 57 | +0.287 | 1.91 | 36 | -0.244 | -8.8 | 42 |
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | 108 | +0.204 | 1.90 | 59 | -0.384 | -22.6 | 36 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | 118 | +0.195 | 1.90 | 64 | -0.280 | -17.9 | 39 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| same_bar · target:opposite | shorts | 96 | +0.056 | -0.220 | 4 | 59 |
| within_n · target:opposite | shorts | 117 | +0.007 | -0.207 | 11 | 53 |
| same_bar · target:opposite | both | 124 | -0.003 | -0.245 | 5 | 76 |
| within_n · target:opposite | longs | 107 | -0.010 | -0.164 | 21 | 55 |
| within_n · target:opposite | both | 139 | -0.027 | -0.206 | 4 | 97 |
| within_n · target:3R | longs | 110 | -0.027 | -0.101 | 23 | 59 |
| within_n · target:2R | longs | 110 | -0.043 | -0.141 | 9 | 62 |
| within_n · target:midline | longs | 112 | -0.066 | -0.221 | 1 | 62 |
| same_bar · target:3R | longs | 87 | -0.077 | -0.161 | 11 | 77 |
| same_bar · target:2R | longs | 91 | -0.092 | -0.196 | 9 | 71 |
| same_bar · target:3R | both | 125 | -0.104 | -0.249 | 1 | 77 |
| within_n · target:3R | both | 141 | -0.105 | -0.177 | 7 | 97 |
| same_bar · target:opposite | longs | 90 | -0.109 | -0.212 | 10 | 52 |
| same_bar · target:3R | shorts | 97 | -0.116 | -0.275 | 2 | 65 |
| within_n · target:2R | both | 141 | -0.116 | -0.202 | 6 | 101 |
| same_bar · target:2R | both | 125 | -0.123 | -0.262 | 0 | 78 |
| same_bar · target:midline | longs | 94 | -0.123 | -0.290 | 1 | 67 |
| within_n · target:midline | both | 142 | -0.128 | -0.221 | 2 | 101 |
| same_bar · target:2R | shorts | 102 | -0.141 | -0.264 | 1 | 58 |
| within_n · target:3R | shorts | 119 | -0.141 | -0.217 | 7 | 52 |
| same_bar · target:midline | both | 125 | -0.148 | -0.288 | 0 | 80 |
| within_n · target:2R | shorts | 120 | -0.154 | -0.213 | 6 | 56 |
| within_n · target:midline | shorts | 119 | -0.158 | -0.211 | 3 | 56 |
| same_bar · target:midline | shorts | 101 | -0.167 | -0.253 | 0 | 59 |


## Daily  (IS 2015-07-20 → 2023-06-15, OOS 2023-06-15 → 2026-11-03; BTC buy & hold: IS +9032%, OOS +201%)

### Range Sweep

2304 settings × 3 sides tested; 1927 combinations had ≥15 IS trades, 20% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.21. Average OOS result of the top-20 IS picks: +0.383 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.055 R/trade over 12 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | 23 | +1.217 | 1.46 | 12 | +0.119 | +1.4 | 25 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | both | 17 | +1.541 | 1.42 | 14 | -0.335 | -4.7 | 14 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | 24 | +1.119 | 1.39 | 12 | +1.042 | +12.5 | 33 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | both | 18 | +1.393 | 1.35 | 14 | +0.451 | +6.3 | 21 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | both | 29 | +0.465 | 1.26 | 14 | +0.951 | +13.3 | 50 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:3R | longs | 52 | +0.072 | +0.166 | 81 | 17 |
| within_n · target:opposite | longs | 44 | +0.064 | -0.026 | 55 | 19 |
| within_n · target:midline | longs | 46 | +0.055 | +0.033 | 52 | 28 |
| same_bar · target:midline | longs | 40 | +0.041 | -0.131 | 12 | 24 |
| same_bar · target:3R | longs | 39 | +0.026 | -0.111 | 26 | 15 |
| same_bar · target:opposite | longs | 35 | +0.005 | -0.126 | 23 | 17 |
| within_n · target:2R | longs | 52 | -0.023 | +0.101 | 75 | 20 |
| same_bar · target:2R | longs | 40 | -0.029 | -0.024 | 40 | 17 |
| within_n · target:3R | both | 114 | -0.083 | +0.092 | 59 | 23 |
| within_n · target:opposite | both | 114 | -0.113 | -0.015 | 42 | 22 |
| same_bar · target:3R | both | 104 | -0.131 | -0.001 | 42 | 20 |
| within_n · target:2R | both | 114 | -0.135 | +0.064 | 58 | 24 |
| same_bar · target:2R | both | 105 | -0.183 | -0.013 | 42 | 20 |
| same_bar · target:opposite | both | 103 | -0.206 | -0.070 | 38 | 19 |
| within_n · target:midline | both | 115 | -0.216 | +0.022 | 47 | 25 |
| within_n · target:3R | shorts | 103 | -0.230 | -0.084 | 34 | 16 |
| within_n · target:2R | shorts | 106 | -0.248 | -0.102 | 34 | 17 |
| same_bar · target:3R | shorts | 74 | -0.259 | -0.068 | 27 | 20 |
| within_n · target:opposite | shorts | 100 | -0.262 | -0.224 | 19 | 16 |
| same_bar · target:midline | both | 102 | -0.278 | -0.041 | 30 | 20 |
| same_bar · target:2R | shorts | 74 | -0.280 | -0.061 | 24 | 21 |
| within_n · target:midline | shorts | 108 | -0.310 | -0.128 | 27 | 17 |
| same_bar · target:opposite | shorts | 74 | -0.326 | -0.164 | 35 | 19 |
| same_bar · target:midline | shorts | 69 | -0.364 | -0.035 | 39 | 25 |

