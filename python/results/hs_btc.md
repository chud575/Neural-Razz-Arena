# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | early · stop:head (longs) | -0.066 | -0.166 | 10 | piv8 tol0.5 early neck:flat stop:head target:3R prior:0.5 exit:TP1 1R 50% BE | 49 | +0.032 | +0.007 |
| 1h | Head & Shoulders | breakout · stop:shoulder (longs) | +0.108 | +0.004 | 48 | piv3 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | 46 | -0.028 | +0.047 |
| 4h | Head & Shoulders | early · stop:head (longs) | +0.359 | -0.069 | 12 | piv3 tol0.5 early neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | 27 | -0.078 | +0.150 |
| 1d | Head & Shoulders | early · stop:head (both) | +0.398 | +0.025 | 66 | piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:single | 6 | -0.588 | -0.007 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | piv8 tol0.5 breakout neck:sloped stop:shoulder target:2R prior:0 exit:single | longs | 140 | +0.278 | 56 | +0.018 | -0.089 | +0.108 | -0.028 | +0.21 |
| 1h | Head & Shoulders | piv5 tol0.25 retest neck:flat stop:shoulder target:3R prior:0 exit:single | both | 90 | +0.435 | 33 | +0.027 | +0.006 | +0.020 | -0.052 | +0.04 |
| 4h | Head & Shoulders | piv3 tol0.5 early neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | longs | 54 | +0.468 | 27 | -0.078 | +0.150 | -0.227 | -0.145 | +0.11 |
| 1d | Head & Shoulders | piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:single | both | 17 | +0.746 | 6 | -0.588 | -0.007 | -0.581 | +0.017 | +0.54 |


## 15-minute  (IS 2020-01-01 → 2024-10-21, OOS 2024-10-21 → 2026-11-12; BTC buy & hold: IS +868%, OOS +5%)

### Head & Shoulders

1152 settings × 3 sides tested; 2536 combinations had ≥120 IS trades, 4% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.21. Average OOS result of the top-20 IS picks: -0.028 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.089 R/trade over 56 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol0.5 breakout neck:sloped stop:shoulder target:2R prior:0 exit:single | longs | 140 | +0.278 | 2.20 | 56 | +0.018 | +1.0 | 38 |
| piv8 tol0.5 early neck:flat stop:head target:3R prior:0.5 exit:TP1 1R 50% BE | longs | 156 | +0.160 | 1.69 | 49 | +0.032 | +1.6 | 49 |
| piv8 tol0.5 early neck:flat stop:head target:measured prior:0.5 exit:TP1 1R 50% BE | longs | 158 | +0.150 | 1.66 | 56 | -0.048 | -2.7 | 50 |
| piv8 tol0.5 early neck:flat stop:head target:1.5R prior:0.5 exit:TP1 1R 50% BE | longs | 159 | +0.124 | 1.50 | 58 | -0.093 | -5.4 | 47 |
| piv8 tol0.5 early neck:flat stop:shoulder target:measured prior:0.5 exit:single | longs | 180 | +0.288 | 1.42 | 61 | +0.050 | +3.1 | 26 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | longs | 181 | -0.066 | -0.166 | 10 | 104 |
| breakout · stop:head | longs | 101 | -0.077 | -0.031 | 39 | 64 |
| retest · stop:head | longs | 78 | -0.083 | -0.061 | 38 | 60 |
| breakout · stop:shoulder | longs | 125 | -0.092 | -0.074 | 26 | 70 |
| breakout · stop:head | both | 174 | -0.122 | -0.064 | 24 | 102 |
| retest · stop:head | both | 156 | -0.129 | -0.065 | 24 | 90 |
| early · stop:head | both | 192 | -0.130 | -0.119 | 11 | 200 |
| breakout · stop:shoulder | both | 183 | -0.134 | -0.093 | 22 | 108 |
| early · stop:shoulder | longs | 184 | -0.149 | -0.252 | 7 | 138 |
| retest · stop:shoulder | both | 160 | -0.154 | -0.107 | 19 | 97 |
| retest · stop:shoulder | longs | 96 | -0.157 | -0.098 | 21 | 62 |
| breakout · stop:head | shorts | 91 | -0.168 | -0.139 | 8 | 65 |
| retest · stop:head | shorts | 64 | -0.188 | -0.061 | 22 | 66 |
| early · stop:head | shorts | 184 | -0.191 | -0.088 | 17 | 101 |
| breakout · stop:shoulder | shorts | 103 | -0.199 | -0.172 | 2 | 70 |
| retest · stop:shoulder | shorts | 80 | -0.208 | -0.079 | 29 | 71 |
| early · stop:shoulder | both | 192 | -0.212 | -0.216 | 9 | 250 |
| early · stop:shoulder | shorts | 192 | -0.278 | -0.202 | 9 | 114 |


## 1-hour  (IS 2016-01-01 → 2023-08-10, OOS 2023-08-10 → 2026-11-12; BTC buy & hold: IS +6748%, OOS +147%)

### Head & Shoulders

