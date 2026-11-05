# XRP strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase XRP-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | traditional pivots:D · breakout (shorts) | -0.006 | -0.179 | 0 | traditional pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | 139 | -0.111 | +0.002 |
| 1h | Pivot Points | traditional pivots:D · breakout (shorts) | +0.090 | -0.103 | 31 | traditional pivots:D breakout level2 stop1ATR target:next exitAtPeriodEnd:no | 40 | +0.048 | +0.090 |
| 4h | Pivot Points | camarilla pivots:W · breakout (shorts) | +0.145 | +0.074 | 68 | camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | 28 | -0.037 | +0.113 |
| 1d | Pivot Points | traditional pivots:chart · breakout (shorts) | +0.272 | +0.031 | 50 | traditional pivots:chart breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | 5 | -0.350 | +0.123 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | shorts | 247 | +0.242 | 137 | -0.160 | +0.031 | -0.191 | -0.123 | +0.42 |
| 1h | Pivot Points | traditional pivots:D breakout level2 stop1ATR target:next exitAtPeriodEnd:no | shorts | 91 | +0.316 | 40 | +0.048 | +0.090 | -0.043 | +0.006 | +0.24 |
| 4h | Pivot Points | traditional pivots:D breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | shorts | 64 | +0.394 | 32 | +0.002 | +0.076 | -0.074 | +0.067 | +0.32 |
| 1d | Pivot Points | camarilla pivots:W bounce-rejection level3 stop1ATR target:next exitAtPeriodEnd:no | longs | 17 | +0.100 | 12 | +0.103 | -0.141 | +0.244 | +0.137 | +0.26 |


## 15-minute  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +171%, OOS -42%)

### Pivot Points

576 settings × 3 sides tested; 762 combinations had ≥120 IS trades, 7% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.42. Average OOS result of the top-20 IS picks: -0.123 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.031 R/trade over 137 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | shorts | 247 | +0.242 | 2.52 | 137 | -0.160 | -22.0 | 31 |
| traditional pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 261 | +0.152 | 1.72 | 139 | -0.111 | -15.5 | 35 |
| woodie pivots:D breakout level1 stop1ATR target:next exitAtPeriodEnd:no | shorts | 248 | +0.199 | 1.69 | 138 | -0.084 | -11.6 | 36 |
| traditional pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | shorts | 241 | +0.162 | 1.68 | 139 | -0.106 | -14.7 | 33 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 270 | +0.145 | 1.67 | 139 | -0.184 | -25.6 | 33 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:D · breakout | shorts | 12 | -0.006 | -0.179 | 0 | 139 |
| woodie pivots:D · breakout | shorts | 16 | -0.026 | -0.270 | 0 | 94 |
| woodie pivots:D · bounce-rejection | shorts | 8 | -0.049 | +0.204 | 100 | 110 |
| fibonacci pivots:D · breakout | shorts | 20 | -0.075 | -0.184 | 5 | 124 |
| traditional pivots:D · bounce-rejection | both | 18 | -0.086 | -0.208 | 6 | 105 |
| traditional pivots:D · bounce-rejection | shorts | 8 | -0.091 | -0.083 | 0 | 102 |
| woodie pivots:D · bounce-rejection | both | 16 | -0.097 | -0.121 | 19 | 170 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.100 | -0.126 | 12 | 168 |
| traditional pivots:D · bounce-rejection | longs | 16 | -0.104 | -0.215 | 19 | 92 |
| fibonacci pivots:W · bounce-touch | both | 8 | -0.104 | -0.366 | 25 | 50 |
| traditional pivots:D · breakout | both | 16 | -0.110 | -0.135 | 0 | 174 |
| woodie pivots:D · breakout | both | 16 | -0.110 | -0.221 | 0 | 172 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.117 | -0.055 | 17 | 64 |
| fibonacci pivots:D · breakout | both | 24 | -0.126 | -0.139 | 0 | 216 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.127 | -0.175 | 0 | 364 |
| fibonacci pivots:D · bounce-rejection | shorts | 16 | -0.128 | -0.136 | 0 | 108 |
| camarilla pivots:W · breakout | both | 24 | -0.148 | -0.283 | 8 | 71 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.151 | -0.218 | 0 | 193 |
| woodie pivots:D · breakout | longs | 8 | -0.158 | -0.165 | 0 | 108 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.160 | -0.257 | 0 | 202 |
| woodie pivots:D · bounce-touch | longs | 16 | -0.170 | -0.058 | 31 | 114 |
| camarilla pivots:D · breakout | shorts | 24 | -0.173 | -0.130 | 0 | 242 |
| woodie pivots:D · bounce-rejection | longs | 16 | -0.174 | -0.187 | 0 | 94 |
| traditional pivots:D · breakout | longs | 8 | -0.176 | -0.123 | 0 | 112 |
| fibonacci pivots:D · breakout | longs | 16 | -0.180 | -0.098 | 38 | 118 |
| traditional pivots:D · bounce-touch | both | 24 | -0.187 | -0.325 | 0 | 128 |
| camarilla pivots:D · breakout | both | 24 | -0.196 | -0.194 | 0 | 464 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.211 | -0.266 | 0 | 116 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.217 | -0.233 | 0 | 264 |
| camarilla pivots:D · breakout | longs | 24 | -0.220 | -0.264 | 0 | 221 |
| woodie pivots:D · bounce-touch | both | 24 | -0.223 | -0.247 | 8 | 125 |
| traditional pivots:D · bounce-touch | longs | 16 | -0.223 | -0.231 | 0 | 120 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.231 | -0.247 | 0 | 498 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.247 | -0.264 | 0 | 234 |
| woodie pivots:D · bounce-touch | shorts | 16 | -0.265 | -0.238 | 12 | 98 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.278 | -0.018 | 25 | 70 |
| traditional pivots:D · bounce-touch | shorts | 16 | -0.287 | -0.322 | 0 | 98 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.318 | -0.300 | 0 | 147 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.353 | -0.310 | 0 | 257 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.386 | -0.318 | 0 | 110 |


