# AVAX strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase AVAX-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | woodie pivots:W · breakout (both) | +0.404 | -0.379 | 0 | woodie pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | 63 | -0.635 | +0.118 |
| 1h | Pivot Points | fibonacci pivots:W · breakout (longs) | +0.262 | +0.041 | 62 | fibonacci pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | 35 | +0.138 | -0.143 |
| 4h | Pivot Points | woodie pivots:W · breakout (shorts) | +0.443 | -0.092 | 25 | woodie pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | 31 | -0.106 | +0.100 |
| 1d | Pivot Points | woodie pivots:M · breakout (both) | +0.330 | +0.149 | 50 | woodie pivots:M breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | 10 | -0.071 | +0.114 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Pivot Points | fibonacci pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | both | 186 | +0.311 | 77 | +0.135 | -0.016 | +0.151 | -0.197 | +0.37 |
| 1h | Pivot Points | fibonacci pivots:D breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 156 | +0.239 | 74 | +0.066 | +0.014 | +0.052 | +0.101 | +0.37 |
| 4h | Pivot Points | traditional pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:no | both | 51 | +0.567 | 14 | +0.203 | -0.053 | +0.256 | +0.003 | +0.26 |
| 1d | Pivot Points | fibonacci pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:yes | shorts | 37 | +0.211 | 14 | +0.026 | -0.003 | +0.029 | +0.041 | +0.10 |


## 15-minute  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Pivot Points

576 settings × 3 sides tested; 1008 combinations had ≥120 IS trades, 10% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.37. Average OOS result of the top-20 IS picks: -0.197 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.016 R/trade over 77 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | both | 186 | +0.311 | 1.88 | 77 | +0.135 | +10.4 | 38 |
| fibonacci pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no | both | 185 | +0.311 | 1.87 | 77 | +0.135 | +10.4 | 38 |
| woodie pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | both | 135 | +0.549 | 1.81 | 63 | -0.635 | -40.0 | 14 |
| woodie pivots:W breakout level1 stop0.5ATR target:next exitAtPeriodEnd:no | both | 135 | +0.723 | 1.80 | 63 | -0.637 | -40.1 | 11 |
| woodie pivots:W breakout level1 stop0.5ATR target:next exitAtPeriodEnd:yes | both | 135 | +0.699 | 1.75 | 63 | -0.722 | -45.5 | 11 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| woodie pivots:W · breakout | both | 8 | +0.404 | -0.379 | 0 | 63 |
| fibonacci pivots:W · breakout | both | 8 | +0.101 | +0.058 | 75 | 77 |
| camarilla pivots:W · bounce-rejection | shorts | 12 | +0.080 | -0.218 | 17 | 51 |
| camarilla pivots:W · breakout | longs | 16 | +0.017 | +0.002 | 25 | 60 |
| traditional pivots:D · breakout | shorts | 16 | -0.024 | +0.052 | 69 | 146 |
| woodie pivots:D · breakout | shorts | 16 | -0.044 | -0.016 | 44 | 143 |
| woodie pivots:W · bounce-rejection | both | 8 | -0.045 | +0.307 | 100 | 57 |
| fibonacci pivots:D · breakout | longs | 24 | -0.051 | -0.068 | 33 | 164 |
| fibonacci pivots:D · breakout | both | 24 | -0.067 | -0.042 | 29 | 338 |
| traditional pivots:D · breakout | longs | 16 | -0.069 | -0.036 | 50 | 139 |
| woodie pivots:D · breakout | both | 24 | -0.071 | -0.043 | 33 | 158 |
| traditional pivots:D · breakout | both | 24 | -0.071 | -0.064 | 38 | 167 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.073 | -0.150 | 17 | 101 |
| camarilla pivots:W · breakout | both | 24 | -0.077 | -0.009 | 42 | 112 |
| fibonacci pivots:D · breakout | shorts | 24 | -0.083 | -0.014 | 58 | 174 |
| woodie pivots:D · breakout | longs | 16 | -0.085 | +0.034 | 50 | 133 |
| traditional pivots:W · bounce-rejection | both | 8 | -0.107 | +0.098 | 75 | 56 |
| camarilla pivots:D · breakout | shorts | 24 | -0.111 | -0.111 | 0 | 392 |
| camarilla pivots:W · bounce-touch | shorts | 12 | -0.119 | -0.326 | 0 | 57 |
| camarilla pivots:D · breakout | both | 24 | -0.119 | -0.118 | 0 | 748 |
| woodie pivots:D · bounce-rejection | shorts | 16 | -0.122 | -0.003 | 38 | 122 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.122 | -0.092 | 17 | 266 |
| camarilla pivots:D · breakout | longs | 24 | -0.126 | -0.125 | 0 | 356 |
| traditional pivots:D · bounce-rejection | longs | 16 | -0.128 | -0.128 | 6 | 120 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.133 | +0.147 | 75 | 128 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.136 | -0.142 | 12 | 136 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.140 | -0.140 | 0 | 552 |
| woodie pivots:D · bounce-rejection | longs | 16 | -0.147 | -0.069 | 31 | 125 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.151 | -0.077 | 25 | 268 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.155 | -0.047 | 17 | 141 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.156 | -0.187 | 0 | 285 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.166 | -0.011 | 38 | 133 |
| woodie pivots:D · bounce-touch | both | 24 | -0.171 | -0.222 | 17 | 196 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.174 | -0.066 | 38 | 138 |
| woodie pivots:W · bounce-touch | both | 8 | -0.194 | -0.187 | 38 | 68 |
| traditional pivots:D · bounce-touch | shorts | 16 | -0.195 | -0.206 | 12 | 162 |
| fibonacci pivots:W · bounce-rejection | both | 8 | -0.203 | -0.036 | 38 | 75 |
| traditional pivots:D · bounce-touch | both | 24 | -0.212 | -0.230 | 8 | 198 |
| camarilla pivots:W · bounce-rejection | longs | 12 | -0.227 | -0.077 | 50 | 56 |
| woodie pivots:D · bounce-touch | shorts | 16 | -0.228 | -0.290 | 0 | 162 |
| camarilla pivots:W · breakout | shorts | 16 | -0.230 | +0.029 | 62 | 63 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.238 | -0.365 | 0 | 191 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.248 | -0.332 | 0 | 402 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.254 | -0.308 | 0 | 776 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.256 | -0.352 | 0 | 404 |
| woodie pivots:D · bounce-touch | longs | 16 | -0.258 | -0.315 | 0 | 171 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.260 | -0.282 | 8 | 374 |
| traditional pivots:W · bounce-touch | both | 8 | -0.262 | -0.479 | 0 | 65 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.274 | -0.203 | 8 | 112 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.275 | -0.339 | 0 | 213 |
| traditional pivots:D · bounce-touch | longs | 16 | -0.282 | -0.412 | 0 | 172 |
| traditional pivots:W · breakout | both | 8 | -0.308 | -0.181 | 0 | 58 |
| camarilla pivots:W · bounce-touch | longs | 20 | -0.407 | -0.175 | 10 | 62 |
| fibonacci pivots:W · bounce-touch | both | 16 | -0.424 | +0.179 | 75 | 72 |


