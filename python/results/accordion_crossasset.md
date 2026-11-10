# Cross-asset check — accordion: settings picked on BTC (in-sample only), tested on ETH, AVAX, XRP

Net of 0.20% round-trip costs. 'Full' = every trade in that asset's history (none of it was used to pick the settings). R = average net R per trade (n = trades).


## 15m

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| fan3ATR stacked20 lookback100 fold0.5 stop2ATR 1.5R | shorts | +0.165 (n=215) | -0.049 (n=119) | -0.032 (n=357) | -0.097 (n=379) | +0.085 (n=168) | 1/4 |
| fan3ATR stacked20 lookback50 fold0.5 stop2ATR 1.5R | shorts | +0.165 (n=213) | -0.040 (n=118) | -0.042 (n=353) | -0.105 (n=377) | +0.085 (n=168) | 1/4 |
| fan3ATR stacked10 lookback100 fold0.5 stop2ATR 1.5R | shorts | +0.131 (n=263) | -0.107 (n=146) | -0.029 (n=424) | -0.067 (n=456) | +0.022 (n=210) | 1/4 |
| fan3ATR stacked10 lookback50 fold0.5 stop2ATR 1.5R | shorts | +0.131 (n=261) | -0.092 (n=144) | -0.041 (n=419) | -0.072 (n=453) | +0.027 (n=209) | 1/4 |
| fan3ATR stacked10 lookback100 fold0.5 stop2ATR 2R | shorts | +0.152 (n=263) | -0.045 (n=145) | -0.060 (n=424) | -0.093 (n=456) | +0.062 (n=210) | 1/4 |
| fan3ATR stacked10 lookback50 fold0.5 stop2ATR 2R | shorts | +0.149 (n=261) | -0.038 (n=144) | -0.077 (n=419) | -0.100 (n=453) | +0.068 (n=209) | 1/4 |
| fan3ATR stacked20 lookback100 fold0.7 stop2ATR 1.5R | shorts | +0.134 (n=216) | -0.046 (n=121) | -0.069 (n=360) | -0.090 (n=383) | +0.152 (n=169) | 1/4 |
| fan3ATR stacked20 lookback100 fold0.5 stop2ATR 2R | shorts | +0.157 (n=215) | +0.010 (n=119) | -0.057 (n=357) | -0.096 (n=379) | +0.148 (n=168) | 2/4 |
| fan3ATR stacked20 lookback50 fold0.5 stop2ATR 2R | shorts | +0.154 (n=213) | +0.020 (n=118) | -0.071 (n=353) | -0.107 (n=377) | +0.148 (n=168) | 2/4 |
| fan3ATR stacked20 lookback50 fold0.7 stop2ATR 1.5R | shorts | +0.128 (n=215) | -0.046 (n=121) | -0.069 (n=360) | -0.094 (n=382) | +0.152 (n=169) | 1/4 |

