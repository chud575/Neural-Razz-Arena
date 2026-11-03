# BTC strategy sweep — 15m / 1h / 4h / 1D

Costs: 0.20% round trip per trade (0.1% per side), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase BTC-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Double Top / Bottom | B (longs) | -0.075 | -0.161 | 8 | piv8 tol0.3 depth1.0 B 3R trend:sma exit:single | 49 | -0.219 | -0.237 |
| 15m | S/R Flip | rejection · levels htf:D (both) | -0.324 | -0.514 | 0 | piv5 rejection 3R tries3 levels:htf:D trend:sma exit:single | 59 | -0.583 | -0.535 |
| 15m | Megaphone | failedBO (shorts) | -0.229 | -0.401 | 0 | piv3 swings4 expand0.5 failedBO midline trend:off exit:single | 83 | -0.431 | -0.461 |
| 1h | Double Top / Bottom | B (longs) | +0.043 | -0.021 | 47 | piv3 tol1.0 depth0.5 B 3R trend:off exit:single | 78 | -0.016 | +0.010 |
| 1h | S/R Flip | sweep · levels htf:D (shorts) | -0.009 | -0.391 | 0 | piv8 sweep 1.5R tries3 levels:htf:D trend:off exit:single | 31 | -0.391 | -0.258 |
| 1h | Megaphone | BO-close (longs) | +0.186 | -0.326 | 6 | piv5 swings4 expand0.5 BO-close measured trend:off exit:single | 64 | -0.264 | -0.107 |
| 4h | Double Top / Bottom | B+Retest (longs) | +0.158 | +0.159 | 61 | piv3 tol1.0 depth0.5 B+Retest 3R trend:sma exit:TP1 1R 50% BE | 27 | -0.053 | +0.146 |
| 4h | S/R Flip | rejection · levels htf:D (longs) | +0.057 | -0.165 | 8 | piv5 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | 47 | -0.148 | -0.209 |
| 4h | Megaphone | BO-close (longs) | +1.074 | +0.063 | 64 | piv5 swings4 expand0.0 BO-close 2R trend:off exit:single | 30 | +0.063 | -0.184 |
| 1d | S/R Flip | sweep · levels chart (longs) | +0.434 | -0.050 | 40 | piv3 sweep 3R tries1 levels:chart trend:off exit:single | 16 | -0.331 | -0.050 |
| 1d | Megaphone | BO-retest (both) | +1.104 | +0.985 | 100 | piv3 swings4 expand0.0 BO-retest 3R trend:off exit:single | 5 | +0.486 | -0.274 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Double Top / Bottom | piv8 tol0.3 depth1.0 B 3R trend:sma exit:single | longs | 165 | +0.194 | 49 | -0.219 | -0.237 | +0.019 | -0.163 | +0.08 |
| 15m | S/R Flip | piv5 rejection 3R tries3 levels:htf:D trend:sma exit:single | both | 133 | -0.276 | 59 | -0.583 | -0.535 | -0.047 | -0.616 | +0.88 |
| 15m | Megaphone | piv8 swings4 expand0.5 BO-close measured trend:sma exit:single | longs | 215 | +0.327 | 91 | -0.545 | -0.717 | +0.172 | -0.853 | +0.79 |
| 1h | Double Top / Bottom | piv8 tol0.3 depth1.0 B+Retest 2R trend:sma exit:single | shorts | 92 | +0.388 | 53 | -0.128 | -0.158 | +0.030 | -0.078 | +0.18 |
| 1h | S/R Flip | piv5 rejection 3R tries3 levels:htf:D trend:sma exit:single | shorts | 98 | +0.156 | 43 | -0.254 | -0.202 | -0.052 | -0.283 | +0.61 |
| 1h | Megaphone | piv5 swings4 expand0.5 BO-close measured trend:off exit:single | longs | 119 | +1.383 | 64 | -0.264 | -0.107 | -0.157 | -0.055 | +0.57 |
| 4h | Double Top / Bottom | piv3 tol1.0 depth0.5 B+Retest 3R trend:sma exit:TP1 1R 50% BE | longs | 51 | +0.472 | 27 | -0.053 | +0.146 | -0.199 | +0.066 | -0.13 |
| 4h | S/R Flip | piv3 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | both | 131 | +0.138 | 72 | -0.148 | -0.194 | +0.046 | -0.212 | +0.35 |
| 4h | Megaphone | piv5 swings4 expand0.0 BO-close 2R trend:off exit:single | longs | 60 | +0.606 | 30 | +0.063 | -0.184 | +0.247 | +0.018 | +0.58 |
| 1d | S/R Flip | piv8 rejection 1.5R tries1 levels:chart trend:sma exit:single | longs | 21 | +0.597 | 10 | -0.319 | -0.089 | -0.230 | -0.116 | -0.05 |
| 1d | Megaphone | piv3 swings4 expand0.0 BO-close 1.5R trend:sma exit:single | both | 16 | +0.988 | 10 | +0.693 | -0.173 | +0.866 | +0.849 | -0.03 |


