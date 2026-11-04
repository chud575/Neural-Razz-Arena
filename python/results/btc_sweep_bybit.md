# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | within_n · target:2R (shorts) | -0.125 | -0.144 | 6 | range144 max10ATR touches2 within_n sweepMax3 stop0.75ATR target:2R exit:single | 83 | +0.045 | -0.113 |
| 15m | Double Top / Bottom | B (longs) | -0.012 | -0.094 | 14 | piv8 tol0.3 depth1.0 B 3R trend:sma exit:single | 49 | -0.181 | -0.201 |
| 15m | Triple Top / Bottom | B (longs) | +0.023 | -0.043 | 28 | piv8 tol3.0 depth0.5 B 3R trend:sma exit:single | 43 | -0.248 | -0.165 |
| 15m | S/R Flip | rejection · levels htf:D (both) | -0.062 | -0.152 | 0 | piv5 rejection 2R tries3 levels:htf:D trend:off exit:single | 57 | -0.167 | -0.226 |
| 15m | Megaphone | failedBO (shorts) | +0.026 | -0.051 | 33 | piv3 swings4 expand0.5 failedBO midline trend:off exit:single | 83 | -0.085 | -0.113 |
| 1h | Range Sweep | same_bar · target:opposite (shorts) | +0.036 | -0.021 | 39 | range48 max6ATR touches1 same_bar sweepMax1 stop0.75ATR target:opposite exit:TP1 1R 50% BE | 139 | -0.110 | +0.020 |
| 1h | Double Top / Bottom | B (both) | +0.070 | -0.111 | 8 | piv5 tol0.6 depth1.0 B 2R trend:sma exit:single | 113 | -0.109 | +0.015 |
| 1h | Triple Top / Bottom | B (longs) | +0.137 | +0.011 | 47 | piv5 tol2.0 depth0.5 B 1.5R trend:sma exit:TP1 1R 50% BE | 66 | +0.090 | +0.016 |
| 1h | S/R Flip | rejection · levels htf:D (shorts) | +0.162 | -0.146 | 0 | piv3 rejection 3R tries3 levels:htf:D trend:sma exit:single | 43 | -0.042 | +0.014 |
| 1h | Megaphone | BO-close (longs) | +0.343 | -0.138 | 12 | piv5 swings4 expand0.5 BO-close measured trend:off exit:single | 64 | -0.106 | +0.033 |
| 4h | Range Sweep | same_bar · target:opposite (shorts) | +0.178 | -0.083 | 22 | range24 max6ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | 31 | +0.035 | -0.029 |
| 4h | Double Top / Bottom | B (both) | +0.161 | +0.109 | 69 | piv5 tol1.0 depth1.0 B 3R trend:sma exit:TP1 1R 50% BE | 24 | +0.247 | +0.014 |
| 4h | Triple Top / Bottom | B+Retest (both) | +0.252 | +0.194 | 91 | piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single | 38 | +0.048 | -0.087 |
| 4h | S/R Flip | rejection · levels htf:D (longs) | +0.135 | -0.077 | 17 | piv3 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | 47 | -0.057 | -0.109 |
| 4h | Megaphone | BO-close (longs) | +1.129 | +0.129 | 82 | piv5 swings4 expand0.0 BO-close 2R trend:off exit:single | 30 | +0.127 | -0.120 |
| 1d | Range Sweep | within_n · target:midline (longs) | +0.025 | +0.006 | 48 | range24 max10ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:single | 32 | -0.026 | +0.052 |
| 1d | S/R Flip | sweep · levels chart (longs) | +0.386 | -0.089 | 32 | piv3 sweep 3R tries1 levels:chart trend:off exit:single | 16 | -0.386 | -0.063 |
| 1d | Megaphone | BO-retest (both) | +1.132 | +1.093 | 100 | piv3 swings4 expand0.0 BO-retest 3R trend:off exit:single | 5 | +0.590 | -0.202 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Range Sweep | range96 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | shorts | 306 | +0.110 | 150 | +0.185 | -0.168 | +0.353 | -0.041 | +0.53 |
| 15m | Double Top / Bottom | piv5 tol0.3 depth1.0 RetestConf 3R trend:sma exit:TP1 1R 50% BE | longs | 149 | +0.180 | 50 | -0.140 | -0.156 | +0.016 | -0.151 | -0.19 |
| 15m | Triple Top / Bottom | piv8 tol3.0 depth1.0 B+Retest 3R trend:sma exit:single | both | 367 | +0.322 | 130 | -0.161 | -0.060 | -0.101 | -0.142 | -0.14 |
| 15m | S/R Flip | piv8 sweep 3R tries3 levels:htf:4h trend:sma exit:single | shorts | 263 | +0.101 | 134 | -0.088 | -0.136 | +0.048 | -0.171 | +0.66 |
| 15m | Megaphone | piv5 swings4 expand0.5 BO-close measured trend:sma exit:single | both | 524 | +0.404 | 223 | -0.344 | -0.218 | -0.126 | -0.287 | +0.51 |
| 1h | Range Sweep | range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | 177 | +0.328 | 129 | +0.123 | -0.159 | +0.281 | +0.024 | +0.08 |
| 1h | Double Top / Bottom | piv8 tol0.3 depth1.0 B+Retest 2R trend:sma exit:single | shorts | 92 | +0.478 | 53 | -0.031 | -0.058 | +0.028 | -0.091 | +0.01 |
| 1h | Triple Top / Bottom | piv5 tol2.0 depth0.5 B 2R trend:sma exit:TP1 1R 50% BE | both | 259 | +0.220 | 118 | -0.003 | +0.010 | -0.013 | -0.046 | +0.03 |
| 1h | S/R Flip | piv3 rejection 3R tries3 levels:htf:D trend:sma exit:single | shorts | 98 | +0.331 | 43 | -0.042 | +0.014 | -0.056 | -0.070 | +0.07 |
| 1h | Megaphone | piv3 swings4 expand0.5 BO-close measured trend:off exit:single | both | 278 | +0.785 | 134 | +0.297 | -0.116 | +0.412 | +0.076 | +0.29 |
| 4h | Range Sweep | range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | 108 | +0.266 | 59 | -0.310 | +0.012 | -0.322 | -0.205 | -0.00 |
| 4h | Double Top / Bottom | piv3 tol1.0 depth0.5 B+Retest 3R trend:sma exit:TP1 1R 50% BE | longs | 51 | +0.456 | 27 | -0.088 | +0.097 | -0.185 | +0.046 | -0.23 |
| 4h | Triple Top / Bottom | piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single | both | 63 | +0.823 | 38 | +0.048 | -0.087 | +0.135 | +0.119 | +0.19 |
| 4h | S/R Flip | piv3 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | both | 131 | +0.227 | 72 | -0.044 | -0.076 | +0.032 | -0.118 | +0.11 |
| 4h | Megaphone | piv5 swings4 expand0.0 BO-close 2R trend:off exit:single | longs | 60 | +0.676 | 30 | +0.127 | -0.120 | +0.247 | +0.080 | +0.53 |
| 1d | Range Sweep | range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | 23 | +1.282 | 12 | +0.181 | +0.119 | +0.062 | +0.569 | +0.11 |
| 1d | S/R Flip | piv8 rejection 2R tries1 levels:chart trend:sma exit:TP1 1R 50% BE | both | 26 | +0.542 | 13 | -0.014 | -0.052 | +0.037 | -0.106 | -0.18 |
| 1d | Megaphone | piv3 swings4 expand0.0 BO-close 1.5R trend:sma exit:single | both | 16 | +0.999 | 10 | +0.657 | -0.166 | +0.823 | +0.840 | -0.09 |