## 1-hour  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +185%, OOS -42%)

### Pivot Points

576 settings × 3 sides tested; 986 combinations had ≥80 IS trades, 13% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.24. Average OOS result of the top-20 IS picks: +0.006 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.090 R/trade over 40 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| traditional pivots:D breakout level2 stop1ATR target:next exitAtPeriodEnd:no | shorts | 91 | +0.316 | 2.84 | 40 | +0.048 | +1.9 | 52 |
| traditional pivots:D bounce-touch level3 stop1ATR target:2R exitAtPeriodEnd:no | longs | 81 | +0.318 | 1.83 | 26 | -0.031 | -0.8 | 35 |
| woodie pivots:D breakout level2 stop1ATR target:next exitAtPeriodEnd:no | shorts | 97 | +0.175 | 1.62 | 40 | +0.021 | +0.8 | 50 |
| camarilla pivots:D bounce-rejection level2 stop1ATR target:2R exitAtPeriodEnd:yes | both | 852 | +0.067 | 1.54 | 340 | +0.002 | +0.8 | 41 |
| fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:no | shorts | 90 | +0.237 | 1.50 | 40 | +0.004 | +0.2 | 35 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:D · breakout | shorts | 16 | +0.090 | -0.103 | 31 | 80 |
| woodie pivots:D · breakout | shorts | 16 | +0.060 | -0.060 | 31 | 76 |
| camarilla pivots:W · breakout | shorts | 8 | -0.016 | -0.213 | 0 | 42 |
| traditional pivots:D · breakout | both | 24 | -0.018 | -0.017 | 33 | 87 |
| fibonacci pivots:D · breakout | shorts | 24 | -0.023 | -0.135 | 8 | 106 |
| woodie pivots:D · bounce-rejection | shorts | 11 | -0.027 | +0.008 | 36 | 96 |
| camarilla pivots:D · breakout | shorts | 24 | -0.031 | -0.116 | 12 | 210 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.035 | +0.023 | 54 | 68 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.053 | -0.036 | 42 | 119 |
| camarilla pivots:W · breakout | both | 24 | -0.056 | -0.061 | 42 | 70 |
| woodie pivots:D · breakout | both | 24 | -0.062 | -0.097 | 21 | 84 |
| camarilla pivots:D · breakout | both | 24 | -0.069 | -0.137 | 0 | 392 |
| woodie pivots:D · breakout | longs | 16 | -0.070 | -0.108 | 19 | 66 |
| fibonacci pivots:D · breakout | both | 24 | -0.074 | -0.132 | 0 | 184 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.074 | -0.106 | 4 | 266 |
| woodie pivots:W · breakout | both | 8 | -0.084 | -0.227 | 0 | 38 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.087 | -0.011 | 54 | 60 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.087 | -0.194 | 0 | 254 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.092 | -0.017 | 29 | 82 |
| traditional pivots:W · breakout | both | 8 | -0.094 | -0.253 | 0 | 33 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.094 | -0.167 | 0 | 150 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.096 | -0.105 | 12 | 72 |
| traditional pivots:D · breakout | longs | 16 | -0.100 | -0.131 | 6 | 73 |
| camarilla pivots:W · bounce-touch | longs | 12 | -0.100 | +0.002 | 67 | 40 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.106 | -0.074 | 12 | 85 |
| camarilla pivots:D · breakout | longs | 24 | -0.108 | -0.158 | 0 | 182 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.111 | -0.096 | 19 | 56 |
| traditional pivots:D · bounce-touch | both | 24 | -0.111 | -0.139 | 17 | 128 |
| camarilla pivots:W · bounce-rejection | shorts | 7 | -0.116 | -0.171 | 29 | 35 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.119 | -0.172 | 0 | 478 |
| woodie pivots:D · bounce-touch | both | 24 | -0.120 | -0.163 | 12 | 125 |
| fibonacci pivots:W · breakout | both | 8 | -0.121 | -0.006 | 25 | 46 |
| fibonacci pivots:D · breakout | longs | 24 | -0.123 | -0.127 | 0 | 78 |
| woodie pivots:D · bounce-touch | longs | 16 | -0.124 | -0.004 | 56 | 114 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.129 | -0.153 | 0 | 165 |
| traditional pivots:W · bounce-rejection | both | 4 | -0.136 | -0.152 | 0 | 33 |
| traditional pivots:D · bounce-rejection | longs | 16 | -0.144 | -0.060 | 31 | 76 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.153 | -0.148 | 0 | 224 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.157 | -0.194 | 4 | 93 |
| fibonacci pivots:W · bounce-touch | both | 16 | -0.165 | -0.334 | 0 | 42 |
| woodie pivots:D · bounce-touch | shorts | 16 | -0.170 | -0.152 | 12 | 98 |
| camarilla pivots:W · bounce-touch | shorts | 20 | -0.181 | -0.281 | 10 | 35 |
| traditional pivots:D · bounce-touch | shorts | 16 | -0.183 | -0.124 | 25 | 96 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.186 | -0.021 | 17 | 70 |
| woodie pivots:W · bounce-rejection | both | 8 | -0.189 | -0.392 | 12 | 37 |
| woodie pivots:D · bounce-rejection | longs | 16 | -0.210 | -0.059 | 19 | 70 |
| camarilla pivots:W · breakout | longs | 16 | -0.224 | -0.064 | 31 | 37 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.227 | -0.154 | 33 | 147 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.237 | -0.181 | 12 | 257 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.245 | -0.210 | 8 | 110 |
| camarilla pivots:W · bounce-rejection | longs | 4 | -0.308 | -0.048 | 25 | 36 |
| woodie pivots:W · bounce-touch | both | 8 | -0.320 | -0.330 | 12 | 44 |
| fibonacci pivots:W · bounce-rejection | both | 8 | -0.353 | +0.240 | 100 | 41 |
| traditional pivots:W · bounce-touch | both | 8 | -0.616 | -0.349 | 0 | 40 |