## 15-minute  (IS 2020-01-01 → 2024-10-14, OOS 2024-10-14 → 2026-11-03; BTC buy & hold: IS +817%, OOS +17%)

### Double Top / Bottom

1620 settings × 3 sides tested; 4066 combinations had ≥120 IS trades, 2% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.08. Average OOS result of the top-20 IS picks: -0.163 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.237 R/trade over 49 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol0.3 depth1.0 B 3R trend:sma exit:single | longs | 165 | +0.194 | 1.33 | 49 | -0.219 | -10.7 | 22 |
| piv5 tol1.0 depth2.0 B+Retest 3R trend:sma exit:single | longs | 225 | +0.151 | 1.22 | 58 | -0.046 | -2.7 | 26 |
| piv5 tol0.3 depth1.0 RetestConf 3R trend:sma exit:single | longs | 139 | +0.196 | 1.22 | 44 | -0.053 | -2.3 | 27 |
| piv5 tol0.3 depth1.0 RetestConf 3R trend:sma exit:TP1 1R 50% BE | longs | 149 | +0.109 | 1.09 | 50 | -0.210 | -10.5 | 48 |
| piv8 tol0.3 depth1.0 B+Retest 3R trend:sma exit:single | longs | 300 | +0.113 | 1.06 | 88 | -0.132 | -11.6 | 25 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 251 | -0.075 | -0.161 | 8 | 138 |
| RetestConf | longs | 243 | -0.120 | -0.170 | 5 | 131 |
| B+Retest | longs | 281 | -0.120 | -0.149 | 11 | 233 |
| B | both | 287 | -0.135 | -0.137 | 7 | 252 |
| B+Mid | longs | 275 | -0.150 | -0.237 | 4 | 193 |
| B+Retest | both | 317 | -0.155 | -0.130 | 11 | 414 |
| RetestConf | both | 278 | -0.156 | -0.151 | 5 | 242 |
| Retest | longs | 245 | -0.170 | -0.185 | 4 | 157 |
| Retest | both | 282 | -0.191 | -0.155 | 6 | 285 |
| RetestConf | shorts | 234 | -0.196 | -0.135 | 9 | 142 |
| B+Mid | both | 304 | -0.197 | -0.190 | 11 | 358 |
| B+Retest | shorts | 286 | -0.198 | -0.137 | 8 | 231 |
| B | shorts | 253 | -0.199 | -0.127 | 8 | 138 |
| Retest | shorts | 250 | -0.218 | -0.154 | 6 | 162 |
| B+Mid | shorts | 280 | -0.252 | -0.173 | 7 | 197 |

### S/R Flip