Entry families on 15m (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| fan2ATR · fold0.3 | -0.203 (0%) | -0.187 (0%) | -0.128 (2%) | -0.155 (8%) |
| fan2ATR · fold0.5 | -0.165 (0%) | -0.146 (0%) | -0.108 (6%) | -0.118 (4%) |
| fan2ATR · fold0.7 | -0.158 (0%) | -0.147 (0%) | -0.102 (4%) | -0.089 (8%) |
| fan3ATR · fold0.3 | -0.159 (0%) | -0.166 (0%) | -0.105 (6%) | -0.163 (8%) |
| fan3ATR · fold0.5 | -0.124 (6%) | -0.110 (4%) | -0.101 (0%) | -0.093 (21%) |
| fan3ATR · fold0.7 | -0.130 (0%) | -0.109 (8%) | -0.086 (0%) | -0.090 (25%) |
| fan5ATR · fold0.3 | +0.103 (88%) | -0.239 (25%) | -0.130 (10%) | – |
| fan5ATR · fold0.5 | +0.031 (83%) | -0.039 (54%) | -0.258 (0%) | – |
| fan5ATR · fold0.7 | -0.141 (12%) | +0.005 (58%) | -0.282 (0%) | – |


## 1h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| fan3ATR stacked20 lookback50 fold0.5 stop1ATR 1.5R | longs | +0.232 (n=199) | -0.014 (n=66) | -0.002 (n=232) | -0.003 (n=93) | +0.023 (n=44) | 1/4 |
| fan3ATR stacked20 lookback50 fold0.5 stop1ATR 2R | longs | +0.264 (n=199) | -0.120 (n=66) | -0.011 (n=232) | -0.087 (n=93) | -0.106 (n=44) | 0/4 |
| fan3ATR stacked20 lookback50 fold0.5 stop2ATR 2R | both | +0.204 (n=316) | -0.155 (n=113) | +0.099 (n=386) | +0.003 (n=196) | -0.197 (n=90) | 2/4 |
| fan3ATR stacked20 lookback100 fold0.5 stop1ATR 1.5R | longs | +0.218 (n=203) | -0.011 (n=68) | +0.017 (n=234) | -0.003 (n=93) | +0.023 (n=44) | 2/4 |
| fan3ATR stacked20 lookback100 fold0.5 stop1ATR 2R | longs | +0.252 (n=203) | -0.152 (n=68) | +0.010 (n=234) | -0.087 (n=93) | -0.106 (n=44) | 1/4 |
| fan3ATR stacked20 lookback50 fold0.7 stop1ATR 2R | longs | +0.235 (n=203) | -0.261 (n=70) | +0.030 (n=237) | -0.065 (n=94) | +0.007 (n=45) | 2/4 |
| fan3ATR stacked20 lookback50 fold0.5 stop2ATR 2R | longs | +0.234 (n=199) | -0.031 (n=66) | +0.059 (n=232) | -0.153 (n=92) | -0.221 (n=44) | 1/4 |
| fan3ATR stacked20 lookback100 fold0.7 stop1ATR 2R | longs | +0.231 (n=206) | -0.261 (n=70) | +0.038 (n=238) | -0.065 (n=94) | +0.007 (n=45) | 2/4 |
| fan3ATR stacked20 lookback50 fold0.7 stop1ATR 1.5R | longs | +0.195 (n=203) | -0.147 (n=70) | +0.007 (n=237) | +0.047 (n=94) | +0.112 (n=45) | 3/4 |
| fan3ATR stacked20 lookback50 fold0.7 stop1.5ATR 1.5R | longs | +0.191 (n=203) | -0.261 (n=70) | +0.024 (n=237) | -0.106 (n=94) | -0.042 (n=45) | 1/4 |

Entry families on 1h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| fan2ATR · fold0.3 | -0.045 (27%) | -0.050 (21%) | -0.126 (0%) | -0.038 (23%) |
| fan2ATR · fold0.5 | -0.010 (48%) | -0.044 (25%) | -0.073 (2%) | -0.100 (8%) |
| fan2ATR · fold0.7 | -0.049 (25%) | -0.027 (40%) | -0.091 (0%) | -0.077 (8%) |
| fan3ATR · fold0.3 | -0.014 (62%) | -0.069 (25%) | -0.095 (4%) | +0.043 (54%) |
| fan3ATR · fold0.5 | +0.016 (73%) | -0.017 (56%) | -0.025 (23%) | -0.122 (17%) |
| fan3ATR · fold0.7 | -0.014 (58%) | +0.002 (62%) | -0.029 (21%) | -0.062 (25%) |
| fan5ATR · fold0.3 | +0.238 (100%) | -0.074 (27%) | – | – |
| fan5ATR · fold0.5 | +0.138 (90%) | -0.094 (42%) | – | – |
| fan5ATR · fold0.7 | +0.167 (96%) | -0.030 (35%) | – | – |


## 4h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| fan2ATR stacked20 lookback100 fold0.7 stop2ATR 2R | shorts | +0.410 (n=54) | -0.119 (n=24) | +0.089 (n=87) | +0.249 (n=58) | -0.199 (n=34) | 2/4 |
| fan2ATR stacked10 lookback100 fold0.5 stop1ATR 1.5R | shorts | +0.285 (n=67) | -0.113 (n=30) | +0.036 (n=109) | -0.044 (n=75) | +0.031 (n=42) | 2/4 |
| fan2ATR stacked10 lookback50 fold0.5 stop1ATR 1.5R | shorts | +0.287 (n=65) | -0.114 (n=30) | +0.046 (n=108) | -0.073 (n=72) | +0.031 (n=42) | 2/4 |
| fan2ATR stacked20 lookback50 fold0.7 stop2ATR 2R | shorts | +0.380 (n=53) | -0.119 (n=24) | +0.089 (n=87) | +0.249 (n=58) | -0.199 (n=34) | 2/4 |
| fan2ATR stacked20 lookback100 fold0.5 stop2ATR 2R | shorts | +0.376 (n=51) | -0.077 (n=23) | +0.029 (n=86) | +0.114 (n=57) | -0.198 (n=34) | 2/4 |
| fan2ATR stacked10 lookback100 fold0.5 stop2ATR 2R | shorts | +0.321 (n=65) | -0.162 (n=29) | +0.009 (n=103) | +0.218 (n=72) | -0.134 (n=42) | 2/4 |
| fan2ATR stacked20 lookback100 fold0.5 stop2ATR 1.5R | shorts | +0.288 (n=51) | -0.128 (n=23) | -0.030 (n=86) | +0.020 (n=59) | -0.187 (n=34) | 1/4 |
| fan2ATR stacked10 lookback100 fold0.5 stop2ATR 1.5R | shorts | +0.250 (n=65) | -0.220 (n=29) | -0.054 (n=107) | +0.151 (n=74) | -0.163 (n=42) | 1/4 |
| fan2ATR stacked20 lookback50 fold0.5 stop2ATR 2R | shorts | +0.343 (n=50) | -0.078 (n=23) | +0.042 (n=85) | +0.134 (n=56) | -0.198 (n=34) | 2/4 |
| fan2ATR stacked10 lookback50 fold0.5 stop2ATR 2R | shorts | +0.294 (n=64) | -0.163 (n=29) | +0.018 (n=102) | +0.252 (n=70) | -0.134 (n=42) | 2/4 |

Entry families on 4h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| fan2ATR · fold0.3 | -0.217 (0%) | +0.004 (58%) | +0.097 (71%) | -0.056 (54%) |
| fan2ATR · fold0.5 | -0.126 (8%) | +0.005 (69%) | +0.029 (52%) | -0.068 (33%) |
| fan2ATR · fold0.7 | -0.115 (4%) | -0.014 (44%) | +0.118 (88%) | -0.117 (25%) |
| fan3ATR · fold0.3 | -0.383 (0%) | +0.037 (81%) | +0.127 (83%) | – |
| fan3ATR · fold0.5 | -0.172 (4%) | +0.010 (69%) | +0.095 (71%) | – |
| fan3ATR · fold0.7 | -0.187 (4%) | -0.005 (46%) | +0.055 (62%) | – |


## 1d

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| fan2ATR stacked10 lookback100 fold0.7 stop0.5ATR 3R | longs | +0.873 (n=23) | +0.403 (n=8) | +0.424 (n=22) | +1.645 (n=6) | +1.345 (n=5) | 4/4 |
| fan2ATR stacked10 lookback50 fold0.7 stop1ATR 1.5R | longs | +0.498 (n=23) | -0.130 (n=8) | +0.450 (n=22) | +0.650 (n=6) | +0.472 (n=5) | 3/4 |
| fan2ATR stacked20 lookback100 fold0.7 stop0.5ATR 3R | longs | +0.777 (n=22) | +0.611 (n=7) | +0.494 (n=21) | +1.645 (n=6) | +0.977 (n=2) | 4/4 |
| fan2ATR stacked20 lookback50 fold0.7 stop1ATR 1.5R | longs | +0.453 (n=22) | +0.011 (n=7) | +0.524 (n=21) | +0.650 (n=6) | +0.238 (n=2) | 4/4 |
| fan2ATR stacked10 lookback100 fold0.3 stop2ATR 2R | both | +0.440 (n=27) | -0.256 (n=12) | -0.330 (n=35) | -0.193 (n=19) | -0.365 (n=9) | 0/4 |
| fan2ATR stacked10 lookback50 fold0.7 stop0.5ATR 2R | longs | +0.510 (n=23) | +0.064 (n=8) | +0.103 (n=22) | +0.980 (n=6) | +0.766 (n=5) | 4/4 |
| fan2ATR stacked10 lookback100 fold0.7 stop2ATR 3R | longs | +0.686 (n=18) | -0.035 (n=7) | +0.511 (n=20) | -0.247 (n=5) | -1.067 (n=4) | 1/4 |
| fan2ATR stacked10 lookback100 fold0.3 stop1.5ATR 3R | both | +0.483 (n=27) | -0.720 (n=13) | -0.348 (n=36) | +0.074 (n=19) | -0.154 (n=9) | 1/4 |
| fan2ATR stacked20 lookback100 fold0.7 stop0.5ATR 2R | longs | +0.443 (n=22) | +0.224 (n=7) | +0.159 (n=21) | +0.980 (n=6) | +0.511 (n=2) | 4/4 |
| fan2ATR stacked10 lookback50 fold0.7 stop2ATR 3R | both | +0.457 (n=27) | -0.387 (n=12) | +0.354 (n=38) | +0.076 (n=19) | -0.575 (n=10) | 2/4 |

Entry families on 1d (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) |
|---|---|---|---|
| fan2ATR · fold0.3 | -0.175 (29%) | -0.114 (29%) | – |
| fan2ATR · fold0.5 | -0.095 (27%) | -0.029 (33%) | – |
| fan2ATR · fold0.7 | +0.041 (71%) | -0.006 (50%) | -0.173 (0%) |
| fan3ATR · fold0.3 | -0.192 (17%) | -0.229 (29%) | – |
| fan3ATR · fold0.5 | -0.125 (29%) | -0.041 (50%) | – |
| fan3ATR · fold0.7 | -0.000 (67%) | +0.038 (58%) | – |