## 15-minute  (IS 2020-01-01 → 2024-10-14, OOS 2024-10-14 → 2026-11-03; BTC buy & hold: IS +817%, OOS +17%)

### Range Sweep

2304 settings × 3 sides tested; 4462 combinations had ≥120 IS trades, 2% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.53. Average OOS result of the top-20 IS picks: -0.041 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.168 R/trade over 150 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range96 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | shorts | 306 | +0.110 | 1.02 | 150 | +0.185 | +27.7 | 34 |
| range96 max10ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:TP1 1R 50% BE | shorts | 215 | +0.100 | 0.93 | 96 | -0.248 | -23.8 | 50 |
| range96 max10ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:TP1 1R 50% BE | shorts | 285 | +0.064 | 0.91 | 133 | +0.115 | +15.3 | 62 |
| range96 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:TP1 1R 50% BE | shorts | 316 | +0.053 | 0.78 | 157 | -0.000 | -0.0 | 58 |
| range96 max10ATR touches2 same_bar sweepMax1 stop0.25ATR target:opposite exit:TP1 1R 50% BE | shorts | 195 | +0.084 | 0.72 | 92 | -0.252 | -23.1 | 50 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:2R | shorts | 186 | -0.125 | -0.144 | 6 | 416 |
| within_n · target:3R | shorts | 185 | -0.133 | -0.133 | 7 | 365 |
| within_n · target:opposite | shorts | 185 | -0.133 | -0.169 | 2 | 390 |
| within_n · target:midline | shorts | 182 | -0.142 | -0.172 | 3 | 464 |
| same_bar · target:opposite | shorts | 152 | -0.145 | -0.189 | 3 | 354 |
| same_bar · target:2R | shorts | 152 | -0.146 | -0.184 | 0 | 367 |
| same_bar · target:midline | shorts | 152 | -0.151 | -0.197 | 1 | 382 |
| same_bar · target:3R | shorts | 152 | -0.155 | -0.202 | 1 | 346 |
| within_n · target:opposite | both | 220 | -0.161 | -0.173 | 1 | 596 |
| within_n · target:3R | both | 220 | -0.164 | -0.151 | 5 | 590 |
| within_n · target:2R | both | 220 | -0.168 | -0.162 | 2 | 643 |
| within_n · target:midline | both | 220 | -0.178 | -0.195 | 0 | 661 |
| within_n · target:opposite | longs | 196 | -0.188 | -0.182 | 2 | 384 |
| within_n · target:3R | longs | 190 | -0.201 | -0.176 | 8 | 374 |
| within_n · target:2R | longs | 196 | -0.203 | -0.181 | 3 | 400 |
| same_bar · target:opposite | both | 206 | -0.205 | -0.210 | 0 | 520 |
| within_n · target:midline | longs | 190 | -0.207 | -0.224 | 0 | 463 |
| same_bar · target:2R | both | 206 | -0.213 | -0.213 | 0 | 536 |
| same_bar · target:opposite | longs | 160 | -0.213 | -0.236 | 0 | 364 |
| same_bar · target:midline | both | 206 | -0.216 | -0.235 | 0 | 543 |
| same_bar · target:3R | both | 206 | -0.219 | -0.220 | 4 | 524 |
| same_bar · target:midline | longs | 160 | -0.234 | -0.259 | 0 | 400 |
| same_bar · target:3R | longs | 160 | -0.239 | -0.245 | 0 | 367 |
| same_bar · target:2R | longs | 160 | -0.242 | -0.239 | 0 | 396 |

### Double Top / Bottom

1620 settings × 3 sides tested; 4066 combinations had ≥120 IS trades, 8% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.19. Average OOS result of the top-20 IS picks: -0.151 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.156 R/trade over 50 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol0.3 depth1.0 RetestConf 3R trend:sma exit:TP1 1R 50% BE | longs | 149 | +0.180 | 1.81 | 50 | -0.140 | -7.0 | 48 |
| piv8 tol0.3 depth1.0 B 3R trend:sma exit:single | longs | 165 | +0.249 | 1.70 | 49 | -0.181 | -8.9 | 22 |
| piv8 tol0.3 depth1.0 B+Retest 3R trend:sma exit:single | longs | 300 | +0.177 | 1.66 | 88 | -0.078 | -6.9 | 25 |
| piv5 tol0.3 depth1.0 RetestConf 3R trend:sma exit:single | longs | 139 | +0.260 | 1.62 | 44 | +0.012 | +0.5 | 27 |
| piv5 tol1.0 depth2.0 B+Retest 3R trend:sma exit:single | longs | 225 | +0.177 | 1.44 | 58 | -0.038 | -2.2 | 26 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 251 | -0.012 | -0.094 | 14 | 138 |
| RetestConf | longs | 243 | -0.045 | -0.088 | 11 | 131 |
| B+Mid | longs | 275 | -0.047 | -0.125 | 13 | 193 |
| B+Retest | longs | 281 | -0.051 | -0.076 | 19 | 233 |
| B | both | 287 | -0.061 | -0.052 | 26 | 252 |
| RetestConf | both | 278 | -0.072 | -0.055 | 16 | 242 |
| B+Retest | both | 317 | -0.076 | -0.041 | 25 | 414 |
| Retest | longs | 245 | -0.081 | -0.090 | 13 | 157 |
| B+Mid | both | 304 | -0.085 | -0.063 | 25 | 358 |
| RetestConf | shorts | 234 | -0.091 | -0.012 | 33 | 142 |
| Retest | both | 282 | -0.096 | -0.049 | 22 | 285 |
| B+Retest | shorts | 286 | -0.103 | -0.023 | 36 | 231 |
| Retest | shorts | 250 | -0.105 | -0.024 | 31 | 162 |
| B | shorts | 253 | -0.107 | -0.016 | 42 | 138 |
| B+Mid | shorts | 280 | -0.123 | -0.023 | 45 | 197 |

### Triple Top / Bottom

