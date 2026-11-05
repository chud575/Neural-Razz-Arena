# ETH strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase ETH-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | fibonacci pivots:W · breakout (longs) | +0.315 | -0.092 | 25 | fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | 57 | +0.123 | -0.041 |
| 1h | Pivot Points | traditional pivots:W · breakout (shorts) | +0.208 | +0.233 | 100 | traditional pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | 55 | +0.383 | -0.107 |
| 4h | Pivot Points | traditional pivots:M · breakout (both) | +0.367 | +0.540 | 100 | traditional pivots:M breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | 29 | +0.313 | +0.004 |
| 1d | Pivot Points | fibonacci pivots:M · breakout (longs) | +0.356 | +0.299 | 88 | fibonacci pivots:M breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | 17 | +0.189 | +0.188 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | 248 | +0.312 | 119 | +0.211 | -0.058 | +0.269 | +0.022 | +0.65 |
| 1h | Pivot Points | woodie pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 321 | +0.325 | 158 | +0.011 | +0.025 | -0.013 | +0.009 | +0.71 |
| 4h | Pivot Points | fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | longs | 290 | +0.276 | 129 | +0.107 | +0.009 | +0.098 | +0.037 | +0.64 |
| 1d | Pivot Points | fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | 248 | +0.222 | 114 | -0.052 | +0.076 | -0.128 | +0.135 | +0.48 |


## 15-minute  (IS 2020-01-01 → 2024-10-15, OOS 2024-10-15 → 2026-11-04; ETH buy & hold: IS +1915%, OOS -10%)

### Pivot Points

576 settings × 3 sides tested; 1128 combinations had ≥120 IS trades, 17% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.65. Average OOS result of the top-20 IS picks: +0.022 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.058 R/trade over 119 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | 248 | +0.312 | 3.24 | 119 | +0.211 | +25.1 | 44 |
| woodie pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | longs | 238 | +0.310 | 3.16 | 117 | +0.080 | +9.4 | 39 |
| fibonacci pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | both | 241 | +0.412 | 3.08 | 106 | +0.053 | +5.6 | 31 |
| fibonacci pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no | both | 241 | +0.376 | 2.81 | 106 | +0.048 | +5.1 | 31 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | both | 1120 | +0.120 | 2.70 | 498 | -0.039 | -19.3 | 35 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fibonacci pivots:W · breakout | longs | 8 | +0.315 | -0.092 | 25 | 57 |
| woodie pivots:W · breakout | both | 8 | +0.183 | +0.330 | 100 | 78 |
| traditional pivots:D · breakout | longs | 16 | +0.122 | -0.020 | 50 | 187 |
| woodie pivots:D · breakout | longs | 16 | +0.103 | -0.042 | 31 | 190 |
| fibonacci pivots:W · bounce-rejection | shorts | 8 | +0.101 | -0.252 | 0 | 54 |
| fibonacci pivots:D · breakout | longs | 24 | +0.082 | -0.053 | 33 | 228 |
| camarilla pivots:W · breakout | longs | 24 | +0.082 | +0.102 | 75 | 75 |
| traditional pivots:W · breakout | both | 8 | +0.078 | +0.055 | 50 | 78 |
| fibonacci pivots:W · breakout | both | 16 | +0.054 | +0.014 | 62 | 88 |
| camarilla pivots:W · breakout | both | 24 | +0.031 | +0.061 | 71 | 147 |
| traditional pivots:D · breakout | both | 24 | +0.027 | +0.046 | 67 | 221 |
| fibonacci pivots:D · breakout | both | 24 | +0.018 | -0.026 | 42 | 426 |
| woodie pivots:D · breakout | both | 24 | +0.016 | -0.012 | 38 | 213 |
| woodie pivots:D · breakout | shorts | 16 | -0.020 | +0.061 | 69 | 165 |
| camarilla pivots:W · breakout | shorts | 24 | -0.021 | +0.019 | 50 | 72 |
| fibonacci pivots:D · breakout | shorts | 24 | -0.053 | +0.005 | 58 | 197 |
| traditional pivots:D · breakout | shorts | 16 | -0.072 | +0.051 | 69 | 169 |
| camarilla pivots:D · breakout | longs | 24 | -0.078 | -0.155 | 0 | 478 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.096 | -0.121 | 0 | 380 |
| camarilla pivots:D · breakout | both | 24 | -0.100 | -0.122 | 0 | 962 |
| camarilla pivots:D · breakout | shorts | 24 | -0.122 | -0.088 | 0 | 484 |
| camarilla pivots:W · bounce-rejection | longs | 20 | -0.136 | -0.141 | 15 | 70 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.138 | -0.114 | 0 | 774 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.167 | -0.188 | 0 | 198 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.171 | -0.160 | 4 | 387 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.176 | -0.136 | 17 | 188 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.180 | -0.108 | 12 | 390 |
| woodie pivots:D · bounce-rejection | shorts | 16 | -0.198 | -0.091 | 19 | 172 |
| woodie pivots:W · bounce-touch | both | 8 | -0.211 | -0.608 | 0 | 81 |
| woodie pivots:W · bounce-rejection | both | 8 | -0.215 | +0.132 | 50 | 68 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.222 | -0.110 | 12 | 176 |
| fibonacci pivots:W · bounce-rejection | both | 16 | -0.236 | -0.140 | 12 | 82 |
| woodie pivots:D · bounce-rejection | longs | 16 | -0.249 | -0.174 | 25 | 166 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.252 | -0.274 | 0 | 260 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.259 | -0.080 | 8 | 135 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.261 | -0.155 | 17 | 205 |
| traditional pivots:D · bounce-rejection | longs | 16 | -0.272 | -0.257 | 0 | 169 |
| fibonacci pivots:W · bounce-touch | shorts | 8 | -0.282 | -0.414 | 0 | 59 |
| traditional pivots:W · bounce-rejection | both | 8 | -0.284 | -0.571 | 0 | 77 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.290 | -0.212 | 0 | 520 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.300 | -0.271 | 0 | 1030 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.310 | -0.331 | 0 | 510 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.319 | -0.149 | 4 | 212 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.320 | -0.308 | 0 | 530 |
| camarilla pivots:W · bounce-touch | longs | 20 | -0.322 | -0.275 | 0 | 82 |
| fibonacci pivots:W · bounce-touch | both | 16 | -0.333 | -0.322 | 0 | 92 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.333 | -0.246 | 8 | 129 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.334 | -0.051 | 25 | 70 |
| woodie pivots:D · bounce-touch | both | 24 | -0.337 | -0.302 | 0 | 276 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.341 | -0.346 | 0 | 147 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.345 | -0.224 | 8 | 132 |
| traditional pivots:D · bounce-touch | both | 24 | -0.363 | -0.306 | 0 | 279 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.379 | -0.368 | 0 | 147 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.384 | -0.344 | 0 | 270 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.411 | -0.245 | 17 | 150 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.465 | -0.336 | 17 | 75 |
| traditional pivots:W · bounce-touch | both | 8 | -0.582 | -0.653 | 0 | 85 |


