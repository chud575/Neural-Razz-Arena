# ETH strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase ETH-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan3ATR · fold0.5 (shorts) | -0.019 | -0.336 | 0 | fan3ATR stacked10 lookback100 fold0.5 stop2ATR 1.5R | 143 | -0.250 | -0.098 |
| 1h | Accordion / EMA Fan | fan2ATR · fold0.3 (shorts) | +0.007 | +0.064 | 71 | fan2ATR stacked20 lookback50 fold0.3 stop2ATR 1.5R | 83 | +0.190 | -0.127 |
| 4h | Accordion / EMA Fan | fan2ATR · fold0.3 (shorts) | +0.085 | -0.062 | 31 | fan2ATR stacked20 lookback100 fold0.3 stop1.5ATR 1.5R | 28 | -0.201 | -0.122 |
| 1d | Accordion / EMA Fan | fan2ATR · fold0.7 (longs) | +0.378 | -0.582 | 0 | fan2ATR stacked20 lookback50 fold0.7 stop1ATR 1.5R | 6 | -0.202 | +0.136 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan3ATR stacked20 lookback100 fold0.7 stop2ATR 3R | longs | 363 | +0.153 | 131 | -0.081 | -0.051 | -0.030 | -0.152 | +0.48 |
| 1h | Accordion / EMA Fan | fan2ATR stacked20 lookback50 fold0.7 stop2ATR 3R | shorts | 194 | +0.267 | 90 | +0.097 | -0.041 | +0.138 | +0.093 | +0.54 |
| 4h | Accordion / EMA Fan | fan2ATR stacked10 lookback50 fold0.5 stop1.5ATR 3R | longs | 86 | +0.345 | 34 | +0.235 | +0.220 | +0.014 | -0.038 | -0.24 |
| 1d | Accordion / EMA Fan | fan2ATR stacked20 lookback50 fold0.7 stop1ATR 1.5R | longs | 15 | +0.815 | 6 | -0.202 | +0.136 | -0.338 | -0.566 | +0.10 |


## 15-minute  (IS 2020-01-01 → 2024-10-15, OOS 2024-10-15 → 2026-11-04; ETH buy & hold: IS +1915%, OOS -10%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 864 combinations had ≥120 IS trades, 20% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.48. Average OOS result of the top-20 IS picks: -0.152 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.051 R/trade over 131 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan3ATR stacked20 lookback100 fold0.7 stop2ATR 3R | longs | 363 | +0.153 | 1.57 | 131 | -0.081 | -10.6 | 25 |
| fan3ATR stacked10 lookback100 fold0.7 stop2ATR 3R | longs | 430 | +0.138 | 1.55 | 166 | -0.173 | -28.7 | 23 |
| fan3ATR stacked20 lookback50 fold0.7 stop2ATR 3R | longs | 362 | +0.146 | 1.49 | 131 | -0.081 | -10.6 | 25 |
| fan3ATR stacked10 lookback50 fold0.7 stop2ATR 3R | longs | 429 | +0.132 | 1.47 | 166 | -0.173 | -28.7 | 23 |
| fan3ATR stacked10 lookback100 fold0.7 stop2ATR 3R | both | 716 | +0.097 | 1.43 | 309 | -0.201 | -62.0 | 22 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan3ATR · fold0.5 | shorts | 48 | -0.019 | -0.336 | 0 | 132 |
| fan3ATR · fold0.7 | longs | 48 | -0.036 | -0.194 | 0 | 148 |
| fan3ATR · fold0.7 | both | 48 | -0.043 | -0.264 | 0 | 282 |
| fan3ATR · fold0.7 | shorts | 48 | -0.054 | -0.342 | 0 | 133 |
| fan3ATR · fold0.5 | both | 48 | -0.061 | -0.225 | 0 | 276 |
| fan3ATR · fold0.3 | shorts | 48 | -0.074 | -0.355 | 0 | 130 |
| fan2ATR · fold0.5 | shorts | 48 | -0.082 | -0.222 | 0 | 258 |
| fan3ATR · fold0.5 | longs | 48 | -0.087 | -0.124 | 0 | 144 |
| fan2ATR · fold0.7 | shorts | 48 | -0.107 | -0.225 | 0 | 262 |
| fan3ATR · fold0.3 | both | 48 | -0.110 | -0.299 | 0 | 266 |
| fan2ATR · fold0.7 | both | 48 | -0.113 | -0.229 | 0 | 560 |
| fan2ATR · fold0.5 | both | 48 | -0.117 | -0.214 | 0 | 541 |
| fan2ATR · fold0.7 | longs | 48 | -0.118 | -0.234 | 0 | 299 |
| fan2ATR · fold0.3 | shorts | 48 | -0.132 | -0.280 | 0 | 238 |
| fan3ATR · fold0.3 | longs | 48 | -0.134 | -0.245 | 0 | 137 |
| fan2ATR · fold0.5 | longs | 48 | -0.145 | -0.208 | 0 | 283 |
| fan2ATR · fold0.3 | both | 48 | -0.162 | -0.247 | 0 | 494 |
| fan2ATR · fold0.3 | longs | 48 | -0.187 | -0.216 | 0 | 256 |


