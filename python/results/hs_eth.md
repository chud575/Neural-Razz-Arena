# ETH strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase ETH-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | retest · stop:head (longs) | -0.020 | +0.037 | 66 | piv3 tol0.5 retest neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | 97 | +0.004 | +0.005 |
| 1h | Head & Shoulders | retest · stop:shoulder (longs) | +0.070 | -0.208 | 3 | piv3 tol0.25 retest neck:sloped stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | 31 | -0.244 | -0.074 |
| 4h | Head & Shoulders | early · stop:head (longs) | +0.068 | -0.049 | 70 | piv3 tol0.5 early neck:flat stop:head target:2R prior:0 exit:TP1 1R 50% BE | 22 | -0.023 | +0.101 |
| 1d | Head & Shoulders | early · stop:shoulder (both) | +0.305 | +0.061 | 43 | piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:single | 14 | +0.407 | +0.136 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | piv5 tol0.25 breakout neck:sloped stop:shoulder target:1.5R prior:0.5 exit:TP1 1R 50% BE | both | 141 | +0.239 | 67 | -0.000 | -0.033 | +0.033 | -0.045 | +0.14 |
| 1h | Head & Shoulders | piv3 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | shorts | 185 | +0.189 | 94 | +0.049 | +0.023 | +0.026 | -0.093 | -0.04 |
| 4h | Head & Shoulders | piv3 tol0.25 early neck:sloped stop:head target:2R prior:0 exit:single | both | 74 | +0.327 | 38 | -0.062 | +0.008 | -0.070 | -0.136 | +0.09 |
| 1d | Head & Shoulders | piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:single | both | 20 | +0.613 | 14 | +0.407 | +0.136 | +0.270 | +0.094 | +0.49 |


## 15-minute  (IS 2020-01-01 → 2024-10-21, OOS 2024-10-21 → 2026-11-12; ETH buy & hold: IS +2043%, OOS -27%)

### Head & Shoulders

1152 settings × 3 sides tested; 2502 combinations had ≥120 IS trades, 19% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.14. Average OOS result of the top-20 IS picks: -0.045 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.033 R/trade over 67 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol0.25 breakout neck:sloped stop:shoulder target:1.5R prior:0.5 exit:TP1 1R 50% BE | both | 141 | +0.239 | 2.73 | 67 | -0.000 | -0.0 | 51 |
| piv5 tol0.25 breakout neck:sloped stop:shoulder target:3R prior:0.5 exit:TP1 1R 50% BE | both | 140 | +0.263 | 2.64 | 66 | -0.029 | -1.9 | 50 |
| piv5 tol0.5 retest neck:sloped stop:head target:1.5R prior:0.5 exit:TP1 1R 50% BE | both | 147 | +0.216 | 2.52 | 68 | -0.138 | -9.4 | 47 |
| piv5 tol0.5 breakout neck:sloped stop:head target:1.5R prior:0.5 exit:TP1 1R 50% BE | both | 190 | +0.179 | 2.38 | 84 | +0.008 | +0.7 | 52 |
| piv5 tol0.25 breakout neck:sloped stop:head target:1.5R prior:0.5 exit:TP1 1R 50% BE | both | 140 | +0.205 | 2.36 | 66 | +0.015 | +1.0 | 52 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| retest · stop:head | longs | 68 | -0.020 | +0.037 | 66 | 68 |
| retest · stop:shoulder | longs | 87 | -0.021 | -0.007 | 51 | 74 |
| breakout · stop:shoulder | longs | 118 | -0.027 | +0.002 | 49 | 69 |
| breakout · stop:head | longs | 97 | -0.028 | +0.030 | 62 | 70 |
| early · stop:head | longs | 172 | -0.044 | +0.023 | 60 | 115 |
| breakout · stop:head | both | 176 | -0.047 | +0.007 | 51 | 98 |
| breakout · stop:shoulder | both | 176 | -0.049 | +0.020 | 53 | 114 |
| retest · stop:head | both | 155 | -0.049 | +0.005 | 52 | 93 |
| early · stop:head | both | 192 | -0.055 | +0.032 | 65 | 204 |
| early · stop:head | shorts | 184 | -0.060 | +0.021 | 60 | 100 |
| retest · stop:shoulder | both | 160 | -0.060 | +0.011 | 48 | 107 |
| breakout · stop:head | shorts | 95 | -0.061 | -0.028 | 42 | 71 |
| retest · stop:head | shorts | 74 | -0.065 | +0.027 | 62 | 68 |
| breakout · stop:shoulder | shorts | 106 | -0.071 | +0.018 | 58 | 77 |
| early · stop:shoulder | shorts | 186 | -0.105 | -0.006 | 40 | 124 |
| retest · stop:shoulder | shorts | 80 | -0.107 | +0.058 | 70 | 74 |
| early · stop:shoulder | both | 192 | -0.134 | -0.049 | 22 | 261 |
| early · stop:shoulder | longs | 184 | -0.173 | -0.089 | 12 | 140 |


## 1-hour  (IS 2016-05-18 → 2023-09-22, OOS 2023-09-22 → 2026-11-12; ETH buy & hold: IS +12197%, OOS +26%)

### Head & Shoulders