## 1-hour  (IS 2016-06-01 → 2023-09-19, OOS 2023-09-19 → 2026-11-04; ETH buy & hold: IS +11664%, OOS +41%)

### Pivot Points

576 settings × 3 sides tested; 1480 combinations had ≥80 IS trades, 28% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.71. Average OOS result of the top-20 IS picks: +0.009 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.025 R/trade over 158 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| woodie pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 321 | +0.325 | 4.74 | 158 | +0.011 | +1.8 | 40 |
| woodie pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | longs | 318 | +0.396 | 4.69 | 155 | -0.060 | -9.3 | 34 |
| fibonacci pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 666 | +0.212 | 4.51 | 304 | +0.011 | +3.3 | 40 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 745 | +0.195 | 4.42 | 341 | -0.001 | -0.4 | 42 |
| fibonacci pivots:D breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 337 | +0.293 | 4.39 | 162 | -0.041 | -6.6 | 36 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:W · breakout | shorts | 8 | +0.208 | +0.233 | 100 | 55 |
| woodie pivots:W · breakout | shorts | 8 | +0.172 | +0.385 | 100 | 55 |
| woodie pivots:D · breakout | longs | 24 | +0.165 | -0.026 | 33 | 156 |
| traditional pivots:D · breakout | longs | 24 | +0.164 | -0.022 | 33 | 160 |
| camarilla pivots:W · breakout | longs | 24 | +0.163 | +0.010 | 46 | 113 |
| fibonacci pivots:W · breakout | longs | 24 | +0.157 | +0.058 | 71 | 52 |
| woodie pivots:W · breakout | longs | 8 | +0.149 | +0.289 | 100 | 60 |
| fibonacci pivots:D · breakout | longs | 24 | +0.148 | -0.062 | 12 | 296 |
| fibonacci pivots:W · breakout | both | 24 | +0.142 | +0.133 | 100 | 100 |
| fibonacci pivots:W · breakout | shorts | 16 | +0.124 | +0.237 | 100 | 58 |
| camarilla pivots:W · breakout | both | 24 | +0.097 | +0.015 | 62 | 213 |
| traditional pivots:W · breakout | both | 16 | +0.088 | +0.247 | 100 | 79 |
| fibonacci pivots:D · breakout | both | 24 | +0.080 | -0.034 | 25 | 556 |
| traditional pivots:D · breakout | both | 24 | +0.077 | +0.058 | 67 | 289 |
| woodie pivots:D · breakout | both | 24 | +0.070 | +0.045 | 62 | 280 |
| woodie pivots:W · breakout | both | 16 | +0.060 | +0.315 | 100 | 82 |
| traditional pivots:W · breakout | longs | 16 | +0.053 | +0.173 | 94 | 42 |
| camarilla pivots:W · breakout | shorts | 24 | +0.030 | +0.024 | 71 | 100 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.010 | -0.001 | 38 | 260 |
| camarilla pivots:D · breakout | longs | 24 | -0.006 | -0.084 | 0 | 579 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.015 | -0.081 | 12 | 449 |
| camarilla pivots:D · breakout | both | 24 | -0.019 | -0.075 | 0 | 1160 |
| traditional pivots:D · breakout | shorts | 24 | -0.020 | +0.170 | 79 | 129 |
| woodie pivots:D · breakout | shorts | 24 | -0.029 | +0.150 | 79 | 123 |
| camarilla pivots:D · breakout | shorts | 24 | -0.032 | -0.066 | 4 | 580 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.060 | -0.074 | 21 | 884 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.076 | -0.128 | 0 | 240 |
| fibonacci pivots:W · bounce-rejection | shorts | 16 | -0.080 | -0.275 | 0 | 60 |
| camarilla pivots:W · bounce-rejection | longs | 24 | -0.087 | -0.078 | 21 | 89 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.097 | -0.118 | 4 | 458 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.100 | -0.066 | 25 | 420 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.117 | -0.106 | 4 | 219 |
| woodie pivots:W · bounce-rejection | shorts | 8 | -0.118 | +0.139 | 75 | 52 |
| traditional pivots:D · bounce-rejection | longs | 24 | -0.121 | -0.074 | 17 | 138 |
| traditional pivots:W · bounce-rejection | longs | 8 | -0.134 | -0.569 | 0 | 51 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.139 | -0.129 | 8 | 184 |
| woodie pivots:D · bounce-rejection | longs | 24 | -0.140 | -0.058 | 17 | 134 |
| woodie pivots:W · bounce-rejection | both | 16 | -0.163 | -0.213 | 0 | 69 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.165 | -0.121 | 17 | 276 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.181 | -0.269 | 0 | 94 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.183 | -0.134 | 4 | 204 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.184 | -0.141 | 0 | 756 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.185 | -0.100 | 4 | 263 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.185 | -0.175 | 0 | 1504 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.187 | -0.210 | 0 | 747 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.190 | -0.183 | 0 | 207 |
| woodie pivots:W · bounce-touch | both | 16 | -0.192 | -0.425 | 0 | 92 |
| woodie pivots:W · bounce-touch | shorts | 16 | -0.193 | -0.327 | 19 | 48 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.193 | -0.178 | 17 | 94 |
| traditional pivots:W · bounce-touch | longs | 8 | -0.206 | -0.623 | 0 | 61 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.209 | -0.183 | 0 | 395 |
| woodie pivots:W · bounce-touch | longs | 8 | -0.210 | -0.602 | 0 | 62 |
| traditional pivots:W · bounce-rejection | both | 16 | -0.217 | -0.350 | 0 | 71 |
| traditional pivots:D · bounce-rejection | shorts | 24 | -0.219 | -0.159 | 4 | 141 |
| woodie pivots:W · bounce-rejection | longs | 8 | -0.225 | -0.508 | 0 | 50 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.231 | -0.151 | 8 | 110 |
| woodie pivots:D · bounce-rejection | shorts | 24 | -0.236 | -0.140 | 4 | 132 |
| fibonacci pivots:W · bounce-rejection | longs | 16 | -0.242 | -0.129 | 12 | 56 |
| traditional pivots:W · bounce-rejection | shorts | 8 | -0.256 | -0.133 | 25 | 50 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.257 | -0.191 | 0 | 810 |
| woodie pivots:D · bounce-touch | both | 24 | -0.264 | -0.163 | 0 | 423 |
| traditional pivots:D · bounce-touch | both | 24 | -0.267 | -0.219 | 0 | 431 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.299 | -0.247 | 0 | 222 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.305 | -0.369 | 0 | 58 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.309 | -0.198 | 0 | 415 |
| traditional pivots:W · bounce-touch | both | 16 | -0.312 | -0.403 | 0 | 94 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.329 | -0.268 | 0 | 114 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.348 | -0.248 | 0 | 224 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.352 | -0.188 | 0 | 219 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.368 | -0.341 | 0 | 112 |
| fibonacci pivots:W · bounce-touch | longs | 16 | -0.428 | -0.172 | 0 | 68 |
| traditional pivots:W · bounce-touch | shorts | 16 | -0.434 | -0.431 | 0 | 49 |


