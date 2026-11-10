# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan3ATR · fold0.5 (shorts) | -0.014 | -0.168 | 12 | fan3ATR stacked20 lookback100 fold0.5 stop2ATR 1.5R | 119 | -0.049 | -0.117 |
| 1h | Accordion / EMA Fan | fan3ATR · fold0.5 (longs) | +0.116 | -0.071 | 27 | fan3ATR stacked20 lookback50 fold0.5 stop1ATR 1.5R | 66 | -0.014 | -0.143 |
| 4h | Accordion / EMA Fan | fan2ATR · fold0.3 (shorts) | +0.120 | -0.161 | 9 | fan2ATR stacked10 lookback100 fold0.3 stop1.5ATR 2R | 26 | -0.426 | +0.046 |
| 1d | Accordion / EMA Fan | fan2ATR · fold0.7 (longs) | +0.290 | +0.204 | 79 | fan2ATR stacked10 lookback100 fold0.7 stop0.5ATR 3R | 8 | +0.403 | -0.236 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan3ATR stacked20 lookback100 fold0.5 stop2ATR 1.5R | shorts | 215 | +0.165 | 119 | -0.049 | -0.117 | +0.068 | -0.015 | +0.67 |
| 1h | Accordion / EMA Fan | fan3ATR stacked20 lookback50 fold0.5 stop1ATR 1.5R | longs | 199 | +0.232 | 66 | -0.014 | -0.143 | +0.129 | -0.144 | +0.15 |
| 4h | Accordion / EMA Fan | fan2ATR stacked20 lookback100 fold0.7 stop2ATR 2R | shorts | 54 | +0.410 | 24 | -0.119 | -0.009 | -0.110 | -0.169 | +0.11 |
| 1d | Accordion / EMA Fan | fan2ATR stacked10 lookback100 fold0.7 stop0.5ATR 3R | longs | 23 | +0.873 | 8 | +0.403 | -0.236 | +0.639 | +0.045 | +0.15 |


## 15-minute  (IS 2020-01-01 → 2024-10-14, OOS 2024-10-14 → 2026-11-03; BTC buy & hold: IS +817%, OOS +17%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 864 combinations had ≥120 IS trades, 22% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.67. Average OOS result of the top-20 IS picks: -0.015 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.117 R/trade over 119 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan3ATR stacked20 lookback100 fold0.5 stop2ATR 1.5R | shorts | 215 | +0.165 | 1.90 | 119 | -0.049 | -5.8 | 42 |
| fan3ATR stacked20 lookback50 fold0.5 stop2ATR 1.5R | shorts | 213 | +0.165 | 1.89 | 118 | -0.040 | -4.7 | 42 |
| fan3ATR stacked10 lookback100 fold0.5 stop2ATR 1.5R | shorts | 263 | +0.131 | 1.68 | 146 | -0.107 | -15.6 | 40 |
| fan3ATR stacked10 lookback50 fold0.5 stop2ATR 1.5R | shorts | 261 | +0.131 | 1.66 | 144 | -0.092 | -13.3 | 40 |
| fan3ATR stacked10 lookback100 fold0.5 stop2ATR 2R | shorts | 263 | +0.152 | 1.65 | 145 | -0.045 | -6.6 | 35 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan3ATR · fold0.5 | shorts | 48 | -0.014 | -0.168 | 12 | 132 |
| fan3ATR · fold0.7 | shorts | 48 | -0.031 | -0.170 | 12 | 134 |
| fan3ATR · fold0.3 | shorts | 48 | -0.036 | -0.252 | 0 | 126 |
| fan2ATR · fold0.5 | shorts | 48 | -0.043 | -0.158 | 4 | 262 |
| fan2ATR · fold0.7 | shorts | 48 | -0.052 | -0.159 | 8 | 273 |
| fan3ATR · fold0.5 | both | 48 | -0.063 | -0.245 | 0 | 289 |
| fan3ATR · fold0.7 | both | 48 | -0.085 | -0.220 | 0 | 296 |
| fan2ATR · fold0.3 | shorts | 48 | -0.090 | -0.230 | 0 | 240 |
| fan3ATR · fold0.5 | longs | 48 | -0.097 | -0.309 | 0 | 158 |
| fan3ATR · fold0.3 | both | 48 | -0.106 | -0.263 | 0 | 277 |
| fan3ATR · fold0.7 | longs | 48 | -0.122 | -0.261 | 0 | 161 |
| fan2ATR · fold0.5 | both | 48 | -0.128 | -0.240 | 0 | 564 |
| fan2ATR · fold0.7 | both | 48 | -0.133 | -0.211 | 0 | 588 |
| fan3ATR · fold0.3 | longs | 48 | -0.157 | -0.273 | 0 | 152 |
| fan2ATR · fold0.3 | both | 48 | -0.183 | -0.245 | 0 | 516 |
| fan2ATR · fold0.5 | longs | 48 | -0.198 | -0.311 | 0 | 303 |
| fan2ATR · fold0.7 | longs | 48 | -0.198 | -0.256 | 0 | 315 |
| fan2ATR · fold0.3 | longs | 48 | -0.260 | -0.258 | 2 | 276 |


