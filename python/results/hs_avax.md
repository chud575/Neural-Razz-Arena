# AVAX strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase AVAX-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | early · stop:head (shorts) | +0.058 | +0.153 | 84 | piv8 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | 56 | -0.022 | +0.054 |
| 1h | Head & Shoulders | early · stop:head (shorts) | +0.154 | +0.247 | 100 | piv3 tol0.5 early neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | 40 | +0.173 | +0.041 |
| 4h | Head & Shoulders | early · stop:head (both) | +0.086 | +0.112 | 88 | piv3 tol0.5 early neck:flat stop:head target:measured prior:0 exit:single | 14 | +0.357 | -0.072 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | piv8 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | shorts | 142 | +0.284 | 56 | -0.022 | +0.054 | -0.076 | -0.122 | +0.29 |
| 1h | Head & Shoulders | piv3 tol0.5 early neck:flat stop:shoulder target:1.5R prior:0 exit:TP1 1R 50% BE | shorts | 136 | +0.186 | 76 | +0.085 | +0.006 | +0.079 | +0.085 | +0.06 |
| 4h | Head & Shoulders | piv3 tol0.5 early neck:flat stop:head target:measured prior:0 exit:single | both | 52 | +0.210 | 14 | +0.357 | -0.072 | +0.429 | +0.052 | +0.36 |


## 15-minute  (IS 2021-09-30 → 2025-04-30, OOS 2025-04-30 → 2026-11-12; AVAX buy & hold: IS -69%, OOS -59%)

### Head & Shoulders

1152 settings × 3 sides tested; 1979 combinations had ≥120 IS trades, 25% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.29. Average OOS result of the top-20 IS picks: -0.122 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.054 R/trade over 56 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | shorts | 142 | +0.284 | 2.77 | 56 | -0.022 | -1.2 | 43 |
| piv8 tol0.5 early neck:sloped stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | shorts | 160 | +0.229 | 2.76 | 60 | -0.067 | -4.0 | 45 |
| piv8 tol0.5 early neck:flat stop:head target:measured prior:0 exit:TP1 1R 50% BE | shorts | 178 | +0.212 | 2.49 | 70 | -0.090 | -6.3 | 46 |
| piv8 tol0.5 early neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | shorts | 154 | +0.218 | 2.47 | 60 | -0.043 | -2.6 | 45 |
| piv8 tol0.25 early neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | shorts | 128 | +0.263 | 2.42 | 58 | -0.216 | -12.5 | 40 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | shorts | 144 | +0.058 | +0.153 | 84 | 74 |
| early · stop:head | both | 192 | -0.002 | -0.031 | 34 | 134 |
| breakout · stop:shoulder | both | 152 | -0.010 | -0.008 | 44 | 79 |
| breakout · stop:head | both | 141 | -0.031 | -0.045 | 35 | 70 |
| breakout · stop:shoulder | longs | 78 | -0.031 | -0.192 | 0 | 54 |
| breakout · stop:shoulder | shorts | 70 | -0.034 | +0.185 | 93 | 60 |
| early · stop:shoulder | shorts | 164 | -0.035 | -0.050 | 31 | 92 |
| breakout · stop:head | shorts | 56 | -0.045 | +0.070 | 73 | 58 |
| early · stop:shoulder | both | 192 | -0.068 | -0.165 | 9 | 185 |
| retest · stop:shoulder | both | 121 | -0.070 | -0.016 | 40 | 78 |
| breakout · stop:head | longs | 61 | -0.071 | -0.246 | 0 | 53 |
| retest · stop:shoulder | shorts | 45 | -0.077 | +0.185 | 80 | 59 |
| early · stop:head | longs | 152 | -0.077 | -0.241 | 0 | 86 |
| retest · stop:shoulder | longs | 54 | -0.087 | -0.220 | 2 | 50 |
| retest · stop:head | both | 116 | -0.087 | -0.054 | 29 | 67 |
| retest · stop:head | shorts | 35 | -0.089 | +0.088 | 86 | 55 |
| early · stop:shoulder | longs | 164 | -0.092 | -0.287 | 3 | 110 |
| retest · stop:head | longs | 42 | -0.149 | -0.268 | 0 | 47 |


