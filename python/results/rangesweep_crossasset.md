# Cross-asset check — rangesweep: settings picked on BTC (in-sample only), tested on ETH, AVAX, XRP

Net of 0.20% round-trip costs. 'Full' = every trade in that asset's history (none of it was used to pick the settings). R = average net R per trade (n = trades).


## 15m

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| range144 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | shorts | -0.097 (n=219) | -0.412 (n=96) | -0.398 (n=299) | -0.184 (n=199) | -0.382 (n=147) | 0/4 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | shorts | -0.131 (n=229) | -0.469 (n=101) | -0.326 (n=316) | -0.203 (n=262) | -0.221 (n=167) | 0/4 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | shorts | -0.151 (n=192) | -0.350 (n=88) | -0.385 (n=274) | -0.201 (n=191) | -0.391 (n=137) | 0/4 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:opposite exit:single | longs | -0.149 (n=223) | -0.402 (n=129) | -0.118 (n=299) | -0.154 (n=290) | -0.530 (n=214) | 0/4 |
| range144 max15ATR touches2 within_n sweepMax3 stop0.75ATR target:opposite exit:single | shorts | -0.127 (n=285) | -0.404 (n=132) | -0.299 (n=389) | -0.175 (n=308) | -0.197 (n=200) | 0/4 |
| range144 max15ATR touches2 same_bar sweepMax3 stop0.25ATR target:opposite exit:single | longs | -0.195 (n=261) | -0.750 (n=140) | -0.254 (n=356) | +0.013 (n=304) | -0.692 (n=234) | 1/4 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.75ATR target:opposite exit:single | longs | -0.184 (n=199) | -0.446 (n=104) | -0.105 (n=277) | +0.020 (n=233) | -0.537 (n=182) | 1/4 |
| range144 max15ATR touches2 same_bar sweepMax3 stop0.75ATR target:opposite exit:single | longs | -0.166 (n=223) | -0.470 (n=110) | -0.192 (n=310) | +0.030 (n=258) | -0.505 (n=201) | 1/4 |
| range144 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | longs | -0.217 (n=267) | -0.550 (n=168) | -0.163 (n=356) | -0.211 (n=359) | -0.807 (n=258) | 0/4 |
| range144 max15ATR touches2 same_bar sweepMax1 stop0.25ATR target:opposite exit:single | longs | -0.249 (n=235) | -0.737 (n=133) | -0.177 (n=321) | +0.002 (n=278) | -0.768 (n=213) | 1/4 |