1620 settings × 3 sides tested; 4556 combinations had ≥120 IS trades, 20% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.14. Average OOS result of the top-20 IS picks: -0.142 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.060 R/trade over 130 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol3.0 depth1.0 B+Retest 3R trend:sma exit:single | both | 367 | +0.322 | 3.26 | 130 | -0.161 | -20.9 | 22 |
| piv8 tol3.0 depth1.0 B+Retest 3R trend:sma exit:single | longs | 195 | +0.415 | 3.01 | 69 | -0.219 | -15.1 | 22 |
| piv8 tol3.0 depth2.0 B+Retest 3R trend:off exit:single | longs | 177 | +0.389 | 2.70 | 71 | -0.236 | -16.7 | 21 |
| piv8 tol3.0 depth1.0 B+Mid 3R trend:sma exit:single | both | 283 | +0.288 | 2.59 | 98 | -0.091 | -8.9 | 23 |
| piv8 tol3.0 depth2.0 B+Mid 3R trend:off exit:single | longs | 135 | +0.418 | 2.52 | 52 | -0.309 | -16.1 | 19 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 296 | +0.023 | -0.043 | 28 | 90 |
| B+Mid | longs | 312 | -0.003 | -0.075 | 24 | 119 |
| B+Retest | longs | 312 | -0.006 | -0.019 | 37 | 156 |
| RetestConf | longs | 285 | -0.014 | -0.039 | 26 | 101 |
| B | both | 314 | -0.041 | -0.011 | 47 | 173 |
| B+Mid | both | 324 | -0.056 | -0.011 | 48 | 232 |
| B+Retest | both | 324 | -0.057 | +0.009 | 52 | 298 |
| Retest | longs | 301 | -0.058 | -0.012 | 38 | 120 |
| RetestConf | both | 312 | -0.062 | -0.012 | 40 | 184 |
| Retest | both | 312 | -0.081 | +0.004 | 48 | 223 |
| Retest | shorts | 287 | -0.094 | +0.027 | 59 | 111 |
| B+Mid | shorts | 309 | -0.100 | +0.043 | 64 | 117 |
| RetestConf | shorts | 278 | -0.101 | +0.028 | 57 | 94 |
| B | shorts | 278 | -0.103 | +0.037 | 64 | 93 |
| B+Retest | shorts | 312 | -0.104 | +0.025 | 59 | 150 |

### S/R Flip

864 settings × 3 sides tested; 2088 combinations had ≥120 IS trades, 1% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.66. Average OOS result of the top-20 IS picks: -0.171 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.136 R/trade over 134 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 sweep 3R tries3 levels:htf:4h trend:sma exit:single | shorts | 263 | +0.101 | 0.87 | 134 | -0.088 | -11.8 | 28 |
| piv8 sweep 3R tries1 levels:htf:4h trend:off exit:single | shorts | 236 | +0.091 | 0.74 | 119 | -0.144 | -17.2 | 26 |
| piv5 rejection 3R tries1 levels:htf:4h trend:off exit:single | shorts | 309 | +0.053 | 0.50 | 147 | -0.127 | -18.6 | 27 |
| piv5 rejection 3R tries3 levels:htf:4h trend:sma exit:single | shorts | 379 | +0.019 | 0.20 | 172 | -0.151 | -25.9 | 26 |
| piv5 rejection 2R tries3 levels:htf:D trend:off exit:single | both | 130 | +0.013 | 0.10 | 57 | -0.167 | -9.5 | 33 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| rejection · levels htf:D | both | 36 | -0.062 | -0.152 | 0 | 56 |
| sweep · levels htf:4h | shorts | 72 | -0.071 | -0.158 | 0 | 127 |
| rejection · levels htf:4h | shorts | 72 | -0.113 | -0.173 | 0 | 160 |
| rejection · levels htf:4h | both | 72 | -0.141 | -0.303 | 0 | 338 |
| sweep · levels htf:4h | both | 72 | -0.155 | -0.256 | 0 | 270 |
| rejection · levels htf:4h | longs | 72 | -0.168 | -0.419 | 0 | 178 |
| rejection · levels chart+4h | shorts | 72 | -0.194 | -0.222 | 1 | 392 |
| touch · levels htf:D | both | 72 | -0.197 | -0.199 | 0 | 81 |
| sweep · levels chart+4h | shorts | 72 | -0.198 | -0.266 | 0 | 307 |
| touch · levels htf:4h | shorts | 72 | -0.200 | -0.244 | 0 | 246 |
| sweep · levels chart | shorts | 72 | -0.226 | -0.258 | 0 | 572 |
| rejection · levels chart+4h | both | 72 | -0.230 | -0.269 | 0 | 786 |
| sweep · levels htf:4h | longs | 72 | -0.233 | -0.342 | 0 | 142 |
| sweep · levels chart+4h | both | 72 | -0.236 | -0.290 | 0 | 611 |
| rejection · levels chart | shorts | 72 | -0.244 | -0.274 | 0 | 724 |
| touch · levels htf:4h | both | 72 | -0.251 | -0.315 | 0 | 508 |
| touch · levels htf:D | longs | 36 | -0.262 | -0.291 | 0 | 44 |
| rejection · levels chart+4h | longs | 72 | -0.263 | -0.314 | 0 | 396 |
| sweep · levels chart+4h | longs | 72 | -0.272 | -0.314 | 0 | 304 |
| sweep · levels chart | both | 72 | -0.274 | -0.273 | 0 | 1136 |
| rejection · levels chart | both | 72 | -0.278 | -0.313 | 0 | 1451 |
| touch · levels chart+4h | shorts | 72 | -0.297 | -0.362 | 0 | 598 |
| touch · levels htf:4h | longs | 72 | -0.298 | -0.383 | 0 | 262 |
| rejection · levels chart | longs | 72 | -0.310 | -0.352 | 0 | 724 |
| sweep · levels chart | longs | 72 | -0.318 | -0.289 | 0 | 560 |
| touch · levels chart | shorts | 72 | -0.323 | -0.442 | 0 | 1198 |
| touch · levels chart+4h | both | 72 | -0.345 | -0.413 | 0 | 1204 |
| touch · levels chart | both | 72 | -0.383 | -0.490 | 0 | 2406 |
| touch · levels chart+4h | longs | 72 | -0.390 | -0.465 | 0 | 606 |
| touch · levels chart | longs | 72 | -0.438 | -0.537 | 0 | 1198 |

### Megaphone

1056 settings × 3 sides tested; 1745 combinations had ≥120 IS trades, 13% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.51. Average OOS result of the top-20 IS picks: -0.287 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.218 R/trade over 223 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 swings4 expand0.5 BO-close measured trend:sma exit:single | both | 524 | +0.404 | 2.45 | 223 | -0.344 | -76.7 | 13 |
| piv5 swings4 expand0.5 BO-close measured trend:off exit:single | both | 570 | +0.359 | 2.31 | 247 | -0.327 | -80.8 | 13 |
| piv3 swings4 expand0.5 failedBO midline trend:off exit:single | shorts | 166 | +0.360 | 2.28 | 83 | -0.085 | -7.1 | 35 |
| piv3 swings4 expand0.5 fade-touch midline trend:sma exit:single | both | 327 | +0.526 | 2.24 | 137 | -0.077 | -10.5 | 19 |
| piv3 swings4 expand0.5 fade-touch opposite trend:sma exit:single | both | 321 | +0.878 | 2.17 | 136 | -0.380 | -51.6 | 7 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| failedBO | shorts | 46 | +0.026 | -0.051 | 33 | 86 |
| BO-close | longs | 128 | -0.000 | -0.228 | 13 | 127 |
| BO-close | both | 144 | -0.052 | -0.218 | 3 | 242 |
| failedBO | both | 80 | -0.056 | -0.095 | 18 | 128 |
| failedBO | longs | 54 | -0.094 | -0.191 | 0 | 80 |
| BO-close | shorts | 128 | -0.104 | -0.259 | 0 | 136 |
| fade-rejection | shorts | 100 | -0.151 | -0.164 | 13 | 120 |
| fade-rejection | both | 152 | -0.218 | -0.276 | 7 | 214 |
| fade-touch | both | 180 | -0.245 | -0.385 | 1 | 226 |
| BO-retest | longs | 112 | -0.252 | -0.438 | 2 | 115 |
| fade-touch | shorts | 120 | -0.255 | -0.398 | 2 | 200 |
| fade-rejection | longs | 110 | -0.284 | -0.339 | 0 | 136 |
| BO-retest | both | 144 | -0.284 | -0.377 | 3 | 208 |
| fade-touch | longs | 135 | -0.313 | -0.429 | 1 | 223 |
| BO-retest | shorts | 112 | -0.343 | -0.437 | 0 | 118 |