## 1-hour  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Pivot Points

576 settings × 3 sides tested; 1140 combinations had ≥80 IS trades, 22% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.37. Average OOS result of the top-20 IS picks: +0.101 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.014 R/trade over 74 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:D breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 156 | +0.239 | 2.71 | 74 | +0.066 | +4.9 | 41 |
| camarilla pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no | longs | 142 | +0.207 | 2.68 | 61 | -0.042 | -2.6 | 57 |
| camarilla pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:yes | longs | 143 | +0.198 | 2.56 | 61 | -0.042 | -2.6 | 57 |
| woodie pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | shorts | 147 | +0.303 | 2.44 | 66 | +0.059 | +3.9 | 36 |
| woodie pivots:D breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | shorts | 150 | +0.217 | 2.38 | 66 | +0.017 | +1.1 | 41 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fibonacci pivots:W · breakout | longs | 8 | +0.262 | +0.041 | 62 | 35 |
| fibonacci pivots:W · breakout | shorts | 8 | +0.145 | +0.282 | 100 | 43 |
| traditional pivots:D · breakout | shorts | 16 | +0.103 | +0.040 | 56 | 120 |
| woodie pivots:W · breakout | both | 8 | +0.079 | -0.197 | 0 | 63 |
| woodie pivots:D · breakout | shorts | 16 | +0.075 | -0.014 | 44 | 116 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.067 | -0.021 | 38 | 156 |
| traditional pivots:D · breakout | both | 24 | +0.042 | +0.062 | 67 | 144 |
| woodie pivots:D · breakout | both | 24 | +0.035 | +0.071 | 67 | 136 |
| fibonacci pivots:W · breakout | both | 16 | +0.033 | -0.007 | 50 | 62 |
| camarilla pivots:W · bounce-rejection | shorts | 20 | +0.033 | -0.090 | 20 | 43 |
| fibonacci pivots:D · breakout | both | 24 | +0.019 | -0.058 | 33 | 289 |
| traditional pivots:W · breakout | both | 8 | -0.007 | -0.284 | 0 | 58 |
| camarilla pivots:D · breakout | shorts | 24 | -0.011 | -0.041 | 12 | 308 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.011 | +0.054 | 75 | 101 |
| fibonacci pivots:D · breakout | longs | 24 | -0.025 | -0.095 | 21 | 133 |
| camarilla pivots:W · breakout | longs | 24 | -0.028 | -0.155 | 0 | 52 |
| camarilla pivots:W · breakout | both | 24 | -0.039 | -0.103 | 17 | 107 |
| camarilla pivots:D · breakout | both | 24 | -0.040 | -0.063 | 0 | 597 |
| camarilla pivots:W · breakout | shorts | 24 | -0.049 | -0.054 | 33 | 55 |
| woodie pivots:D · bounce-rejection | shorts | 16 | -0.050 | +0.141 | 50 | 92 |
| traditional pivots:W · bounce-touch | both | 8 | -0.052 | -0.284 | 38 | 65 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.058 | -0.068 | 12 | 191 |
| traditional pivots:D · breakout | longs | 16 | -0.061 | -0.034 | 38 | 114 |
| traditional pivots:W · bounce-rejection | both | 8 | -0.062 | +0.223 | 50 | 51 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.064 | -0.111 | 17 | 89 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.067 | +0.014 | 58 | 115 |
| camarilla pivots:D · breakout | longs | 24 | -0.069 | -0.087 | 0 | 290 |
| traditional pivots:D · bounce-rejection | longs | 16 | -0.073 | -0.076 | 12 | 104 |
| woodie pivots:D · breakout | longs | 16 | -0.076 | +0.027 | 50 | 114 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.078 | -0.059 | 25 | 234 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.085 | -0.117 | 8 | 393 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.086 | -0.127 | 4 | 122 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.091 | -0.020 | 42 | 119 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.109 | -0.162 | 0 | 202 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.120 | -0.021 | 29 | 112 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.125 | -0.057 | 33 | 91 |
| woodie pivots:D · bounce-rejection | longs | 16 | -0.129 | -0.109 | 6 | 100 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.135 | -0.149 | 17 | 53 |
| camarilla pivots:W · bounce-rejection | longs | 24 | -0.144 | -0.165 | 12 | 47 |
| woodie pivots:W · bounce-touch | both | 8 | -0.144 | +0.061 | 50 | 68 |
| traditional pivots:D · bounce-touch | shorts | 16 | -0.147 | -0.105 | 31 | 162 |
| woodie pivots:W · bounce-rejection | both | 8 | -0.153 | +0.223 | 75 | 54 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.154 | -0.177 | 0 | 389 |
| woodie pivots:D · bounce-touch | both | 24 | -0.165 | -0.122 | 12 | 196 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.166 | -0.183 | 0 | 748 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.177 | -0.204 | 0 | 404 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.177 | -0.199 | 0 | 213 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.177 | -0.212 | 4 | 191 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.178 | -0.188 | 0 | 360 |
| traditional pivots:D · bounce-touch | both | 24 | -0.185 | -0.141 | 21 | 198 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.192 | -0.219 | 0 | 107 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.195 | -0.093 | 17 | 112 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.201 | -0.192 | 0 | 105 |
| fibonacci pivots:W · bounce-rejection | both | 16 | -0.220 | +0.200 | 94 | 58 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.247 | -0.039 | 33 | 58 |
| fibonacci pivots:W · bounce-touch | longs | 8 | -0.255 | -0.131 | 25 | 47 |
| fibonacci pivots:W · bounce-touch | both | 16 | -0.286 | +0.128 | 69 | 72 |
| fibonacci pivots:W · bounce-touch | shorts | 8 | -0.321 | +0.135 | 100 | 41 |
| fibonacci pivots:W · bounce-rejection | longs | 8 | -0.364 | +0.074 | 75 | 34 |