Entry families on 15m (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| same_bar · target:2R | -0.610 (0%) | -0.449 (0%) | -0.322 (0%) | -0.473 (0%) |
| same_bar · target:3R | -0.598 (0%) | -0.431 (0%) | -0.321 (0%) | -0.465 (0%) |
| same_bar · target:midline | -0.619 (0%) | -0.464 (0%) | -0.348 (0%) | -0.469 (0%) |
| same_bar · target:opposite | -0.572 (0%) | -0.418 (0%) | -0.303 (1%) | -0.487 (0%) |
| within_n · target:2R | -0.513 (0%) | -0.380 (0%) | -0.287 (2%) | -0.430 (0%) |
| within_n · target:3R | -0.490 (0%) | -0.367 (0%) | -0.280 (4%) | -0.410 (0%) |
| within_n · target:midline | -0.535 (0%) | -0.400 (0%) | -0.316 (0%) | -0.435 (0%) |
| within_n · target:opposite | -0.490 (0%) | -0.363 (0%) | -0.277 (2%) | -0.433 (0%) |


## 1h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| range48 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:single | longs | +0.335 (n=85) | -0.166 (n=60) | -0.158 (n=136) | -0.181 (n=86) | -0.396 (n=74) | 0/4 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | longs | +0.221 (n=153) | +0.107 (n=110) | -0.324 (n=242) | -0.190 (n=188) | -0.357 (n=123) | 1/4 |
| range48 max6ATR touches2 same_bar sweepMax3 stop0.25ATR target:3R exit:single | longs | +0.284 (n=91) | -0.314 (n=65) | -0.247 (n=149) | -0.180 (n=101) | -0.451 (n=86) | 0/4 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | +0.185 (n=177) | -0.067 (n=129) | -0.232 (n=292) | -0.292 (n=241) | -0.529 (n=169) | 0/4 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | longs | +0.196 (n=156) | +0.109 (n=113) | -0.341 (n=253) | -0.253 (n=193) | -0.332 (n=124) | 1/4 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | +0.155 (n=181) | -0.101 (n=133) | -0.234 (n=306) | -0.342 (n=252) | -0.533 (n=170) | 0/4 |
| range48 max6ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | longs | +0.169 (n=129) | -0.106 (n=86) | -0.083 (n=222) | -0.231 (n=156) | -0.366 (n=124) | 0/4 |
| range48 max6ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | longs | +0.198 (n=93) | -0.127 (n=68) | -0.092 (n=164) | -0.328 (n=134) | -0.520 (n=101) | 0/4 |
| range48 max6ATR touches2 within_n sweepMax1 stop0.75ATR target:3R exit:single | longs | +0.210 (n=80) | +0.054 (n=59) | -0.045 (n=144) | -0.192 (n=109) | -0.425 (n=77) | 1/4 |
| range48 max6ATR touches2 within_n sweepMax3 stop0.75ATR target:3R exit:single | longs | +0.162 (n=112) | +0.018 (n=75) | -0.130 (n=199) | -0.135 (n=128) | -0.323 (n=99) | 1/4 |

Entry families on 1h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| same_bar · target:2R | -0.195 (6%) | -0.172 (8%) | -0.220 (1%) | -0.309 (1%) |
| same_bar · target:3R | -0.160 (9%) | -0.163 (9%) | -0.197 (6%) | -0.290 (2%) |
| same_bar · target:midline | -0.197 (8%) | -0.172 (11%) | -0.249 (1%) | -0.282 (6%) |
| same_bar · target:opposite | -0.166 (12%) | -0.200 (8%) | -0.200 (8%) | -0.281 (5%) |
| within_n · target:2R | -0.154 (10%) | -0.170 (6%) | -0.185 (2%) | -0.299 (0%) |
| within_n · target:3R | -0.112 (15%) | -0.165 (6%) | -0.162 (7%) | -0.293 (0%) |
| within_n · target:midline | -0.177 (10%) | -0.177 (7%) | -0.220 (0%) | -0.275 (0%) |
| within_n · target:opposite | -0.133 (16%) | -0.205 (6%) | -0.173 (8%) | -0.303 (1%) |


## 4h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | +0.343 (n=50) | -0.376 (n=32) | +0.163 (n=81) | -0.083 (n=67) | -0.141 (n=31) | 1/4 |
| range24 max10ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | +0.315 (n=51) | -0.302 (n=33) | +0.146 (n=91) | -0.067 (n=70) | -0.141 (n=31) | 1/4 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | +0.287 (n=57) | -0.244 (n=36) | +0.233 (n=89) | -0.101 (n=71) | -0.169 (n=35) | 1/4 |
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | +0.204 (n=108) | -0.384 (n=59) | +0.095 (n=157) | -0.073 (n=115) | -0.145 (n=47) | 1/4 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | both | +0.195 (n=118) | -0.280 (n=64) | +0.130 (n=168) | -0.084 (n=119) | -0.180 (n=52) | 1/4 |
| range24 max10ATR touches2 within_n sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | +0.226 (n=82) | +0.143 (n=55) | +0.215 (n=138) | +0.019 (n=90) | -0.159 (n=56) | 3/4 |
| range24 max6ATR touches2 same_bar sweepMax1 stop0.75ATR target:3R exit:TP1 1R 50% BE | both | +0.213 (n=103) | -0.334 (n=56) | +0.162 (n=151) | -0.009 (n=110) | -0.155 (n=47) | 1/4 |
| range24 max10ATR touches2 same_bar sweepMax3 stop0.75ATR target:2R exit:TP1 1R 50% BE | longs | +0.264 (n=58) | -0.181 (n=37) | +0.223 (n=100) | -0.086 (n=74) | -0.168 (n=35) | 1/4 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:TP1 1R 50% BE | both | +0.193 (n=112) | -0.221 (n=61) | +0.199 (n=162) | -0.019 (n=114) | -0.184 (n=52) | 1/4 |
| range24 max6ATR touches2 same_bar sweepMax3 stop0.75ATR target:3R exit:TP1 1R 50% BE | longs | +0.272 (n=53) | -0.146 (n=33) | +0.325 (n=85) | -0.052 (n=70) | -0.174 (n=35) | 1/4 |

Entry families on 4h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| same_bar · target:2R | -0.180 (4%) | -0.128 (19%) | -0.094 (17%) | -0.205 (4%) |
| same_bar · target:3R | -0.159 (14%) | -0.113 (23%) | -0.057 (32%) | -0.243 (3%) |
| same_bar · target:midline | -0.198 (3%) | -0.122 (20%) | -0.097 (12%) | -0.261 (3%) |
| same_bar · target:opposite | -0.111 (23%) | -0.103 (29%) | +0.009 (36%) | -0.244 (5%) |
| within_n · target:2R | -0.163 (6%) | -0.080 (29%) | -0.056 (31%) | -0.215 (1%) |
| within_n · target:3R | -0.153 (10%) | -0.068 (28%) | -0.030 (38%) | -0.229 (2%) |
| within_n · target:midline | -0.183 (3%) | -0.101 (28%) | -0.046 (28%) | -0.264 (0%) |
| within_n · target:opposite | -0.119 (25%) | -0.123 (22%) | +0.004 (38%) | -0.236 (9%) |


## 1d

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | +1.217 (n=23) | +0.119 (n=12) | -0.131 (n=35) | +0.668 (n=12) | -0.502 (n=7) | 2/4 |
| range48 max10ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | both | +1.541 (n=17) | -0.335 (n=14) | -0.313 (n=30) | +0.819 (n=11) | -0.502 (n=7) | 1/4 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:single | both | +1.119 (n=24) | +1.042 (n=12) | -0.131 (n=35) | +0.423 (n=14) | -0.502 (n=7) | 2/4 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:single | both | +1.393 (n=18) | +0.451 (n=14) | -0.313 (n=30) | +0.532 (n=13) | -0.502 (n=7) | 2/4 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:3R exit:single | both | +0.465 (n=29) | +0.951 (n=14) | -0.144 (n=36) | +0.112 (n=14) | +0.685 (n=7) | 3/4 |
| range48 max15ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:TP1 1R 50% BE | both | +0.424 (n=29) | +0.445 (n=17) | -0.011 (n=38) | +0.183 (n=15) | -0.195 (n=7) | 2/4 |
| range24 max10ATR touches1 within_n sweepMax3 stop0.75ATR target:midline exit:single | longs | +0.206 (n=53) | -0.005 (n=32) | -0.036 (n=83) | -0.196 (n=51) | +0.144 (n=33) | 1/4 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:3R exit:single | both | +0.505 (n=23) | +0.935 (n=16) | -0.262 (n=31) | +0.505 (n=13) | +0.685 (n=7) | 3/4 |
| range48 max10ATR touches2 within_n sweepMax3 stop0.25ATR target:opposite exit:TP1 1R 50% BE | both | +0.426 (n=28) | +0.224 (n=16) | -0.011 (n=38) | +0.256 (n=13) | -0.195 (n=7) | 2/4 |
| range48 max15ATR touches2 within_n sweepMax1 stop0.25ATR target:opposite exit:TP1 1R 50% BE | both | +0.478 (n=23) | +0.545 (n=14) | -0.058 (n=31) | +0.266 (n=14) | -0.195 (n=7) | 2/4 |

Entry families on 1d (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| same_bar · target:2R | -0.125 (16%) | -0.175 (6%) | -0.093 (21%) | +0.124 (90%) |
| same_bar · target:3R | -0.102 (24%) | -0.215 (3%) | -0.075 (34%) | +0.323 (100%) |
| same_bar · target:midline | -0.187 (7%) | -0.175 (7%) | -0.043 (35%) | +0.008 (56%) |
| same_bar · target:opposite | -0.177 (15%) | -0.176 (11%) | +0.022 (56%) | +0.229 (100%) |
| within_n · target:2R | -0.044 (30%) | -0.130 (8%) | -0.107 (21%) | +0.242 (90%) |
| within_n · target:3R | -0.013 (42%) | -0.184 (5%) | -0.081 (25%) | +0.221 (100%) |
| within_n · target:midline | -0.102 (22%) | -0.139 (17%) | -0.070 (26%) | +0.076 (88%) |
| within_n · target:opposite | -0.065 (22%) | -0.095 (21%) | -0.043 (32%) | +0.247 (93%) |