## 4-hour  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +182%, OOS -42%)

### Pivot Points

864 settings × 3 sides tested; 1139 combinations had ≥50 IS trades, 26% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.32. Average OOS result of the top-20 IS picks: +0.067 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.076 R/trade over 32 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| traditional pivots:D breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | shorts | 64 | +0.394 | 2.08 | 32 | +0.002 | +0.1 | 34 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | longs | 75 | +0.361 | 2.06 | 50 | -0.026 | -1.3 | 34 |
| fibonacci pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:no | shorts | 53 | +0.419 | 2.01 | 29 | +0.338 | +9.8 | 45 |
| traditional pivots:D breakout level3 stop1ATR target:2R exitAtPeriodEnd:no | both | 60 | +0.392 | 2.00 | 16 | -0.079 | -1.3 | 31 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 56 | +0.358 | 1.93 | 28 | -0.037 | -1.0 | 39 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| camarilla pivots:W · breakout | shorts | 22 | +0.145 | +0.074 | 68 | 36 |
| woodie pivots:W · breakout | both | 8 | +0.123 | +0.018 | 38 | 32 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.098 | +0.043 | 50 | 75 |
| traditional pivots:D · breakout | shorts | 16 | +0.095 | -0.005 | 38 | 46 |
| woodie pivots:D · breakout | shorts | 16 | +0.086 | +0.055 | 56 | 44 |
| fibonacci pivots:D · breakout | both | 24 | +0.056 | -0.005 | 42 | 123 |
| woodie pivots:W · bounce-rejection | both | 8 | +0.054 | +0.178 | 62 | 34 |
| traditional pivots:D · breakout | both | 24 | +0.048 | +0.022 | 38 | 66 |
| woodie pivots:D · breakout | both | 24 | +0.044 | +0.038 | 58 | 66 |
| camarilla pivots:D · breakout | shorts | 24 | +0.036 | +0.041 | 50 | 132 |
| camarilla pivots:D · breakout | both | 24 | +0.028 | -0.057 | 17 | 242 |
| camarilla pivots:D · breakout | longs | 24 | +0.020 | -0.164 | 0 | 110 |
| fibonacci pivots:D · breakout | longs | 24 | +0.020 | -0.047 | 42 | 53 |
| traditional pivots:W · breakout | both | 8 | -0.009 | -0.068 | 25 | 31 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.017 | +0.047 | 62 | 70 |
| woodie pivots:D · breakout | longs | 16 | -0.028 | -0.057 | 31 | 44 |
| camarilla pivots:W · breakout | both | 24 | -0.029 | +0.010 | 50 | 63 |
| traditional pivots:D · breakout | longs | 16 | -0.034 | -0.084 | 38 | 43 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.036 | -0.052 | 31 | 32 |
| fibonacci pivots:W · breakout | both | 16 | -0.038 | -0.014 | 44 | 36 |
| camarilla pivots:W · bounce-rejection | shorts | 16 | -0.045 | +0.004 | 50 | 24 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.048 | -0.054 | 21 | 159 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.048 | -0.046 | 29 | 68 |
| camarilla pivots:W · bounce-rejection | longs | 15 | -0.050 | -0.141 | 27 | 25 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.052 | -0.042 | 29 | 45 |
| woodie pivots:D · bounce-rejection | shorts | 16 | -0.052 | -0.039 | 44 | 36 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.061 | -0.168 | 0 | 242 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.061 | -0.052 | 38 | 65 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.067 | +0.009 | 58 | 49 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.070 | -0.124 | 0 | 90 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.074 | -0.015 | 46 | 38 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.101 | -0.080 | 8 | 105 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.109 | -0.064 | 8 | 66 |
| traditional pivots:W · bounce-rejection | both | 8 | -0.112 | +0.184 | 100 | 33 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.116 | -0.154 | 0 | 446 |
| fibonacci pivots:W · bounce-rejection | both | 16 | -0.118 | +0.019 | 50 | 33 |
| woodie pivots:D · bounce-touch | both | 24 | -0.123 | -0.127 | 4 | 125 |
| traditional pivots:D · bounce-touch | both | 24 | -0.124 | -0.119 | 4 | 128 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.126 | -0.036 | 29 | 66 |
| traditional pivots:D · bounce-rejection | longs | 19 | -0.126 | -0.095 | 11 | 46 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.130 | -0.142 | 12 | 56 |
| woodie pivots:D · bounce-rejection | longs | 18 | -0.141 | -0.078 | 22 | 46 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.143 | -0.055 | 33 | 70 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.160 | -0.070 | 29 | 147 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.185 | -0.131 | 4 | 257 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.186 | -0.135 | 4 | 206 |
| camarilla pivots:W · breakout | longs | 24 | -0.194 | -0.075 | 29 | 27 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.195 | -0.202 | 0 | 60 |
| fibonacci pivots:W · breakout | longs | 8 | -0.200 | +0.151 | 100 | 17 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.210 | -0.109 | 29 | 32 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.212 | -0.203 | 0 | 110 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.213 | -0.200 | 4 | 60 |
| fibonacci pivots:W · bounce-touch | both | 16 | -0.232 | -0.290 | 0 | 42 |
| fibonacci pivots:W · bounce-touch | longs | 8 | -0.239 | -0.359 | 0 | 29 |
| fibonacci pivots:W · bounce-touch | shorts | 8 | -0.304 | -0.157 | 0 | 21 |
| fibonacci pivots:W · bounce-rejection | longs | 1 | -0.309 | -0.254 | 0 | 23 |
| woodie pivots:W · bounce-touch | shorts | 8 | -0.350 | -0.117 | 50 | 20 |
| woodie pivots:W · bounce-touch | both | 8 | -0.374 | -0.160 | 50 | 44 |
| traditional pivots:W · bounce-touch | both | 8 | -0.474 | -0.343 | 0 | 40 |
| traditional pivots:W · bounce-touch | shorts | 8 | -0.561 | -0.074 | 25 | 17 |