1152 settings × 3 sides tested; 1664 combinations had ≥80 IS trades, 35% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.04. Average OOS result of the top-20 IS picks: -0.052 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.006 R/trade over 33 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol0.25 retest neck:flat stop:shoulder target:3R prior:0 exit:single | both | 90 | +0.435 | 2.14 | 33 | +0.027 | +0.9 | 27 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | both | 210 | +0.152 | 2.01 | 80 | -0.028 | -2.3 | 49 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:1.5R prior:0 exit:TP1 1R 50% BE | both | 214 | +0.138 | 1.92 | 81 | -0.057 | -4.6 | 48 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 204 | +0.156 | 1.88 | 76 | -0.014 | -1.1 | 47 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | longs | 116 | +0.192 | 1.83 | 46 | -0.028 | -1.3 | 48 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| breakout · stop:shoulder | longs | 58 | +0.108 | +0.004 | 48 | 40 |
| breakout · stop:shoulder | both | 154 | +0.089 | -0.123 | 23 | 40 |
| breakout · stop:shoulder | shorts | 40 | +0.072 | -0.063 | 25 | 37 |
| retest · stop:shoulder | both | 88 | +0.048 | -0.087 | 17 | 44 |
| retest · stop:shoulder | longs | 24 | +0.030 | -0.101 | 17 | 43 |
| breakout · stop:head | longs | 37 | +0.015 | -0.022 | 43 | 41 |
| retest · stop:head | longs | 18 | -0.012 | -0.091 | 28 | 42 |
| retest · stop:shoulder | shorts | 16 | -0.021 | -0.019 | 25 | 36 |
| breakout · stop:head | both | 131 | -0.021 | -0.046 | 41 | 38 |
| breakout · stop:head | shorts | 28 | -0.041 | -0.145 | 4 | 34 |
| retest · stop:head | shorts | 7 | -0.076 | -0.058 | 0 | 33 |
| retest · stop:head | both | 86 | -0.079 | -0.059 | 36 | 40 |
| early · stop:head | shorts | 156 | -0.087 | -0.310 | 1 | 42 |
| early · stop:head | both | 189 | -0.088 | -0.226 | 12 | 71 |
| early · stop:shoulder | shorts | 168 | -0.093 | -0.206 | 9 | 48 |
| early · stop:shoulder | both | 192 | -0.095 | -0.141 | 12 | 90 |
| early · stop:head | longs | 120 | -0.108 | +0.045 | 62 | 49 |
| early · stop:shoulder | longs | 152 | -0.153 | +0.005 | 62 | 55 |


## 4-hour  (IS 2016-01-01 → 2023-08-10, OOS 2023-08-10 → 2026-11-12; BTC buy & hold: IS +6729%, OOS +146%)

### Head & Shoulders

1152 settings × 3 sides tested; 376 combinations had ≥50 IS trades, 41% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.11. Average OOS result of the top-20 IS picks: -0.145 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.150 R/trade over 27 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.5 early neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | longs | 54 | +0.468 | 2.96 | 27 | -0.078 | -2.1 | 48 |
| piv3 tol0.5 early neck:flat stop:head target:2R prior:0 exit:TP1 1R 50% BE | longs | 57 | +0.375 | 2.68 | 27 | -0.129 | -3.5 | 48 |
| piv3 tol0.5 early neck:flat stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | longs | 58 | +0.328 | 2.55 | 27 | -0.180 | -4.9 | 48 |
| piv3 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | longs | 51 | +0.413 | 2.54 | 24 | +0.044 | +1.1 | 54 |
| piv3 tol0.5 early neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | longs | 54 | +0.362 | 2.54 | 24 | -0.013 | -0.3 | 54 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | longs | 8 | +0.359 | -0.069 | 12 | 26 |
| early · stop:shoulder | longs | 51 | +0.079 | -0.049 | 33 | 26 |
| early · stop:shoulder | shorts | 34 | +0.025 | -0.390 | 0 | 28 |
| retest · stop:shoulder | both | 6 | +0.025 | +0.007 | 50 | 19 |
| early · stop:shoulder | both | 136 | -0.048 | -0.169 | 19 | 32 |
| early · stop:head | both | 90 | -0.101 | -0.283 | 2 | 29 |
| breakout · stop:shoulder | both | 23 | -0.113 | -0.222 | 4 | 23 |
| early · stop:head | shorts | 12 | -0.170 | -0.384 | 0 | 19 |
| breakout · stop:head | both | 16 | -0.177 | -0.159 | 0 | 20 |


## Daily  (IS 2015-07-20 → 2023-06-21, OOS 2023-06-21 → 2026-11-12; BTC buy & hold: IS +10613%, OOS +143%)

### Head & Shoulders

1152 settings × 3 sides tested; 97 combinations had ≥15 IS trades, 93% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.54. Average OOS result of the top-20 IS picks: +0.017 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.007 R/trade over 6 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:single | both | 17 | +0.746 | 2.63 | 6 | -0.588 | -3.5 | 17 |
| piv3 tol0.5 early neck:sloped stop:head target:1.5R prior:0 exit:single | both | 19 | +0.699 | 2.56 | 9 | -0.141 | -1.3 | 33 |
| piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | both | 17 | +0.600 | 2.53 | 6 | -0.375 | -2.2 | 33 |
| piv3 tol0.5 early neck:sloped stop:shoulder target:3R prior:0 exit:single | both | 23 | +1.064 | 2.49 | 10 | +0.179 | +1.8 | 30 |
| piv3 tol0.25 early neck:sloped stop:shoulder target:3R prior:0 exit:single | both | 21 | +1.064 | 2.38 | 7 | -0.454 | -3.2 | 14 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | both | 29 | +0.398 | +0.025 | 66 | 8 |
| early · stop:shoulder | both | 54 | +0.331 | +0.130 | 50 | 7 |
| early · stop:shoulder | longs | 10 | +0.037 | +0.487 | 100 | 4 |
| breakout · stop:shoulder | both | 4 | +0.006 | +0.750 | 100 | 8 |

