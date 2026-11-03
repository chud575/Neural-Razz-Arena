# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: 0.20% round trip per trade (0.1% per side), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Triple Top / Bottom | B (longs) | -0.011 | -0.074 | 19 | piv8 tol3.0 depth0.5 B 3R trend:sma exit:single | 43 | -0.240 | -0.147 |
| 1h | Triple Top / Bottom | B (longs) | +0.131 | +0.017 | 50 | piv5 tol2.0 depth0.5 B 2R trend:sma exit:TP1 1R 50% BE | 60 | +0.123 | +0.059 |
| 4h | Triple Top / Bottom | B+Retest (both) | +0.236 | +0.189 | 91 | piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single | 38 | +0.062 | -0.091 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Triple Top / Bottom | piv8 tol3.0 depth1.0 B+Retest 3R trend:sma exit:single | longs | 195 | +0.405 | 69 | -0.213 | -0.072 | -0.140 | -0.152 | +0.05 |
| 1h | Triple Top / Bottom | piv5 tol2.0 depth0.5 B 2R trend:sma exit:TP1 1R 50% BE | longs | 135 | +0.265 | 60 | +0.123 | +0.059 | +0.064 | -0.045 | +0.16 |
| 4h | Triple Top / Bottom | piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single | both | 63 | +0.813 | 38 | +0.062 | -0.091 | +0.153 | +0.138 | +0.19 |


## 15-minute  (IS 2020-01-01 → 2024-10-14, OOS 2024-10-14 → 2026-11-03; BTC buy & hold: IS +817%, OOS +17%)

### Triple Top / Bottom

1620 settings × 3 sides tested; 4556 combinations had ≥120 IS trades, 10% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.05. Average OOS result of the top-20 IS picks: -0.152 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.072 R/trade over 69 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol3.0 depth1.0 B+Retest 3R trend:sma exit:single | longs | 195 | +0.405 | 2.91 | 69 | -0.213 | -14.7 | 22 |
| piv8 tol3.0 depth1.0 B+Retest 3R trend:sma exit:single | both | 367 | +0.271 | 2.75 | 130 | -0.220 | -28.6 | 22 |
| piv8 tol3.0 depth2.0 B+Retest 3R trend:off exit:single | longs | 177 | +0.387 | 2.67 | 71 | -0.222 | -15.8 | 21 |
| piv8 tol3.0 depth2.0 B+Mid 3R trend:off exit:single | longs | 135 | +0.407 | 2.44 | 52 | -0.309 | -16.1 | 19 |
| piv8 tol3.0 depth2.0 B+Retest 3R trend:sma exit:single | longs | 178 | +0.332 | 2.31 | 51 | -0.278 | -14.2 | 20 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 296 | -0.011 | -0.074 | 19 | 90 |
| B+Retest | longs | 312 | -0.046 | -0.057 | 25 | 156 |
| RetestConf | longs | 285 | -0.058 | -0.081 | 22 | 101 |
| B+Mid | longs | 312 | -0.066 | -0.138 | 12 | 119 |
| B | both | 314 | -0.094 | -0.074 | 24 | 173 |
| Retest | longs | 301 | -0.111 | -0.064 | 27 | 120 |
| B+Retest | both | 324 | -0.117 | -0.059 | 30 | 298 |
| RetestConf | both | 312 | -0.124 | -0.082 | 20 | 184 |
| B+Mid | both | 324 | -0.136 | -0.102 | 18 | 232 |
| Retest | both | 312 | -0.150 | -0.073 | 22 | 223 |
| B | shorts | 278 | -0.180 | -0.059 | 33 | 93 |
| Retest | shorts | 287 | -0.184 | -0.081 | 22 | 111 |
| B+Retest | shorts | 312 | -0.184 | -0.074 | 31 | 150 |
| RetestConf | shorts | 278 | -0.186 | -0.076 | 22 | 94 |
| B+Mid | shorts | 309 | -0.201 | -0.077 | 30 | 117 |


## 1-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6684%, OOS +163%)

### Triple Top / Bottom