## Daily  (IS 2023-07-14 → 2025-11-07, OOS 2025-11-07 → 2026-11-04; XRP buy & hold: IS +222%, OOS -44%)

### Pivot Points

720 settings × 3 sides tested; 1291 combinations had ≥15 IS trades, 34% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.26. Average OOS result of the top-20 IS picks: +0.137 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.141 R/trade over 12 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| camarilla pivots:W bounce-rejection level3 stop1ATR target:next exitAtPeriodEnd:no | longs | 17 | +0.100 | 6.02 | 12 | +0.103 | +1.2 | 100 |
| camarilla pivots:W bounce-rejection level3 stop1ATR target:next exitAtPeriodEnd:yes | longs | 17 | +0.091 | 5.07 | 12 | +0.091 | +1.1 | 92 |
| woodie pivots:W bounce-rejection level1 stop1ATR target:2R exitAtPeriodEnd:no | shorts | 18 | +1.056 | 3.05 | 5 | +0.840 | +4.2 | 60 |
| woodie pivots:W bounce-rejection level1 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 29 | +0.531 | 2.77 | 10 | +0.430 | +4.3 | 70 |
| woodie pivots:chart breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | both | 42 | +0.585 | 2.48 | 15 | -0.416 | -6.2 | 20 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| traditional pivots:chart · breakout | shorts | 10 | +0.272 | +0.031 | 50 | 7 |
| woodie pivots:W · bounce-rejection | shorts | 12 | +0.264 | +0.653 | 100 | 10 |
| woodie pivots:chart · breakout | shorts | 10 | +0.263 | -0.026 | 30 | 7 |
| fibonacci pivots:M · breakout | both | 8 | +0.240 | -0.069 | 38 | 8 |
| fibonacci pivots:chart · breakout | shorts | 12 | +0.213 | -0.112 | 33 | 8 |
| camarilla pivots:chart · breakout | shorts | 8 | +0.209 | +0.207 | 88 | 10 |
| camarilla pivots:chart · breakout | both | 12 | +0.188 | +0.122 | 67 | 14 |
| camarilla pivots:chart · breakout | longs | 12 | +0.186 | +0.059 | 33 | 6 |
| traditional pivots:W · breakout | shorts | 8 | +0.185 | -0.038 | 50 | 13 |
| fibonacci pivots:chart · breakout | both | 12 | +0.176 | -0.126 | 33 | 18 |
| traditional pivots:chart · breakout | both | 12 | +0.172 | -0.072 | 25 | 18 |
| fibonacci pivots:W · bounce-rejection | shorts | 16 | +0.153 | +0.555 | 88 | 6 |
| woodie pivots:chart · breakout | both | 12 | +0.149 | -0.160 | 33 | 16 |
| fibonacci pivots:chart · breakout | longs | 12 | +0.147 | -0.079 | 50 | 12 |
| camarilla pivots:W · breakout | shorts | 24 | +0.141 | +0.017 | 62 | 20 |
| traditional pivots:chart · breakout | longs | 12 | +0.102 | -0.181 | 33 | 9 |
| camarilla pivots:M · breakout | both | 24 | +0.099 | +0.070 | 58 | 12 |
| woodie pivots:chart · breakout | longs | 12 | +0.090 | -0.175 | 17 | 10 |
| woodie pivots:W · breakout | shorts | 8 | +0.077 | +0.157 | 75 | 10 |
| woodie pivots:M · bounce-rejection | both | 8 | +0.070 | -0.220 | 25 | 8 |
| camarilla pivots:M · breakout | shorts | 8 | +0.051 | +0.269 | 88 | 6 |
| woodie pivots:W · bounce-rejection | both | 16 | +0.047 | +0.156 | 88 | 16 |
| camarilla pivots:W · bounce-rejection | shorts | 22 | +0.043 | +0.079 | 59 | 10 |
| camarilla pivots:M · breakout | longs | 21 | +0.028 | -0.014 | 38 | 6 |
| fibonacci pivots:W · breakout | shorts | 15 | +0.019 | +0.112 | 80 | 12 |
| traditional pivots:W · breakout | longs | 8 | +0.007 | +0.168 | 75 | 12 |
| camarilla pivots:W · breakout | both | 24 | +0.004 | -0.190 | 12 | 37 |
| fibonacci pivots:W · bounce-rejection | both | 24 | +0.001 | +0.219 | 62 | 18 |
| traditional pivots:M · bounce-touch | both | 8 | +0.000 | +0.071 | 38 | 10 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.020 | -0.142 | 17 | 22 |
| camarilla pivots:M · bounce-rejection | both | 24 | -0.027 | -0.039 | 42 | 11 |
| woodie pivots:chart · bounce-rejection | shorts | 11 | -0.031 | +0.249 | 64 | 10 |
| traditional pivots:W · bounce-rejection | shorts | 7 | -0.039 | +0.343 | 100 | 9 |
| fibonacci pivots:chart · bounce-rejection | shorts | 11 | -0.043 | +0.319 | 45 | 11 |
| camarilla pivots:chart · bounce-rejection | shorts | 9 | -0.044 | -0.045 | 33 | 18 |
| traditional pivots:W · breakout | both | 16 | -0.047 | +0.228 | 75 | 10 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.052 | -0.198 | 12 | 36 |
| fibonacci pivots:M · bounce-rejection | both | 11 | -0.054 | -0.076 | 27 | 9 |
| camarilla pivots:chart · bounce-touch | longs | 12 | -0.057 | -0.229 | 0 | 184 |
| traditional pivots:chart · bounce-rejection | both | 12 | -0.058 | -0.108 | 17 | 18 |
| traditional pivots:W · bounce-rejection | both | 16 | -0.058 | +0.208 | 75 | 10 |
| woodie pivots:M · breakout | both | 8 | -0.062 | +1.493 | 100 | 4 |
| traditional pivots:chart · bounce-rejection | shorts | 10 | -0.067 | +0.190 | 40 | 10 |
| woodie pivots:chart · bounce-rejection | both | 12 | -0.070 | -0.157 | 17 | 19 |
| camarilla pivots:M · bounce-rejection | shorts | 6 | -0.075 | +0.305 | 67 | 7 |
| woodie pivots:W · breakout | longs | 8 | -0.077 | +0.047 | 62 | 11 |
| traditional pivots:chart · bounce-rejection | longs | 12 | -0.084 | -0.281 | 0 | 12 |
| fibonacci pivots:chart · bounce-rejection | both | 12 | -0.084 | -0.087 | 17 | 30 |
| camarilla pivots:W · bounce-rejection | longs | 23 | -0.086 | -0.339 | 9 | 16 |
| woodie pivots:chart · bounce-touch | longs | 12 | -0.092 | -0.242 | 0 | 46 |
| camarilla pivots:M · bounce-touch | longs | 24 | -0.095 | -0.252 | 0 | 9 |
| woodie pivots:chart · bounce-rejection | longs | 12 | -0.095 | -0.283 | 8 | 12 |
| traditional pivots:chart · bounce-touch | longs | 12 | -0.096 | -0.184 | 0 | 52 |
| traditional pivots:M · bounce-rejection | both | 8 | -0.097 | -0.350 | 12 | 6 |
| camarilla pivots:chart · bounce-rejection | both | 12 | -0.097 | -0.171 | 8 | 34 |
| fibonacci pivots:W · breakout | longs | 16 | -0.101 | -0.167 | 25 | 7 |
| fibonacci pivots:W · breakout | both | 24 | -0.103 | +0.141 | 54 | 13 |
| woodie pivots:W · breakout | both | 16 | -0.104 | +0.517 | 88 | 8 |
| camarilla pivots:W · breakout | longs | 24 | -0.114 | -0.433 | 0 | 17 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.117 | -0.195 | 8 | 64 |
| traditional pivots:W · bounce-touch | both | 24 | -0.119 | +0.078 | 54 | 17 |
| woodie pivots:W · bounce-touch | shorts | 16 | -0.120 | +0.129 | 69 | 10 |
| fibonacci pivots:chart · bounce-rejection | longs | 12 | -0.123 | -0.306 | 0 | 24 |
| camarilla pivots:chart · bounce-rejection | longs | 11 | -0.138 | -0.260 | 9 | 20 |
| traditional pivots:M · breakout | both | 8 | -0.147 | +0.653 | 100 | 6 |
| camarilla pivots:chart · bounce-touch | both | 12 | -0.152 | -0.254 | 0 | 238 |
| fibonacci pivots:W · bounce-rejection | longs | 15 | -0.154 | -0.244 | 7 | 15 |
| fibonacci pivots:M · bounce-touch | both | 16 | -0.155 | -0.057 | 25 | 11 |
| fibonacci pivots:W · bounce-touch | longs | 24 | -0.166 | -0.116 | 25 | 21 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.172 | -0.087 | 29 | 34 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.180 | -0.042 | 17 | 13 |
| camarilla pivots:M · bounce-touch | both | 24 | -0.187 | -0.296 | 25 | 14 |
| fibonacci pivots:chart · bounce-touch | longs | 12 | -0.187 | -0.200 | 0 | 86 |
| camarilla pivots:M · bounce-rejection | longs | 3 | -0.188 | -0.692 | 0 | 8 |
| traditional pivots:chart · bounce-touch | both | 12 | -0.193 | -0.156 | 8 | 88 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.198 | -0.192 | 17 | 28 |
| woodie pivots:chart · bounce-touch | both | 12 | -0.201 | -0.202 | 0 | 78 |
| woodie pivots:W · bounce-touch | both | 24 | -0.232 | +0.107 | 71 | 18 |
| fibonacci pivots:chart · bounce-touch | both | 12 | -0.237 | -0.217 | 0 | 140 |
| traditional pivots:W · bounce-touch | longs | 16 | -0.240 | -0.068 | 31 | 15 |
| traditional pivots:W · bounce-touch | shorts | 16 | -0.241 | +0.143 | 69 | 10 |
| traditional pivots:W · bounce-rejection | longs | 8 | -0.249 | -0.175 | 12 | 16 |
| woodie pivots:W · bounce-rejection | longs | 8 | -0.254 | -0.145 | 12 | 18 |
| woodie pivots:M · bounce-touch | both | 8 | -0.297 | -0.125 | 62 | 10 |
| fibonacci pivots:chart · bounce-touch | shorts | 12 | -0.300 | -0.247 | 0 | 56 |
| camarilla pivots:M · bounce-touch | shorts | 20 | -0.304 | -0.513 | 20 | 7 |
| traditional pivots:chart · bounce-touch | shorts | 12 | -0.308 | -0.127 | 17 | 38 |
| woodie pivots:chart · bounce-touch | shorts | 12 | -0.332 | -0.162 | 8 | 37 |
| woodie pivots:W · bounce-touch | longs | 16 | -0.405 | +0.202 | 62 | 14 |
| camarilla pivots:chart · bounce-touch | shorts | 12 | -0.462 | -0.347 | 8 | 58 |