## 4-hour  (IS 2016-06-01 → 2023-09-18, OOS 2023-09-18 → 2026-11-04; ETH buy & hold: IS +11307%, OOS +42%)

### Pivot Points

864 settings × 3 sides tested; 1833 combinations had ≥50 IS trades, 38% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.64. Average OOS result of the top-20 IS picks: +0.037 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.009 R/trade over 129 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | longs | 290 | +0.276 | 5.77 | 129 | +0.107 | +13.9 | 43 |
| woodie pivots:D breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:yes | longs | 626 | +0.223 | 5.71 | 277 | +0.031 | +8.5 | 40 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 626 | +0.176 | 5.68 | 277 | +0.016 | +4.5 | 42 |
| fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | both | 563 | +0.190 | 5.50 | 231 | +0.088 | +20.2 | 41 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | 1257 | +0.115 | 5.25 | 532 | +0.035 | +18.7 | 42 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:M · breakout | both | 8 | +0.367 | +0.540 | 100 | 29 |
| traditional pivots:W · breakout | shorts | 8 | +0.322 | +0.111 | 88 | 47 |
| camarilla pivots:M · breakout | both | 24 | +0.222 | +0.291 | 92 | 49 |
| woodie pivots:D · breakout | longs | 24 | +0.217 | +0.032 | 67 | 124 |
| traditional pivots:D · breakout | longs | 24 | +0.205 | +0.031 | 75 | 124 |
| fibonacci pivots:W · breakout | longs | 24 | +0.203 | +0.077 | 62 | 43 |
| camarilla pivots:M · breakout | longs | 21 | +0.194 | +0.230 | 62 | 24 |
| fibonacci pivots:W · breakout | both | 24 | +0.194 | +0.156 | 100 | 86 |
| fibonacci pivots:W · breakout | shorts | 16 | +0.188 | +0.226 | 94 | 48 |
| fibonacci pivots:D · breakout | longs | 24 | +0.182 | +0.017 | 58 | 202 |
| woodie pivots:W · breakout | shorts | 16 | +0.157 | +0.272 | 88 | 35 |
| woodie pivots:D · breakout | both | 24 | +0.152 | +0.096 | 96 | 212 |
| traditional pivots:W · breakout | both | 24 | +0.149 | +0.148 | 83 | 41 |
| camarilla pivots:W · breakout | longs | 24 | +0.149 | -0.176 | 8 | 98 |
| fibonacci pivots:M · breakout | both | 16 | +0.147 | +0.396 | 100 | 30 |
| traditional pivots:D · breakout | both | 24 | +0.146 | +0.086 | 96 | 220 |
| camarilla pivots:M · breakout | shorts | 16 | +0.142 | +0.283 | 100 | 28 |
| fibonacci pivots:D · breakout | both | 24 | +0.136 | +0.022 | 71 | 371 |
| woodie pivots:W · breakout | both | 24 | +0.134 | +0.115 | 67 | 43 |
| traditional pivots:W · breakout | longs | 16 | +0.132 | +0.233 | 88 | 36 |
| camarilla pivots:W · breakout | both | 24 | +0.108 | -0.055 | 38 | 184 |
| woodie pivots:M · breakout | both | 8 | +0.104 | +0.688 | 100 | 28 |
| woodie pivots:W · breakout | longs | 16 | +0.102 | +0.345 | 100 | 38 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.088 | +0.027 | 62 | 169 |
| woodie pivots:D · breakout | shorts | 24 | +0.080 | +0.179 | 100 | 88 |
| traditional pivots:D · breakout | shorts | 24 | +0.080 | +0.163 | 100 | 96 |
| camarilla pivots:W · breakout | shorts | 24 | +0.066 | +0.087 | 58 | 87 |
| camarilla pivots:D · breakout | longs | 24 | +0.053 | -0.027 | 25 | 364 |
| camarilla pivots:D · breakout | both | 24 | +0.035 | -0.014 | 25 | 722 |
| camarilla pivots:D · breakout | shorts | 24 | +0.016 | -0.001 | 42 | 358 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.008 | -0.086 | 8 | 78 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.014 | -0.099 | 8 | 242 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.032 | -0.098 | 0 | 172 |
| camarilla pivots:M · bounce-touch | longs | 12 | -0.035 | -0.295 | 0 | 28 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.038 | -0.092 | 8 | 506 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.039 | -0.040 | 21 | 137 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.057 | -0.062 | 12 | 322 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.058 | -0.084 | 17 | 243 |
| camarilla pivots:W · bounce-rejection | longs | 24 | -0.068 | +0.004 | 62 | 62 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.078 | -0.024 | 42 | 150 |
| camarilla pivots:M · bounce-rejection | shorts | 12 | -0.082 | +0.097 | 67 | 23 |
| woodie pivots:D · bounce-rejection | longs | 24 | -0.097 | -0.040 | 29 | 109 |
| traditional pivots:D · bounce-rejection | longs | 24 | -0.099 | -0.050 | 29 | 109 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.113 | -0.055 | 21 | 218 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.123 | -0.062 | 8 | 712 |
| woodie pivots:W · bounce-touch | longs | 16 | -0.126 | -0.372 | 6 | 44 |
| traditional pivots:D · bounce-rejection | shorts | 24 | -0.131 | -0.062 | 17 | 109 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.143 | -0.104 | 0 | 204 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.144 | -0.058 | 25 | 208 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.148 | -0.129 | 0 | 1385 |
| traditional pivots:W · bounce-touch | longs | 16 | -0.149 | -0.298 | 31 | 46 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.149 | -0.121 | 0 | 206 |
| fibonacci pivots:W · bounce-rejection | longs | 18 | -0.151 | -0.120 | 11 | 39 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.156 | -0.092 | 21 | 78 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.160 | -0.130 | 0 | 394 |
| traditional pivots:W · bounce-rejection | longs | 10 | -0.160 | -0.358 | 0 | 47 |
| woodie pivots:W · bounce-rejection | longs | 8 | -0.162 | -0.130 | 0 | 44 |
| fibonacci pivots:M · bounce-rejection | both | 8 | -0.172 | +0.050 | 75 | 31 |
| fibonacci pivots:W · bounce-rejection | shorts | 24 | -0.174 | -0.161 | 33 | 43 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.180 | -0.208 | 0 | 671 |
| traditional pivots:W · bounce-rejection | both | 24 | -0.182 | -0.077 | 29 | 36 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.192 | -0.116 | 0 | 110 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.197 | -0.151 | 0 | 804 |
| woodie pivots:D · bounce-rejection | shorts | 24 | -0.201 | -0.079 | 8 | 99 |
| traditional pivots:W · bounce-rejection | shorts | 16 | -0.205 | -0.113 | 31 | 30 |
| traditional pivots:D · bounce-touch | both | 24 | -0.221 | -0.152 | 0 | 430 |
| woodie pivots:D · bounce-touch | both | 24 | -0.230 | -0.136 | 0 | 422 |
| traditional pivots:M · bounce-rejection | both | 8 | -0.231 | -0.120 | 25 | 26 |
| camarilla pivots:M · bounce-touch | both | 24 | -0.233 | -0.384 | 0 | 52 |
| camarilla pivots:M · bounce-rejection | both | 24 | -0.235 | -0.198 | 21 | 40 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.236 | -0.170 | 0 | 410 |
| traditional pivots:W · bounce-touch | both | 24 | -0.238 | -0.093 | 33 | 60 |
| woodie pivots:W · bounce-touch | both | 24 | -0.238 | -0.213 | 17 | 55 |
| woodie pivots:W · bounce-rejection | both | 20 | -0.239 | -0.134 | 20 | 38 |
| woodie pivots:W · bounce-rejection | shorts | 16 | -0.240 | +0.012 | 50 | 31 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.242 | -0.162 | 0 | 221 |
| camarilla pivots:M · bounce-rejection | longs | 8 | -0.258 | -0.163 | 0 | 22 |
| camarilla pivots:M · bounce-touch | shorts | 20 | -0.260 | -0.297 | 0 | 29 |
| woodie pivots:W · bounce-touch | shorts | 16 | -0.282 | -0.301 | 12 | 47 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.293 | -0.206 | 8 | 111 |
| fibonacci pivots:W · bounce-touch | longs | 24 | -0.296 | -0.136 | 21 | 56 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.297 | -0.180 | 0 | 224 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.301 | -0.210 | 0 | 114 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.304 | -0.291 | 12 | 58 |
| traditional pivots:W · bounce-touch | shorts | 16 | -0.320 | -0.314 | 6 | 49 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.325 | -0.165 | 0 | 219 |
| traditional pivots:M · bounce-touch | both | 8 | -0.422 | -0.120 | 25 | 33 |
| fibonacci pivots:M · bounce-touch | both | 16 | -0.536 | -0.270 | 12 | 34 |
| woodie pivots:M · bounce-touch | both | 8 | -0.562 | -0.296 | 0 | 31 |


