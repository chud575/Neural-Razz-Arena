# XRP strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase XRP-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | early · stop:shoulder (longs) | +0.099 | -0.125 | 11 | piv5 tol0.5 early neck:flat stop:shoulder target:1.5R prior:0.5 exit:single | 73 | -0.114 | -0.238 |
| 1h | Head & Shoulders | breakout · stop:head (both) | +0.127 | +0.006 | 50 | piv3 tol0.25 breakout neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | 35 | +0.016 | +0.072 |
| 4h | Head & Shoulders | early · stop:shoulder (shorts) | +0.156 | +0.817 | 100 | piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | 12 | +0.735 | +0.203 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Head & Shoulders | piv3 tol0.5 breakout neck:flat stop:shoulder target:1.5R prior:0.5 exit:single | shorts | 120 | +0.213 | 37 | +0.174 | +0.080 | +0.094 | +0.179 | +0.06 |
| 1h | Head & Shoulders | piv3 tol0.25 breakout neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | both | 82 | +0.231 | 35 | +0.016 | +0.072 | -0.056 | +0.004 | -0.21 |
| 4h | Head & Shoulders | piv5 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 61 | +0.375 | 31 | +0.082 | -0.042 | +0.124 | +0.267 | +0.37 |


## 15-minute  (IS 2020-01-01 → 2025-07-19, OOS 2025-07-19 → 2026-11-12; XRP buy & hold: IS +1676%, OOS -70%)

### Head & Shoulders

1152 settings × 3 sides tested; 1698 combinations had ≥120 IS trades, 31% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.06. Average OOS result of the top-20 IS picks: +0.179 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.080 R/trade over 37 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.5 breakout neck:flat stop:shoulder target:1.5R prior:0.5 exit:single | shorts | 120 | +0.213 | 1.85 | 37 | +0.174 | +6.5 | 49 |
| piv3 tol0.5 retest neck:flat stop:shoulder target:2R prior:0 exit:single | shorts | 171 | +0.178 | 1.57 | 74 | +0.125 | +9.3 | 39 |
| piv5 tol0.5 retest neck:flat stop:head target:3R prior:0 exit:single | both | 156 | +0.232 | 1.55 | 55 | +0.715 | +39.3 | 44 |
| piv5 tol0.5 early neck:sloped stop:head target:1.5R prior:0.5 exit:single | shorts | 128 | +0.172 | 1.55 | 37 | +0.031 | +1.1 | 43 |
| piv3 tol0.5 breakout neck:flat stop:shoulder target:2R prior:0.5 exit:single | both | 226 | +0.145 | 1.48 | 84 | +0.159 | +13.4 | 40 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:shoulder | longs | 152 | +0.099 | -0.125 | 11 | 96 |
| early · stop:head | longs | 121 | +0.051 | -0.052 | 26 | 89 |
| early · stop:head | both | 185 | -0.001 | +0.068 | 62 | 124 |
| early · stop:shoulder | both | 192 | -0.004 | -0.086 | 17 | 155 |
| early · stop:head | shorts | 129 | -0.037 | +0.060 | 62 | 68 |
| early · stop:shoulder | shorts | 160 | -0.071 | -0.109 | 16 | 84 |
| retest · stop:head | longs | 29 | -0.096 | -0.091 | 17 | 56 |
| breakout · stop:head | longs | 34 | -0.099 | -0.094 | 15 | 68 |
| retest · stop:head | shorts | 20 | -0.109 | +0.094 | 70 | 60 |
| breakout · stop:head | both | 111 | -0.109 | +0.066 | 64 | 75 |
| breakout · stop:head | shorts | 34 | -0.113 | +0.078 | 74 | 62 |
| breakout · stop:shoulder | both | 129 | -0.128 | +0.028 | 56 | 81 |
| retest · stop:head | both | 105 | -0.138 | +0.090 | 65 | 65 |
| breakout · stop:shoulder | longs | 52 | -0.155 | -0.047 | 29 | 73 |
| breakout · stop:shoulder | shorts | 55 | -0.164 | -0.040 | 35 | 69 |
| retest · stop:shoulder | longs | 32 | -0.181 | -0.086 | 19 | 66 |
| retest · stop:shoulder | both | 119 | -0.186 | +0.054 | 60 | 67 |
| retest · stop:shoulder | shorts | 39 | -0.220 | +0.049 | 56 | 59 |


