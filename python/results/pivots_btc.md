# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | fibonacci pivots:W · breakout (longs) | +0.311 | -0.074 | 12 | fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | 60 | -0.141 | -0.156 |
| 1h | Pivot Points | traditional pivots:W · breakout (longs) | +0.382 | +0.068 | 75 | traditional pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no | 64 | +0.099 | -0.041 |
| 4h | Pivot Points | traditional pivots:W · breakout (longs) | +0.431 | +0.149 | 94 | traditional pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | 59 | +0.114 | -0.103 |
| 1d | Pivot Points | fibonacci pivots:M · breakout (longs) | +0.523 | +0.294 | 83 | fibonacci pivots:M breakout level3 stop1ATR target:2R exitAtPeriodEnd:no | 8 | +0.803 | -0.003 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 146 | +0.421 | 67 | -0.287 | -0.124 | -0.163 | -0.127 | +0.45 |
| 1h | Pivot Points | woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | 1554 | +0.121 | 703 | +0.017 | -0.085 | +0.101 | -0.041 | +0.41 |
| 4h | Pivot Points | fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | longs | 125 | +0.652 | 51 | +0.114 | -0.108 | +0.221 | +0.023 | +0.29 |
| 1d | Pivot Points | traditional pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | longs | 85 | +0.708 | 42 | +0.141 | +0.032 | +0.109 | +0.065 | +0.36 |


## 15-minute  (IS 2020-01-01 → 2024-10-14, OOS 2024-10-14 → 2026-11-03; BTC buy & hold: IS +817%, OOS +17%)

### Pivot Points

576 settings × 3 sides tested; 1136 combinations had ≥120 IS trades, 16% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.45. Average OOS result of the top-20 IS picks: -0.127 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.124 R/trade over 67 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 146 | +0.421 | 3.34 | 67 | -0.287 | -19.2 | 28 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:no | longs | 146 | +0.421 | 3.34 | 67 | -0.243 | -16.3 | 30 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | both | 282 | +0.300 | 3.34 | 134 | -0.210 | -28.2 | 31 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:no | both | 281 | +0.296 | 3.27 | 133 | -0.181 | -24.1 | 32 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | both | 282 | +0.454 | 3.25 | 134 | -0.161 | -21.6 | 26 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fibonacci pivots:W · breakout | longs | 8 | +0.311 | -0.074 | 12 | 60 |
| camarilla pivots:W · breakout | longs | 24 | +0.214 | -0.217 | 0 | 74 |
| fibonacci pivots:W · breakout | both | 16 | +0.172 | -0.032 | 38 | 90 |
| traditional pivots:W · breakout | both | 8 | +0.170 | +0.110 | 75 | 80 |
| camarilla pivots:W · breakout | both | 24 | +0.128 | -0.146 | 8 | 149 |
| traditional pivots:D · breakout | longs | 24 | +0.081 | -0.229 | 8 | 116 |
| woodie pivots:D · breakout | longs | 16 | +0.044 | -0.283 | 0 | 187 |
| camarilla pivots:W · breakout | shorts | 24 | +0.034 | -0.075 | 17 | 75 |
| traditional pivots:D · breakout | both | 24 | -0.002 | -0.204 | 0 | 233 |
| woodie pivots:D · breakout | both | 24 | -0.009 | -0.178 | 0 | 231 |
| fibonacci pivots:D · breakout | longs | 24 | -0.012 | -0.299 | 0 | 231 |
| woodie pivots:W · breakout | both | 8 | -0.021 | -0.343 | 0 | 87 |
| fibonacci pivots:D · breakout | both | 24 | -0.026 | -0.233 | 0 | 465 |
| traditional pivots:D · breakout | shorts | 16 | -0.031 | -0.255 | 0 | 193 |
| fibonacci pivots:D · breakout | shorts | 24 | -0.042 | -0.166 | 0 | 234 |
| woodie pivots:D · breakout | shorts | 16 | -0.047 | -0.174 | 25 | 184 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.150 | -0.266 | 4 | 367 |
| camarilla pivots:W · bounce-rejection | longs | 20 | -0.180 | -0.292 | 0 | 73 |
| fibonacci pivots:W · bounce-rejection | shorts | 8 | -0.181 | -0.466 | 0 | 59 |
| camarilla pivots:D · breakout | shorts | 24 | -0.186 | -0.199 | 0 | 498 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.187 | -0.292 | 0 | 757 |
| camarilla pivots:D · breakout | both | 24 | -0.191 | -0.237 | 0 | 972 |
| camarilla pivots:D · breakout | longs | 24 | -0.196 | -0.274 | 0 | 473 |
| woodie pivots:W · bounce-rejection | both | 8 | -0.208 | -0.247 | 0 | 90 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.221 | -0.169 | 4 | 135 |
| fibonacci pivots:W · bounce-rejection | both | 16 | -0.224 | -0.197 | 12 | 90 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.225 | -0.318 | 0 | 388 |
| traditional pivots:D · bounce-rejection | longs | 16 | -0.231 | -0.237 | 0 | 178 |
| woodie pivots:D · bounce-rejection | longs | 20 | -0.232 | -0.155 | 10 | 121 |
| camarilla pivots:W · bounce-rejection | shorts | 20 | -0.237 | -0.036 | 50 | 71 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.239 | -0.306 | 21 | 154 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.245 | -0.268 | 0 | 206 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.248 | -0.268 | 0 | 414 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.250 | -0.269 | 0 | 208 |
| woodie pivots:D · bounce-rejection | shorts | 16 | -0.252 | -0.180 | 0 | 168 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.252 | -0.156 | 0 | 229 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.265 | -0.330 | 0 | 226 |
| traditional pivots:W · bounce-rejection | both | 8 | -0.282 | +0.583 | 75 | 91 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.283 | -0.339 | 0 | 277 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.291 | -0.416 | 0 | 516 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.292 | -0.252 | 0 | 170 |
| fibonacci pivots:W · bounce-touch | both | 16 | -0.307 | -0.297 | 31 | 99 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.309 | -0.457 | 0 | 1022 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.328 | -0.498 | 0 | 506 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.329 | -0.399 | 0 | 154 |
| camarilla pivots:W · bounce-touch | longs | 20 | -0.331 | -0.331 | 0 | 79 |
| woodie pivots:D · bounce-touch | both | 24 | -0.334 | -0.358 | 0 | 298 |
| woodie pivots:W · bounce-touch | both | 8 | -0.352 | -0.354 | 0 | 94 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.390 | -0.450 | 0 | 552 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.395 | -0.302 | 8 | 150 |
| traditional pivots:D · bounce-touch | both | 24 | -0.398 | -0.428 | 0 | 299 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.401 | -0.302 | 8 | 74 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.434 | -0.413 | 0 | 144 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.464 | -0.469 | 0 | 145 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.489 | -0.565 | 0 | 275 |
| traditional pivots:W · bounce-touch | both | 8 | -0.498 | +0.399 | 75 | 97 |
| fibonacci pivots:W · bounce-touch | shorts | 8 | -0.517 | -0.607 | 0 | 64 |


