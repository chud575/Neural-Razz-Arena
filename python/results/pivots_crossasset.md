# Cross-asset check — pivots: settings picked on BTC (in-sample only), tested on ETH, AVAX, XRP

Net of 0.20% round-trip costs. 'Full' = every trade in that asset's history (none of it was used to pick the settings). R = average net R per trade (n = trades).


## 15m

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | longs | +0.421 (n=146) | -0.287 (n=67) | +0.198 (n=210) | -0.067 (n=150) | +0.024 (n=104) | 2/4 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:no | longs | +0.421 (n=146) | -0.243 (n=67) | +0.187 (n=210) | -0.067 (n=150) | +0.062 (n=102) | 2/4 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.300 (n=282) | -0.210 (n=134) | +0.088 (n=408) | -0.093 (n=312) | -0.059 (n=199) | 1/4 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:no | both | +0.296 (n=281) | -0.181 (n=133) | +0.093 (n=406) | -0.091 (n=312) | -0.039 (n=196) | 1/4 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | both | +0.454 (n=282) | -0.161 (n=134) | +0.164 (n=408) | +0.063 (n=312) | -0.130 (n=199) | 2/4 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:no | both | +0.432 (n=282) | -0.165 (n=134) | +0.156 (n=407) | +0.048 (n=312) | -0.118 (n=196) | 2/4 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | longs | +0.483 (n=146) | -0.300 (n=67) | +0.167 (n=210) | +0.065 (n=150) | -0.043 (n=104) | 2/4 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | +0.482 (n=146) | -0.308 (n=67) | +0.140 (n=210) | +0.051 (n=150) | -0.019 (n=102) | 2/4 |
| traditional pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no | both | +0.464 (n=189) | +0.129 (n=80) | +0.313 (n=266) | -0.320 (n=195) | +0.094 (n=127) | 3/4 |
| fibonacci pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:no | both | +0.473 (n=164) | +0.277 (n=63) | +0.090 (n=223) | -0.317 (n=167) | -0.123 (n=105) | 2/4 |