864 settings × 3 sides tested; 2088 combinations had ≥120 IS trades, 0% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.88. Average OOS result of the top-20 IS picks: -0.616 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.535 R/trade over 59 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 rejection 3R tries3 levels:htf:D trend:sma exit:single | both | 133 | -0.276 | -1.75 | 59 | -0.583 | -34.4 | 24 |
| piv3 rejection 2R tries3 levels:htf:D trend:sma exit:single | both | 130 | -0.251 | -1.98 | 57 | -0.530 | -30.2 | 33 |
| piv5 sweep 3R tries1 levels:htf:4h trend:sma exit:single | shorts | 236 | -0.253 | -2.06 | 119 | -0.572 | -68.1 | 26 |
| piv3 sweep 3R tries3 levels:htf:4h trend:sma exit:single | shorts | 263 | -0.243 | -2.08 | 134 | -0.534 | -71.5 | 28 |
| piv5 rejection 3R tries1 levels:htf:4h trend:sma exit:single | shorts | 309 | -0.300 | -2.83 | 147 | -0.554 | -81.5 | 27 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| rejection · levels htf:D | both | 36 | -0.324 | -0.514 | 0 | 56 |
| sweep · levels htf:4h | shorts | 72 | -0.411 | -0.591 | 0 | 127 |
| rejection · levels htf:4h | shorts | 72 | -0.466 | -0.608 | 0 | 160 |
| rejection · levels htf:4h | both | 72 | -0.508 | -0.799 | 0 | 338 |
| sweep · levels htf:4h | both | 72 | -0.511 | -0.736 | 0 | 270 |
| rejection · levels htf:4h | longs | 72 | -0.547 | -0.970 | 0 | 178 |
| sweep · levels htf:4h | longs | 72 | -0.605 | -0.864 | 0 | 142 |
| touch · levels htf:D | both | 72 | -0.605 | -0.773 | 0 | 81 |
| sweep · levels chart+4h | shorts | 72 | -0.626 | -0.805 | 0 | 307 |
| rejection · levels chart+4h | shorts | 72 | -0.641 | -0.788 | 0 | 392 |
| sweep · levels chart+4h | both | 72 | -0.669 | -0.847 | 0 | 611 |
| rejection · levels chart+4h | both | 72 | -0.677 | -0.858 | 0 | 786 |
| sweep · levels chart | shorts | 72 | -0.695 | -0.871 | 0 | 572 |
| touch · levels htf:D | longs | 36 | -0.709 | -0.872 | 0 | 44 |
| touch · levels htf:4h | shorts | 72 | -0.710 | -0.896 | 0 | 246 |
| sweep · levels chart+4h | longs | 72 | -0.711 | -0.890 | 0 | 304 |
| rejection · levels chart+4h | longs | 72 | -0.712 | -0.927 | 0 | 396 |
| rejection · levels chart | shorts | 72 | -0.717 | -0.908 | 0 | 724 |
| sweep · levels chart | both | 72 | -0.747 | -0.894 | 0 | 1136 |
| rejection · levels chart | both | 72 | -0.766 | -0.955 | 0 | 1451 |
| sweep · levels chart | longs | 72 | -0.794 | -0.918 | 0 | 560 |
| touch · levels htf:4h | both | 72 | -0.804 | -1.069 | 0 | 508 |
| rejection · levels chart | longs | 72 | -0.811 | -1.003 | 0 | 724 |
| touch · levels htf:4h | longs | 72 | -0.890 | -1.231 | 0 | 262 |
| touch · levels chart+4h | shorts | 72 | -0.920 | -1.186 | 0 | 598 |
| touch · levels chart+4h | both | 72 | -0.991 | -1.278 | 0 | 1204 |
| touch · levels chart | shorts | 72 | -1.012 | -1.355 | 0 | 1198 |
| touch · levels chart+4h | longs | 72 | -1.060 | -1.368 | 0 | 606 |
| touch · levels chart | both | 72 | -1.096 | -1.416 | 0 | 2406 |
| touch · levels chart | longs | 72 | -1.174 | -1.478 | 0 | 1198 |

### Megaphone

1056 settings × 3 sides tested; 1745 combinations had ≥120 IS trades, 1% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.79. Average OOS result of the top-20 IS picks: -0.853 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.717 R/trade over 91 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 swings4 expand0.5 BO-close measured trend:sma exit:single | longs | 215 | +0.327 | 0.99 | 91 | -0.545 | -49.6 | 12 |
| piv8 swings4 expand0.5 BO-close measured trend:off exit:single | longs | 225 | +0.291 | 0.91 | 94 | -0.544 | -51.1 | 13 |
| piv3 swings4 expand0.5 fade-touch opposite trend:sma exit:single | longs | 196 | +0.459 | 0.78 | 85 | -1.133 | -96.3 | 8 |
| piv3 swings4 expand0.5 fade-touch opposite trend:sma exit:single | both | 321 | +0.248 | 0.61 | 136 | -1.247 | -169.7 | 7 |
| piv5 swings4 expand0.5 BO-close measured trend:off exit:single | longs | 274 | +0.148 | 0.60 | 121 | -0.730 | -88.3 | 16 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| failedBO | shorts | 46 | -0.229 | -0.401 | 0 | 86 |
| failedBO | both | 80 | -0.284 | -0.427 | 0 | 128 |
| failedBO | longs | 54 | -0.291 | -0.489 | 0 | 80 |
| BO-close | longs | 128 | -0.338 | -0.690 | 0 | 127 |
| BO-close | both | 144 | -0.380 | -0.663 | 1 | 242 |
| BO-close | shorts | 128 | -0.427 | -0.704 | 0 | 136 |
| fade-rejection | shorts | 100 | -0.588 | -0.813 | 1 | 120 |
| fade-rejection | both | 152 | -0.624 | -0.851 | 0 | 214 |
| fade-rejection | longs | 110 | -0.673 | -0.864 | 0 | 136 |
| BO-retest | both | 144 | -0.885 | -1.153 | 3 | 208 |
| BO-retest | longs | 112 | -0.892 | -1.272 | 0 | 115 |
| fade-touch | both | 180 | -0.895 | -1.238 | 0 | 226 |
| BO-retest | shorts | 112 | -0.918 | -1.191 | 0 | 118 |
| fade-touch | shorts | 120 | -0.941 | -1.315 | 0 | 200 |
| fade-touch | longs | 135 | -0.949 | -1.230 | 0 | 223 |


## 1-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6684%, OOS +163%)

### Double Top / Bottom