## 1-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6684%, OOS +163%)

### Range Sweep

2304 settings × 3 sides tested; 3416 combinations had ≥80 IS trades, 25% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.08. Average OOS result of the top-20 IS picks: +0.024 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.159 R/trade over 129 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | 177 | +0.328 | 2.27 | 129 | +0.123 | +15.8 | 31 |
| range48 max6ATR touches2 same_bar sweepMax3 stop0.25ATR target:3R exit:single | longs | 91 | +0.433 | 2.12 | 65 | -0.088 | -5.7 | 26 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | 181 | +0.296 | 2.08 | 133 | +0.086 | +11.5 | 30 |
| range48 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | 85 | +0.426 | 2.03 | 60 | -0.030 | -1.8 | 27 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | longs | 153 | +0.306 | 1.98 | 110 | +0.222 | +24.4 | 33 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| same_bar · target:opposite | shorts | 120 | +0.036 | -0.021 | 39 | 164 |
| same_bar · target:3R | shorts | 120 | -0.020 | -0.026 | 43 | 164 |
| same_bar · target:midline | shorts | 120 | -0.027 | -0.027 | 31 | 177 |
| same_bar · target:opposite | both | 152 | -0.032 | -0.048 | 23 | 292 |
| same_bar · target:3R | longs | 139 | -0.032 | -0.091 | 13 | 147 |
| same_bar · target:2R | shorts | 120 | -0.037 | -0.028 | 33 | 174 |
| same_bar · target:3R | both | 152 | -0.038 | -0.057 | 22 | 282 |
| within_n · target:opposite | shorts | 128 | -0.040 | +0.006 | 40 | 199 |
| within_n · target:3R | both | 164 | -0.045 | -0.020 | 31 | 322 |
| within_n · target:midline | shorts | 132 | -0.049 | -0.011 | 34 | 221 |
| within_n · target:3R | longs | 150 | -0.050 | -0.065 | 25 | 170 |
| within_n · target:3R | shorts | 128 | -0.052 | +0.001 | 41 | 198 |
| within_n · target:2R | shorts | 129 | -0.054 | -0.010 | 30 | 211 |
| same_bar · target:2R | both | 152 | -0.061 | -0.085 | 7 | 298 |
| same_bar · target:2R | longs | 139 | -0.065 | -0.135 | 6 | 155 |
| within_n · target:opposite | both | 164 | -0.065 | -0.031 | 32 | 342 |
| within_n · target:2R | both | 164 | -0.069 | -0.043 | 24 | 356 |
| same_bar · target:midline | both | 152 | -0.075 | -0.061 | 21 | 305 |
| within_n · target:midline | both | 164 | -0.077 | -0.055 | 18 | 386 |
| within_n · target:opposite | longs | 148 | -0.085 | -0.095 | 16 | 172 |
| within_n · target:2R | longs | 150 | -0.086 | -0.092 | 8 | 182 |
| same_bar · target:opposite | longs | 138 | -0.088 | -0.125 | 10 | 152 |
| same_bar · target:midline | longs | 139 | -0.090 | -0.115 | 11 | 160 |
| within_n · target:midline | longs | 152 | -0.091 | -0.097 | 12 | 202 |

### Double Top / Bottom

1620 settings × 3 sides tested; 3931 combinations had ≥80 IS trades, 56% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.01. Average OOS result of the top-20 IS picks: -0.091 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.058 R/trade over 53 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol0.3 depth1.0 B+Retest 2R trend:sma exit:single | shorts | 92 | +0.478 | 3.03 | 53 | -0.031 | -1.6 | 32 |
| piv3 tol1.0 depth1.0 B+Retest 2R trend:sma exit:single | both | 581 | +0.213 | 2.87 | 282 | -0.138 | -38.9 | 30 |
| piv8 tol0.3 depth0.5 B+Retest 2R trend:sma exit:single | shorts | 102 | +0.417 | 2.79 | 68 | -0.171 | -11.6 | 28 |
| piv5 tol0.6 depth1.0 B+Retest 2R trend:sma exit:single | both | 424 | +0.196 | 2.72 | 204 | -0.116 | -23.6 | 31 |
| piv3 tol1.0 depth1.0 B+Retest 2R trend:sma exit:single | longs | 331 | +0.221 | 2.70 | 147 | +0.116 | +17.0 | 39 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | both | 300 | +0.070 | -0.111 | 8 | 114 |
| B | longs | 236 | +0.068 | +0.001 | 53 | 65 |
| B | shorts | 236 | +0.065 | -0.192 | 0 | 66 |
| B+Retest | shorts | 299 | +0.063 | -0.222 | 1 | 104 |
| RetestConf | longs | 173 | +0.039 | +0.104 | 81 | 60 |
| B+Retest | both | 324 | +0.032 | -0.126 | 8 | 199 |
| RetestConf | shorts | 175 | +0.026 | -0.184 | 7 | 57 |
| RetestConf | both | 281 | +0.023 | -0.060 | 33 | 92 |
| Retest | shorts | 214 | +0.018 | -0.213 | 1 | 64 |
| B+Retest | longs | 297 | +0.008 | +0.004 | 58 | 103 |
| Retest | both | 296 | -0.004 | -0.096 | 12 | 112 |
| B+Mid | shorts | 293 | -0.021 | -0.223 | 0 | 93 |
| Retest | longs | 198 | -0.034 | +0.052 | 68 | 67 |
| B+Mid | both | 324 | -0.036 | -0.157 | 0 | 174 |
| B+Mid | longs | 285 | -0.039 | -0.052 | 35 | 88 |

### Triple Top / Bottom