## 1-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6684%, OOS +163%)

### Pivot Points

576 settings × 3 sides tested; 1464 combinations had ≥80 IS trades, 28% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.41. Average OOS result of the top-20 IS picks: -0.041 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.085 R/trade over 703 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | 1554 | +0.121 | 3.98 | 703 | +0.017 | +11.8 | 39 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 788 | +0.166 | 3.90 | 362 | +0.048 | +17.5 | 41 |
| traditional pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | 175 | +0.401 | 3.50 | 81 | -0.090 | -7.3 | 33 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | 217 | +0.482 | 3.48 | 99 | -0.193 | -19.1 | 35 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | longs | 197 | +0.373 | 3.46 | 93 | -0.120 | -11.2 | 32 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:W · breakout | longs | 8 | +0.382 | +0.068 | 75 | 64 |
| fibonacci pivots:W · breakout | longs | 16 | +0.357 | +0.075 | 62 | 74 |
| woodie pivots:W · breakout | longs | 8 | +0.280 | +0.044 | 50 | 63 |
| fibonacci pivots:W · breakout | both | 24 | +0.205 | +0.098 | 79 | 101 |
| woodie pivots:W · breakout | both | 16 | +0.200 | -0.124 | 19 | 85 |
| traditional pivots:W · breakout | both | 16 | +0.197 | +0.129 | 94 | 83 |
| camarilla pivots:W · breakout | longs | 24 | +0.195 | -0.110 | 4 | 116 |
| camarilla pivots:W · breakout | both | 24 | +0.174 | -0.056 | 33 | 227 |
| fibonacci pivots:W · breakout | shorts | 16 | +0.162 | +0.021 | 62 | 60 |
| woodie pivots:W · breakout | shorts | 8 | +0.160 | -0.339 | 0 | 65 |
| camarilla pivots:W · breakout | shorts | 24 | +0.151 | +0.001 | 54 | 111 |
| traditional pivots:D · breakout | longs | 24 | +0.130 | -0.022 | 38 | 164 |
| woodie pivots:D · breakout | longs | 24 | +0.098 | -0.033 | 25 | 165 |
| traditional pivots:D · breakout | both | 24 | +0.096 | -0.062 | 17 | 318 |
| traditional pivots:W · breakout | shorts | 8 | +0.083 | +0.100 | 75 | 58 |
| woodie pivots:D · breakout | both | 24 | +0.079 | -0.054 | 17 | 312 |
| woodie pivots:D · breakout | shorts | 24 | +0.058 | -0.078 | 4 | 146 |
| traditional pivots:D · breakout | shorts | 24 | +0.056 | -0.106 | 4 | 154 |
| fibonacci pivots:D · breakout | longs | 24 | +0.048 | -0.041 | 21 | 312 |
| woodie pivots:W · bounce-rejection | longs | 8 | +0.039 | -0.283 | 0 | 62 |
| fibonacci pivots:D · breakout | both | 24 | +0.038 | -0.037 | 17 | 612 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.026 | -0.033 | 17 | 299 |
| camarilla pivots:D · breakout | shorts | 24 | -0.047 | -0.074 | 17 | 604 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.054 | -0.103 | 0 | 425 |
| fibonacci pivots:W · bounce-touch | longs | 16 | -0.065 | -0.104 | 19 | 71 |
| camarilla pivots:D · breakout | both | 24 | -0.078 | -0.089 | 0 | 1206 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.082 | -0.175 | 8 | 94 |
| traditional pivots:D · bounce-rejection | shorts | 24 | -0.095 | -0.215 | 0 | 157 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.095 | -0.117 | 0 | 829 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.095 | -0.142 | 8 | 235 |
| camarilla pivots:D · breakout | longs | 24 | -0.109 | -0.103 | 0 | 602 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.122 | -0.198 | 0 | 190 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.123 | -0.142 | 0 | 474 |
| fibonacci pivots:W · bounce-rejection | longs | 16 | -0.129 | -0.216 | 12 | 60 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.133 | -0.131 | 4 | 412 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.141 | -0.196 | 0 | 316 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.151 | -0.143 | 0 | 238 |
| camarilla pivots:W · bounce-rejection | longs | 24 | -0.166 | -0.222 | 0 | 96 |
| woodie pivots:D · bounce-rejection | longs | 24 | -0.175 | -0.161 | 0 | 162 |
| woodie pivots:W · bounce-touch | longs | 8 | -0.178 | -0.217 | 0 | 75 |
| traditional pivots:D · bounce-rejection | longs | 24 | -0.182 | -0.176 | 0 | 164 |
| fibonacci pivots:W · bounce-rejection | shorts | 16 | -0.193 | -0.092 | 50 | 67 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.197 | +0.016 | 46 | 98 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.198 | -0.189 | 0 | 301 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.219 | -0.179 | 0 | 776 |
| woodie pivots:W · bounce-rejection | both | 16 | -0.227 | -0.245 | 12 | 83 |
| woodie pivots:D · bounce-rejection | shorts | 24 | -0.230 | -0.223 | 0 | 144 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.245 | -0.207 | 0 | 1542 |
| traditional pivots:W · bounce-rejection | shorts | 8 | -0.249 | +0.364 | 100 | 63 |
| traditional pivots:W · bounce-touch | shorts | 16 | -0.264 | +0.072 | 50 | 56 |
| woodie pivots:W · bounce-touch | shorts | 16 | -0.266 | -0.173 | 12 | 51 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.273 | -0.235 | 0 | 757 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.273 | -0.071 | 33 | 237 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.278 | -0.234 | 0 | 116 |
| woodie pivots:W · bounce-touch | both | 16 | -0.283 | -0.147 | 19 | 100 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.298 | -0.160 | 21 | 240 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.303 | -0.184 | 12 | 412 |
| traditional pivots:D · bounce-touch | both | 24 | -0.310 | -0.217 | 0 | 472 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.321 | -0.221 | 0 | 846 |
| woodie pivots:D · bounce-touch | both | 24 | -0.321 | -0.187 | 0 | 468 |
| traditional pivots:W · bounce-rejection | both | 16 | -0.323 | +0.307 | 100 | 80 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.323 | -0.271 | 0 | 232 |
| woodie pivots:W · bounce-rejection | shorts | 8 | -0.329 | -0.444 | 0 | 64 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.334 | -0.119 | 42 | 122 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.339 | -0.260 | 0 | 434 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.340 | -0.248 | 0 | 236 |
| traditional pivots:W · bounce-touch | both | 16 | -0.358 | +0.032 | 62 | 103 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.370 | -0.299 | 0 | 231 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.396 | -0.262 | 0 | 119 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.433 | -0.194 | 33 | 67 |
| traditional pivots:W · bounce-rejection | longs | 8 | -0.457 | +0.113 | 62 | 55 |
| traditional pivots:W · bounce-touch | longs | 8 | -0.502 | -0.073 | 50 | 72 |