1620 settings × 3 sides tested; 3931 combinations had ≥80 IS trades, 31% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.18. Average OOS result of the top-20 IS picks: -0.078 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.158 R/trade over 53 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 tol0.3 depth1.0 B+Retest 2R trend:sma exit:single | shorts | 92 | +0.388 | 2.47 | 53 | -0.128 | -6.8 | 32 |
| piv3 tol1.0 depth0.5 B+Retest 3R trend:off exit:single | longs | 313 | +0.253 | 2.36 | 141 | +0.002 | +0.3 | 28 |
| piv3 tol1.0 depth0.5 B 3R trend:off exit:single | longs | 181 | +0.337 | 2.36 | 78 | -0.016 | -1.3 | 27 |
| piv3 tol1.0 depth1.0 B+Retest 2R trend:sma exit:single | longs | 331 | +0.187 | 2.28 | 147 | +0.085 | +12.5 | 39 |
| piv8 tol0.6 depth2.0 B+Retest 2R trend:sma exit:single | shorts | 100 | +0.327 | 2.18 | 51 | -0.183 | -9.3 | 29 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B | longs | 236 | +0.043 | -0.021 | 47 | 65 |
| B | both | 300 | +0.020 | -0.164 | 1 | 114 |
| RetestConf | longs | 173 | +0.010 | +0.075 | 76 | 60 |
| B | shorts | 236 | -0.013 | -0.281 | 0 | 66 |
| B+Retest | shorts | 299 | -0.019 | -0.315 | 0 | 104 |
| B+Retest | longs | 297 | -0.023 | -0.023 | 48 | 103 |
| B+Retest | both | 324 | -0.023 | -0.183 | 1 | 199 |
| RetestConf | both | 281 | -0.035 | -0.119 | 10 | 92 |
| RetestConf | shorts | 175 | -0.062 | -0.282 | 1 | 57 |
| Retest | both | 296 | -0.071 | -0.164 | 3 | 112 |
| Retest | shorts | 214 | -0.074 | -0.315 | 0 | 64 |
| Retest | longs | 198 | -0.075 | +0.013 | 47 | 67 |
| B+Mid | longs | 285 | -0.090 | -0.103 | 21 | 88 |
| B+Mid | both | 324 | -0.112 | -0.241 | 0 | 174 |
| B+Mid | shorts | 293 | -0.128 | -0.344 | 0 | 93 |

### S/R Flip

864 settings × 3 sides tested; 1806 combinations had ≥80 IS trades, 1% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.61. Average OOS result of the top-20 IS picks: -0.283 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.202 R/trade over 43 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 rejection 3R tries3 levels:htf:D trend:sma exit:single | shorts | 98 | +0.156 | 0.80 | 43 | -0.254 | -10.9 | 26 |
| piv8 rejection 2R tries3 levels:htf:D trend:sma exit:single | shorts | 99 | +0.011 | 0.07 | 43 | -0.371 | -15.9 | 30 |
| piv8 sweep 1.5R tries3 levels:htf:D trend:off exit:single | shorts | 81 | -0.009 | -0.06 | 31 | -0.391 | -12.1 | 35 |
| piv8 rejection 3R tries3 levels:htf:D trend:sma exit:TP1 1R 50% BE | shorts | 95 | -0.014 | -0.11 | 41 | -0.329 | -13.5 | 44 |
| piv8 rejection 1.5R tries3 levels:htf:D trend:sma exit:TP1 1R 50% BE | shorts | 96 | -0.044 | -0.36 | 41 | -0.370 | -15.2 | 44 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| sweep · levels htf:D | shorts | 6 | -0.009 | -0.391 | 0 | 31 |
| rejection · levels htf:D | shorts | 36 | -0.010 | -0.353 | 0 | 42 |
| sweep · levels htf:D | both | 72 | -0.198 | -0.333 | 0 | 74 |
| rejection · levels htf:D | both | 72 | -0.229 | -0.349 | 0 | 92 |
| sweep · levels chart | shorts | 72 | -0.281 | -0.386 | 0 | 216 |
| sweep · levels chart+D | shorts | 72 | -0.288 | -0.287 | 1 | 123 |
| rejection · levels chart+D | shorts | 72 | -0.288 | -0.263 | 1 | 162 |
| sweep · levels htf:D | longs | 36 | -0.318 | -0.285 | 0 | 48 |
| sweep · levels chart+D | both | 72 | -0.323 | -0.322 | 0 | 277 |
| rejection · levels chart+D | both | 72 | -0.325 | -0.322 | 0 | 352 |
| rejection · levels htf:D | longs | 72 | -0.346 | -0.367 | 0 | 53 |
| sweep · levels chart | both | 72 | -0.351 | -0.386 | 0 | 472 |
| sweep · levels chart+D | longs | 72 | -0.354 | -0.353 | 0 | 150 |
| rejection · levels chart+D | longs | 72 | -0.356 | -0.374 | 0 | 190 |
| touch · levels htf:D | shorts | 72 | -0.367 | -0.362 | 0 | 62 |
| rejection · levels chart | shorts | 72 | -0.367 | -0.334 | 0 | 276 |
| rejection · levels chart | both | 72 | -0.387 | -0.395 | 0 | 598 |
| rejection · levels chart | longs | 72 | -0.403 | -0.447 | 0 | 322 |
| sweep · levels chart | longs | 72 | -0.410 | -0.385 | 0 | 258 |
| touch · levels htf:D | both | 72 | -0.463 | -0.379 | 0 | 136 |
| touch · levels chart+D | shorts | 72 | -0.474 | -0.515 | 0 | 256 |
| touch · levels chart | longs | 72 | -0.489 | -0.612 | 0 | 524 |
| touch · levels chart | both | 72 | -0.519 | -0.563 | 0 | 978 |
| touch · levels chart+D | both | 72 | -0.528 | -0.490 | 0 | 531 |
| touch · levels htf:D | longs | 72 | -0.543 | -0.394 | 0 | 74 |
| touch · levels chart | shorts | 72 | -0.551 | -0.508 | 0 | 466 |
| touch · levels chart+D | longs | 72 | -0.575 | -0.468 | 0 | 274 |