1620 settings × 3 sides tested; 3675 combinations had ≥80 IS trades, 71% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.03. Average OOS result of the top-20 IS picks: -0.046 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.010 R/trade over 118 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol2.0 depth0.5 B 2R trend:sma exit:TP1 1R 50% BE | both | 259 | +0.220 | 3.28 | 118 | -0.003 | -0.4 | 50 |
| piv5 tol2.0 depth1.0 B 2R trend:sma exit:TP1 1R 50% BE | both | 252 | +0.211 | 3.09 | 118 | -0.003 | -0.4 | 50 |
| piv5 tol2.0 depth0.5 B+Mid 2R trend:sma exit:TP1 1R 50% BE | both | 369 | +0.173 | 3.03 | 174 | -0.044 | -7.7 | 49 |
| piv5 tol2.0 depth0.5 B+Retest 1.5R trend:sma exit:TP1 1R 50% BE | both | 463 | +0.147 | 3.02 | 235 | -0.042 | -9.9 | 49 |
| piv5 tol2.0 depth0.5 B+Retest 1.5R trend:sma exit:TP1 1R 50% BE | longs | 236 | +0.206 | 2.99 | 113 | +0.080 | +9.1 | 57 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 213 | +0.137 | +0.011 | 47 | 51 |
| B | shorts | 190 | +0.113 | -0.160 | 4 | 52 |
| B | both | 305 | +0.109 | -0.081 | 24 | 94 |
| B+Retest | shorts | 285 | +0.065 | -0.194 | 8 | 83 |
| B+Retest | both | 318 | +0.054 | -0.113 | 13 | 165 |
| RetestConf | longs | 134 | +0.050 | -0.030 | 46 | 49 |
| B+Retest | longs | 303 | +0.047 | -0.028 | 42 | 85 |
| B+Mid | shorts | 257 | +0.043 | -0.168 | 4 | 73 |
| RetestConf | both | 276 | +0.037 | -0.127 | 6 | 82 |
| B+Mid | longs | 285 | +0.031 | -0.030 | 44 | 70 |
| B+Mid | both | 312 | +0.030 | -0.106 | 14 | 134 |
| RetestConf | shorts | 145 | +0.023 | -0.190 | 6 | 45 |
| Retest | shorts | 182 | -0.008 | -0.201 | 3 | 56 |
| Retest | longs | 182 | -0.011 | -0.089 | 18 | 57 |
| Retest | both | 288 | -0.013 | -0.142 | 7 | 99 |

### S/R Flip

864 settings × 3 sides tested; 1806 combinations had ≥80 IS trades, 7% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.07. Average OOS result of the top-20 IS picks: -0.070 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.014 R/trade over 43 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 rejection 3R tries3 levels:htf:D trend:sma exit:single | shorts | 98 | +0.331 | 1.70 | 43 | -0.042 | -1.8 | 26 |
| piv3 rejection 2R tries3 levels:htf:D trend:off exit:single | shorts | 99 | +0.185 | 1.23 | 43 | -0.162 | -7.0 | 30 |
| piv8 rejection 3R tries3 levels:htf:D trend:sma exit:TP1 1R 50% BE | shorts | 95 | +0.155 | 1.18 | 41 | -0.124 | -5.1 | 44 |
| piv3 sweep 1.5R tries3 levels:htf:D trend:sma exit:single | shorts | 81 | +0.153 | 1.09 | 31 | -0.183 | -5.7 | 35 |
| piv8 rejection 1.5R tries3 levels:htf:D trend:sma exit:TP1 1R 50% BE | shorts | 96 | +0.125 | 1.04 | 41 | -0.165 | -6.7 | 44 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| rejection · levels htf:D | shorts | 36 | +0.162 | -0.146 | 0 | 42 |
| sweep · levels htf:D | shorts | 6 | +0.153 | -0.183 | 0 | 31 |
| sweep · levels htf:D | both | 72 | -0.032 | -0.127 | 17 | 74 |
| sweep · levels chart | shorts | 72 | -0.047 | -0.112 | 0 | 216 |
| rejection · levels htf:D | both | 72 | -0.057 | -0.136 | 0 | 92 |
| rejection · levels chart+D | shorts | 72 | -0.059 | +0.002 | 36 | 162 |
| sweep · levels chart+D | shorts | 72 | -0.060 | -0.029 | 25 | 123 |
| rejection · levels chart+D | both | 72 | -0.099 | -0.061 | 15 | 352 |
| sweep · levels chart+D | both | 72 | -0.101 | -0.067 | 18 | 277 |
| sweep · levels chart | both | 72 | -0.123 | -0.118 | 0 | 472 |
| rejection · levels chart | shorts | 72 | -0.131 | -0.058 | 17 | 276 |
| touch · levels htf:D | shorts | 72 | -0.132 | -0.069 | 17 | 62 |
| rejection · levels chart+D | longs | 72 | -0.134 | -0.115 | 10 | 190 |
| touch · levels chart | longs | 72 | -0.135 | -0.197 | 0 | 524 |
| sweep · levels chart+D | longs | 72 | -0.136 | -0.100 | 19 | 150 |
| touch · levels chart+D | shorts | 72 | -0.143 | -0.122 | 6 | 256 |
| rejection · levels chart | both | 72 | -0.152 | -0.121 | 3 | 598 |
| sweep · levels htf:D | longs | 36 | -0.153 | -0.082 | 33 | 48 |
| rejection · levels chart | longs | 72 | -0.171 | -0.177 | 3 | 322 |
| rejection · levels htf:D | longs | 72 | -0.171 | -0.151 | 8 | 53 |
| touch · levels chart | both | 72 | -0.177 | -0.150 | 0 | 978 |
| touch · levels chart+D | both | 72 | -0.180 | -0.091 | 6 | 531 |
| touch · levels htf:D | both | 72 | -0.186 | -0.068 | 0 | 136 |
| sweep · levels chart | longs | 72 | -0.187 | -0.124 | 3 | 258 |
| touch · levels chart+D | longs | 72 | -0.213 | -0.063 | 15 | 274 |
| touch · levels chart | shorts | 72 | -0.223 | -0.099 | 1 | 466 |
| touch · levels htf:D | longs | 72 | -0.232 | -0.068 | 8 | 74 |

### Megaphone

1056 settings × 3 sides tested; 1259 combinations had ≥80 IS trades, 30% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.29. Average OOS result of the top-20 IS picks: +0.076 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.116 R/trade over 134 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 swings4 expand0.5 BO-close measured trend:off exit:single | both | 278 | +0.785 | 3.37 | 134 | +0.297 | +39.7 | 19 |
| piv3 swings4 expand0.0 BO-close measured trend:sma exit:single | both | 440 | +0.565 | 3.31 | 229 | -0.054 | -12.3 | 20 |
| piv3 swings4 expand0.5 BO-close measured trend:sma exit:single | both | 237 | +0.857 | 3.29 | 123 | +0.340 | +41.8 | 20 |
| piv3 swings4 expand0.0 BO-close measured trend:off exit:single | both | 535 | +0.456 | 3.09 | 271 | -0.094 | -25.4 | 19 |
| piv5 swings4 expand0.5 BO-close measured trend:off exit:single | longs | 119 | +1.516 | 3.02 | 64 | -0.106 | -6.8 | 16 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| BO-close | longs | 103 | +0.343 | -0.138 | 12 | 66 |
| BO-close | both | 128 | +0.313 | -0.157 | 9 | 121 |
| BO-close | shorts | 86 | +0.051 | -0.150 | 13 | 62 |
| BO-retest | longs | 79 | +0.047 | -0.115 | 22 | 61 |
| fade-rejection | shorts | 75 | -0.000 | -0.236 | 1 | 71 |
| BO-retest | both | 112 | -0.032 | -0.171 | 12 | 98 |
| failedBO | shorts | 16 | -0.045 | -0.153 | 0 | 71 |
| BO-retest | shorts | 63 | -0.100 | -0.278 | 10 | 69 |
| fade-rejection | both | 110 | -0.100 | -0.251 | 5 | 110 |
| failedBO | longs | 16 | -0.188 | +0.186 | 100 | 58 |
| fade-rejection | longs | 70 | -0.212 | -0.269 | 7 | 82 |
| failedBO | both | 56 | -0.225 | -0.009 | 54 | 74 |
| fade-touch | both | 145 | -0.243 | -0.187 | 21 | 162 |
| fade-touch | longs | 110 | -0.250 | -0.197 | 16 | 88 |
| fade-touch | shorts | 90 | -0.279 | -0.302 | 9 | 122 |