## 1-hour  (IS 2019-02-26 → 2025-04-18, OOS 2025-04-18 → 2026-11-12; XRP buy & hold: IS +547%, OOS -50%)

### Head & Shoulders

1152 settings × 3 sides tested; 604 combinations had ≥80 IS trades, 38% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.21. Average OOS result of the top-20 IS picks: +0.004 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.072 R/trade over 35 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol0.25 breakout neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | both | 82 | +0.231 | 1.78 | 35 | +0.016 | +0.6 | 54 |
| piv3 tol0.5 retest neck:sloped stop:head target:1.5R prior:0 exit:single | both | 91 | +0.218 | 1.65 | 35 | +0.069 | +2.4 | 43 |
| piv3 tol0.25 breakout neck:flat stop:head target:2R prior:0 exit:single | both | 83 | +0.253 | 1.55 | 33 | -0.008 | -0.3 | 33 |
| piv3 tol0.5 breakout neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | both | 94 | +0.185 | 1.53 | 39 | +0.119 | +4.6 | 59 |
| piv3 tol0.5 retest neck:sloped stop:shoulder target:measured prior:0 exit:single | both | 106 | +0.281 | 1.50 | 46 | +0.142 | +6.5 | 39 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| breakout · stop:head | both | 28 | +0.127 | +0.006 | 50 | 39 |
| retest · stop:head | both | 14 | +0.086 | +0.048 | 71 | 36 |
| early · stop:shoulder | shorts | 78 | +0.024 | +0.113 | 63 | 31 |
| retest · stop:shoulder | both | 30 | +0.022 | -0.006 | 50 | 40 |
| breakout · stop:shoulder | both | 48 | +0.021 | -0.023 | 35 | 42 |
| early · stop:head | longs | 20 | +0.007 | -0.049 | 30 | 48 |
| early · stop:head | both | 136 | -0.048 | +0.126 | 71 | 43 |
| early · stop:shoulder | both | 160 | -0.055 | +0.086 | 53 | 49 |
| early · stop:shoulder | longs | 71 | -0.115 | -0.078 | 27 | 41 |
| early · stop:head | shorts | 19 | -0.137 | +0.206 | 84 | 28 |


## 4-hour  (IS 2019-02-26 → 2025-04-18, OOS 2025-04-18 → 2026-11-12; XRP buy & hold: IS +554%, OOS -50%)

### Head & Shoulders

1152 settings × 3 sides tested; 92 combinations had ≥50 IS trades, 60% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.37. Average OOS result of the top-20 IS picks: +0.267 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.042 R/trade over 31 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | 61 | +0.375 | 2.32 | 31 | +0.082 | +2.6 | 48 |
| piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | shorts | 56 | +0.304 | 1.91 | 12 | +0.735 | +8.8 | 67 |
| piv5 tol0.5 early neck:flat stop:shoulder target:measured prior:0 exit:TP1 1R 50% BE | both | 61 | +0.328 | 1.79 | 31 | -0.133 | -4.1 | 48 |
| piv3 tol0.5 early neck:flat stop:shoulder target:1.5R prior:0 exit:TP1 1R 50% BE | shorts | 57 | +0.238 | 1.76 | 12 | +0.488 | +5.9 | 67 |
| piv3 tol0.5 early neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | shorts | 57 | +0.245 | 1.75 | 12 | +0.491 | +5.9 | 67 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| early · stop:shoulder | shorts | 8 | +0.156 | +0.817 | 100 | 12 |
| early · stop:shoulder | both | 53 | +0.085 | +0.167 | 85 | 25 |
| early · stop:head | both | 28 | +0.029 | +0.064 | 61 | 20 |
| early · stop:shoulder | longs | 3 | -0.077 | +0.038 | 67 | 16 |


## Daily  (IS 2019-02-26 → 2025-04-18, OOS 2025-04-18 → 2026-11-12; XRP buy & hold: IS +552%, OOS -50%)

### Head & Shoulders

No configuration reached 15 IS trades.