### Megaphone

1056 settings × 3 sides tested; 1259 combinations had ≥80 IS trades, 10% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.57. Average OOS result of the top-20 IS picks: -0.055 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.107 R/trade over 64 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 swings4 expand0.5 BO-close measured trend:off exit:single | longs | 119 | +1.383 | 2.75 | 64 | -0.264 | -16.9 | 16 |
| piv5 swings4 expand0.5 BO-close measured trend:sma exit:single | longs | 111 | +1.455 | 2.73 | 60 | -0.187 | -11.2 | 17 |
| piv3 swings4 expand0.5 BO-close measured trend:off exit:single | both | 278 | +0.636 | 2.73 | 134 | +0.095 | +12.8 | 19 |
| piv3 swings4 expand0.5 BO-close measured trend:sma exit:single | both | 237 | +0.710 | 2.72 | 123 | +0.148 | +18.2 | 20 |
| piv8 swings4 expand0.0 BO-close measured trend:sma exit:single | both | 226 | +0.987 | 2.59 | 112 | -0.100 | -11.2 | 18 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| BO-close | longs | 103 | +0.186 | -0.326 | 6 | 66 |
| BO-close | both | 128 | +0.159 | -0.357 | 3 | 121 |
| BO-close | shorts | 86 | -0.106 | -0.354 | 2 | 62 |
| failedBO | shorts | 16 | -0.211 | -0.337 | 0 | 71 |
| fade-rejection | shorts | 75 | -0.227 | -0.532 | 0 | 71 |
| failedBO | longs | 16 | -0.272 | +0.066 | 88 | 58 |
| BO-retest | longs | 79 | -0.278 | -0.479 | 6 | 61 |
| fade-rejection | both | 110 | -0.287 | -0.512 | 2 | 110 |
| BO-retest | both | 112 | -0.326 | -0.533 | 5 | 98 |
| failedBO | both | 56 | -0.338 | -0.166 | 12 | 74 |
| fade-rejection | longs | 70 | -0.366 | -0.494 | 4 | 82 |
| BO-retest | shorts | 63 | -0.378 | -0.643 | 0 | 69 |
| fade-touch | longs | 110 | -0.539 | -0.578 | 1 | 88 |
| fade-touch | both | 145 | -0.549 | -0.601 | 2 | 162 |
| fade-touch | shorts | 90 | -0.628 | -0.728 | 0 | 122 |


## 4-hour  (IS 2016-01-01 → 2023-08-03, OOS 2023-08-03 → 2026-11-03; BTC buy & hold: IS +6640%, OOS +164%)

### Double Top / Bottom

1620 settings × 3 sides tested; 751 combinations had ≥50 IS trades, 63% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.13. Average OOS result of the top-20 IS picks: +0.066 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.146 R/trade over 27 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 tol1.0 depth0.5 B+Retest 3R trend:sma exit:TP1 1R 50% BE | longs | 51 | +0.472 | 2.50 | 27 | -0.053 | -1.4 | 41 |
| piv3 tol1.0 depth1.0 B+Retest 3R trend:sma exit:TP1 1R 50% BE | longs | 50 | +0.444 | 2.33 | 27 | -0.053 | -1.4 | 41 |
| piv3 tol1.0 depth0.5 B+Retest 3R trend:off exit:single | longs | 56 | +0.587 | 2.22 | 31 | +0.109 | +3.4 | 29 |
| piv8 tol1.0 depth0.5 B+Retest 2R trend:sma exit:TP1 1R 50% BE | longs | 52 | +0.336 | 2.09 | 28 | +0.105 | +2.9 | 50 |
| piv3 tol1.0 depth0.5 B+Retest 2R trend:sma exit:TP1 1R 50% BE | longs | 50 | +0.338 | 2.08 | 29 | -0.135 | -3.9 | 38 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| B+Retest | longs | 76 | +0.158 | +0.159 | 61 | 30 |
| B | both | 99 | +0.134 | +0.100 | 64 | 28 |
| B+Retest | both | 210 | +0.087 | +0.139 | 73 | 44 |
| B+Mid | longs | 27 | +0.039 | +0.155 | 93 | 30 |
| B+Mid | both | 169 | -0.011 | +0.155 | 82 | 40 |
| B+Retest | shorts | 63 | -0.038 | -0.047 | 38 | 24 |
| RetestConf | both | 19 | -0.038 | +0.145 | 95 | 29 |
| Retest | both | 60 | -0.053 | +0.121 | 88 | 30 |
| B+Mid | shorts | 28 | -0.099 | +0.047 | 57 | 22 |