## 4-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6640%, OOS +164%)

### Range Sweep

2304 settings × 3 sides tested; 2734 combinations had ≥50 IS trades, 36% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.00. Average OOS result of the top-20 IS picks: -0.205 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.012 R/trade over 59 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | 108 | +0.266 | 2.48 | 59 | -0.310 | -18.3 | 36 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | 118 | +0.254 | 2.46 | 64 | -0.210 | -13.5 | 39 |
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | 50 | +0.371 | 2.34 | 32 | -0.327 | -10.5 | 38 |
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:3R exit:TP1 1R 50% BE | both | 103 | +0.276 | 2.33 | 56 | -0.255 | -14.3 | 36 |
| range24 max10ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | 128 | +0.226 | 2.26 | 71 | -0.184 | -13.0 | 42 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| same_bar · target:opposite | shorts | 96 | +0.178 | -0.083 | 22 | 59 |
| within_n · target:opposite | shorts | 117 | +0.123 | -0.069 | 20 | 53 |
| same_bar · target:opposite | both | 124 | +0.075 | -0.157 | 10 | 76 |
| within_n · target:opposite | both | 139 | +0.045 | -0.120 | 15 | 97 |
| within_n · target:opposite | longs | 107 | +0.004 | -0.136 | 21 | 55 |
| within_n · target:3R | longs | 110 | -0.007 | -0.065 | 28 | 59 |
| same_bar · target:3R | shorts | 97 | -0.008 | -0.145 | 10 | 65 |
| within_n · target:2R | longs | 110 | -0.012 | -0.092 | 17 | 62 |
| within_n · target:midline | longs | 112 | -0.030 | -0.165 | 3 | 62 |
| same_bar · target:3R | both | 125 | -0.035 | -0.159 | 2 | 77 |
| within_n · target:3R | shorts | 119 | -0.038 | -0.087 | 24 | 52 |
| same_bar · target:2R | shorts | 102 | -0.038 | -0.143 | 11 | 58 |
| within_n · target:3R | both | 141 | -0.039 | -0.092 | 19 | 97 |
| within_n · target:2R | both | 141 | -0.049 | -0.116 | 11 | 101 |
| same_bar · target:2R | both | 125 | -0.052 | -0.173 | 2 | 78 |
| same_bar · target:3R | longs | 87 | -0.052 | -0.115 | 15 | 77 |
| within_n · target:midline | shorts | 119 | -0.056 | -0.088 | 18 | 56 |
| within_n · target:2R | shorts | 120 | -0.056 | -0.091 | 22 | 56 |
| within_n · target:midline | both | 142 | -0.057 | -0.133 | 3 | 101 |
| same_bar · target:2R | longs | 91 | -0.058 | -0.139 | 9 | 71 |
| same_bar · target:midline | shorts | 101 | -0.060 | -0.129 | 19 | 59 |
| same_bar · target:midline | both | 125 | -0.071 | -0.196 | 0 | 80 |
| same_bar · target:midline | longs | 94 | -0.084 | -0.230 | 2 | 67 |
| same_bar · target:opposite | longs | 90 | -0.089 | -0.178 | 10 | 52 |

### Double Top / Bottom

1620 settings × 3 sides tested; 751 combinations had ≥50 IS trades, 74% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.23. Average OOS result of the top-20 IS picks: +0.046 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.097 R/trade over 27 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol1.0 depth0.5 B+Retest 3R trend:sma exit:TP1 1R 50% BE | longs | 51 | +0.456 | 2.44 | 27 | -0.088 | -2.4 | 41 |
| piv3 tol1.0 depth1.0 B+Retest 3R trend:sma exit:TP1 1R 50% BE | longs | 50 | +0.426 | 2.26 | 27 | -0.088 | -2.4 | 41 |
| piv8 tol1.0 depth0.5 B+Retest 3R trend:sma exit:TP1 1R 50% BE | both | 87 | +0.299 | 2.18 | 34 | +0.098 | +3.3 | 50 |
| piv3 tol1.0 depth0.5 B+Retest 3R trend:off exit:single | longs | 56 | +0.558 | 2.14 | 31 | +0.062 | +1.9 | 29 |
| piv3 tol1.0 depth0.5 B+Retest 2R trend:sma exit:TP1 1R 50% BE | longs | 50 | +0.337 | 2.07 | 29 | -0.154 | -4.5 | 38 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | both | 99 | +0.161 | +0.109 | 69 | 28 |
| B+Retest | longs | 76 | +0.143 | +0.117 | 58 | 30 |
| B+Retest | both | 210 | +0.121 | +0.154 | 74 | 44 |
| B+Retest | shorts | 63 | +0.042 | +0.045 | 62 | 24 |
| B+Mid | both | 169 | +0.037 | +0.178 | 86 | 40 |
| B+Mid | longs | 27 | +0.028 | +0.127 | 74 | 30 |
| B+Mid | shorts | 28 | +0.004 | +0.157 | 75 | 22 |
| RetestConf | both | 19 | -0.011 | +0.162 | 95 | 29 |
| Retest | both | 60 | -0.018 | +0.149 | 92 | 30 |

### Triple Top / Bottom

1620 settings × 3 sides tested; 252 combinations had ≥50 IS trades, 93% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.19. Average OOS result of the top-20 IS picks: +0.119 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.087 R/trade over 38 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single | both | 63 | +0.823 | 4.51 | 38 | +0.048 | +1.8 | 37 |
| piv5 tol2.0 depth2.0 B+Retest 2R trend:off exit:single | both | 61 | +0.785 | 4.21 | 38 | +0.048 | +1.8 | 37 |
| piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:TP1 1R 50% BE | both | 66 | +0.545 | 3.98 | 40 | -0.023 | -0.9 | 50 |
| piv5 tol2.0 depth2.0 B+Retest 2R trend:off exit:TP1 1R 50% BE | both | 65 | +0.515 | 3.75 | 40 | -0.023 | -0.9 | 50 |
| piv5 tol2.0 depth2.0 B+Retest 1.5R trend:off exit:single | both | 63 | +0.560 | 3.71 | 42 | +0.133 | +5.6 | 48 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B+Retest | both | 141 | +0.252 | +0.194 | 91 | 38 |
| B+Retest | longs | 3 | +0.178 | +0.179 | 100 | 32 |
| B | both | 24 | +0.163 | +0.170 | 100 | 28 |
| B+Mid | both | 84 | +0.147 | +0.169 | 93 | 35 |