## 4-hour  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Pivot Points

864 settings × 3 sides tested; 1387 combinations had ≥50 IS trades, 35% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.26. Average OOS result of the top-20 IS picks: +0.003 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.053 R/trade over 14 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| traditional pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:no | both | 51 | +0.567 | 3.05 | 14 | +0.203 | +2.8 | 57 |
| camarilla pivots:W bounce-rejection level2 stop0.5ATR target:2R exitAtPeriodEnd:yes | both | 206 | +0.296 | 2.90 | 86 | -0.249 | -21.4 | 28 |
| camarilla pivots:W bounce-rejection level2 stop0.5ATR target:2R exitAtPeriodEnd:no | both | 205 | +0.276 | 2.64 | 85 | -0.228 | -19.4 | 27 |
| fibonacci pivots:D breakout level3 stop0.5ATR target:2R exitAtPeriodEnd:yes | shorts | 130 | +0.215 | 2.63 | 60 | +0.135 | +8.1 | 37 |
| fibonacci pivots:D breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | shorts | 206 | +0.269 | 2.58 | 102 | -0.135 | -13.8 | 29 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| woodie pivots:W · breakout | shorts | 8 | +0.443 | -0.092 | 25 | 31 |
| fibonacci pivots:W · breakout | shorts | 8 | +0.302 | +0.098 | 62 | 38 |
| traditional pivots:W · breakout | both | 16 | +0.229 | +0.091 | 69 | 33 |
| woodie pivots:W · breakout | both | 16 | +0.215 | +0.222 | 62 | 33 |
| camarilla pivots:M · breakout | both | 16 | +0.204 | -0.117 | 50 | 26 |
| traditional pivots:W · breakout | shorts | 7 | +0.197 | -0.303 | 0 | 32 |
| fibonacci pivots:D · breakout | shorts | 24 | +0.143 | +0.004 | 50 | 104 |
| traditional pivots:D · breakout | shorts | 22 | +0.134 | +0.018 | 45 | 60 |
| fibonacci pivots:W · breakout | both | 24 | +0.130 | +0.138 | 75 | 35 |
| camarilla pivots:W · breakout | shorts | 24 | +0.109 | +0.078 | 67 | 52 |
| woodie pivots:D · breakout | shorts | 16 | +0.106 | +0.036 | 69 | 66 |
| woodie pivots:W · breakout | longs | 8 | +0.099 | +0.173 | 100 | 21 |
| traditional pivots:D · breakout | both | 24 | +0.089 | +0.026 | 54 | 116 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | +0.082 | -0.011 | 54 | 35 |
| fibonacci pivots:D · breakout | both | 24 | +0.072 | -0.045 | 17 | 186 |
| traditional pivots:W · bounce-rejection | shorts | 8 | +0.049 | +0.535 | 100 | 19 |
| camarilla pivots:W · bounce-rejection | both | 24 | +0.046 | -0.044 | 33 | 71 |
| woodie pivots:D · breakout | both | 24 | +0.045 | +0.059 | 42 | 106 |
| woodie pivots:W · bounce-touch | both | 16 | +0.038 | +0.072 | 62 | 44 |
| traditional pivots:W · breakout | longs | 8 | +0.026 | +0.419 | 100 | 21 |
| fibonacci pivots:W · breakout | longs | 16 | +0.023 | +0.191 | 50 | 22 |
| camarilla pivots:D · breakout | shorts | 24 | +0.022 | -0.025 | 25 | 191 |
| camarilla pivots:W · bounce-rejection | longs | 24 | +0.016 | -0.067 | 29 | 35 |
| traditional pivots:D · breakout | longs | 16 | +0.009 | -0.019 | 38 | 62 |
| camarilla pivots:W · breakout | both | 24 | +0.006 | -0.059 | 38 | 101 |
| fibonacci pivots:D · breakout | longs | 24 | +0.005 | -0.091 | 12 | 82 |
| camarilla pivots:M · bounce-rejection | both | 8 | +0.004 | +0.267 | 100 | 24 |
| woodie pivots:D · breakout | longs | 16 | -0.006 | -0.133 | 0 | 64 |
| camarilla pivots:D · breakout | both | 24 | -0.007 | -0.088 | 4 | 374 |
| woodie pivots:D · bounce-rejection | shorts | 16 | -0.008 | -0.026 | 38 | 50 |
| traditional pivots:D · bounce-rejection | shorts | 16 | -0.010 | +0.029 | 69 | 56 |
| fibonacci pivots:D · bounce-rejection | shorts | 24 | -0.035 | +0.019 | 62 | 72 |
| camarilla pivots:D · breakout | longs | 24 | -0.035 | -0.158 | 0 | 184 |
| woodie pivots:W · bounce-touch | shorts | 8 | -0.036 | +0.687 | 100 | 31 |
| camarilla pivots:D · bounce-rejection | shorts | 24 | -0.049 | -0.092 | 0 | 100 |
| traditional pivots:W · bounce-touch | longs | 8 | -0.054 | -0.336 | 0 | 38 |
| fibonacci pivots:D · bounce-rejection | both | 24 | -0.056 | -0.077 | 21 | 148 |
| traditional pivots:W · bounce-touch | both | 16 | -0.060 | +0.044 | 50 | 44 |
| traditional pivots:W · bounce-rejection | both | 8 | -0.062 | +0.136 | 75 | 46 |
| fibonacci pivots:W · bounce-rejection | shorts | 10 | -0.063 | +0.282 | 100 | 32 |
| camarilla pivots:D · bounce-rejection | both | 24 | -0.067 | -0.128 | 0 | 202 |
| traditional pivots:D · bounce-rejection | both | 24 | -0.072 | +0.002 | 33 | 94 |
| fibonacci pivots:D · bounce-rejection | longs | 24 | -0.075 | -0.158 | 4 | 76 |
| camarilla pivots:D · bounce-rejection | longs | 24 | -0.080 | -0.151 | 8 | 112 |
| camarilla pivots:M · bounce-touch | both | 20 | -0.080 | +0.140 | 80 | 25 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.082 | -0.146 | 17 | 53 |
| woodie pivots:D · bounce-rejection | both | 24 | -0.084 | -0.008 | 50 | 89 |
| camarilla pivots:W · breakout | longs | 24 | -0.100 | -0.207 | 8 | 48 |
| woodie pivots:D · bounce-touch | shorts | 24 | -0.100 | -0.031 | 42 | 91 |
| traditional pivots:W · bounce-touch | shorts | 8 | -0.106 | +0.463 | 100 | 27 |
| fibonacci pivots:W · bounce-touch | shorts | 16 | -0.107 | +0.384 | 100 | 32 |
| fibonacci pivots:W · bounce-rejection | both | 16 | -0.110 | +0.015 | 56 | 53 |
| traditional pivots:D · bounce-rejection | longs | 20 | -0.114 | -0.111 | 10 | 64 |
| camarilla pivots:D · bounce-touch | longs | 24 | -0.121 | -0.075 | 4 | 368 |
| traditional pivots:D · bounce-touch | shorts | 24 | -0.124 | -0.009 | 62 | 91 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.125 | -0.089 | 21 | 112 |
| woodie pivots:D · bounce-rejection | longs | 20 | -0.132 | -0.054 | 30 | 58 |
| fibonacci pivots:D · bounce-touch | longs | 24 | -0.140 | -0.138 | 0 | 212 |
| woodie pivots:D · bounce-touch | both | 24 | -0.141 | -0.054 | 33 | 196 |
| fibonacci pivots:D · bounce-touch | both | 24 | -0.146 | -0.139 | 0 | 401 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.148 | +0.080 | 75 | 56 |
| fibonacci pivots:D · bounce-touch | shorts | 24 | -0.152 | -0.145 | 29 | 189 |
| woodie pivots:W · bounce-touch | longs | 8 | -0.154 | -0.256 | 0 | 37 |
| camarilla pivots:D · bounce-touch | both | 24 | -0.160 | -0.135 | 0 | 693 |
| traditional pivots:D · bounce-touch | both | 24 | -0.161 | -0.090 | 17 | 198 |
| fibonacci pivots:W · bounce-rejection | longs | 8 | -0.163 | -0.219 | 0 | 34 |
| traditional pivots:W · bounce-rejection | longs | 8 | -0.165 | -0.134 | 25 | 28 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.166 | -0.036 | 46 | 58 |
| woodie pivots:D · bounce-touch | longs | 24 | -0.177 | -0.084 | 8 | 105 |
| woodie pivots:W · bounce-rejection | shorts | 8 | -0.190 | +0.479 | 100 | 22 |
| traditional pivots:D · bounce-touch | longs | 24 | -0.193 | -0.182 | 0 | 107 |
| camarilla pivots:D · bounce-touch | shorts | 24 | -0.209 | -0.209 | 0 | 322 |
| woodie pivots:W · bounce-rejection | both | 8 | -0.225 | +0.246 | 100 | 52 |
| woodie pivots:W · bounce-rejection | longs | 8 | -0.259 | +0.079 | 62 | 30 |
| fibonacci pivots:W · bounce-touch | longs | 16 | -0.303 | -0.143 | 19 | 40 |