### S/R Flip

864 settings × 3 sides tested; 1931 combinations had ≥50 IS trades, 20% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.35. Average OOS result of the top-20 IS picks: -0.212 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.194 R/trade over 72 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | both | 131 | +0.138 | 1.44 | 72 | -0.148 | -10.7 | 46 |
| piv5 rejection 3R tries1 levels:htf:D trend:off exit:TP1 1R 50% BE | both | 141 | +0.118 | 1.30 | 77 | -0.179 | -13.8 | 45 |
| piv5 rejection 3R tries1 levels:htf:D trend:sma exit:TP1 1R 50% BE | longs | 75 | +0.168 | 1.24 | 47 | -0.148 | -7.0 | 47 |
| piv3 sweep 2R tries1 levels:chart trend:sma exit:single | longs | 141 | +0.147 | 1.15 | 64 | -0.263 | -16.9 | 31 |
| piv3 sweep 2R tries3 levels:chart trend:sma exit:single | longs | 159 | +0.135 | 1.13 | 76 | -0.289 | -22.0 | 30 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| rejection · levels htf:D | longs | 72 | +0.057 | -0.165 | 8 | 54 |
| rejection · levels htf:D | both | 72 | +0.036 | -0.181 | 0 | 83 |
| sweep · levels htf:D | longs | 72 | +0.024 | -0.042 | 38 | 48 |
| sweep · levels chart | longs | 72 | +0.010 | -0.258 | 0 | 68 |
| rejection · levels htf:D | shorts | 72 | +0.007 | -0.204 | 8 | 29 |
| rejection · levels chart+D | longs | 72 | +0.004 | -0.248 | 1 | 63 |
| rejection · levels chart | longs | 72 | -0.015 | -0.248 | 0 | 82 |
| sweep · levels chart+D | longs | 72 | -0.029 | -0.202 | 3 | 52 |
| sweep · levels htf:D | both | 72 | -0.030 | -0.054 | 29 | 70 |
| rejection · levels chart | both | 72 | -0.060 | -0.270 | 0 | 155 |
| sweep · levels htf:D | shorts | 51 | -0.079 | -0.057 | 29 | 23 |
| rejection · levels chart+D | both | 72 | -0.079 | -0.209 | 0 | 105 |
| sweep · levels chart | both | 72 | -0.081 | -0.269 | 0 | 124 |
| touch · levels chart | longs | 72 | -0.084 | -0.277 | 0 | 129 |
| sweep · levels chart+D | both | 72 | -0.084 | -0.206 | 0 | 84 |
| touch · levels htf:D | shorts | 72 | -0.096 | -0.307 | 0 | 52 |
| touch · levels chart | both | 72 | -0.096 | -0.321 | 0 | 250 |
| touch · levels chart | shorts | 72 | -0.109 | -0.370 | 0 | 119 |
| touch · levels chart+D | longs | 72 | -0.110 | -0.305 | 0 | 88 |
| touch · levels htf:D | both | 72 | -0.114 | -0.329 | 0 | 126 |
| rejection · levels chart | shorts | 72 | -0.117 | -0.292 | 0 | 70 |
| touch · levels chart+D | both | 72 | -0.127 | -0.321 | 0 | 167 |
| touch · levels htf:D | longs | 72 | -0.129 | -0.345 | 0 | 74 |
| touch · levels chart+D | shorts | 72 | -0.146 | -0.341 | 0 | 78 |
| sweep · levels chart+D | shorts | 68 | -0.151 | -0.204 | 9 | 32 |
| rejection · levels chart+D | shorts | 72 | -0.188 | -0.148 | 14 | 41 |
| sweep · levels chart | shorts | 72 | -0.194 | -0.281 | 0 | 54 |
| touch · levels htf:W | both | 12 | -0.759 | -0.489 | 0 | 29 |

### Megaphone

