# Cross-asset check — hs: settings picked on BTC (in-sample only), tested on ETH, AVAX, XRP

Net of Bybit VIP 3 futures fees and funding. 'Full' = every trade in that asset's history (none of it was used to pick the settings). R = average net R per trade (n = trades).


## 15m

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| piv8 tol0.5 breakout neck:sloped stop:shoulder target:2R prior:0 exit:single | longs | +0.278 (n=140) | +0.018 (n=56) | -0.190 (n=189) | -0.047 (n=111) | +0.001 (n=102) | 2/4 |
| piv8 tol0.5 early neck:flat stop:head target:3R prior:0.5 exit:TP1 1R 50% BE | longs | +0.160 (n=156) | +0.032 (n=49) | -0.061 (n=203) | -0.045 (n=146) | +0.091 (n=117) | 2/4 |
| piv8 tol0.5 early neck:flat stop:head target:measured prior:0.5 exit:TP1 1R 50% BE | longs | +0.150 (n=158) | -0.048 (n=56) | -0.038 (n=217) | -0.036 (n=164) | +0.026 (n=125) | 1/4 |
| piv8 tol0.5 early neck:flat stop:head target:1.5R prior:0.5 exit:TP1 1R 50% BE | longs | +0.124 (n=159) | -0.093 (n=58) | -0.056 (n=217) | -0.112 (n=170) | +0.001 (n=128) | 1/4 |
| piv8 tol0.5 early neck:flat stop:shoulder target:measured prior:0.5 exit:single | longs | +0.288 (n=180) | +0.050 (n=61) | -0.182 (n=249) | +0.019 (n=183) | -0.375 (n=139) | 2/4 |
| piv8 tol0.5 early neck:flat stop:head target:2R prior:0.5 exit:TP1 1R 50% BE | longs | +0.115 (n=159) | -0.004 (n=55) | -0.034 (n=214) | -0.095 (n=165) | +0.000 (n=127) | 1/4 |
| piv8 tol0.25 early neck:flat stop:head target:1.5R prior:0.5 exit:TP1 1R 50% BE | longs | +0.123 (n=126) | -0.102 (n=34) | -0.052 (n=177) | -0.101 (n=139) | +0.003 (n=97) | 1/4 |
| piv8 tol0.5 breakout neck:sloped stop:shoulder target:1.5R prior:0 exit:single | longs | +0.130 (n=148) | -0.138 (n=57) | -0.173 (n=192) | -0.143 (n=122) | -0.029 (n=105) | 0/4 |
| piv8 tol0.5 early neck:flat stop:shoulder target:3R prior:0.5 exit:single | longs | +0.176 (n=180) | +0.036 (n=63) | -0.223 (n=244) | -0.014 (n=190) | -0.246 (n=148) | 1/4 |
| piv8 tol0.5 early neck:flat stop:head target:1.5R prior:0.5 exit:single | longs | +0.124 (n=149) | -0.030 (n=57) | -0.077 (n=213) | -0.089 (n=166) | -0.055 (n=123) | 0/4 |

