# AVAX strategy sweep — 15m / 1h / 4h / 1D

Costs: futures fees: taker 0.035% on entry, exit maker 0.014% at target / taker 0.035% at stop, funding 0.010% per 8 h (longs pay, shorts receive), charged in R. In-sample (IS) = first 70% of each timeframe's history, out-of-sample (OOS) = last 30%. Rankings use IS only. Data: Coinbase AVAX-USD (4h resampled from 1h).


## Summary A — best entry family per strategy and timeframe (chosen on IS only)

| TF | Strategy | Best family (by IS) | Family IS avg R | Family OOS avg R | % variants OOS > 0 | Top IS settings in that family | OOS n | OOS avg R | Random OOS |
|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan3ATR · fold0.5 (longs) | -0.038 | -0.226 | 0 | fan3ATR stacked20 lookback50 fold0.5 stop1.5ATR 1.5R | 114 | -0.152 | -0.130 |
| 1h | Accordion / EMA Fan | fan3ATR · fold0.7 (both) | +0.063 | -0.244 | 0 | fan3ATR stacked20 lookback100 fold0.7 stop0.5ATR 1.5R | 59 | -0.348 | -0.126 |
| 4h | Accordion / EMA Fan | fan2ATR · fold0.7 (both) | +0.184 | -0.099 | 35 | fan2ATR stacked20 lookback50 fold0.7 stop1.5ATR 3R | 22 | -0.292 | +0.033 |

## Summary B — single #1 in-sample settings (more prone to luck)

| TF | Strategy | Best IS settings | Side | IS n | IS avg R | OOS n | OOS avg R | Random OOS | OOS edge | Top-20 OOS avg | IS→OOS ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | Accordion / EMA Fan | fan3ATR stacked20 lookback50 fold0.5 stop1.5ATR 1.5R | longs | 255 | +0.113 | 114 | -0.152 | -0.130 | -0.021 | -0.074 | +0.46 |
| 1h | Accordion / EMA Fan | fan3ATR stacked10 lookback100 fold0.7 stop0.5ATR 1.5R | longs | 91 | +0.304 | 32 | -0.162 | -0.233 | +0.072 | -0.124 | -0.16 |
| 4h | Accordion / EMA Fan | fan2ATR stacked20 lookback50 fold0.7 stop1.5ATR 3R | both | 78 | +0.586 | 22 | -0.292 | +0.033 | -0.325 | -0.123 | -0.24 |


## 15-minute  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 864 combinations had ≥120 IS trades, 17% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): +0.46. Average OOS result of the top-20 IS picks: -0.074 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.130 R/trade over 114 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan3ATR stacked20 lookback50 fold0.5 stop1.5ATR 1.5R | longs | 255 | +0.113 | 1.43 | 114 | -0.152 | -17.3 | 37 |
| fan2ATR stacked10 lookback50 fold0.7 stop2ATR 3R | shorts | 608 | +0.104 | 1.41 | 302 | +0.126 | +38.1 | 30 |
| fan3ATR stacked20 lookback100 fold0.5 stop1.5ATR 1.5R | longs | 256 | +0.108 | 1.37 | 115 | -0.160 | -18.4 | 37 |
| fan3ATR stacked20 lookback100 fold0.7 stop1.5ATR 1.5R | longs | 256 | +0.107 | 1.36 | 116 | -0.175 | -20.3 | 36 |
| fan2ATR stacked10 lookback100 fold0.7 stop2ATR 3R | shorts | 611 | +0.099 | 1.34 | 304 | +0.132 | +40.0 | 30 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan3ATR · fold0.5 | longs | 48 | -0.038 | -0.226 | 0 | 130 |
| fan2ATR · fold0.7 | shorts | 48 | -0.040 | -0.065 | 29 | 266 |
| fan3ATR · fold0.7 | longs | 48 | -0.049 | -0.240 | 0 | 132 |
| fan3ATR · fold0.7 | both | 48 | -0.053 | -0.152 | 8 | 279 |
| fan3ATR · fold0.7 | shorts | 48 | -0.057 | -0.073 | 33 | 146 |
| fan3ATR · fold0.3 | longs | 48 | -0.063 | -0.158 | 0 | 120 |
| fan3ATR · fold0.5 | both | 48 | -0.082 | -0.139 | 8 | 276 |
| fan2ATR · fold0.7 | both | 48 | -0.082 | -0.146 | 2 | 499 |
| fan2ATR · fold0.5 | shorts | 48 | -0.085 | -0.083 | 44 | 257 |
| fan3ATR · fold0.3 | both | 48 | -0.092 | -0.130 | 12 | 256 |
| fan2ATR · fold0.5 | both | 48 | -0.095 | -0.136 | 6 | 484 |
| fan2ATR · fold0.5 | longs | 48 | -0.104 | -0.196 | 0 | 227 |
| fan2ATR · fold0.3 | shorts | 48 | -0.107 | -0.125 | 19 | 230 |
| fan2ATR · fold0.3 | both | 48 | -0.122 | -0.140 | 4 | 431 |
| fan3ATR · fold0.3 | shorts | 48 | -0.122 | -0.105 | 27 | 136 |
| fan2ATR · fold0.7 | longs | 48 | -0.126 | -0.237 | 0 | 234 |
| fan3ATR · fold0.5 | shorts | 48 | -0.127 | -0.061 | 48 | 145 |
| fan2ATR · fold0.3 | longs | 48 | -0.138 | -0.158 | 0 | 202 |