## 1-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6684%, OOS +163%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 864 combinations had ≥80 IS trades, 53% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.15. Average OOS result of the top-20 IS picks: -0.144 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.143 R/trade over 66 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan3ATR stacked20 lookback50 fold0.5 stop1ATR 1.5R | longs | 199 | +0.232 | 2.55 | 66 | -0.014 | -0.9 | 44 |
| fan3ATR stacked20 lookback50 fold0.5 stop1ATR 2R | longs | 199 | +0.264 | 2.47 | 66 | -0.120 | -7.9 | 33 |
| fan3ATR stacked20 lookback50 fold0.5 stop2ATR 2R | both | 316 | +0.204 | 2.43 | 113 | -0.155 | -17.5 | 30 |
| fan3ATR stacked20 lookback100 fold0.5 stop1ATR 1.5R | longs | 203 | +0.218 | 2.43 | 68 | -0.011 | -0.7 | 44 |
| fan3ATR stacked20 lookback100 fold0.5 stop1ATR 2R | longs | 203 | +0.252 | 2.39 | 68 | -0.152 | -10.3 | 32 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan3ATR · fold0.5 | longs | 48 | +0.116 | -0.071 | 27 | 74 |
| fan3ATR · fold0.7 | longs | 48 | +0.099 | -0.142 | 4 | 76 |
| fan2ATR · fold0.5 | shorts | 48 | +0.084 | -0.202 | 0 | 108 |
| fan3ATR · fold0.5 | both | 48 | +0.067 | -0.125 | 0 | 126 |
| fan3ATR · fold0.7 | both | 48 | +0.043 | -0.170 | 0 | 128 |
| fan2ATR · fold0.3 | shorts | 48 | +0.040 | -0.094 | 19 | 102 |
| fan2ATR · fold0.5 | both | 48 | +0.037 | -0.121 | 0 | 234 |
| fan3ATR · fold0.3 | shorts | 48 | +0.018 | -0.142 | 23 | 52 |
| fan2ATR · fold0.7 | longs | 48 | +0.007 | -0.068 | 12 | 132 |
| fan2ATR · fold0.5 | longs | 48 | +0.002 | -0.050 | 19 | 126 |
| fan3ATR · fold0.3 | both | 48 | -0.002 | -0.045 | 44 | 124 |
| fan3ATR · fold0.3 | longs | 48 | -0.014 | +0.023 | 65 | 72 |
| fan3ATR · fold0.5 | shorts | 48 | -0.016 | -0.202 | 0 | 52 |
| fan2ATR · fold0.7 | both | 48 | -0.019 | -0.122 | 0 | 244 |
| fan2ATR · fold0.3 | both | 48 | -0.031 | -0.078 | 19 | 218 |
| fan3ATR · fold0.7 | shorts | 48 | -0.050 | -0.210 | 0 | 52 |
| fan2ATR · fold0.7 | shorts | 48 | -0.054 | -0.186 | 0 | 112 |
| fan2ATR · fold0.3 | longs | 48 | -0.084 | -0.064 | 23 | 116 |


