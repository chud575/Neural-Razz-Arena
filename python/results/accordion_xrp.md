# XRP strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase XRP-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan2ATR · fold0.5 (shorts) | +0.005 | -0.046 | 23 | fan2ATR stacked20 lookback100 fold0.5 stop2ATR 3R | 146 | -0.055 | +0.093 |
| 1h | Accordion / EMA Fan | fan2ATR · fold0.3 (shorts) | -0.006 | +0.123 | 78 | fan2ATR stacked10 lookback100 fold0.3 stop1ATR 1.5R | 49 | +0.364 | +0.056 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan2ATR stacked10 lookback100 fold0.7 stop2ATR 3R | shorts | 339 | +0.228 | 178 | -0.171 | +0.064 | -0.235 | -0.095 | +0.65 |
| 1h | Accordion / EMA Fan | fan2ATR stacked10 lookback100 fold0.3 stop1ATR 1.5R | shorts | 82 | +0.101 | 49 | +0.364 | +0.056 | +0.308 | +0.032 | +0.28 |


## 15-minute  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +171%, OOS -42%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 696 combinations had ≥120 IS trades, 27% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.65. Average OOS result of the top-20 IS picks: -0.095 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.064 R/trade over 178 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked10 lookback100 fold0.7 stop2ATR 3R | shorts | 339 | +0.228 | 2.22 | 178 | -0.171 | -30.5 | 22 |
| fan2ATR stacked10 lookback50 fold0.7 stop2ATR 3R | shorts | 335 | +0.219 | 2.13 | 177 | -0.166 | -29.4 | 23 |
| fan2ATR stacked10 lookback100 fold0.7 stop2ATR 2R | shorts | 356 | +0.153 | 1.94 | 183 | -0.146 | -26.8 | 31 |
| fan2ATR stacked10 lookback50 fold0.7 stop2ATR 2R | shorts | 354 | +0.152 | 1.92 | 182 | -0.141 | -25.6 | 31 |
| fan2ATR stacked20 lookback50 fold0.7 stop2ATR 2R | shorts | 270 | +0.164 | 1.81 | 149 | -0.055 | -8.2 | 34 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.5 | shorts | 48 | +0.005 | -0.046 | 23 | 157 |
| fan2ATR · fold0.7 | shorts | 48 | -0.004 | -0.069 | 21 | 164 |
| fan2ATR · fold0.3 | shorts | 48 | -0.034 | -0.162 | 10 | 144 |
| fan3ATR · fold0.7 | both | 48 | -0.062 | -0.137 | 4 | 142 |
| fan2ATR · fold0.7 | both | 48 | -0.071 | -0.128 | 0 | 278 |
| fan3ATR · fold0.5 | both | 48 | -0.077 | -0.118 | 8 | 142 |
| fan2ATR · fold0.5 | both | 48 | -0.109 | -0.137 | 0 | 266 |
| fan2ATR · fold0.3 | both | 48 | -0.129 | -0.213 | 0 | 242 |
| fan2ATR · fold0.7 | longs | 48 | -0.140 | -0.215 | 0 | 115 |
| fan3ATR · fold0.3 | both | 48 | -0.143 | -0.197 | 4 | 131 |
| fan3ATR · fold0.7 | longs | 48 | -0.150 | -0.395 | 0 | 58 |
| fan3ATR · fold0.5 | longs | 48 | -0.182 | -0.353 | 0 | 58 |
| fan2ATR · fold0.5 | longs | 48 | -0.225 | -0.268 | 0 | 110 |
| fan2ATR · fold0.3 | longs | 48 | -0.226 | -0.287 | 0 | 98 |
| fan3ATR · fold0.3 | longs | 24 | -0.244 | -0.206 | 12 | 57 |


## 1-hour  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +185%, OOS -42%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 262 combinations had ≥80 IS trades, 23% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.28. Average OOS result of the top-20 IS picks: +0.032 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.056 R/trade over 49 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked10 lookback100 fold0.3 stop1ATR 1.5R | shorts | 82 | +0.101 | 0.72 | 49 | +0.364 | +17.8 | 57 |
| fan2ATR stacked10 lookback50 fold0.7 stop2ATR 3R | both | 166 | +0.100 | 0.71 | 78 | -0.154 | -12.0 | 22 |
| fan2ATR stacked20 lookback50 fold0.5 stop1ATR 1.5R | both | 125 | +0.079 | 0.70 | 61 | +0.166 | +10.1 | 49 |
| fan2ATR stacked20 lookback100 fold0.5 stop1ATR 1.5R | both | 125 | +0.079 | 0.70 | 62 | +0.144 | +9.0 | 48 |
| fan2ATR stacked10 lookback100 fold0.7 stop2ATR 3R | both | 167 | +0.094 | 0.67 | 79 | -0.115 | -9.1 | 23 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.3 | shorts | 9 | -0.006 | +0.123 | 78 | 49 |
| fan2ATR · fold0.7 | both | 48 | -0.026 | -0.183 | 0 | 70 |
| fan2ATR · fold0.7 | shorts | 24 | -0.027 | -0.047 | 33 | 53 |
| fan2ATR · fold0.7 | longs | 24 | -0.050 | -0.375 | 0 | 29 |
| fan2ATR · fold0.5 | shorts | 20 | -0.052 | +0.036 | 75 | 52 |
| fan2ATR · fold0.3 | both | 48 | -0.057 | +0.002 | 52 | 65 |
| fan2ATR · fold0.5 | both | 48 | -0.076 | -0.149 | 8 | 68 |
| fan2ATR · fold0.5 | longs | 22 | -0.150 | -0.406 | 0 | 28 |
| fan2ATR · fold0.3 | longs | 19 | -0.173 | -0.204 | 16 | 27 |


## 4-hour  (IS 2023-07-14 → 2025-11-06, OOS 2025-11-06 → 2026-11-04; XRP buy & hold: IS +182%, OOS -42%)

### Accordion / EMA Fan

No configuration reached 50 IS trades.


## Daily  (IS 2023-07-14 → 2025-11-07, OOS 2025-11-07 → 2026-11-04; XRP buy & hold: IS +222%, OOS -44%)

### Accordion / EMA Fan

No configuration reached 15 IS trades.