## 1-hour  (IS 2016-06-01 → 2023-09-19, OOS 2023-09-19 → 2026-11-04; ETH buy & hold: IS +11664%, OOS +41%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 864 combinations had ≥80 IS trades, 40% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.54. Average OOS result of the top-20 IS picks: +0.093 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.041 R/trade over 90 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked20 lookback50 fold0.7 stop2ATR 3R | shorts | 194 | +0.267 | 1.98 | 90 | +0.097 | +8.8 | 28 |
| fan3ATR stacked10 lookback50 fold0.7 stop2ATR 3R | shorts | 130 | +0.314 | 1.88 | 57 | +0.110 | +6.3 | 28 |
| fan2ATR stacked20 lookback50 fold0.3 stop2ATR 1.5R | shorts | 185 | +0.174 | 1.88 | 83 | +0.190 | +15.7 | 48 |
| fan2ATR stacked20 lookback50 fold0.5 stop2ATR 3R | shorts | 183 | +0.259 | 1.86 | 87 | -0.003 | -0.3 | 25 |
| fan2ATR stacked20 lookback100 fold0.7 stop2ATR 3R | shorts | 197 | +0.248 | 1.86 | 91 | +0.085 | +7.8 | 27 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.3 | shorts | 48 | +0.007 | +0.064 | 71 | 93 |
| fan2ATR · fold0.5 | shorts | 48 | +0.001 | -0.033 | 33 | 98 |
| fan3ATR · fold0.7 | longs | 48 | -0.003 | +0.023 | 62 | 68 |
| fan3ATR · fold0.7 | both | 48 | -0.011 | +0.036 | 71 | 118 |
| fan3ATR · fold0.3 | shorts | 48 | -0.016 | +0.069 | 62 | 48 |
| fan2ATR · fold0.7 | shorts | 48 | -0.017 | +0.019 | 56 | 100 |
| fan3ATR · fold0.5 | shorts | 48 | -0.019 | +0.081 | 75 | 50 |
| fan3ATR · fold0.7 | shorts | 48 | -0.022 | +0.051 | 67 | 50 |
| fan2ATR · fold0.5 | both | 48 | -0.035 | -0.066 | 12 | 218 |
| fan3ATR · fold0.5 | both | 48 | -0.038 | +0.039 | 71 | 118 |
| fan2ATR · fold0.3 | both | 48 | -0.040 | -0.073 | 10 | 201 |
| fan2ATR · fold0.7 | both | 48 | -0.041 | +0.008 | 60 | 226 |
| fan3ATR · fold0.5 | longs | 48 | -0.050 | +0.007 | 62 | 67 |
| fan2ATR · fold0.7 | longs | 48 | -0.059 | -0.001 | 50 | 126 |
| fan3ATR · fold0.3 | both | 48 | -0.062 | -0.088 | 17 | 111 |
| fan2ATR · fold0.5 | longs | 48 | -0.062 | -0.093 | 12 | 120 |
| fan2ATR · fold0.3 | longs | 48 | -0.077 | -0.194 | 8 | 108 |
| fan3ATR · fold0.3 | longs | 48 | -0.092 | -0.208 | 6 | 63 |