### S/R Flip

864 settings × 3 sides tested; 1931 combinations had ≥50 IS trades, 77% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.11. Average OOS result of the top-20 IS picks: -0.118 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.076 R/trade over 72 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | both | 131 | +0.227 | 2.35 | 72 | -0.044 | -3.2 | 47 |
| piv5 rejection 3R tries1 levels:htf:D trend:off exit:TP1 1R 50% BE | both | 141 | +0.209 | 2.29 | 77 | -0.072 | -5.5 | 47 |
| piv5 rejection 2R tries1 levels:htf:D trend:off exit:TP1 1R 50% BE | both | 143 | +0.184 | 2.15 | 77 | -0.131 | -10.1 | 47 |
| piv8 rejection 2R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | both | 133 | +0.185 | 2.06 | 72 | -0.121 | -8.7 | 47 |
| piv5 rejection 3R tries3 levels:htf:D trend:sma exit:TP1 1R 50% BE | both | 146 | +0.188 | 2.05 | 88 | -0.023 | -2.1 | 49 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| rejection · levels htf:D | longs | 72 | +0.135 | -0.077 | 17 | 54 |
| rejection · levels htf:D | both | 72 | +0.131 | -0.074 | 4 | 83 |
| rejection · levels htf:D | shorts | 72 | +0.125 | -0.061 | 29 | 29 |
| rejection · levels chart+D | longs | 72 | +0.091 | -0.165 | 3 | 63 |
| sweep · levels htf:D | longs | 72 | +0.087 | +0.032 | 54 | 48 |
| sweep · levels chart | longs | 72 | +0.084 | -0.173 | 0 | 68 |
| rejection · levels chart | longs | 72 | +0.069 | -0.157 | 0 | 82 |
| sweep · levels htf:D | both | 72 | +0.065 | +0.042 | 67 | 70 |
| touch · levels chart | shorts | 72 | +0.063 | -0.162 | 0 | 119 |
| sweep · levels htf:D | shorts | 51 | +0.062 | +0.090 | 71 | 23 |
| touch · levels chart | both | 72 | +0.056 | -0.140 | 0 | 250 |
| touch · levels chart | longs | 72 | +0.053 | -0.121 | 4 | 129 |
| touch · levels htf:D | shorts | 72 | +0.050 | -0.125 | 8 | 52 |
| rejection · levels chart | both | 72 | +0.048 | -0.145 | 0 | 155 |
| sweep · levels chart+D | longs | 72 | +0.046 | -0.129 | 8 | 52 |
| rejection · levels chart+D | both | 72 | +0.033 | -0.096 | 7 | 105 |
| touch · levels chart+D | longs | 72 | +0.033 | -0.154 | 0 | 88 |
| touch · levels chart+D | both | 72 | +0.032 | -0.148 | 0 | 167 |
| touch · levels chart+D | shorts | 72 | +0.032 | -0.140 | 6 | 78 |
| touch · levels htf:D | both | 72 | +0.027 | -0.169 | 0 | 126 |
| sweep · levels chart | both | 72 | +0.023 | -0.146 | 0 | 124 |
| sweep · levels chart+D | both | 72 | +0.021 | -0.098 | 7 | 84 |
| rejection · levels chart | shorts | 72 | +0.020 | -0.128 | 15 | 70 |
| touch · levels htf:D | longs | 72 | +0.009 | -0.200 | 0 | 74 |
| sweep · levels chart+D | shorts | 68 | -0.006 | -0.040 | 44 | 32 |
| rejection · levels chart+D | shorts | 72 | -0.044 | +0.011 | 57 | 41 |
| sweep · levels chart | shorts | 72 | -0.053 | -0.109 | 12 | 54 |
| touch · levels htf:W | both | 12 | -0.653 | -0.363 | 0 | 29 |

### Megaphone

1056 settings × 3 sides tested; 455 combinations had ≥50 IS trades, 49% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.53. Average OOS result of the top-20 IS picks: +0.080 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.120 R/trade over 30 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 swings4 expand0.0 BO-close 2R trend:off exit:single | longs | 60 | +0.676 | 3.49 | 30 | +0.127 | +3.8 | 40 |
| piv5 swings4 expand0.0 BO-close 1.5R trend:off exit:single | longs | 61 | +0.497 | 3.14 | 30 | +0.016 | +0.5 | 43 |
| piv5 swings4 expand0.0 BO-close 3R trend:off exit:single | longs | 59 | +0.811 | 3.08 | 30 | +0.251 | +7.5 | 33 |
| piv5 swings4 expand0.0 BO-close 2R trend:sma exit:single | longs | 50 | +0.605 | 2.82 | 27 | +0.039 | +1.1 | 37 |
| piv5 swings4 expand0.0 BO-close 3R trend:off exit:single | both | 93 | +0.576 | 2.81 | 56 | +0.158 | +8.8 | 30 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| BO-close | longs | 28 | +1.129 | +0.129 | 82 | 33 |
| BO-close | both | 74 | +0.984 | +0.014 | 57 | 35 |
| BO-retest | both | 44 | +0.795 | -0.183 | 20 | 41 |
| BO-retest | longs | 7 | +0.669 | +0.046 | 86 | 32 |
| BO-close | shorts | 6 | +0.367 | -0.003 | 50 | 32 |
| fade-touch | longs | 47 | +0.018 | -0.438 | 0 | 35 |
| failedBO | both | 6 | -0.014 | -0.490 | 0 | 35 |
| fade-rejection | both | 69 | -0.053 | -0.533 | 1 | 39 |
| fade-touch | both | 80 | -0.075 | -0.538 | 4 | 60 |
| fade-touch | shorts | 60 | -0.112 | -0.617 | 0 | 39 |
| fade-rejection | shorts | 10 | -0.138 | -0.334 | 0 | 37 |
| fade-rejection | longs | 24 | -0.195 | -0.408 | 0 | 30 |


## Daily  (IS 2015-07-20 → 2023-06-15, OOS 2023-06-15 → 2026-11-03; BTC buy & hold: IS +9032%, OOS +201%)

### Range Sweep