1620 settings × 3 sides tested; 3675 combinations had ≥80 IS trades, 52% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.16. Average OOS result of the top-20 IS picks: -0.045 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.059 R/trade over 60 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol2.0 depth0.5 B 2R trend:sma exit:TP1 1R 50% BE | longs | 135 | +0.265 | 2.81 | 60 | +0.123 | +7.4 | 58 |
| piv5 tol2.0 depth0.5 B 1.5R trend:sma exit:TP1 1R 50% BE | longs | 142 | +0.243 | 2.76 | 66 | +0.078 | +5.2 | 56 |
| piv5 tol2.0 depth1.0 B 2R trend:sma exit:TP1 1R 50% BE | longs | 132 | +0.262 | 2.72 | 60 | +0.123 | +7.4 | 58 |
| piv5 tol2.0 depth0.5 B+Retest 1.5R trend:sma exit:TP1 1R 50% BE | longs | 236 | +0.185 | 2.68 | 113 | +0.064 | +7.2 | 57 |
| piv5 tol2.0 depth0.5 B 2R trend:sma exit:TP1 1R 50% BE | both | 259 | +0.179 | 2.67 | 118 | -0.042 | -4.9 | 50 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 213 | +0.131 | +0.017 | 50 | 51 |
| B | both | 305 | +0.070 | -0.121 | 11 | 94 |
| RetestConf | longs | 134 | +0.047 | -0.021 | 48 | 49 |
| B | shorts | 190 | +0.043 | -0.241 | 0 | 52 |
| B+Retest | longs | 303 | +0.035 | -0.032 | 39 | 85 |
| B+Retest | both | 318 | +0.010 | -0.157 | 3 | 165 |
| B+Mid | longs | 285 | +0.005 | -0.051 | 39 | 70 |
| RetestConf | both | 276 | -0.007 | -0.169 | 3 | 82 |
| B+Retest | shorts | 285 | -0.012 | -0.280 | 1 | 83 |
| Retest | longs | 182 | -0.024 | -0.091 | 18 | 57 |
| B+Mid | both | 312 | -0.029 | -0.167 | 3 | 134 |
| B+Mid | shorts | 257 | -0.047 | -0.268 | 1 | 73 |
| RetestConf | shorts | 145 | -0.050 | -0.276 | 1 | 45 |
| Retest | both | 288 | -0.063 | -0.191 | 0 | 99 |
| Retest | shorts | 182 | -0.085 | -0.290 | 1 | 56 |


## 4-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6640%, OOS +164%)

### Triple Top / Bottom

1620 settings × 3 sides tested; 252 combinations had ≥50 IS trades, 91% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.19. Average OOS result of the top-20 IS picks: +0.138 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.091 R/trade over 38 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:single | both | 63 | +0.813 | 4.40 | 38 | +0.062 | +2.4 | 37 |
| piv5 tol2.0 depth2.0 B+Retest 2R trend:off exit:single | both | 61 | +0.778 | 4.11 | 38 | +0.062 | +2.4 | 37 |
| piv5 tol2.0 depth1.0 B+Retest 2R trend:off exit:TP1 1R 50% BE | both | 66 | +0.524 | 3.77 | 40 | -0.018 | -0.7 | 50 |
| piv5 tol2.0 depth2.0 B+Retest 1.5R trend:off exit:single | both | 63 | +0.544 | 3.56 | 42 | +0.150 | +6.3 | 48 |
| piv5 tol2.0 depth2.0 B+Retest 2R trend:off exit:TP1 1R 50% BE | both | 65 | +0.496 | 3.55 | 40 | -0.018 | -0.7 | 50 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B+Retest | both | 141 | +0.236 | +0.189 | 91 | 38 |
| B+Retest | longs | 3 | +0.214 | +0.203 | 100 | 32 |
| B | both | 24 | +0.153 | +0.158 | 100 | 28 |
| B+Mid | both | 84 | +0.118 | +0.162 | 93 | 35 |


## Daily  (IS 2015-07-20 → 2023-06-15, OOS 2023-06-15 → 2026-11-03; BTC buy & hold: IS +9032%, OOS +201%)

### Triple Top / Bottom

No configuration reached 15 IS trades.


## Conclusions (written after the sweep)

* Peak tolerance matters: with 0.3–1% (the double-top grid) triple patterns almost never occur on BTC 4h / daily
  (max 21 trades on 4h, zero on daily). This run uses 1 / 2 / 3%.
* **4h is the only timeframe that works — and it works consistently:** 91% of all variants with ≥50 in-sample trades
  were profitable in-sample, and in the best families 91–100% of variants were also profitable out-of-sample
  (+0.16 to +0.19 R/trade OOS after costs). Random entries in the same window lost money (≈ −0.09 R).
  Best family: Breakout + Retest, both directions, tolerance 2%, 2R single target. Only ~30–40 OOS trades per setting.
* 15m loses after costs; 1h is roughly break-even; daily has too few patterns even at 3% tolerance.
* Same picture as the double-top sweep: 4h, both directions, single target, no trend filter.