1152 settings × 3 sides tested; 1660 combinations had ≥80 IS trades, 38% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.04. Average OOS result of the top-20 IS picks: -0.093 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.023 R/trade over 94 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | shorts | 185 | +0.189 | 2.26 | 94 | +0.049 | +4.6 | 53 |
| piv3 tol0.5 early neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | shorts | 208 | +0.165 | 2.21 | 101 | +0.001 | +0.1 | 51 |
| piv3 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | both | 379 | +0.131 | 2.16 | 181 | -0.016 | -2.9 | 49 |
| piv3 tol0.5 early neck:flat stop:head target:2R prior:0 exit:TP1 1R 50% BE | shorts | 210 | +0.160 | 2.16 | 110 | -0.033 | -3.7 | 50 |
| piv3 tol0.25 early neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | shorts | 166 | +0.177 | 2.13 | 84 | -0.082 | -6.9 | 48 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| retest · stop:shoulder | longs | 32 | +0.070 | -0.208 | 3 | 30 |
| early · stop:head | shorts | 120 | +0.049 | -0.119 | 16 | 56 |
| early · stop:shoulder | shorts | 152 | +0.037 | -0.240 | 2 | 66 |
| retest · stop:shoulder | shorts | 20 | +0.032 | -0.177 | 15 | 44 |
| retest · stop:shoulder | both | 105 | +0.026 | -0.127 | 18 | 42 |
| retest · stop:head | shorts | 15 | +0.021 | -0.231 | 0 | 42 |
| breakout · stop:shoulder | longs | 62 | +0.000 | -0.086 | 31 | 30 |
| early · stop:head | both | 188 | -0.019 | -0.065 | 27 | 81 |
| breakout · stop:head | shorts | 28 | -0.031 | -0.142 | 7 | 43 |
| breakout · stop:shoulder | both | 144 | -0.036 | -0.110 | 22 | 47 |
| early · stop:head | longs | 122 | -0.043 | -0.095 | 29 | 44 |
| early · stop:shoulder | both | 192 | -0.044 | -0.134 | 15 | 105 |
| breakout · stop:shoulder | shorts | 53 | -0.059 | -0.179 | 9 | 40 |
| retest · stop:head | longs | 26 | -0.071 | -0.161 | 8 | 29 |
| retest · stop:head | both | 87 | -0.073 | -0.159 | 22 | 39 |
| early · stop:shoulder | longs | 152 | -0.086 | -0.096 | 26 | 53 |
| breakout · stop:head | both | 122 | -0.089 | -0.127 | 22 | 44 |
| breakout · stop:head | longs | 40 | -0.095 | -0.216 | 18 | 30 |


## 4-hour  (IS 2016-05-18 → 2023-09-21, OOS 2023-09-21 → 2026-11-12; ETH buy & hold: IS +11210%, OOS +27%)

### Head & Shoulders

1152 settings × 3 sides tested; 336 combinations had ≥50 IS trades, 31% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.09. Average OOS result of the top-20 IS picks: -0.136 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.008 R/trade over 38 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.25 early neck:sloped stop:head target:2R prior:0 exit:single | both | 74 | +0.327 | 1.87 | 38 | -0.062 | -2.4 | 32 |
| piv3 tol0.25 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | both | 67 | +0.267 | 1.77 | 38 | -0.011 | -0.4 | 53 |
| piv3 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | both | 83 | +0.231 | 1.67 | 43 | -0.093 | -4.0 | 49 |
| piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:single | both | 83 | +0.191 | 1.38 | 40 | -0.005 | -0.2 | 40 |
| piv3 tol0.25 early neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | both | 80 | +0.170 | 1.36 | 43 | +0.056 | +2.4 | 53 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | longs | 10 | +0.068 | -0.049 | 70 | 20 |
| early · stop:head | shorts | 3 | +0.029 | -0.149 | 0 | 30 |
| early · stop:head | both | 89 | +0.026 | -0.242 | 10 | 31 |
| early · stop:shoulder | longs | 46 | -0.017 | -0.201 | 33 | 22 |
| breakout · stop:head | both | 2 | -0.031 | -0.530 | 0 | 28 |
| early · stop:shoulder | both | 125 | -0.087 | -0.245 | 10 | 34 |
| breakout · stop:shoulder | both | 15 | -0.185 | -0.471 | 0 | 32 |
| early · stop:shoulder | shorts | 46 | -0.186 | -0.151 | 7 | 38 |


## Daily  (IS 2016-05-18 → 2023-09-21, OOS 2023-09-21 → 2026-11-12; ETH buy & hold: IS +11917%, OOS +27%)

### Head & Shoulders

1152 settings × 3 sides tested; 33 combinations had ≥15 IS trades, 100% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.49. Average OOS result of the top-20 IS picks: +0.094 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.136 R/trade over 14 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:single | both | 20 | +0.613 | 1.36 | 14 | +0.407 | +5.7 | 36 |
| piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 20 | +0.349 | 1.23 | 15 | -0.023 | -0.3 | 53 |
| piv3 tol0.5 early neck:sloped stop:shoulder target:3R prior:0 exit:single | both | 18 | +0.572 | 1.21 | 13 | +0.513 | +6.7 | 38 |
| piv3 tol0.25 early neck:flat stop:shoulder target:3R prior:0 exit:single | both | 15 | +0.600 | 1.14 | 12 | +0.325 | +3.9 | 33 |
| piv3 tol0.5 early neck:sloped stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 18 | +0.334 | 1.14 | 14 | +0.046 | +0.6 | 57 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:shoulder | both | 21 | +0.305 | +0.061 | 43 | 14 |
| early · stop:head | both | 12 | +0.194 | +0.104 | 67 | 11 |