2304 settings × 3 sides tested; 1927 combinations had ≥15 IS trades, 21% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.11. Average OOS result of the top-20 IS picks: +0.569 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.119 R/trade over 12 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | 23 | +1.282 | 1.54 | 12 | +0.181 | +2.2 | 25 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | both | 17 | +1.606 | 1.48 | 14 | -0.281 | -3.9 | 14 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | 24 | +1.188 | 1.48 | 12 | +1.018 | +12.2 | 33 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | both | 29 | +0.537 | 1.48 | 14 | +1.002 | +14.0 | 50 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:TP1 1R 50% BE | both | 29 | +0.508 | 1.45 | 17 | +0.437 | +7.4 | 65 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| within_n · target:midline | longs | 46 | +0.025 | +0.006 | 48 | 28 |
| same_bar · target:midline | longs | 40 | +0.020 | -0.147 | 12 | 24 |
| within_n · target:3R | longs | 52 | +0.019 | +0.125 | 73 | 17 |
| within_n · target:opposite | longs | 44 | +0.001 | -0.076 | 39 | 19 |
| same_bar · target:3R | longs | 39 | -0.028 | -0.142 | 26 | 15 |
| within_n · target:3R | both | 114 | -0.043 | +0.144 | 73 | 23 |
| same_bar · target:opposite | longs | 35 | -0.055 | -0.161 | 20 | 17 |
| within_n · target:opposite | both | 114 | -0.055 | +0.045 | 55 | 22 |
| within_n · target:2R | longs | 52 | -0.061 | +0.081 | 65 | 20 |
| same_bar · target:2R | longs | 40 | -0.066 | -0.035 | 40 | 17 |
| same_bar · target:3R | both | 104 | -0.092 | +0.063 | 59 | 20 |
| within_n · target:2R | both | 114 | -0.096 | +0.117 | 68 | 24 |
| same_bar · target:2R | both | 105 | -0.143 | +0.049 | 53 | 20 |
| within_n · target:3R | shorts | 103 | -0.150 | +0.040 | 61 | 16 |
| same_bar · target:opposite | both | 103 | -0.150 | +0.007 | 58 | 19 |
| within_n · target:opposite | shorts | 100 | -0.153 | -0.062 | 48 | 16 |
| within_n · target:midline | both | 115 | -0.174 | +0.071 | 59 | 25 |
| within_n · target:2R | shorts | 106 | -0.176 | +0.005 | 54 | 17 |
| same_bar · target:3R | shorts | 74 | -0.184 | +0.049 | 62 | 20 |
| same_bar · target:2R | shorts | 74 | -0.210 | +0.041 | 64 | 21 |
| same_bar · target:opposite | shorts | 74 | -0.222 | +0.010 | 62 | 19 |
| same_bar · target:midline | both | 102 | -0.233 | +0.017 | 42 | 20 |
| within_n · target:midline | shorts | 108 | -0.237 | -0.019 | 49 | 17 |
| same_bar · target:midline | shorts | 69 | -0.293 | +0.081 | 59 | 25 |

### Double Top / Bottom

No configuration reached 15 IS trades.

### Triple Top / Bottom

No configuration reached 15 IS trades.

### S/R Flip

864 settings × 3 sides tested; 1224 combinations had ≥15 IS trades, 63% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.18. Average OOS result of the top-20 IS picks: -0.106 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.052 R/trade over 13 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 rejection 2R tries1 levels:chart trend:sma exit:TP1 1R 50% BE | both | 26 | +0.542 | 2.14 | 13 | -0.014 | -0.2 | 54 |
| piv5 sweep 2R tries1 levels:chart trend:off exit:TP1 1R 50% BE | both | 41 | +0.408 | 2.13 | 25 | +0.033 | +0.8 | 56 |
| piv3 sweep 1.5R tries3 levels:chart+W merged>=2 trend:sma exit:single | longs | 16 | +0.622 | 2.10 | 9 | -0.316 | -2.8 | 33 |
| piv8 rejection 1.5R tries1 levels:chart trend:sma exit:single | longs | 21 | +0.563 | 2.10 | 10 | -0.360 | -3.6 | 30 |
| piv8 rejection 1.5R tries1 levels:chart trend:sma exit:TP1 1R 50% BE | both | 26 | +0.515 | 2.08 | 13 | -0.035 | -0.5 | 54 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| sweep · levels chart | longs | 72 | +0.386 | -0.089 | 32 | 15 |
| sweep · levels chart+W | both | 60 | +0.324 | -0.238 | 18 | 7 |
| sweep · levels chart | both | 72 | +0.310 | -0.088 | 28 | 19 |
| sweep · levels chart+W | longs | 30 | +0.303 | -0.346 | 7 | 8 |
| rejection · levels chart | longs | 72 | +0.300 | -0.223 | 12 | 17 |
| rejection · levels htf:W | longs | 36 | +0.298 | -0.056 | 50 | 6 |
| sweep · levels htf:W | both | 54 | +0.282 | -0.181 | 33 | 5 |
| rejection · levels chart | both | 72 | +0.261 | -0.127 | 14 | 24 |
| rejection · levels chart+W | longs | 54 | +0.237 | -0.313 | 17 | 8 |
| sweep · levels htf:W | longs | 18 | +0.221 | -0.200 | 33 | 5 |
| rejection · levels htf:W | both | 72 | +0.210 | +0.010 | 58 | 8 |
| rejection · levels chart+W | both | 72 | +0.204 | -0.181 | 28 | 10 |
| sweep · levels chart | shorts | 12 | +0.202 | +0.176 | 75 | 11 |
| rejection · levels chart | shorts | 30 | +0.148 | +0.089 | 60 | 12 |
| touch · levels chart | longs | 72 | +0.030 | -0.038 | 38 | 23 |
| touch · levels chart | both | 72 | -0.099 | -0.144 | 14 | 38 |
| touch · levels htf:W | longs | 72 | -0.167 | +0.296 | 92 | 8 |
| touch · levels chart+W | longs | 72 | -0.182 | +0.400 | 96 | 9 |
| touch · levels htf:W | both | 72 | -0.237 | +0.199 | 83 | 11 |
| touch · levels chart+W | both | 72 | -0.252 | +0.184 | 75 | 14 |
| touch · levels chart | shorts | 66 | -0.346 | -0.311 | 0 | 16 |

### Megaphone

1056 settings × 3 sides tested; 172 combinations had ≥15 IS trades, 40% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.09. Average OOS result of the top-20 IS picks: +0.840 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.166 R/trade over 10 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 swings4 expand0.0 BO-close 1.5R trend:sma exit:single | both | 16 | +0.999 | 3.96 | 10 | +0.657 | +6.6 | 70 |
| piv3 swings4 expand0.5 BO-close 1.5R trend:off exit:single | both | 15 | +0.974 | 3.63 | 8 | +0.783 | +6.3 | 75 |
| piv3 swings4 expand0.0 BO-close 1.5R trend:off exit:single | longs | 17 | +0.859 | 3.24 | 8 | +0.444 | +3.6 | 62 |
| piv3 swings4 expand0.0 BO-close 1.5R trend:off exit:single | both | 24 | +0.742 | 3.16 | 11 | +0.515 | +5.7 | 64 |
| piv3 swings4 expand0.5 BO-close 1.5R trend:off exit:TP1 1R 50% BE | both | 15 | +0.717 | 2.61 | 8 | +0.813 | +6.5 | 88 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| BO-retest | both | 8 | +1.132 | +1.093 | 100 | 6 |
| BO-close | longs | 7 | +0.840 | +0.994 | 100 | 8 |
| BO-close | both | 20 | +0.754 | +1.213 | 100 | 10 |
| BO-retest | longs | 6 | +0.421 | +0.193 | 67 | 3 |
| fade-touch | longs | 14 | -0.061 | +0.108 | 71 | 10 |
| fade-rejection | both | 27 | -0.118 | +0.110 | 67 | 12 |
| fade-touch | both | 65 | -0.150 | -0.014 | 51 | 13 |
| fade-touch | shorts | 25 | -0.329 | -0.025 | 48 | 15 |