Entry families on 15m (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| breakout · stop:head | -0.103 (9%) | -0.026 (33%) | -0.017 (47%) | -0.009 (46%) |
| breakout · stop:shoulder | -0.122 (9%) | -0.025 (37%) | -0.004 (44%) | -0.059 (31%) |
| early · stop:head | -0.128 (1%) | -0.029 (22%) | -0.012 (31%) | +0.022 (57%) |
| early · stop:shoulder | -0.216 (0%) | -0.110 (0%) | -0.097 (4%) | -0.027 (31%) |
| retest · stop:head | -0.103 (7%) | -0.024 (35%) | -0.057 (24%) | -0.015 (48%) |
| retest · stop:shoulder | -0.132 (4%) | -0.035 (26%) | -0.050 (28%) | -0.089 (29%) |


## 1h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| piv5 tol0.25 retest neck:flat stop:shoulder target:3R prior:0 exit:single | both | +0.435 (n=90) | +0.027 (n=33) | -0.030 (n=130) | +0.097 (n=68) | +0.538 (n=62) | 3/4 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | both | +0.152 (n=210) | -0.028 (n=80) | -0.057 (n=286) | -0.042 (n=150) | -0.034 (n=154) | 0/4 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:1.5R prior:0 exit:TP1 1R 50% BE | both | +0.138 (n=214) | -0.057 (n=81) | -0.080 (n=291) | -0.047 (n=150) | -0.010 (n=154) | 0/4 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | +0.156 (n=204) | -0.014 (n=76) | -0.093 (n=279) | -0.062 (n=144) | +0.028 (n=149) | 1/4 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0 exit:TP1 1R 50% BE | longs | +0.192 (n=116) | -0.028 (n=46) | -0.006 (n=156) | -0.057 (n=77) | -0.031 (n=78) | 0/4 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:3R prior:0.5 exit:TP1 1R 50% BE | both | +0.201 (n=107) | +0.052 (n=34) | -0.162 (n=162) | -0.098 (n=75) | +0.047 (n=83) | 2/4 |
| piv5 tol0.5 retest neck:flat stop:shoulder target:3R prior:0 exit:single | both | +0.307 (n=116) | -0.087 (n=46) | -0.167 (n=160) | +0.117 (n=88) | +0.546 (n=82) | 2/4 |
| piv5 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0.5 exit:single | both | +0.290 (n=80) | -0.381 (n=18) | +0.097 (n=109) | +0.073 (n=49) | +0.198 (n=37) | 3/4 |
| piv5 tol0.25 breakout neck:flat stop:shoulder target:measured prior:0 exit:single | both | +0.154 (n=136) | -0.225 (n=42) | -0.042 (n=193) | +0.111 (n=93) | +0.161 (n=80) | 2/4 |
| piv3 tol0.25 breakout neck:flat stop:shoulder target:2R prior:0.5 exit:TP1 1R 50% BE | both | +0.181 (n=109) | +0.011 (n=34) | -0.145 (n=163) | -0.058 (n=77) | -0.028 (n=86) | 1/4 |

Entry families on 1h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| breakout · stop:head | -0.014 (43%) | -0.062 (22%) | -0.000 (58%) | -0.003 (66%) |
| breakout · stop:shoulder | +0.044 (81%) | -0.038 (32%) | +0.065 (70%) | +0.047 (63%) |
| early · stop:head | -0.119 (6%) | -0.033 (22%) | +0.035 (68%) | -0.008 (43%) |
| early · stop:shoulder | -0.103 (7%) | -0.069 (13%) | +0.051 (74%) | -0.018 (35%) |
| retest · stop:head | -0.042 (35%) | -0.042 (30%) | +0.027 (62%) | -0.007 (58%) |
| retest · stop:shoulder | +0.009 (51%) | +0.027 (59%) | +0.111 (75%) | +0.038 (50%) |


## 4h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| piv3 tol0.5 early neck:flat stop:head target:3R prior:0 exit:TP1 1R 50% BE | longs | +0.468 (n=54) | -0.078 (n=27) | +0.068 (n=66) | -0.000 (n=33) | +0.383 (n=40) | 2/4 |
| piv3 tol0.5 early neck:flat stop:head target:2R prior:0 exit:TP1 1R 50% BE | longs | +0.375 (n=57) | -0.129 (n=27) | +0.101 (n=77) | +0.161 (n=35) | +0.348 (n=43) | 3/4 |
| piv3 tol0.5 early neck:flat stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | longs | +0.328 (n=58) | -0.180 (n=27) | +0.063 (n=81) | +0.149 (n=35) | +0.020 (n=49) | 3/4 |
| piv3 tol0.5 early neck:sloped stop:head target:3R prior:0 exit:TP1 1R 50% BE | longs | +0.413 (n=51) | +0.044 (n=24) | +0.122 (n=64) | -0.057 (n=35) | +0.342 (n=38) | 3/4 |
| piv3 tol0.5 early neck:sloped stop:head target:2R prior:0 exit:TP1 1R 50% BE | longs | +0.362 (n=54) | -0.013 (n=24) | +0.088 (n=72) | +0.098 (n=37) | +0.320 (n=41) | 3/4 |
| piv3 tol0.5 early neck:flat stop:head target:measured prior:0 exit:TP1 1R 50% BE | longs | +0.327 (n=54) | -0.121 (n=27) | +0.052 (n=78) | +0.226 (n=34) | +0.317 (n=44) | 3/4 |
| piv3 tol0.5 early neck:sloped stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | longs | +0.306 (n=54) | -0.071 (n=24) | +0.045 (n=76) | +0.087 (n=37) | -0.051 (n=45) | 2/4 |
| piv3 tol0.25 early neck:sloped stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | both | +0.256 (n=114) | -0.310 (n=51) | -0.072 (n=166) | +0.083 (n=77) | +0.095 (n=84) | 2/4 |
| piv3 tol0.25 early neck:sloped stop:shoulder target:3R prior:0 exit:TP1 1R 50% BE | longs | +0.347 (n=56) | -0.033 (n=26) | +0.011 (n=78) | -0.079 (n=40) | -0.060 (n=41) | 1/4 |
| piv3 tol0.5 early neck:sloped stop:head target:measured prior:0 exit:TP1 1R 50% BE | longs | +0.293 (n=52) | -0.007 (n=24) | +0.064 (n=73) | +0.081 (n=37) | +0.256 (n=42) | 3/4 |

Entry families on 4h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| breakout · stop:head | -0.290 (9%) | -0.132 (14%) | -0.038 (45%) | -0.135 (31%) |
| breakout · stop:shoulder | -0.240 (10%) | -0.227 (14%) | +0.048 (60%) | -0.079 (42%) |
| early · stop:head | -0.171 (14%) | -0.052 (34%) | -0.031 (45%) | +0.095 (71%) |
| early · stop:shoulder | -0.076 (28%) | -0.128 (5%) | -0.005 (45%) | +0.107 (76%) |
| retest · stop:head | -0.261 (13%) | -0.181 (10%) | -0.046 (36%) | -0.111 (39%) |
| retest · stop:shoulder | -0.152 (24%) | -0.225 (10%) | -0.083 (25%) | -0.040 (48%) |


## 1d

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:single | both | +0.746 (n=17) | -0.588 (n=6) | +0.051 (n=22) | -0.317 (n=7) | -0.512 (n=6) | 1/4 |
| piv3 tol0.5 early neck:sloped stop:head target:1.5R prior:0 exit:single | both | +0.699 (n=19) | -0.141 (n=9) | +0.275 (n=26) | -0.333 (n=11) | -0.459 (n=10) | 1/4 |
| piv3 tol0.25 early neck:sloped stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | both | +0.600 (n=17) | -0.375 (n=6) | -0.022 (n=24) | -0.283 (n=8) | +0.222 (n=8) | 1/4 |
| piv3 tol0.5 early neck:sloped stop:shoulder target:3R prior:0 exit:single | both | +1.064 (n=23) | +0.179 (n=10) | +0.548 (n=31) | -0.703 (n=13) | -0.369 (n=18) | 2/4 |
| piv3 tol0.25 early neck:sloped stop:shoulder target:3R prior:0 exit:single | both | +1.064 (n=21) | -0.454 (n=7) | +0.497 (n=24) | -0.567 (n=9) | -0.230 (n=10) | 1/4 |
| piv3 tol0.5 early neck:sloped stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | both | +0.523 (n=19) | +0.122 (n=9) | +0.161 (n=28) | -0.330 (n=12) | +0.001 (n=12) | 3/4 |
| piv3 tol0.25 early neck:flat stop:head target:1.5R prior:0 exit:single | both | +0.644 (n=18) | -0.075 (n=8) | +0.025 (n=25) | -0.679 (n=7) | -0.628 (n=8) | 1/4 |
| piv3 tol0.25 early neck:flat stop:head target:1.5R prior:0 exit:TP1 1R 50% BE | both | +0.508 (n=19) | +0.022 (n=8) | -0.047 (n=27) | -0.268 (n=8) | +0.230 (n=11) | 2/4 |
| piv3 tol0.25 early neck:flat stop:shoulder target:3R prior:0 exit:single | both | +0.879 (n=23) | +0.545 (n=10) | +0.478 (n=27) | -0.220 (n=10) | -0.169 (n=14) | 2/4 |
| piv3 tol0.5 early neck:flat stop:shoulder target:3R prior:0 exit:single | both | +0.821 (n=26) | +0.679 (n=14) | +0.528 (n=34) | -0.445 (n=14) | -0.305 (n=22) | 2/4 |

Entry families on 1d (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|
| breakout · stop:head | -0.039 (0%) | – | – |
| breakout · stop:shoulder | +0.308 (100%) | – | – |
| early · stop:head | +0.310 (100%) | +0.166 (79%) | – |
| early · stop:shoulder | +0.283 (98%) | +0.130 (72%) | -0.183 (0%) |