## 1-hour  (IS 2021-09-30 → 2025-04-30, OOS 2025-04-30 → 2026-11-12; AVAX buy & hold: IS -68%, OOS -60%)

### Head & Shoulders

1152 settings × 3 sides tested; 455 combinations had ≥80 IS trades, 68% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.06. Average OOS result of the top-20 IS picks: +0.085 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.006 R/trade over 76 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.5 early neck:flat stop:shoulder target:1.5R prior:0 exit:TP1 1R 50% BE | shorts | 136 | +0.186 | 2.05 | 76 | +0.085 | +6.4 | 58 |
| piv3 tol0.5 early neck:flat stop:shoulder target:measured prior:0 exit:TP1 1R 50% BE | shorts | 130 | +0.228 | 1.95 | 73 | +0.143 | +10.5 | 58 |
| piv3 tol0.5 early neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | shorts | 136 | +0.173 | 1.86 | 74 | +0.095 | +7.0 | 58 |
| piv3 tol0.25 early neck:flat stop:shoulder target:3R prior:0 exit:single | shorts | 92 | +0.367 | 1.83 | 53 | -0.204 | -10.8 | 21 |
| piv3 tol0.5 early neck:sloped stop:shoulder target:measured prior:0 exit:TP1 1R 50% BE | shorts | 114 | +0.227 | 1.81 | 64 | +0.285 | +18.2 | 62 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | shorts | 13 | +0.154 | +0.247 | 100 | 47 |
| early · stop:shoulder | shorts | 53 | +0.141 | -0.045 | 45 | 51 |
| early · stop:shoulder | both | 133 | +0.070 | +0.040 | 56 | 57 |
| breakout · stop:shoulder | both | 40 | +0.046 | -0.006 | 42 | 48 |
| retest · stop:shoulder | both | 15 | +0.032 | +0.029 | 53 | 45 |
| early · stop:head | both | 101 | +0.027 | +0.153 | 93 | 49 |
| early · stop:shoulder | longs | 43 | -0.014 | +0.023 | 47 | 49 |
| breakout · stop:head | both | 21 | -0.084 | +0.026 | 57 | 43 |
| early · stop:head | longs | 30 | -0.131 | +0.059 | 77 | 32 |
| retest · stop:head | both | 6 | -0.218 | -0.032 | 33 | 36 |


## 4-hour  (IS 2021-09-30 → 2025-04-30, OOS 2025-04-30 → 2026-11-12; AVAX buy & hold: IS -68%, OOS -60%)

### Head & Shoulders

1152 settings × 3 sides tested; 47 combinations had ≥50 IS trades, 85% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.36. Average OOS result of the top-20 IS picks: +0.052 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.072 R/trade over 14 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.5 early neck:flat stop:head target:measured prior:0 exit:single | both | 52 | +0.210 | 0.99 | 14 | +0.357 | +5.0 | 50 |
| piv3 tol0.5 early neck:sloped stop:head target:measured prior:0 exit:single | both | 52 | +0.191 | 0.97 | 15 | -0.028 | -0.4 | 40 |
| piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 81 | +0.126 | 0.94 | 33 | +0.063 | +2.1 | 48 |
| piv3 tol0.25 early neck:flat stop:head target:2R prior:0 exit:TP1 1R 50% BE | both | 51 | +0.147 | 0.93 | 16 | +0.018 | +0.3 | 56 |
| piv3 tol0.5 early neck:sloped stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 72 | +0.122 | 0.84 | 30 | +0.126 | +3.8 | 50 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:head | both | 16 | +0.086 | +0.112 | 88 | 14 |
| early · stop:shoulder | both | 31 | +0.041 | -0.065 | 39 | 27 |


## Daily  (IS 2021-09-30 → 2025-05-01, OOS 2025-05-01 → 2026-11-12; AVAX buy & hold: IS -68%, OOS -61%)

### Head & Shoulders

No configuration reached 15 IS trades.