1056 settings × 3 sides tested; 455 combinations had ≥50 IS trades, 32% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.58. Average OOS result of the top-20 IS picks: +0.018 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.184 R/trade over 30 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv5 swings4 expand0.0 BO-close 2R trend:off exit:single | longs | 60 | +0.606 | 3.09 | 30 | +0.063 | +1.9 | 40 |
| piv5 swings4 expand0.0 BO-close 3R trend:off exit:single | longs | 59 | +0.754 | 2.85 | 30 | +0.196 | +5.9 | 33 |
| piv5 swings4 expand0.0 BO-close 1.5R trend:off exit:single | longs | 61 | +0.414 | 2.58 | 30 | -0.054 | -1.6 | 43 |
| piv5 swings4 expand0.0 BO-close 3R trend:off exit:single | both | 93 | +0.507 | 2.46 | 56 | +0.073 | +4.1 | 30 |
| piv5 swings4 expand0.0 BO-close 2R trend:sma exit:single | longs | 50 | +0.534 | 2.45 | 27 | -0.025 | -0.7 | 37 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| BO-close | longs | 28 | +1.074 | +0.063 | 64 | 33 |
| BO-close | both | 74 | +0.920 | -0.077 | 26 | 35 |
| BO-retest | both | 44 | +0.649 | -0.349 | 0 | 41 |
| BO-retest | longs | 7 | +0.533 | -0.114 | 14 | 32 |
| BO-close | shorts | 6 | +0.261 | -0.119 | 17 | 32 |
| failedBO | both | 6 | -0.092 | -0.553 | 0 | 35 |
| fade-touch | longs | 47 | -0.096 | -0.590 | 0 | 35 |
| fade-rejection | both | 69 | -0.135 | -0.649 | 0 | 39 |
| fade-touch | both | 80 | -0.228 | -0.714 | 2 | 60 |
| fade-rejection | longs | 24 | -0.246 | -0.500 | 0 | 30 |
| fade-rejection | shorts | 10 | -0.261 | -0.502 | 0 | 37 |
| fade-touch | shorts | 60 | -0.303 | -0.814 | 0 | 39 |


## Daily  (IS 2015-07-20 → 2023-06-15, OOS 2023-06-15 → 2026-11-03; BTC buy & hold: IS +9032%, OOS +201%)

### Double Top / Bottom

No configuration reached 15 IS trades.

### S/R Flip

864 settings × 3 sides tested; 1224 combinations had ≥15 IS trades, 64% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.05. Average OOS result of the top-20 IS picks: -0.116 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.089 R/trade over 10 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv8 rejection 1.5R tries1 levels:chart trend:sma exit:single | longs | 21 | +0.597 | 2.26 | 10 | -0.319 | -3.2 | 30 |
| piv8 rejection 2R tries1 levels:chart trend:sma exit:TP1 1R 50% BE | both | 26 | +0.564 | 2.25 | 13 | -0.026 | -0.3 | 54 |
| piv3 sweep 1.5R tries3 levels:chart+W merged>=2 trend:sma exit:single | longs | 16 | +0.660 | 2.23 | 9 | -0.242 | -2.2 | 33 |
| piv8 rejection 1.5R tries1 levels:chart trend:sma exit:TP1 1R 50% BE | both | 26 | +0.536 | 2.19 | 13 | -0.047 | -0.6 | 54 |
| piv8 rejection 2R tries1 levels:chart trend:sma exit:TP1 1R 50% BE | longs | 21 | +0.538 | 2.16 | 10 | +0.037 | +0.4 | 60 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| sweep · levels chart | longs | 72 | +0.434 | -0.050 | 40 | 15 |
| rejection · levels htf:W | longs | 36 | +0.358 | +0.048 | 67 | 6 |
| sweep · levels chart+W | longs | 30 | +0.353 | -0.292 | 7 | 8 |
| sweep · levels chart+W | both | 60 | +0.343 | -0.211 | 15 | 7 |
| rejection · levels chart | longs | 72 | +0.340 | -0.181 | 21 | 17 |
| sweep · levels chart | both | 72 | +0.314 | -0.105 | 24 | 19 |
| sweep · levels htf:W | both | 54 | +0.312 | -0.145 | 33 | 5 |
| rejection · levels chart+W | longs | 54 | +0.289 | -0.246 | 24 | 8 |
| sweep · levels htf:W | longs | 18 | +0.273 | -0.159 | 33 | 5 |
| rejection · levels chart | both | 72 | +0.267 | -0.138 | 15 | 24 |
| rejection · levels htf:W | both | 72 | +0.245 | +0.024 | 58 | 8 |
| rejection · levels chart+W | both | 72 | +0.231 | -0.189 | 25 | 10 |
| sweep · levels chart | shorts | 12 | +0.078 | +0.005 | 33 | 11 |
| touch · levels chart | longs | 72 | +0.050 | -0.041 | 38 | 23 |
| rejection · levels chart | shorts | 30 | +0.049 | -0.043 | 40 | 12 |
| touch · levels chart | both | 72 | -0.115 | -0.187 | 11 | 38 |
| touch · levels htf:W | longs | 72 | -0.115 | +0.347 | 96 | 8 |
| touch · levels chart+W | longs | 72 | -0.137 | +0.414 | 97 | 9 |
| touch · levels htf:W | both | 72 | -0.214 | +0.171 | 79 | 11 |
| touch · levels chart+W | both | 72 | -0.240 | +0.127 | 67 | 14 |
| touch · levels chart | shorts | 66 | -0.432 | -0.418 | 0 | 16 |