## 4-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6640%, OOS +164%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 688 combinations had ≥50 IS trades, 22% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.11. Average OOS result of the top-20 IS picks: -0.169 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.009 R/trade over 24 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked20 lookback100 fold0.7 stop2ATR 2R | shorts | 54 | +0.410 | 1.97 | 24 | -0.119 | -2.9 | 29 |
| fan2ATR stacked10 lookback100 fold0.5 stop1ATR 1.5R | shorts | 67 | +0.285 | 1.83 | 30 | -0.113 | -3.4 | 37 |
| fan2ATR stacked10 lookback50 fold0.5 stop1ATR 1.5R | shorts | 65 | +0.287 | 1.81 | 30 | -0.114 | -3.4 | 37 |
| fan2ATR stacked20 lookback50 fold0.7 stop2ATR 2R | shorts | 53 | +0.380 | 1.81 | 24 | -0.119 | -2.9 | 29 |
| fan2ATR stacked20 lookback100 fold0.5 stop2ATR 2R | shorts | 51 | +0.376 | 1.76 | 23 | -0.077 | -1.8 | 30 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.3 | shorts | 23 | +0.120 | -0.161 | 9 | 26 |
| fan2ATR · fold0.5 | shorts | 45 | +0.089 | -0.234 | 7 | 27 |
| fan2ATR · fold0.7 | shorts | 46 | +0.074 | -0.221 | 4 | 30 |
| fan2ATR · fold0.5 | both | 48 | -0.080 | -0.229 | 0 | 62 |
| fan2ATR · fold0.7 | both | 48 | -0.092 | -0.165 | 4 | 65 |
| fan3ATR · fold0.5 | both | 48 | -0.145 | -0.249 | 2 | 30 |
| fan3ATR · fold0.5 | longs | 47 | -0.164 | -0.112 | 15 | 23 |
| fan3ATR · fold0.7 | both | 48 | -0.180 | -0.208 | 6 | 32 |
| fan2ATR · fold0.5 | longs | 48 | -0.193 | -0.230 | 0 | 36 |
| fan3ATR · fold0.7 | longs | 48 | -0.202 | -0.051 | 46 | 24 |
| fan2ATR · fold0.7 | longs | 48 | -0.208 | -0.123 | 4 | 38 |
| fan2ATR · fold0.3 | both | 48 | -0.252 | -0.142 | 4 | 56 |
| fan3ATR · fold0.3 | both | 48 | -0.446 | -0.217 | 12 | 30 |
| fan2ATR · fold0.3 | longs | 48 | -0.450 | -0.150 | 0 | 35 |
| fan3ATR · fold0.3 | longs | 47 | -0.639 | -0.114 | 15 | 23 |


## Daily  (IS 2015-07-20 → 2023-06-15, OOS 2023-06-15 → 2026-11-03; BTC buy & hold: IS +9032%, OOS +201%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 576 combinations had ≥15 IS trades, 39% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.15. Average OOS result of the top-20 IS picks: +0.045 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.236 R/trade over 8 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked10 lookback100 fold0.7 stop0.5ATR 3R | longs | 23 | +0.873 | 2.05 | 8 | +0.403 | +3.2 | 38 |
| fan2ATR stacked10 lookback50 fold0.7 stop1ATR 1.5R | longs | 23 | +0.498 | 1.91 | 8 | -0.130 | -1.0 | 38 |
| fan2ATR stacked20 lookback100 fold0.7 stop0.5ATR 3R | longs | 22 | +0.777 | 1.79 | 7 | +0.611 | +4.3 | 43 |
| fan2ATR stacked20 lookback50 fold0.7 stop1ATR 1.5R | longs | 22 | +0.453 | 1.68 | 7 | +0.011 | +0.1 | 43 |
| fan2ATR stacked10 lookback100 fold0.3 stop2ATR 2R | both | 27 | +0.440 | 1.48 | 12 | -0.256 | -3.1 | 25 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.7 | longs | 48 | +0.290 | +0.204 | 79 | 7 |
| fan2ATR · fold0.7 | both | 48 | +0.072 | -0.032 | 50 | 12 |
| fan3ATR · fold0.7 | longs | 48 | +0.065 | +0.340 | 75 | 5 |
| fan3ATR · fold0.7 | both | 48 | -0.010 | +0.025 | 58 | 8 |
| fan2ATR · fold0.3 | both | 48 | -0.050 | -0.464 | 0 | 12 |
| fan2ATR · fold0.3 | longs | 48 | -0.089 | -0.348 | 21 | 7 |
| fan2ATR · fold0.5 | both | 48 | -0.119 | -0.031 | 50 | 12 |
| fan3ATR · fold0.3 | both | 48 | -0.167 | -0.254 | 17 | 8 |
| fan2ATR · fold0.5 | longs | 48 | -0.170 | +0.207 | 79 | 7 |
| fan3ATR · fold0.5 | both | 48 | -0.182 | +0.025 | 58 | 8 |
| fan3ATR · fold0.3 | longs | 48 | -0.235 | +0.046 | 33 | 5 |
| fan3ATR · fold0.5 | longs | 48 | -0.252 | +0.340 | 75 | 5 |