## 4-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6640%, OOS +164%)

### Pivot Points

864 settings × 3 sides tested; 1835 combinations had ≥50 IS trades, 36% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.29. Average OOS result of the top-20 IS picks: +0.023 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.108 R/trade over 51 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | longs | 125 | +0.652 | 4.88 | 51 | +0.114 | +5.8 | 39 |
| woodie pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | both | 236 | +0.471 | 4.81 | 110 | +0.027 | +3.0 | 35 |
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | both | 212 | +0.444 | 4.75 | 96 | -0.006 | -0.5 | 38 |
| woodie pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | 248 | +0.411 | 4.72 | 115 | -0.009 | -1.1 | 41 |
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 129 | +0.552 | 4.64 | 53 | +0.026 | +1.4 | 42 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:W · breakout | longs | 16 | +0.431 | +0.149 | 94 | 40 |
| fibonacci pivots:W · breakout | longs | 24 | +0.339 | +0.109 | 83 | 52 |
| woodie pivots:W · breakout | shorts | 8 | +0.337 | -0.157 | 0 | 56 |
| fibonacci pivots:W · breakout | both | 24 | +0.271 | +0.014 | 62 | 96 |
| fibonacci pivots:M · breakout | both | 8 | +0.268 | +0.111 | 75 | 39 |
| traditional pivots:M · breakout | both | 8 | +0.265 | +0.295 | 100 | 29 |
| camarilla pivots:M · breakout | longs | 24 | +0.259 | +0.164 | 83 | 30 |
| fibonacci pivots:W · breakout | shorts | 16 | +0.245 | -0.111 | 6 | 53 |
| woodie pivots:M · breakout | both | 8 | +0.230 | +0.316 | 100 | 29 |
| traditional pivots:W · breakout | both | 24 | +0.227 | +0.307 | 83 | 38 |
| fibonacci pivots:M · breakout | longs | 8 | +0.205 | -0.088 | 50 | 23 |
| camarilla pivots:M · bounce-rejection | shorts | 11 | +0.193 | -0.366 | 0 | 24 |
| traditional pivots:D · breakout | longs | 24 | +0.186 | -0.028 | 33 | 140 |
| camarilla pivots:W · breakout | longs | 24 | +0.186 | -0.137 | 0 | 108 |
| camarilla pivots:W · breakout | both | 24 | +0.178 | -0.056 | 12 | 206 |
| woodie pivots:W · breakout | longs | 16 | +0.171 | +0.104 | 62 | 38 |
| camarilla pivots:W · breakout | shorts | 24 | +0.170 | +0.031 | 62 | 99 |
| camarilla pivots:M · breakout | both | 24 | +0.167 | +0.074 | 83 | 52 |
| traditional pivots:D · breakout | both | 24 | +0.147 | -0.008 | 58 | 250 |
| traditional pivots:W · breakout | shorts | 8 | +0.145 | +0.028 | 50 | 50 |
| woodie pivots:D · breakout | longs | 24 | +0.138 | -0.024 | 54 | 140 |
| woodie pivots:W · breakout | both | 24 | +0.136 | +0.302 | 58 | 36 |
| woodie pivots:D · breakout | both | 24 | +0.116 | +0.015 | 67 | 252 |
| traditional pivots:D · breakout | shorts | 24 | +0.094 | +0.021 | 62 | 110 |
| fibonacci pivots:D · breakout | longs | 24 | +0.091 | +0.045 | 75 | 206 |
| woodie pivots:D · breakout | shorts | 24 | +0.086 | +0.067 | 79 | 112 |
| fibonacci pivots:D · breakout | both | 24 | +0.075 | +0.010 | 50 | 404 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.056 | -0.027 | 25 | 199 |
| camarilla pivots:M · bounce-rejection | longs | 4 | +0.016 | -0.056 | 50 | 26 |
| camarilla pivots:M · breakout | shorts | 16 | +0.014 | -0.091 | 25 | 25 |
| fibonacci pivots:W · bounce-rejection | longs | 16 | +0.010 | -0.184 | 6 | 49 |
| traditional pivots:D · bounce-rejection | shorts | 24 | +0.008 | -0.155 | 4 | 118 |
| camarilla pivots:D · breakout | longs | 24 | +0.006 | -0.027 | 29 | 378 |
| camarilla pivots:D · breakout | both | 24 | +0.001 | -0.032 | 25 | 759 |
| camarilla pivots:D · breakout | shorts | 24 | -0.004 | -0.037 | 25 | 381 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.021 | -0.070 | 17 | 248 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.036 | -0.081 | 8 | 524 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.047 | -0.203 | 17 | 74 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.049 | -0.141 | 0 | 232 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.049 | -0.089 | 8 | 255 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.050 | -0.110 | 12 | 144 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.057 | -0.118 | 4 | 295 |
| traditional pivots:M · bounce-touch | both | 8 | -0.058 | -0.044 | 38 | 32 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.063 | -0.127 | 4 | 151 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.084 | -0.182 | 17 | 146 |
| traditional pivots:M · bounce-rejection | both | 8 | -0.088 | +0.052 | 50 | 26 |
| traditional pivots:D · bounce-rejection | longs | 24 | -0.093 | -0.128 | 0 | 114 |
| woodie pivots:D · bounce-rejection | longs | 24 | -0.096 | -0.114 | 12 | 121 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.099 | -0.137 | 8 | 232 |
| woodie pivots:D · bounce-rejection | shorts | 24 | -0.101 | -0.165 | 12 | 111 |
| fibonacci pivots:M · bounce-rejection | both | 8 | -0.109 | +0.088 | 75 | 32 |
| camarilla pivots:W · bounce-rejection | longs | 24 | -0.122 | -0.159 | 12 | 74 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.126 | -0.064 | 8 | 742 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.169 | -0.128 | 0 | 1429 |
| camarilla pivots:M · bounce-touch | longs | 20 | -0.177 | +0.198 | 70 | 26 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.177 | -0.086 | 17 | 237 |
| camarilla pivots:M · bounce-rejection | both | 24 | -0.183 | -0.199 | 8 | 42 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.192 | -0.065 | 29 | 80 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.195 | -0.123 | 21 | 412 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.199 | -0.128 | 17 | 240 |
| fibonacci pivots:W · bounce-touch | longs | 24 | -0.208 | +0.102 | 50 | 55 |
| woodie pivots:W · bounce-rejection | shorts | 8 | -0.215 | -0.164 | 0 | 54 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.220 | -0.201 | 0 | 682 |
| traditional pivots:W · bounce-touch | both | 24 | -0.223 | -0.030 | 67 | 56 |
| fibonacci pivots:W · bounce-rejection | shorts | 24 | -0.226 | +0.012 | 38 | 39 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.228 | -0.150 | 0 | 840 |
| traditional pivots:W · bounce-rejection | shorts | 16 | -0.232 | +0.052 | 62 | 36 |
| traditional pivots:D · bounce-touch | both | 24 | -0.234 | -0.170 | 0 | 471 |
| woodie pivots:D · bounce-touch | both | 24 | -0.236 | -0.161 | 0 | 467 |
| woodie pivots:W · bounce-rejection | longs | 8 | -0.246 | -0.196 | 0 | 56 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.246 | -0.164 | 0 | 116 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.259 | -0.179 | 0 | 428 |
| traditional pivots:W · bounce-rejection | both | 24 | -0.268 | -0.208 | 25 | 40 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.269 | -0.211 | 0 | 231 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.274 | -0.201 | 0 | 235 |
| camarilla pivots:M · bounce-touch | both | 24 | -0.279 | -0.077 | 17 | 55 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.298 | -0.234 | 0 | 230 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.300 | -0.236 | 0 | 118 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.313 | +0.001 | 42 | 122 |
| traditional pivots:W · bounce-touch | shorts | 16 | -0.315 | +0.147 | 88 | 56 |
| woodie pivots:W · bounce-touch | longs | 16 | -0.318 | -0.035 | 38 | 48 |
| woodie pivots:W · bounce-touch | both | 24 | -0.335 | -0.327 | 17 | 55 |
| traditional pivots:W · bounce-rejection | longs | 8 | -0.341 | -0.050 | 25 | 51 |
| woodie pivots:W · bounce-rejection | both | 16 | -0.378 | -0.109 | 19 | 73 |
| camarilla pivots:M · bounce-touch | shorts | 24 | -0.379 | -0.237 | 25 | 32 |
| woodie pivots:W · bounce-touch | shorts | 16 | -0.394 | -0.168 | 19 | 50 |
| fibonacci pivots:M · bounce-touch | both | 16 | -0.397 | -0.216 | 25 | 36 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.402 | -0.069 | 33 | 67 |
| fibonacci pivots:M · bounce-touch | shorts | 8 | -0.417 | -0.288 | 25 | 26 |
| woodie pivots:M · bounce-rejection | both | 8 | -0.429 | +0.161 | 75 | 24 |
| woodie pivots:M · bounce-touch | both | 8 | -0.437 | -0.291 | 25 | 32 |
| traditional pivots:W · bounce-touch | longs | 16 | -0.501 | +0.250 | 94 | 46 |