## Daily  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -67%, OOS -61%)

### Pivot Points

720 settings × 3 sides tested; 1593 combinations had ≥15 IS trades, 39% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.10. Average OOS result of the top-20 IS picks: +0.041 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.003 R/trade over 14 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fibonacci pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:yes | shorts | 37 | +0.211 | 4.95 | 14 | +0.026 | +0.4 | 64 |
| fibonacci pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:yes | both | 79 | +0.158 | 3.17 | 25 | +0.099 | +2.5 | 68 |
| fibonacci pivots:chart breakout level1 stop0.5ATR target:next exitAtPeriodEnd:no | both | 132 | +0.374 | 2.98 | 26 | -0.149 | -3.9 | 35 |
| woodie pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | both | 73 | +0.514 | 2.90 | 30 | +0.094 | +2.8 | 37 |
| fibonacci pivots:chart breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | both | 128 | +0.381 | 2.86 | 25 | -0.054 | -1.4 | 32 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| woodie pivots:M · breakout | both | 8 | +0.330 | +0.149 | 50 | 10 |
| camarilla pivots:chart · breakout | longs | 11 | +0.321 | -0.176 | 45 | 8 |
| fibonacci pivots:chart · breakout | shorts | 12 | +0.320 | -0.016 | 42 | 7 |
| fibonacci pivots:chart · breakout | both | 12 | +0.305 | +0.040 | 67 | 13 |
| fibonacci pivots:chart · breakout | longs | 12 | +0.291 | +0.118 | 67 | 8 |
| traditional pivots:M · breakout | both | 6 | +0.257 | +0.175 | 100 | 11 |
| traditional pivots:chart · breakout | shorts | 12 | +0.244 | +0.327 | 58 | 6 |
| woodie pivots:chart · breakout | longs | 12 | +0.235 | +0.591 | 83 | 8 |
| woodie pivots:chart · breakout | both | 12 | +0.230 | +0.442 | 75 | 13 |
| fibonacci pivots:M · breakout | longs | 4 | +0.228 | +0.138 | 75 | 7 |
| woodie pivots:chart · breakout | shorts | 12 | +0.227 | +0.258 | 50 | 6 |
| camarilla pivots:chart · breakout | both | 12 | +0.225 | -0.243 | 25 | 14 |
| traditional pivots:W · breakout | shorts | 13 | +0.216 | -0.146 | 23 | 16 |
| woodie pivots:M · bounce-rejection | both | 8 | +0.206 | -0.034 | 50 | 8 |
| camarilla pivots:W · breakout | shorts | 24 | +0.198 | +0.145 | 75 | 34 |
| traditional pivots:chart · breakout | both | 12 | +0.198 | +0.422 | 83 | 14 |
| woodie pivots:W · breakout | shorts | 14 | +0.177 | -0.206 | 50 | 12 |
| camarilla pivots:chart · breakout | shorts | 12 | +0.161 | -0.295 | 25 | 6 |
| traditional pivots:chart · breakout | longs | 12 | +0.153 | +0.519 | 83 | 8 |
| traditional pivots:W · breakout | longs | 15 | +0.147 | +0.136 | 53 | 8 |
| fibonacci pivots:M · breakout | shorts | 8 | +0.147 | +0.706 | 100 | 6 |
| fibonacci pivots:M · breakout | both | 14 | +0.138 | +0.279 | 79 | 10 |
| woodie pivots:W · breakout | both | 15 | +0.137 | +0.167 | 80 | 25 |
| camarilla pivots:W · breakout | both | 24 | +0.127 | -0.001 | 42 | 63 |
| fibonacci pivots:W · breakout | shorts | 20 | +0.124 | -0.058 | 40 | 14 |
| fibonacci pivots:W · breakout | longs | 22 | +0.122 | +0.323 | 86 | 11 |
| camarilla pivots:M · breakout | longs | 24 | +0.110 | +0.103 | 50 | 10 |
| traditional pivots:M · bounce-touch | longs | 8 | +0.104 | -0.361 | 38 | 6 |
| fibonacci pivots:W · breakout | both | 24 | +0.099 | +0.117 | 71 | 22 |
| traditional pivots:W · breakout | both | 24 | +0.096 | -0.045 | 46 | 10 |
| camarilla pivots:M · breakout | both | 24 | +0.092 | +0.144 | 79 | 18 |
| woodie pivots:M · bounce-touch | longs | 8 | +0.087 | -0.637 | 12 | 5 |
| woodie pivots:M · bounce-touch | both | 16 | +0.080 | -0.572 | 12 | 8 |
| camarilla pivots:M · breakout | shorts | 24 | +0.075 | +0.155 | 75 | 8 |
| woodie pivots:W · breakout | longs | 15 | +0.072 | +0.350 | 93 | 11 |
| camarilla pivots:W · breakout | longs | 24 | +0.057 | -0.164 | 8 | 30 |
| fibonacci pivots:chart · bounce-rejection | longs | 12 | +0.016 | -0.244 | 17 | 33 |
| camarilla pivots:W · bounce-rejection | longs | 24 | +0.012 | -0.108 | 29 | 23 |
| camarilla pivots:M · bounce-rejection | shorts | 12 | +0.006 | -0.246 | 33 | 7 |
| camarilla pivots:W · bounce-touch | longs | 24 | -0.001 | -0.155 | 0 | 54 |
| fibonacci pivots:M · bounce-rejection | both | 16 | -0.007 | -0.040 | 38 | 8 |
| traditional pivots:M · bounce-touch | both | 16 | -0.012 | -0.416 | 19 | 8 |
| fibonacci pivots:chart · bounce-rejection | both | 12 | -0.032 | -0.154 | 17 | 58 |
| traditional pivots:chart · bounce-rejection | longs | 12 | -0.032 | -0.079 | 33 | 26 |
| woodie pivots:W · bounce-touch | longs | 16 | -0.044 | -0.039 | 38 | 18 |
| camarilla pivots:W · bounce-rejection | both | 24 | -0.044 | -0.029 | 42 | 37 |
| camarilla pivots:W · bounce-touch | both | 24 | -0.058 | -0.122 | 25 | 103 |
| fibonacci pivots:chart · bounce-rejection | shorts | 12 | -0.075 | -0.029 | 58 | 24 |
| traditional pivots:M · bounce-rejection | longs | 8 | -0.076 | -0.678 | 0 | 3 |
| camarilla pivots:M · bounce-touch | shorts | 24 | -0.077 | -0.024 | 46 | 10 |
| fibonacci pivots:W · bounce-rejection | longs | 24 | -0.078 | +0.283 | 62 | 20 |
| traditional pivots:W · bounce-rejection | shorts | 16 | -0.079 | -0.165 | 25 | 6 |
| camarilla pivots:chart · bounce-touch | longs | 12 | -0.089 | -0.158 | 0 | 284 |
| traditional pivots:chart · bounce-rejection | both | 12 | -0.090 | +0.028 | 50 | 44 |
| traditional pivots:W · bounce-rejection | longs | 16 | -0.093 | +0.462 | 62 | 8 |
| fibonacci pivots:W · bounce-rejection | both | 24 | -0.094 | +0.173 | 71 | 30 |
| fibonacci pivots:W · bounce-touch | longs | 24 | -0.102 | +0.087 | 71 | 33 |
| fibonacci pivots:chart · bounce-touch | longs | 12 | -0.106 | -0.170 | 0 | 131 |
| traditional pivots:W · bounce-touch | longs | 16 | -0.109 | +0.112 | 62 | 20 |
| woodie pivots:chart · bounce-rejection | longs | 12 | -0.115 | -0.019 | 17 | 23 |
| fibonacci pivots:W · bounce-rejection | shorts | 24 | -0.117 | +0.015 | 50 | 10 |
| traditional pivots:M · bounce-rejection | both | 8 | -0.117 | -0.197 | 50 | 7 |
| camarilla pivots:M · bounce-rejection | both | 24 | -0.118 | -0.033 | 54 | 15 |
| traditional pivots:W · bounce-touch | shorts | 24 | -0.121 | -0.223 | 38 | 12 |
| camarilla pivots:W · bounce-rejection | shorts | 24 | -0.123 | +0.094 | 58 | 14 |
| camarilla pivots:chart · bounce-rejection | both | 12 | -0.130 | -0.273 | 8 | 62 |
| camarilla pivots:chart · bounce-rejection | shorts | 12 | -0.132 | -0.253 | 33 | 28 |
| woodie pivots:W · bounce-rejection | longs | 16 | -0.132 | -0.069 | 25 | 8 |
| camarilla pivots:chart · bounce-rejection | longs | 12 | -0.132 | -0.288 | 8 | 34 |
| camarilla pivots:W · bounce-touch | shorts | 24 | -0.136 | -0.075 | 38 | 49 |
| traditional pivots:W · bounce-touch | both | 24 | -0.138 | -0.175 | 50 | 22 |
| woodie pivots:chart · bounce-rejection | both | 12 | -0.142 | +0.014 | 33 | 39 |
| fibonacci pivots:W · bounce-touch | both | 24 | -0.148 | +0.107 | 71 | 56 |
| woodie pivots:W · bounce-touch | both | 24 | -0.150 | -0.184 | 38 | 21 |
| traditional pivots:W · bounce-rejection | both | 24 | -0.158 | -0.043 | 42 | 10 |
| traditional pivots:chart · bounce-touch | longs | 12 | -0.161 | -0.145 | 0 | 72 |
| traditional pivots:chart · bounce-rejection | shorts | 12 | -0.163 | +0.108 | 67 | 22 |
| woodie pivots:chart · bounce-rejection | shorts | 12 | -0.171 | +0.070 | 58 | 19 |
| fibonacci pivots:chart · bounce-touch | both | 12 | -0.176 | -0.193 | 0 | 235 |
| woodie pivots:chart · bounce-touch | longs | 12 | -0.189 | -0.134 | 8 | 73 |
| camarilla pivots:chart · bounce-touch | both | 12 | -0.190 | -0.223 | 0 | 377 |
| fibonacci pivots:W · bounce-touch | shorts | 24 | -0.198 | +0.152 | 71 | 23 |
| traditional pivots:M · bounce-touch | shorts | 8 | -0.199 | +0.066 | 75 | 8 |
| woodie pivots:chart · bounce-touch | both | 12 | -0.203 | -0.075 | 25 | 129 |
| traditional pivots:chart · bounce-touch | both | 12 | -0.204 | -0.059 | 17 | 126 |
| camarilla pivots:M · bounce-rejection | longs | 24 | -0.205 | +0.114 | 75 | 9 |
| woodie pivots:W · bounce-rejection | both | 20 | -0.215 | -0.037 | 50 | 12 |
| fibonacci pivots:M · bounce-touch | both | 24 | -0.223 | -0.155 | 33 | 12 |
| woodie pivots:chart · bounce-touch | shorts | 12 | -0.223 | -0.027 | 42 | 59 |
| woodie pivots:W · bounce-touch | shorts | 24 | -0.226 | -0.153 | 38 | 12 |
| woodie pivots:W · bounce-rejection | shorts | 16 | -0.239 | +0.231 | 81 | 5 |
| camarilla pivots:M · bounce-touch | both | 24 | -0.241 | +0.065 | 71 | 24 |
| traditional pivots:chart · bounce-touch | shorts | 12 | -0.255 | +0.011 | 42 | 60 |
| fibonacci pivots:M · bounce-touch | shorts | 8 | -0.267 | +0.654 | 100 | 9 |
| fibonacci pivots:chart · bounce-touch | shorts | 12 | -0.268 | -0.225 | 8 | 104 |
| fibonacci pivots:M · bounce-rejection | longs | 8 | -0.304 | -0.123 | 50 | 8 |
| fibonacci pivots:M · bounce-touch | longs | 16 | -0.319 | -0.070 | 50 | 7 |
| camarilla pivots:M · bounce-touch | longs | 24 | -0.386 | +0.155 | 71 | 13 |
| woodie pivots:M · bounce-touch | shorts | 8 | -0.476 | -0.056 | 25 | 8 |
| camarilla pivots:chart · bounce-touch | shorts | 12 | -0.493 | -0.483 | 0 | 100 |