Entry families on 15m (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| camarilla pivots:D · bounce-rejection | -0.219 (0%) | -0.131 (0%) | -0.140 (0%) | -0.141 (0%) |
| camarilla pivots:D · bounce-touch | -0.353 (0%) | -0.291 (0%) | -0.270 (0%) | -0.236 (0%) |
| camarilla pivots:D · breakout | -0.205 (0%) | -0.106 (0%) | -0.118 (0%) | -0.196 (0%) |
| camarilla pivots:W · bounce-rejection | -0.205 (0%) | -0.206 (0%) | -0.098 (4%) | -0.101 (17%) |
| camarilla pivots:W · bounce-touch | -0.367 (0%) | -0.363 (0%) | -0.252 (8%) | -0.204 (0%) |
| camarilla pivots:W · breakout | +0.041 (58%) | +0.040 (67%) | -0.057 (25%) | -0.189 (0%) |
| fibonacci pivots:D · bounce-rejection | -0.254 (0%) | -0.168 (0%) | -0.129 (4%) | -0.189 (0%) |
| fibonacci pivots:D · bounce-touch | -0.408 (0%) | -0.316 (0%) | -0.285 (0%) | -0.340 (0%) |
| fibonacci pivots:D · breakout | -0.090 (0%) | +0.005 (42%) | -0.060 (17%) | -0.130 (0%) |
| fibonacci pivots:W · bounce-rejection | -0.160 (12%) | -0.273 (8%) | -0.219 (8%) | -0.194 (0%) |
| fibonacci pivots:W · bounce-touch | -0.289 (4%) | -0.356 (0%) | -0.314 (0%) | -0.339 (4%) |
| fibonacci pivots:W · breakout | +0.011 (50%) | +0.059 (67%) | -0.081 (25%) | -0.071 (25%) |
| traditional pivots:D · bounce-rejection | -0.285 (0%) | -0.267 (0%) | -0.143 (4%) | -0.086 (21%) |
| traditional pivots:D · bounce-touch | -0.407 (0%) | -0.345 (0%) | -0.216 (8%) | -0.224 (0%) |
| traditional pivots:D · breakout | -0.066 (0%) | +0.033 (67%) | -0.069 (21%) | -0.104 (8%) |
| traditional pivots:W · bounce-rejection | +0.171 (62%) | -0.350 (0%) | -0.133 (33%) | -0.108 (21%) |
| traditional pivots:W · bounce-touch | +0.052 (50%) | -0.437 (0%) | -0.258 (8%) | -0.441 (0%) |
| traditional pivots:W · breakout | +0.003 (54%) | +0.001 (46%) | -0.111 (21%) | -0.037 (54%) |
| woodie pivots:D · bounce-rejection | -0.222 (0%) | -0.229 (0%) | -0.121 (0%) | -0.071 (21%) |
| woodie pivots:D · bounce-touch | -0.341 (0%) | -0.327 (0%) | -0.187 (8%) | -0.228 (0%) |
| woodie pivots:D · breakout | -0.062 (21%) | +0.007 (54%) | -0.063 (21%) | -0.150 (0%) |
| woodie pivots:W · bounce-rejection | -0.321 (0%) | -0.222 (8%) | -0.062 (54%) | -0.278 (8%) |
| woodie pivots:W · bounce-touch | -0.263 (0%) | -0.349 (0%) | -0.225 (12%) | -0.374 (8%) |
| woodie pivots:W · breakout | -0.079 (38%) | +0.027 (46%) | +0.054 (67%) | -0.146 (0%) |


## 1h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.121 (n=1554) | +0.017 (n=703) | +0.079 (n=2191) | -0.009 (n=1152) | -0.011 (n=693) | 2/4 |
| woodie pivots:D breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | +0.166 (n=788) | +0.048 (n=362) | +0.133 (n=1086) | -0.049 (n=577) | -0.042 (n=337) | 2/4 |
| traditional pivots:D breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | +0.401 (n=175) | -0.090 (n=81) | +0.206 (n=236) | +0.032 (n=78) | +0.054 (n=63) | 3/4 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:no | longs | +0.482 (n=217) | -0.193 (n=99) | +0.040 (n=291) | -0.030 (n=142) | +0.019 (n=94) | 2/4 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | longs | +0.373 (n=197) | -0.120 (n=93) | +0.286 (n=265) | +0.104 (n=118) | -0.149 (n=77) | 2/4 |
| fibonacci pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | longs | +0.371 (n=200) | -0.043 (n=95) | +0.233 (n=265) | +0.295 (n=118) | -0.126 (n=77) | 2/4 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.271 (n=348) | +0.001 (n=171) | +0.242 (n=483) | +0.099 (n=260) | -0.064 (n=159) | 3/4 |
| camarilla pivots:W breakout level3 stop1ATR target:next exitAtPeriodEnd:yes | longs | +0.446 (n=219) | -0.205 (n=99) | +0.050 (n=294) | -0.065 (n=143) | +0.016 (n=96) | 2/4 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | both | +0.279 (n=337) | -0.049 (n=167) | +0.245 (n=481) | +0.108 (n=258) | -0.097 (n=159) | 2/4 |
| traditional pivots:W breakout level1 stop1ATR target:next exitAtPeriodEnd:no | both | +0.521 (n=269) | +0.045 (n=122) | +0.240 (n=371) | +0.015 (n=188) | -0.312 (n=119) | 3/4 |

Entry families on 1h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| camarilla pivots:D · bounce-rejection | -0.102 (4%) | -0.064 (17%) | -0.094 (0%) | -0.083 (8%) |
| camarilla pivots:D · bounce-touch | -0.234 (0%) | -0.182 (0%) | -0.171 (0%) | -0.135 (0%) |
| camarilla pivots:D · breakout | -0.082 (0%) | -0.036 (12%) | -0.047 (8%) | -0.090 (0%) |
| camarilla pivots:W · bounce-rejection | -0.147 (0%) | -0.136 (0%) | -0.078 (25%) | -0.066 (33%) |
| camarilla pivots:W · bounce-touch | -0.311 (0%) | -0.284 (0%) | -0.164 (0%) | -0.139 (0%) |
| camarilla pivots:W · breakout | +0.101 (83%) | +0.072 (100%) | -0.059 (25%) | -0.057 (33%) |
| fibonacci pivots:D · bounce-rejection | -0.129 (0%) | -0.104 (0%) | -0.072 (4%) | -0.137 (0%) |
| fibonacci pivots:D · bounce-touch | -0.290 (0%) | -0.237 (0%) | -0.185 (0%) | -0.220 (0%) |
| fibonacci pivots:D · breakout | +0.015 (50%) | +0.045 (83%) | -0.004 (46%) | -0.092 (8%) |
| fibonacci pivots:W · bounce-rejection | -0.135 (0%) | -0.207 (0%) | -0.178 (8%) | -0.189 (0%) |
| fibonacci pivots:W · bounce-touch | -0.272 (0%) | -0.310 (0%) | -0.182 (4%) | -0.284 (4%) |
| fibonacci pivots:W · breakout | +0.168 (100%) | +0.138 (100%) | +0.046 (67%) | -0.082 (0%) |
| traditional pivots:D · bounce-rejection | -0.158 (0%) | -0.151 (0%) | -0.068 (17%) | -0.096 (4%) |
| traditional pivots:D · bounce-touch | -0.283 (0%) | -0.252 (0%) | -0.171 (0%) | -0.116 (8%) |
| traditional pivots:D · breakout | +0.047 (67%) | +0.070 (83%) | +0.049 (75%) | -0.021 (33%) |
| traditional pivots:W · bounce-rejection | -0.018 (29%) | -0.158 (21%) | -0.104 (38%) | -0.116 (17%) |
| traditional pivots:W · bounce-touch | -0.074 (33%) | -0.275 (4%) | -0.131 (12%) | -0.506 (0%) |
| traditional pivots:W · breakout | +0.149 (100%) | +0.077 (67%) | +0.001 (58%) | -0.162 (6%) |
| woodie pivots:D · bounce-rejection | -0.195 (0%) | -0.159 (0%) | -0.090 (0%) | -0.071 (8%) |
| woodie pivots:D · bounce-touch | -0.280 (0%) | -0.234 (0%) | -0.151 (0%) | -0.130 (0%) |
| woodie pivots:D · breakout | +0.038 (62%) | +0.061 (92%) | +0.046 (62%) | -0.073 (25%) |
| woodie pivots:W · bounce-rejection | -0.279 (0%) | -0.177 (0%) | +0.009 (50%) | -0.184 (20%) |
| woodie pivots:W · bounce-touch | -0.233 (0%) | -0.236 (0%) | -0.122 (21%) | -0.382 (8%) |
| woodie pivots:W · breakout | +0.128 (88%) | +0.037 (54%) | -0.065 (42%) | -0.154 (19%) |


## 4h

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | longs | +0.652 (n=125) | +0.114 (n=51) | +0.260 (n=169) | +0.292 (n=66) | -0.316 (n=46) | 3/4 |
| woodie pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:no | both | +0.471 (n=236) | +0.027 (n=110) | +0.194 (n=328) | +0.181 (n=163) | +0.228 (n=106) | 4/4 |
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.444 (n=212) | -0.006 (n=96) | +0.231 (n=295) | +0.076 (n=137) | +0.047 (n=96) | 3/4 |
| woodie pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.411 (n=248) | -0.009 (n=115) | +0.221 (n=345) | +0.168 (n=163) | +0.203 (n=106) | 3/4 |
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | +0.552 (n=129) | +0.026 (n=53) | +0.231 (n=171) | +0.257 (n=68) | -0.271 (n=48) | 3/4 |
| fibonacci pivots:W breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:yes | both | +0.446 (n=212) | -0.022 (n=96) | +0.301 (n=295) | -0.028 (n=137) | +0.012 (n=96) | 2/4 |
| fibonacci pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:no | both | +0.468 (n=208) | +0.038 (n=92) | +0.204 (n=291) | +0.095 (n=130) | +0.013 (n=93) | 4/4 |
| fibonacci pivots:W breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | both | +0.450 (n=209) | +0.033 (n=94) | +0.325 (n=294) | -0.039 (n=131) | +0.001 (n=93) | 3/4 |
| woodie pivots:D breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.207 (n=275) | +0.039 (n=122) | +0.168 (n=356) | +0.055 (n=131) | -0.087 (n=98) | 3/4 |
| camarilla pivots:W breakout level3 stop1ATR target:2R exitAtPeriodEnd:yes | both | +0.297 (n=391) | +0.041 (n=168) | +0.172 (n=526) | +0.023 (n=272) | +0.004 (n=176) | 4/4 |

Entry families on 4h (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| camarilla pivots:D · bounce-rejection | -0.049 (25%) | -0.055 (12%) | -0.085 (0%) | -0.050 (25%) |
| camarilla pivots:D · bounce-touch | -0.157 (0%) | -0.142 (0%) | -0.152 (0%) | -0.128 (0%) |
| camarilla pivots:D · breakout | -0.009 (29%) | +0.020 (71%) | -0.030 (17%) | +0.002 (38%) |
| camarilla pivots:M · bounce-rejection | -0.188 (0%) | -0.225 (4%) | -0.041 (46%) | +0.058 (62%) |
| camarilla pivots:M · bounce-touch | -0.221 (0%) | -0.280 (0%) | -0.058 (25%) | -0.115 (33%) |
| camarilla pivots:M · breakout | +0.138 (100%) | +0.243 (100%) | +0.158 (92%) | +0.204 (75%) |
| camarilla pivots:W · bounce-rejection | -0.117 (4%) | -0.039 (38%) | +0.021 (54%) | -0.050 (25%) |
| camarilla pivots:W · bounce-touch | -0.251 (0%) | -0.218 (0%) | -0.115 (12%) | -0.118 (0%) |
| camarilla pivots:W · breakout | +0.105 (100%) | +0.059 (79%) | -0.014 (42%) | -0.017 (42%) |
| fibonacci pivots:D · bounce-rejection | -0.077 (0%) | -0.058 (21%) | -0.062 (8%) | -0.094 (0%) |
| fibonacci pivots:D · bounce-touch | -0.204 (0%) | -0.182 (0%) | -0.144 (0%) | -0.169 (0%) |
| fibonacci pivots:D · breakout | +0.055 (96%) | +0.102 (100%) | +0.037 (79%) | +0.036 (71%) |
| fibonacci pivots:M · bounce-rejection | -0.110 (29%) | -0.194 (0%) | -0.110 (38%) | +0.031 (44%) |
| fibonacci pivots:M · bounce-touch | -0.341 (4%) | -0.416 (17%) | -0.161 (29%) | -0.108 (38%) |
| fibonacci pivots:M · breakout | +0.383 (100%) | +0.244 (92%) | +0.173 (67%) | +0.277 (100%) |
| fibonacci pivots:W · bounce-rejection | -0.155 (0%) | -0.140 (4%) | -0.009 (42%) | -0.058 (25%) |
| fibonacci pivots:W · bounce-touch | -0.223 (0%) | -0.273 (0%) | -0.080 (29%) | -0.257 (0%) |
| fibonacci pivots:W · breakout | +0.192 (100%) | +0.182 (100%) | +0.129 (83%) | -0.054 (29%) |
| traditional pivots:D · bounce-rejection | -0.078 (25%) | -0.096 (17%) | -0.046 (12%) | -0.098 (4%) |
| traditional pivots:D · bounce-touch | -0.215 (0%) | -0.200 (0%) | -0.138 (0%) | -0.120 (0%) |
| traditional pivots:D · breakout | +0.100 (96%) | +0.128 (100%) | +0.071 (79%) | +0.039 (46%) |
| traditional pivots:M · bounce-rejection | -0.123 (25%) | -0.275 (4%) | -0.218 (0%) | +0.290 (75%) |
| traditional pivots:M · bounce-touch | +0.062 (46%) | -0.232 (38%) | +0.017 (56%) | +0.263 (75%) |
| traditional pivots:M · breakout | +0.354 (83%) | +0.390 (100%) | +0.190 (75%) | -0.088 (38%) |
| traditional pivots:W · bounce-rejection | -0.228 (0%) | -0.157 (4%) | -0.018 (38%) | -0.005 (25%) |
| traditional pivots:W · bounce-touch | -0.148 (17%) | -0.200 (0%) | -0.047 (25%) | -0.381 (0%) |
| traditional pivots:W · breakout | +0.232 (100%) | +0.151 (92%) | +0.125 (79%) | -0.084 (31%) |
| woodie pivots:D · bounce-rejection | -0.111 (0%) | -0.120 (8%) | -0.057 (12%) | -0.104 (0%) |
| woodie pivots:D · bounce-touch | -0.214 (0%) | -0.202 (0%) | -0.113 (0%) | -0.123 (0%) |
| woodie pivots:D · breakout | +0.085 (88%) | +0.135 (100%) | +0.051 (79%) | +0.041 (46%) |
| woodie pivots:M · bounce-rejection | -0.414 (0%) | -0.285 (0%) | +0.010 (50%) | +0.203 (75%) |
| woodie pivots:M · bounce-touch | -0.277 (12%) | -0.322 (17%) | -0.025 (38%) | -0.207 (0%) |
| woodie pivots:M · breakout | +0.688 (100%) | +0.295 (100%) | +0.276 (100%) | -0.030 (25%) |
| woodie pivots:W · bounce-rejection | -0.333 (0%) | -0.206 (0%) | -0.044 (33%) | +0.004 (44%) |
| woodie pivots:W · bounce-touch | -0.319 (0%) | -0.231 (0%) | -0.053 (46%) | -0.356 (0%) |
| woodie pivots:W · breakout | +0.155 (83%) | +0.134 (92%) | +0.179 (92%) | -0.035 (50%) |


## 1d

| Settings (top by BTC IS t-stat) | BTC IS | BTC OOS | ETH full | AVAX full | XRP full | Positive on |
|---|---|---|---|---|---|---|
| traditional pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | longs | +0.708 (n=85) | +0.141 (n=42) | +0.337 (n=120) | +0.222 (n=55) | +0.195 (n=39) | 4/4 |
| camarilla pivots:W breakout level2 stop1ATR target:2R exitAtPeriodEnd:yes | longs | +0.243 (n=212) | -0.056 (n=91) | +0.071 (n=271) | +0.042 (n=116) | -0.146 (n=78) | 2/4 |
| fibonacci pivots:W breakout level1 stop1ATR target:2R exitAtPeriodEnd:yes | longs | +0.277 (n=172) | -0.150 (n=74) | +0.167 (n=202) | +0.169 (n=84) | +0.012 (n=54) | 3/4 |
| fibonacci pivots:W breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | both | +0.488 (n=131) | +0.074 (n=65) | +0.158 (n=192) | +0.059 (n=87) | -0.269 (n=57) | 3/4 |
| traditional pivots:W breakout level1 stop0.5ATR target:2R exitAtPeriodEnd:no | both | +0.453 (n=149) | +0.013 (n=75) | +0.212 (n=221) | +0.231 (n=104) | +0.127 (n=74) | 4/4 |
| camarilla pivots:W breakout level2 stop1ATR target:next exitAtPeriodEnd:yes | longs | +0.207 (n=212) | -0.037 (n=91) | +0.085 (n=271) | +0.031 (n=116) | -0.139 (n=78) | 2/4 |
| fibonacci pivots:W breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | longs | +0.584 (n=82) | +0.182 (n=38) | +0.306 (n=107) | +0.030 (n=45) | -0.531 (n=30) | 3/4 |
| camarilla pivots:chart breakout level2 stop0.5ATR target:next exitAtPeriodEnd:no | longs | +0.474 (n=124) | +0.158 (n=54) | +0.063 (n=155) | +0.325 (n=51) | +0.052 (n=41) | 4/4 |
| camarilla pivots:chart breakout level2 stop0.5ATR target:2R exitAtPeriodEnd:no | longs | +0.462 (n=123) | +0.194 (n=54) | +0.063 (n=155) | +0.325 (n=51) | +0.052 (n=41) | 4/4 |
| camarilla pivots:W breakout level3 stop0.5ATR target:2R exitAtPeriodEnd:yes | longs | +0.291 (n=172) | -0.006 (n=77) | +0.078 (n=224) | -0.022 (n=103) | -0.187 (n=67) | 1/4 |

Entry families on 1d (all variants averaged, full history, both sides):

| Family | BTC avg R (% variants > 0) | ETH avg R (% variants > 0) | AVAX avg R (% variants > 0) | XRP avg R (% variants > 0) |
|---|---|---|---|---|
| camarilla pivots:M · bounce-rejection | -0.070 (29%) | -0.067 (21%) | -0.087 (33%) | -0.032 (33%) |
| camarilla pivots:M · bounce-touch | -0.191 (0%) | -0.283 (0%) | -0.148 (8%) | -0.219 (29%) |
| camarilla pivots:M · breakout | +0.120 (96%) | +0.154 (96%) | +0.096 (88%) | +0.095 (71%) |
| camarilla pivots:W · bounce-rejection | +0.017 (50%) | -0.016 (42%) | -0.040 (29%) | -0.057 (17%) |
| camarilla pivots:W · bounce-touch | -0.188 (0%) | -0.177 (0%) | -0.076 (25%) | -0.141 (4%) |
| camarilla pivots:W · breakout | +0.087 (92%) | +0.039 (75%) | +0.088 (92%) | -0.059 (21%) |
| camarilla pivots:chart · bounce-rejection | -0.034 (50%) | -0.043 (33%) | -0.162 (0%) | -0.118 (17%) |
| camarilla pivots:chart · bounce-touch | -0.175 (0%) | -0.169 (0%) | -0.199 (0%) | -0.183 (0%) |
| camarilla pivots:chart · breakout | +0.160 (100%) | +0.108 (100%) | +0.141 (83%) | +0.173 (100%) |
| fibonacci pivots:M · bounce-rejection | -0.174 (17%) | -0.055 (33%) | -0.019 (44%) | -0.038 (60%) |
| fibonacci pivots:M · bounce-touch | -0.317 (0%) | -0.247 (8%) | -0.201 (12%) | -0.123 (12%) |
| fibonacci pivots:M · breakout | +0.316 (100%) | +0.293 (96%) | +0.148 (94%) | +0.153 (100%) |
| fibonacci pivots:W · bounce-rejection | -0.064 (17%) | -0.063 (17%) | -0.023 (46%) | +0.026 (62%) |
| fibonacci pivots:W · bounce-touch | -0.238 (0%) | -0.239 (0%) | -0.073 (8%) | -0.151 (0%) |
| fibonacci pivots:W · breakout | +0.156 (100%) | +0.115 (92%) | +0.094 (92%) | -0.051 (25%) |
| fibonacci pivots:chart · bounce-rejection | -0.063 (33%) | -0.095 (17%) | -0.066 (17%) | -0.081 (25%) |
| fibonacci pivots:chart · bounce-touch | -0.266 (0%) | -0.234 (0%) | -0.181 (0%) | -0.231 (0%) |
| fibonacci pivots:chart · breakout | +0.130 (100%) | +0.123 (100%) | +0.262 (100%) | +0.089 (75%) |
| traditional pivots:M · bounce-rejection | -0.182 (25%) | -0.111 (6%) | -0.125 (12%) | -0.156 (12%) |
| traditional pivots:M · bounce-touch | -0.157 (21%) | -0.269 (4%) | -0.105 (25%) | +0.030 (50%) |
| traditional pivots:M · breakout | +0.150 (83%) | +0.182 (83%) | +0.257 (100%) | +0.033 (50%) |
| traditional pivots:W · bounce-rejection | -0.124 (4%) | -0.099 (8%) | -0.132 (25%) | -0.002 (50%) |
| traditional pivots:W · bounce-touch | -0.199 (0%) | -0.249 (0%) | -0.139 (4%) | -0.068 (33%) |
| traditional pivots:W · breakout | +0.142 (96%) | +0.077 (83%) | +0.055 (62%) | +0.007 (44%) |
| traditional pivots:chart · bounce-rejection | -0.059 (25%) | -0.063 (8%) | -0.052 (25%) | -0.065 (33%) |
| traditional pivots:chart · bounce-touch | -0.250 (0%) | -0.223 (0%) | -0.160 (0%) | -0.182 (8%) |
| traditional pivots:chart · breakout | +0.113 (100%) | +0.129 (100%) | +0.207 (100%) | +0.097 (75%) |
| woodie pivots:M · bounce-rejection | -0.258 (8%) | -0.244 (0%) | +0.142 (88%) | -0.003 (38%) |
| woodie pivots:M · bounce-touch | -0.354 (0%) | -0.291 (8%) | -0.078 (38%) | -0.232 (0%) |
| woodie pivots:M · breakout | +0.073 (58%) | +0.166 (75%) | +0.273 (100%) | +0.171 (100%) |
| woodie pivots:W · bounce-rejection | -0.108 (4%) | -0.112 (0%) | -0.167 (10%) | +0.075 (81%) |
| woodie pivots:W · bounce-touch | -0.232 (0%) | -0.238 (0%) | -0.154 (12%) | -0.136 (4%) |
| woodie pivots:W · breakout | +0.175 (96%) | +0.102 (83%) | +0.124 (93%) | +0.004 (69%) |
| woodie pivots:chart · bounce-rejection | -0.075 (25%) | -0.067 (0%) | -0.091 (0%) | -0.089 (17%) |
| woodie pivots:chart · bounce-touch | -0.249 (0%) | -0.220 (0%) | -0.163 (0%) | -0.200 (0%) |
| woodie pivots:chart · breakout | +0.119 (100%) | +0.133 (100%) | +0.246 (100%) | +0.059 (75%) |