## Daily  (IS 2015-07-20 → 2023-06-15, OOS 2023-06-15 → 2026-11-03; BTC buy & hold: IS +9032%, OOS +201%)

### Pivot Points

720 settings × 3 sides tested; 1960 combinations had ≥15 IS trades, 39% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.36. Average OOS result of the top-20 IS picks: +0.065 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.032 R/trade over 42 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| traditional pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | longs | 85 | +0.708 | 4.41 | 42 | +0.141 | +5.9 | 40 |
| camarilla pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 212 | +0.243 | 3.81 | 91 | -0.056 | -5.1 | 44 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | 172 | +0.277 | 3.73 | 74 | -0.150 | -11.1 | 36 |
| fibonacci pivots:W breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | both | 131 | +0.488 | 3.71 | 65 | +0.074 | +4.8 | 37 |
| traditional pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | both | 149 | +0.453 | 3.69 | 75 | +0.013 | +1.0 | 35 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fibonacci pivots:M · breakout | longs | 24 | +0.523 | +0.294 | 83 | 14 |
| woodie pivots:M · breakout | longs | 16 | +0.414 | +0.307 | 81 | 11 |
| camarilla pivots:chart · breakout | longs | 12 | +0.351 | +0.135 | 83 | 43 |
| fibonacci pivots:M · breakout | both | 24 | +0.349 | +0.249 | 88 | 20 |
| fibonacci pivots:chart · breakout | longs | 12 | +0.296 | +0.065 | 75 | 52 |
| traditional pivots:M · breakout | longs | 24 | +0.270 | +0.365 | 79 | 8 |
| fibonacci pivots:W · breakout | longs | 24 | +0.259 | +0.124 | 62 | 42 |
| woodie pivots:chart · breakout | longs | 12 | +0.249 | +0.098 | 83 | 47 |
| traditional pivots:chart · breakout | longs | 12 | +0.248 | +0.114 | 83 | 46 |
| camarilla pivots:W · breakout | longs | 24 | +0.226 | -0.051 | 12 | 69 |
| woodie pivots:W · breakout | longs | 24 | +0.214 | +0.447 | 88 | 16 |
| traditional pivots:W · breakout | longs | 24 | +0.205 | +0.404 | 88 | 18 |
| camarilla pivots:chart · breakout | both | 12 | +0.194 | +0.079 | 67 | 78 |
| fibonacci pivots:W · breakout | both | 24 | +0.194 | +0.098 | 46 | 74 |
| camarilla pivots:M · breakout | longs | 24 | +0.175 | +0.012 | 38 | 29 |
| fibonacci pivots:chart · breakout | both | 12 | +0.171 | +0.037 | 67 | 94 |
| camarilla pivots:M · breakout | both | 24 | +0.168 | +0.006 | 50 | 44 |
| camarilla pivots:M · breakout | shorts | 24 | +0.164 | -0.023 | 50 | 16 |
| woodie pivots:chart · breakout | both | 12 | +0.163 | +0.034 | 58 | 81 |
| woodie pivots:W · breakout | both | 24 | +0.152 | +0.267 | 79 | 28 |
| fibonacci pivots:M · breakout | shorts | 12 | +0.151 | +0.234 | 83 | 13 |
| traditional pivots:chart · breakout | both | 12 | +0.147 | +0.038 | 92 | 77 |
| camarilla pivots:W · breakout | both | 24 | +0.144 | -0.024 | 25 | 126 |
| traditional pivots:M · breakout | both | 24 | +0.132 | +0.221 | 75 | 11 |
| traditional pivots:W · breakout | both | 24 | +0.119 | +0.248 | 83 | 28 |
| fibonacci pivots:W · breakout | shorts | 24 | +0.078 | +0.059 | 46 | 32 |
| camarilla pivots:W · bounce-rejection | longs | 24 | +0.071 | -0.029 | 46 | 38 |
| woodie pivots:W · breakout | shorts | 24 | +0.061 | -0.001 | 42 | 11 |
| camarilla pivots:chart · bounce-rejection | longs | 12 | +0.052 | -0.085 | 25 | 74 |
| woodie pivots:chart · breakout | shorts | 12 | +0.042 | -0.050 | 33 | 35 |
| camarilla pivots:W · bounce-rejection | both | 24 | +0.038 | -0.026 | 38 | 76 |
| camarilla pivots:W · breakout | shorts | 24 | +0.038 | +0.004 | 46 | 58 |
| fibonacci pivots:M · bounce-rejection | shorts | 8 | +0.031 | -0.062 | 50 | 18 |
| fibonacci pivots:chart · bounce-rejection | longs | 12 | +0.022 | -0.072 | 25 | 80 |
| traditional pivots:chart · bounce-rejection | longs | 12 | +0.022 | -0.044 | 33 | 64 |
| woodie pivots:M · breakout | both | 24 | +0.015 | +0.287 | 92 | 11 |
| camarilla pivots:chart · bounce-rejection | both | 12 | +0.007 | -0.116 | 8 | 136 |
| traditional pivots:chart · breakout | shorts | 12 | +0.004 | -0.067 | 42 | 31 |
| woodie pivots:chart · bounce-rejection | longs | 12 | -0.001 | -0.050 | 33 | 64 |
| fibonacci pivots:chart · breakout | shorts | 12 | -0.006 | -0.001 | 58 | 42 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.011 | -0.032 | 42 | 40 |
| camarilla pivots:chart · breakout | shorts | 12 | -0.012 | +0.007 | 33 | 34 |
| traditional pivots:W · breakout | shorts | 24 | -0.012 | -0.019 | 38 | 9 |
| camarilla pivots:chart · bounce-touch | longs | 12 | -0.036 | -0.047 | 25 | 612 |
| fibonacci pivots:chart · bounce-rejection | both | 12 | -0.052 | -0.089 | 25 | 130 |
| woodie pivots:chart · bounce-rejection | both | 12 | -0.057 | -0.111 | 25 | 109 |
| fibonacci pivots:W · bounce-rejection | longs | 24 | -0.063 | +0.011 | 42 | 27 |
| traditional pivots:chart · bounce-rejection | both | 12 | -0.063 | -0.053 | 33 | 108 |
| fibonacci pivots:M · bounce-rejection | longs | 8 | -0.063 | +0.030 | 75 | 13 |
| camarilla pivots:M · bounce-rejection | longs | 24 | -0.071 | +0.115 | 75 | 14 |
| woodie pivots:W · bounce-rejection | longs | 20 | -0.078 | +0.011 | 60 | 19 |
| traditional pivots:M · breakout | shorts | 8 | -0.083 | -0.179 | 12 | 8 |
| camarilla pivots:chart · bounce-rejection | shorts | 12 | -0.084 | -0.161 | 8 | 65 |
| traditional pivots:W · bounce-rejection | longs | 24 | -0.084 | -0.189 | 38 | 13 |
| camarilla pivots:M · bounce-rejection | both | 24 | -0.086 | -0.038 | 50 | 32 |
| camarilla pivots:M · bounce-rejection | shorts | 24 | -0.096 | -0.162 | 17 | 18 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.100 | +0.015 | 54 | 56 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.113 | -0.106 | 25 | 112 |
| woodie pivots:W · bounce-rejection | both | 24 | -0.116 | -0.212 | 38 | 33 |
| camarilla pivots:M · bounce-touch | longs | 24 | -0.128 | +0.046 | 67 | 24 |
| fibonacci pivots:W · bounce-rejection | shorts | 24 | -0.141 | +0.015 | 46 | 29 |
| woodie pivots:chart · bounce-rejection | shorts | 12 | -0.148 | -0.188 | 17 | 47 |
| traditional pivots:W · bounce-rejection | both | 24 | -0.148 | -0.147 | 42 | 32 |
| fibonacci pivots:chart · bounce-touch | longs | 12 | -0.151 | -0.129 | 8 | 284 |
| fibonacci pivots:chart · bounce-rejection | shorts | 12 | -0.152 | -0.116 | 8 | 56 |
| traditional pivots:chart · bounce-touch | longs | 12 | -0.161 | -0.156 | 8 | 184 |
| woodie pivots:chart · bounce-touch | longs | 12 | -0.163 | -0.133 | 0 | 187 |
| woodie pivots:W · bounce-rejection | shorts | 24 | -0.169 | -0.323 | 21 | 14 |
| camarilla pivots:chart · bounce-touch | both | 12 | -0.177 | -0.170 | 0 | 831 |
| traditional pivots:chart · bounce-rejection | shorts | 12 | -0.179 | -0.068 | 25 | 48 |
| traditional pivots:W · bounce-touch | longs | 24 | -0.179 | -0.157 | 42 | 23 |
| traditional pivots:M · bounce-touch | both | 24 | -0.183 | -0.114 | 33 | 15 |
| traditional pivots:M · bounce-rejection | both | 24 | -0.190 | -0.182 | 17 | 8 |
| traditional pivots:W · bounce-rejection | shorts | 24 | -0.194 | -0.128 | 38 | 20 |
| woodie pivots:M · bounce-rejection | longs | 8 | -0.198 | -0.041 | 38 | 10 |
| woodie pivots:W · bounce-touch | longs | 24 | -0.202 | -0.183 | 42 | 25 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.205 | -0.152 | 0 | 222 |
| camarilla pivots:M · bounce-touch | both | 24 | -0.207 | -0.154 | 4 | 58 |
| woodie pivots:M · bounce-rejection | both | 16 | -0.207 | +0.004 | 50 | 12 |
| woodie pivots:M · breakout | shorts | 8 | -0.210 | +0.286 | 100 | 8 |
| fibonacci pivots:W · bounce-touch | longs | 24 | -0.216 | -0.072 | 21 | 57 |
| traditional pivots:M · bounce-touch | shorts | 24 | -0.216 | -0.394 | 21 | 9 |
| fibonacci pivots:M · bounce-rejection | both | 24 | -0.219 | -0.103 | 29 | 18 |
| traditional pivots:W · bounce-touch | both | 24 | -0.258 | -0.104 | 62 | 58 |
| woodie pivots:M · bounce-rejection | shorts | 8 | -0.260 | +0.132 | 50 | 8 |
| woodie pivots:chart · bounce-touch | both | 12 | -0.263 | -0.218 | 0 | 342 |
| woodie pivots:W · bounce-touch | both | 24 | -0.266 | -0.193 | 29 | 57 |
| traditional pivots:chart · bounce-touch | both | 12 | -0.268 | -0.210 | 0 | 350 |
| camarilla pivots:M · bounce-touch | shorts | 24 | -0.268 | -0.320 | 0 | 34 |
| fibonacci pivots:chart · bounce-touch | both | 12 | -0.280 | -0.233 | 0 | 540 |
| traditional pivots:M · bounce-rejection | shorts | 8 | -0.281 | -0.002 | 38 | 11 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.301 | -0.203 | 4 | 111 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.306 | -0.060 | 33 | 126 |
| traditional pivots:M · bounce-touch | longs | 8 | -0.310 | -0.231 | 25 | 12 |
| traditional pivots:W · bounce-touch | shorts | 24 | -0.315 | -0.074 | 58 | 35 |
| fibonacci pivots:M · bounce-touch | longs | 16 | -0.319 | -0.054 | 38 | 14 |
| woodie pivots:W · bounce-touch | shorts | 24 | -0.325 | -0.225 | 21 | 32 |
| traditional pivots:M · bounce-rejection | longs | 8 | -0.358 | -0.750 | 0 | 6 |
| woodie pivots:chart · bounce-touch | shorts | 12 | -0.370 | -0.322 | 0 | 157 |
| traditional pivots:chart · bounce-touch | shorts | 12 | -0.374 | -0.272 | 0 | 166 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.378 | -0.056 | 38 | 69 |
| woodie pivots:M · bounce-touch | both | 24 | -0.400 | -0.286 | 0 | 14 |
| fibonacci pivots:chart · bounce-touch | shorts | 12 | -0.410 | -0.360 | 0 | 256 |
| woodie pivots:M · bounce-touch | shorts | 24 | -0.415 | -0.321 | 12 | 8 |
| fibonacci pivots:M · bounce-touch | both | 24 | -0.426 | -0.076 | 33 | 29 |
| woodie pivots:M · bounce-touch | longs | 8 | -0.456 | -0.222 | 0 | 13 |
| fibonacci pivots:M · bounce-touch | shorts | 24 | -0.460 | -0.167 | 33 | 19 |
| camarilla pivots:chart · bounce-touch | shorts | 12 | -0.547 | -0.539 | 0 | 248 |