## Daily  (IS 2016-06-01 → 2023-09-19, OOS 2023-09-19 → 2026-11-04; ETH buy & hold: IS +11698%, OOS +41%)

### Pivot Points

720 settings × 3 sides tested; 1970 combinations had ≥15 IS trades, 39% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.48. Average OOS result of the top-20 IS picks: +0.135 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.076 R/trade over 114 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | 248 | +0.222 | 3.87 | 114 | -0.052 | -6.0 | 44 |
| woodie pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | longs | 58 | +0.725 | 3.70 | 27 | +0.273 | +7.4 | 44 |
| woodie pivots:M breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | longs | 28 | +0.893 | 3.24 | 15 | +0.136 | +2.0 | 40 |
| traditional pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | longs | 67 | +0.573 | 3.11 | 28 | -0.097 | -2.7 | 32 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 141 | +0.251 | 3.08 | 61 | -0.027 | -1.7 | 43 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fibonacci pivots:M · breakout | longs | 24 | +0.356 | +0.299 | 88 | 12 |
| traditional pivots:M · breakout | longs | 16 | +0.331 | +0.291 | 75 | 10 |
| traditional pivots:M · bounce-rejection | shorts | 8 | +0.326 | +0.392 | 100 | 7 |
| fibonacci pivots:M · breakout | both | 24 | +0.292 | +0.315 | 100 | 20 |
| traditional pivots:M · breakout | both | 24 | +0.280 | -0.095 | 67 | 12 |
| traditional pivots:chart · breakout | longs | 12 | +0.239 | -0.046 | 25 | 34 |
| woodie pivots:chart · breakout | longs | 12 | +0.232 | -0.014 | 33 | 34 |
| fibonacci pivots:chart · breakout | longs | 12 | +0.225 | -0.002 | 33 | 42 |
| fibonacci pivots:W · breakout | longs | 24 | +0.221 | +0.083 | 67 | 28 |
| woodie pivots:M · breakout | longs | 24 | +0.199 | +0.208 | 58 | 7 |
| camarilla pivots:M · breakout | longs | 24 | +0.193 | +0.141 | 62 | 22 |
| traditional pivots:chart · breakout | both | 12 | +0.191 | -0.042 | 33 | 63 |
| woodie pivots:chart · breakout | both | 12 | +0.188 | -0.007 | 33 | 58 |
| camarilla pivots:chart · breakout | longs | 12 | +0.180 | +0.256 | 100 | 32 |
| camarilla pivots:M · breakout | both | 24 | +0.177 | +0.100 | 83 | 38 |
| woodie pivots:M · breakout | both | 24 | +0.167 | +0.133 | 67 | 10 |
| fibonacci pivots:M · bounce-rejection | shorts | 16 | +0.161 | -0.183 | 31 | 8 |
| fibonacci pivots:W · breakout | both | 24 | +0.158 | +0.017 | 62 | 56 |
| camarilla pivots:M · breakout | shorts | 24 | +0.154 | +0.052 | 54 | 19 |
| fibonacci pivots:chart · breakout | both | 12 | +0.150 | +0.055 | 67 | 72 |
| traditional pivots:W · breakout | longs | 24 | +0.141 | +0.138 | 79 | 19 |
| woodie pivots:chart · breakout | shorts | 12 | +0.128 | +0.006 | 42 | 26 |
| traditional pivots:chart · breakout | shorts | 12 | +0.124 | -0.037 | 33 | 28 |
| camarilla pivots:W · breakout | longs | 24 | +0.116 | -0.120 | 8 | 61 |
| woodie pivots:W · breakout | longs | 24 | +0.115 | +0.358 | 88 | 14 |
| traditional pivots:W · breakout | both | 24 | +0.099 | +0.012 | 58 | 30 |
| woodie pivots:W · breakout | both | 24 | +0.090 | +0.162 | 83 | 27 |
| camarilla pivots:chart · breakout | both | 12 | +0.083 | +0.169 | 100 | 66 |
| fibonacci pivots:W · breakout | shorts | 24 | +0.067 | -0.074 | 38 | 28 |
| camarilla pivots:W · breakout | both | 24 | +0.064 | -0.019 | 62 | 112 |
| fibonacci pivots:chart · breakout | shorts | 12 | +0.047 | +0.124 | 92 | 32 |
| woodie pivots:chart · bounce-rejection | longs | 12 | +0.032 | -0.211 | 0 | 56 |
| traditional pivots:W · breakout | shorts | 22 | +0.032 | -0.160 | 59 | 12 |
| camarilla pivots:M · bounce-rejection | shorts | 24 | +0.025 | -0.073 | 50 | 14 |
| woodie pivots:W · breakout | shorts | 20 | +0.023 | -0.003 | 70 | 13 |
| camarilla pivots:W · bounce-rejection | longs | 24 | +0.023 | -0.064 | 42 | 36 |
| traditional pivots:chart · bounce-rejection | longs | 12 | +0.014 | -0.164 | 8 | 60 |
| traditional pivots:W · bounce-rejection | longs | 24 | +0.006 | -0.152 | 33 | 19 |
| camarilla pivots:W · bounce-rejection | both | 24 | +0.002 | -0.055 | 29 | 74 |
| camarilla pivots:W · breakout | shorts | 24 | +0.001 | +0.106 | 88 | 52 |
| fibonacci pivots:M · breakout | shorts | 16 | -0.013 | +0.635 | 100 | 10 |
| camarilla pivots:chart · bounce-rejection | longs | 12 | -0.015 | -0.016 | 33 | 56 |
| fibonacci pivots:W · bounce-rejection | longs | 24 | -0.017 | -0.095 | 33 | 24 |
| fibonacci pivots:M · bounce-rejection | longs | 16 | -0.022 | -0.174 | 19 | 13 |
| woodie pivots:chart · bounce-rejection | both | 12 | -0.023 | -0.173 | 0 | 96 |
| woodie pivots:W · bounce-rejection | longs | 16 | -0.023 | -0.161 | 0 | 19 |
| camarilla pivots:M · bounce-rejection | both | 24 | -0.029 | -0.159 | 17 | 28 |
| fibonacci pivots:M · bounce-rejection | both | 24 | -0.032 | -0.112 | 21 | 19 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.032 | -0.056 | 42 | 38 |
| traditional pivots:chart · bounce-rejection | both | 12 | -0.034 | -0.130 | 8 | 96 |
| fibonacci pivots:chart · bounce-rejection | longs | 12 | -0.035 | -0.102 | 17 | 70 |
| camarilla pivots:chart · breakout | shorts | 12 | -0.037 | +0.075 | 83 | 34 |
| camarilla pivots:chart · bounce-rejection | both | 12 | -0.046 | -0.033 | 25 | 118 |
| camarilla pivots:chart · bounce-touch | longs | 12 | -0.051 | -0.058 | 8 | 572 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.070 | -0.049 | 29 | 51 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.074 | -0.087 | 21 | 102 |
| woodie pivots:M · breakout | shorts | 8 | -0.075 | +0.568 | 100 | 10 |
| camarilla pivots:M · bounce-rejection | longs | 24 | -0.076 | -0.235 | 8 | 14 |
| fibonacci pivots:chart · bounce-rejection | both | 12 | -0.087 | -0.109 | 25 | 113 |
| woodie pivots:W · bounce-rejection | both | 24 | -0.089 | -0.158 | 8 | 26 |
| traditional pivots:W · bounce-rejection | both | 24 | -0.099 | -0.100 | 33 | 32 |
| traditional pivots:M · breakout | shorts | 8 | -0.101 | +0.300 | 100 | 10 |
| camarilla pivots:chart · bounce-rejection | shorts | 12 | -0.104 | -0.061 | 25 | 57 |
| traditional pivots:chart · bounce-rejection | shorts | 12 | -0.112 | -0.103 | 25 | 38 |
| woodie pivots:chart · bounce-rejection | shorts | 12 | -0.114 | -0.150 | 17 | 38 |
| woodie pivots:chart · bounce-touch | longs | 12 | -0.118 | -0.133 | 17 | 159 |
| traditional pivots:chart · bounce-touch | longs | 12 | -0.119 | -0.136 | 17 | 162 |
| fibonacci pivots:W · bounce-rejection | shorts | 24 | -0.125 | -0.011 | 46 | 27 |
| traditional pivots:M · bounce-rejection | both | 16 | -0.137 | -0.098 | 38 | 15 |
| fibonacci pivots:chart · bounce-touch | longs | 12 | -0.142 | -0.112 | 8 | 254 |
| woodie pivots:W · bounce-rejection | shorts | 24 | -0.143 | -0.051 | 29 | 11 |
| woodie pivots:W · bounce-touch | longs | 24 | -0.147 | -0.221 | 8 | 28 |
| camarilla pivots:chart · bounce-touch | both | 12 | -0.170 | -0.167 | 0 | 760 |
| fibonacci pivots:chart · bounce-rejection | shorts | 12 | -0.175 | -0.117 | 25 | 46 |
| fibonacci pivots:W · bounce-touch | longs | 24 | -0.175 | -0.161 | 12 | 56 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.183 | -0.163 | 0 | 202 |
| traditional pivots:W · bounce-touch | longs | 24 | -0.193 | -0.055 | 46 | 31 |
| camarilla pivots:M · bounce-touch | longs | 24 | -0.194 | -0.359 | 8 | 26 |
| traditional pivots:W · bounce-rejection | shorts | 24 | -0.196 | -0.057 | 38 | 13 |
| woodie pivots:chart · bounce-touch | both | 12 | -0.234 | -0.187 | 0 | 294 |
| traditional pivots:M · bounce-touch | both | 24 | -0.237 | -0.427 | 4 | 16 |
| traditional pivots:chart · bounce-touch | both | 12 | -0.241 | -0.180 | 8 | 303 |
| fibonacci pivots:chart · bounce-touch | both | 12 | -0.248 | -0.202 | 0 | 488 |
| woodie pivots:W · bounce-touch | both | 24 | -0.262 | -0.175 | 4 | 55 |
| fibonacci pivots:M · bounce-touch | both | 24 | -0.264 | -0.212 | 4 | 28 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.272 | -0.163 | 0 | 114 |
| camarilla pivots:M · bounce-touch | both | 24 | -0.278 | -0.297 | 0 | 52 |
| traditional pivots:W · bounce-touch | both | 24 | -0.299 | -0.119 | 21 | 60 |
| traditional pivots:M · bounce-touch | shorts | 24 | -0.305 | -0.402 | 8 | 10 |
| traditional pivots:M · bounce-rejection | longs | 8 | -0.309 | -0.555 | 0 | 11 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.312 | -0.254 | 0 | 100 |
| woodie pivots:M · bounce-touch | both | 24 | -0.323 | -0.298 | 17 | 16 |
| woodie pivots:W · bounce-touch | shorts | 24 | -0.350 | -0.138 | 25 | 27 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.351 | -0.174 | 8 | 58 |
| camarilla pivots:M · bounce-touch | shorts | 24 | -0.356 | -0.238 | 17 | 26 |
| woodie pivots:M · bounce-rejection | shorts | 16 | -0.364 | +0.026 | 62 | 8 |
| woodie pivots:chart · bounce-touch | shorts | 12 | -0.365 | -0.259 | 0 | 136 |
| fibonacci pivots:chart · bounce-touch | shorts | 12 | -0.370 | -0.312 | 0 | 234 |
| fibonacci pivots:M · bounce-touch | longs | 16 | -0.373 | -0.196 | 12 | 16 |
| traditional pivots:chart · bounce-touch | shorts | 12 | -0.373 | -0.237 | 8 | 141 |
| traditional pivots:W · bounce-touch | shorts | 24 | -0.380 | -0.180 | 4 | 29 |
| fibonacci pivots:M · bounce-touch | shorts | 24 | -0.386 | -0.276 | 8 | 14 |
| woodie pivots:M · bounce-rejection | both | 16 | -0.389 | +0.012 | 56 | 16 |
| woodie pivots:M · bounce-touch | shorts | 24 | -0.422 | -0.351 | 17 | 9 |
| camarilla pivots:chart · bounce-touch | shorts | 12 | -0.510 | -0.500 | 0 | 234 |
| woodie pivots:M · bounce-rejection | longs | 8 | -0.596 | -0.095 | 25 | 10 |
| woodie pivots:M · bounce-touch | longs | 8 | -0.635 | -0.157 | 12 | 14 |
| traditional pivots:M · bounce-touch | longs | 8 | -0.787 | -0.509 | 0 | 15 |