## 1-hour  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 678 combinations had ≥80 IS trades, 32% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.16. Average OOS result of the top-20 IS picks: -0.124 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): -0.233 R/trade over 32 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan3ATR stacked10 lookback100 fold0.7 stop0.5ATR 1.5R | longs | 91 | +0.304 | 2.04 | 32 | -0.162 | -5.2 | 38 |
| fan2ATR stacked10 lookback50 fold0.5 stop2ATR 2R | shorts | 171 | +0.213 | 1.87 | 73 | -0.154 | -11.2 | 29 |
| fan2ATR stacked10 lookback100 fold0.5 stop2ATR 2R | shorts | 172 | +0.206 | 1.81 | 74 | -0.125 | -9.2 | 30 |
| fan2ATR stacked10 lookback50 fold0.5 stop2ATR 1.5R | shorts | 174 | +0.163 | 1.70 | 74 | +0.029 | +2.1 | 42 |
| fan2ATR stacked10 lookback100 fold0.5 stop2ATR 1.5R | shorts | 175 | +0.156 | 1.64 | 76 | +0.067 | +5.1 | 43 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan3ATR · fold0.7 | both | 48 | +0.063 | -0.244 | 0 | 67 |
| fan3ATR · fold0.5 | both | 48 | +0.038 | -0.171 | 8 | 66 |
| fan3ATR · fold0.5 | shorts | 10 | +0.036 | -0.202 | 30 | 46 |
| fan2ATR · fold0.5 | shorts | 48 | +0.031 | -0.093 | 29 | 65 |
| fan3ATR · fold0.7 | longs | 24 | +0.028 | -0.124 | 8 | 32 |
| fan3ATR · fold0.7 | shorts | 20 | +0.017 | -0.319 | 0 | 46 |
| fan2ATR · fold0.7 | shorts | 48 | -0.016 | -0.179 | 2 | 67 |
| fan3ATR · fold0.5 | longs | 24 | -0.038 | -0.078 | 8 | 32 |
| fan2ATR · fold0.5 | both | 48 | -0.049 | -0.131 | 8 | 114 |
| fan2ATR · fold0.7 | both | 48 | -0.063 | -0.161 | 0 | 118 |
| fan3ATR · fold0.3 | both | 48 | -0.070 | -0.153 | 17 | 65 |
| fan2ATR · fold0.3 | shorts | 48 | -0.072 | -0.003 | 52 | 62 |
| fan2ATR · fold0.7 | longs | 48 | -0.115 | -0.137 | 4 | 51 |
| fan3ATR · fold0.3 | longs | 24 | -0.136 | -0.111 | 21 | 30 |
| fan2ATR · fold0.5 | longs | 48 | -0.136 | -0.181 | 0 | 49 |
| fan2ATR · fold0.3 | both | 48 | -0.144 | -0.084 | 17 | 108 |
| fan2ATR · fold0.3 | longs | 48 | -0.221 | -0.197 | 4 | 46 |


## 4-hour  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -66%, OOS -61%)

### Accordion / EMA Fan

432 settings × 3 sides tested; 188 combinations had ≥50 IS trades, 76% of them were profitable in-sample after costs. IS→OOS rank correlation (Spearman): -0.24. Average OOS result of the top-20 IS picks: -0.123 R/trade.

Random-entry benchmark for the #1 pick (OOS window, same direction/stop/R:R/costs): +0.033 R/trade over 22 mirrored trades.

| Settings | Side | IS trades | IS avg R (net) | IS t-stat | OOS trades | OOS avg R (net) | OOS total R | OOS win % |
|---|---|---|---|---|---|---|---|---|
| fan2ATR stacked20 lookback50 fold0.7 stop1.5ATR 3R | both | 78 | +0.586 | 2.61 | 22 | -0.292 | -6.4 | 18 |
| fan2ATR stacked20 lookback100 fold0.7 stop1.5ATR 3R | both | 79 | +0.566 | 2.54 | 22 | -0.292 | -6.4 | 18 |
| fan2ATR stacked10 lookback100 fold0.7 stop1.5ATR 3R | both | 100 | +0.432 | 2.23 | 33 | -0.163 | -5.4 | 21 |
| fan2ATR stacked20 lookback100 fold0.3 stop1.5ATR 3R | both | 65 | +0.532 | 2.18 | 21 | -0.058 | -1.2 | 24 |
| fan2ATR stacked10 lookback50 fold0.7 stop1.5ATR 3R | both | 98 | +0.420 | 2.15 | 32 | -0.136 | -4.4 | 22 |

Families (all eligible variants of each entry type averaged — less prone to luck than the single best):

| Family | Side | Variants | IS avg R | OOS avg R | % variants OOS > 0 | Median OOS trades |
|---|---|---|---|---|---|---|
| fan2ATR · fold0.7 | both | 48 | +0.184 | -0.099 | 35 | 26 |
| fan2ATR · fold0.3 | both | 48 | +0.169 | -0.110 | 21 | 25 |
| fan2ATR · fold0.7 | shorts | 22 | +0.150 | -0.063 | 64 | 21 |
| fan2ATR · fold0.5 | shorts | 22 | +0.098 | +0.148 | 86 | 20 |
| fan2ATR · fold0.5 | both | 48 | +0.084 | -0.142 | 19 | 26 |


## Daily  (IS 2021-09-30 → 2025-04-25, OOS 2025-04-25 → 2026-11-04; AVAX buy & hold: IS -67%, OOS -61%)

### Accordion / EMA Fan

No configuration reached 15 IS trades.