### Megaphone

1056 settings × 3 sides tested; 172 combinations had ≥15 IS trades, 38% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.03. Average OOS result of the top-20 IS picks: +0.849 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.173 R/trade over 10 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| piv3 swings4 expand0.0 BO-close 1.5R trend:sma exit:single | both | 16 | +0.988 | 3.89 | 10 | +0.693 | +6.9 | 70 |
| piv3 swings4 expand0.5 BO-close 1.5R trend:off exit:single | both | 15 | +0.950 | 3.53 | 8 | +0.829 | +6.6 | 75 |
| piv3 swings4 expand0.0 BO-close 1.5R trend:off exit:single | longs | 17 | +0.855 | 3.19 | 8 | +0.507 | +4.1 | 62 |
| piv3 swings4 expand0.0 BO-close 1.5R trend:off exit:single | both | 24 | +0.721 | 3.02 | 11 | +0.531 | +5.8 | 64 |
| piv3 swings4 expand0.5 BO-close 1.5R trend:off exit:TP1 1R 50% BE | both | 15 | +0.700 | 2.53 | 8 | +0.806 | +6.4 | 88 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| BO-retest | both | 8 | +1.104 | +0.985 | 100 | 6 |
| BO-close | longs | 7 | +0.858 | +1.043 | 100 | 8 |
| BO-close | both | 20 | +0.743 | +1.240 | 100 | 10 |
| BO-retest | longs | 6 | +0.377 | +0.138 | 67 | 3 |
| fade-touch | longs | 14 | -0.071 | +0.072 | 57 | 10 |
| fade-rejection | both | 27 | -0.153 | +0.053 | 63 | 12 |
| fade-touch | both | 65 | -0.241 | -0.084 | 38 | 13 |
| fade-touch | shorts | 25 | -0.413 | -0.128 | 40 | 15 |


## Conclusions (written after the sweep)

**Typical-settings check** (not the single best — ordinary middle-of-the-grid settings, random benchmark with 60 samples per trade):

| TF | Strategy | Settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|
| 4h | Double Top / Bottom | piv5 tol0.6 depth1.0 B+Retest 2R | both | 103 | +0.144 | 48 | +0.324 | -0.084 |
| 4h | Double Top / Bottom | piv5 tol0.6 depth1.0 B+Mid 2R | both | 88 | +0.090 | 42 | +0.284 | -0.049 |
| 4h | Double Top / Bottom | piv5 tol0.6 depth1.0 B 2R | both | 56 | +0.240 | 26 | +0.338 | -0.060 |
| 4h | Megaphone | piv5 swings4 BO-close 3R | longs | 59 | +0.754 | 30 | +0.196 | -0.027 |
| 4h | Megaphone | piv5 swings4 BO-close 2R | longs | 60 | +0.606 | 30 | +0.063 | -0.060 |
| 4h | Megaphone | piv3 swings4 BO-close 2R | both | 135 | +0.183 | 71 | -0.088 | -0.148 |
| 1d | Megaphone | piv3 swings4 BO-close 2R | both | 23 | +0.514 | 11 | +0.849 | -0.149 |

1. **15-minute: nothing works after costs.** With 0.1% per side, the fees on tight intraday stops cost more than any pattern earns. Every family lost money in-sample and out-of-sample for all three strategies.
2. **1-hour: nothing robust.** A few single settings looked good in-sample but did not hold up.
3. **S/R Flip: no profitable BTC configuration on any timeframe** once costs and the held-out period are considered.
4. **Best overall: Double Top / Bottom on 4h, both directions, single 2R target.** Most entry families and ~60–95% of their variants were profitable out-of-sample; ordinary settings were positive in both periods and beat random entries by ~0.35 R/trade OOS. Caveat: only ~25–50 OOS trades per setting, and the OOS profit came mainly from longs during a rising market (shorts were positive IS, negative OOS).
5. **Runner-up: Megaphone breakout at the close (4h and daily), longs.** Strongly positive in-sample and beat random OOS, but results vary a lot between neighbouring settings on 4h, and the daily sample is tiny (5–11 OOS trades).
6. Scaling out (TP1 1R 50% + breakeven) did not beat a single target in the top results.