## 4-hour  (IS 2016-06-01 → 2023-09-18, OOS 2023-09-18 → 2026-11-04; ETH buy & hold: IS +11307%, OOS +42%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 635 combinations had ≥50 IS trades, 44% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.24. Average OOS result of the top-20 IS picks: -0.038 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.220 R/trade over 34 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked10 lookback50 fold0.5 stop1.5ATR 3R | longs | 86 | +0.345 | 1.63 | 34 | +0.235 | +8.0 | 32 |
| fan2ATR stacked10 lookback100 fold0.5 stop1.5ATR 3R | longs | 90 | +0.327 | 1.59 | 35 | +0.198 | +6.9 | 31 |
| fan2ATR stacked20 lookback50 fold0.5 stop2ATR 3R | longs | 64 | +0.353 | 1.46 | 26 | +0.168 | +4.4 | 31 |
| fan2ATR stacked20 lookback50 fold0.5 stop1.5ATR 3R | longs | 68 | +0.348 | 1.46 | 26 | +0.170 | +4.4 | 31 |
| fan2ATR stacked20 lookback100 fold0.5 stop2ATR 3R | longs | 68 | +0.330 | 1.42 | 27 | +0.123 | +3.3 | 30 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.3 | shorts | 35 | +0.085 | -0.062 | 31 | 32 |
| fan2ATR · fold0.3 | both | 48 | +0.035 | -0.064 | 31 | 58 |
| fan3ATR · fold0.3 | both | 48 | +0.025 | +0.069 | 71 | 32 |
| fan2ATR · fold0.5 | shorts | 48 | +0.005 | -0.088 | 25 | 30 |
| fan2ATR · fold0.5 | both | 48 | +0.003 | +0.009 | 60 | 60 |
| fan2ATR · fold0.5 | longs | 48 | +0.003 | +0.107 | 77 | 30 |
| fan3ATR · fold0.5 | both | 48 | -0.022 | +0.095 | 75 | 32 |
| fan2ATR · fold0.3 | longs | 48 | -0.029 | -0.061 | 42 | 28 |
| fan3ATR · fold0.3 | longs | 24 | -0.039 | -0.119 | 25 | 21 |
| fan2ATR · fold0.7 | shorts | 48 | -0.046 | +0.127 | 71 | 31 |
| fan2ATR · fold0.7 | both | 48 | -0.076 | +0.133 | 94 | 60 |
| fan3ATR · fold0.5 | longs | 24 | -0.088 | +0.013 | 58 | 21 |
| fan2ATR · fold0.7 | longs | 48 | -0.100 | +0.138 | 83 | 30 |
| fan3ATR · fold0.7 | both | 48 | -0.117 | +0.301 | 100 | 32 |
| fan3ATR · fold0.7 | longs | 24 | -0.226 | +0.083 | 75 | 21 |


## Daily  (IS 2016-06-01 → 2023-09-19, OOS 2023-09-19 → 2026-11-04; ETH buy & hold: IS +11698%, OOS +41%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 324 combinations had ≥15 IS trades, 52% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.10. Average OOS result of the top-20 IS picks: -0.566 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.136 R/trade over 6 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked20 lookback50 fold0.7 stop1ATR 1.5R | longs | 15 | +0.815 | 2.77 | 6 | -0.202 | -1.2 | 33 |
| fan2ATR stacked10 lookback100 fold0.7 stop1ATR 1.5R | longs | 15 | +0.814 | 2.77 | 7 | -0.331 | -2.3 | 29 |
| fan3ATR stacked10 lookback50 fold0.7 stop0.5ATR 3R | both | 19 | +1.087 | 2.32 | 9 | -1.018 | -9.2 | 0 |
| fan3ATR stacked10 lookback50 fold0.7 stop0.5ATR 2R | both | 19 | +0.765 | 2.12 | 9 | -0.693 | -6.2 | 11 |
| fan2ATR stacked10 lookback50 fold0.7 stop0.5ATR 3R | longs | 15 | +1.106 | 2.08 | 7 | -1.038 | -7.3 | 0 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.7 | longs | 36 | +0.378 | -0.582 | 0 | 6 |
| fan3ATR · fold0.7 | both | 48 | +0.167 | -0.228 | 25 | 9 |
| fan2ATR · fold0.7 | both | 48 | +0.159 | -0.362 | 17 | 12 |
| fan2ATR · fold0.5 | both | 48 | +0.128 | -0.340 | 4 | 12 |
| fan3ATR · fold0.5 | both | 48 | +0.023 | -0.172 | 17 | 9 |
| fan2ATR · fold0.3 | both | 48 | -0.130 | -0.084 | 42 | 12 |
| fan3ATR · fold0.3 | both | 48 | -0.238 | -0.210 | 33 | 9 |

