# Double Top / Bottom experiments (1d)

Universe: 34 symbols — SPY, QQQ, IWM, DIA, TLT, AAPL, MSFT, AMZN, GOOGL, META, NVDA, JPM, BAC, XOM, CVX, JNJ, PFE, PG, KO, WMT, HD, DIS, INTC, CSCO, T, BTC-USD, ETH-USD, GC=F, SI=F, CL=F, EURUSD=X, GBPUSD=X, USDJPY=X, AUDUSD=X

No commissions/slippage. Stop and target touched in the same bar = loss. R = multiple of risk. 'B/E win %' = win rate needed to break even at that R:R.

## Requested test: no second entry, enter only on a retest of the breakout point

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Retest only (limit at neckline) | 1:1 | off | Both | 691 | 51.7 | 50.0 | +0.042 | +29.1 | 1.09 | +53.2 | -24.1 | 62 | 24.1 |
| Retest only (limit at neckline) | 2:1 | off | Both | 707 | 35.5 | 33.3 | +0.060 | +42.6 | 1.09 | +88.1 | -45.4 | 56 | 25.5 |
| Retest only (limit at neckline) | 3:1 | off | Both | 668 | 27.7 | 25.0 | +0.099 | +66.2 | 1.13 | +133.2 | -67.0 | 47 | 33.5 |

## Top 10 configurations by avg R per trade (min 100 trades)

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Breakout only | 3:1 | SMA200 | Longs only | 326 | 35.9 | 25.0 | +0.441 | +143.9 | 1.67 | +143.9 | +0.0 | 71 | 15.0 |
| Breakout + Retest | 3:1 | SMA200 | Longs only | 611 | 35.0 | 25.0 | +0.408 | +249.4 | 1.62 | +249.4 | +0.0 | 76 | 26.0 |
| Breakout only | 3:1 | off | Longs only | 423 | 35.0 | 25.0 | +0.403 | +170.4 | 1.61 | +170.4 | +0.0 | 71 | 19.1 |
| Breakout + Retest | 3:1 | off | Longs only | 796 | 34.8 | 25.0 | +0.396 | +315.0 | 1.59 | +315.0 | +0.0 | 74 | 40.6 |
| Breakout + Midpoint (original) | 3:1 | SMA200 | Longs only | 521 | 34.2 | 25.0 | +0.370 | +192.7 | 1.55 | +192.7 | +0.0 | 71 | 28.0 |
| Retest only (limit at neckline) | 3:1 | off | Longs only | 396 | 33.8 | 25.0 | +0.357 | +141.3 | 1.53 | +141.3 | +0.0 | 62 | 22.9 |
| Retest only (limit at neckline) | 3:1 | SMA200 | Longs only | 297 | 33.7 | 25.0 | +0.355 | +105.5 | 1.52 | +105.5 | +0.0 | 65 | 14.0 |
| Breakout + Midpoint (original) | 3:1 | off | Longs only | 675 | 33.3 | 25.0 | +0.337 | +227.7 | 1.50 | +227.7 | +0.0 | 68 | 29.8 |
| Retest only (confirmed close) | 3:1 | SMA200 | Longs only | 251 | 33.5 | 25.0 | +0.337 | +84.5 | 1.50 | +84.5 | +0.0 | 68 | 14.1 |
| Retest only (confirmed close) | 3:1 | off | Longs only | 328 | 33.5 | 25.0 | +0.336 | +110.4 | 1.49 | +110.4 | +0.0 | 62 | 21.0 |

## All configurations — both directions

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Breakout + Midpoint (original) | 1:1 | off | Both | 1332 | 51.3 | 50.0 | +0.040 | +53.7 | 1.08 | +89.5 | -35.7 | 50 | 29.4 |
| Breakout + Midpoint (original) | 1:1 | SMA200 | Both | 869 | 51.2 | 50.0 | +0.043 | +37.6 | 1.09 | +64.6 | -27.0 | 53 | 28.1 |
| Breakout + Midpoint (original) | 2:1 | off | Both | 1206 | 36.9 | 33.3 | +0.103 | +124.7 | 1.16 | +173.6 | -48.9 | 68 | 55.0 |
| Breakout + Midpoint (original) | 2:1 | SMA200 | Both | 819 | 37.4 | 33.3 | +0.124 | +101.8 | 1.19 | +121.2 | -19.4 | 65 | 27.0 |
| Breakout + Midpoint (original) | 3:1 | off | Both | 1116 | 28.7 | 25.0 | +0.139 | +155.1 | 1.19 | +224.5 | -69.4 | 68 | 54.9 |
| Breakout + Midpoint (original) | 3:1 | SMA200 | Both | 777 | 29.7 | 25.0 | +0.189 | +146.7 | 1.26 | +165.7 | -19.0 | 68 | 29.9 |
| Breakout only | 1:1 | off | Both | 854 | 52.1 | 50.0 | +0.050 | +43.1 | 1.10 | +69.4 | -26.3 | 59 | 21.2 |
| Breakout only | 1:1 | SMA200 | Both | 563 | 52.8 | 50.0 | +0.066 | +37.3 | 1.14 | +48.9 | -11.6 | 59 | 18.3 |
| Breakout only | 2:1 | off | Both | 749 | 37.7 | 33.3 | +0.123 | +92.2 | 1.19 | +147.3 | -55.1 | 62 | 49.2 |
| Breakout only | 2:1 | SMA200 | Both | 517 | 38.7 | 33.3 | +0.161 | +83.2 | 1.26 | +107.0 | -23.8 | 65 | 25.0 |
| Breakout only | 3:1 | off | Both | 685 | 28.2 | 25.0 | +0.122 | +83.3 | 1.17 | +166.2 | -82.9 | 62 | 46.3 |
| Breakout only | 3:1 | SMA200 | Both | 486 | 29.8 | 25.0 | +0.196 | +95.0 | 1.27 | +127.7 | -32.7 | 65 | 23.1 |
| Retest only (limit at neckline) | 1:1 | off | Both | 691 | 51.7 | 50.0 | +0.042 | +29.1 | 1.09 | +53.2 | -24.1 | 62 | 24.1 |
| Retest only (limit at neckline) | 1:1 | SMA200 | Both | 449 | 53.7 | 50.0 | +0.084 | +37.8 | 1.18 | +38.8 | -1.0 | 56 | 18.1 |
| Retest only (limit at neckline) | 2:1 | off | Both | 707 | 35.5 | 33.3 | +0.060 | +42.6 | 1.09 | +88.1 | -45.4 | 56 | 25.5 |
| Retest only (limit at neckline) | 2:1 | SMA200 | Both | 464 | 34.3 | 33.3 | +0.029 | +13.3 | 1.04 | +46.6 | -33.3 | 47 | 26.5 |
| Retest only (limit at neckline) | 3:1 | off | Both | 668 | 27.7 | 25.0 | +0.099 | +66.2 | 1.13 | +133.2 | -67.0 | 47 | 33.5 |
| Retest only (limit at neckline) | 3:1 | SMA200 | Both | 445 | 28.3 | 25.0 | +0.136 | +60.6 | 1.19 | +101.5 | -40.9 | 53 | 22.4 |
| Retest only (confirmed close) | 1:1 | off | Both | 570 | 49.8 | 50.0 | +0.000 | +0.2 | 1.00 | +35.5 | -35.3 | 44 | 31.9 |
| Retest only (confirmed close) | 1:1 | SMA200 | Both | 375 | 50.4 | 50.0 | +0.015 | +5.7 | 1.03 | +26.9 | -21.3 | 50 | 18.9 |
| Retest only (confirmed close) | 2:1 | off | Both | 577 | 35.5 | 33.3 | +0.060 | +34.8 | 1.09 | +85.5 | -50.7 | 53 | 31.3 |
| Retest only (confirmed close) | 2:1 | SMA200 | Both | 394 | 35.3 | 33.3 | +0.064 | +25.4 | 1.10 | +56.5 | -31.1 | 47 | 17.9 |
| Retest only (confirmed close) | 3:1 | off | Both | 546 | 27.1 | 25.0 | +0.070 | +38.2 | 1.09 | +108.3 | -70.1 | 50 | 34.4 |
| Retest only (confirmed close) | 3:1 | SMA200 | Both | 378 | 27.2 | 25.0 | +0.087 | +32.8 | 1.12 | +75.5 | -42.8 | 50 | 25.8 |
| Breakout + Retest | 1:1 | off | Both | 1502 | 51.9 | 50.0 | +0.045 | +67.3 | 1.09 | +115.9 | -48.6 | 56 | 36.6 |
| Breakout + Retest | 1:1 | SMA200 | Both | 991 | 53.2 | 50.0 | +0.074 | +73.3 | 1.16 | +86.2 | -12.9 | 59 | 26.2 |
| Breakout + Retest | 2:1 | off | Both | 1378 | 37.1 | 33.3 | +0.106 | +146.5 | 1.16 | +229.3 | -82.8 | 62 | 69.0 |
| Breakout + Retest | 2:1 | SMA200 | Both | 941 | 36.7 | 33.3 | +0.100 | +93.8 | 1.15 | +146.4 | -52.6 | 53 | 42.3 |
| Breakout + Retest | 3:1 | off | Both | 1279 | 28.5 | 25.0 | +0.132 | +168.3 | 1.18 | +295.8 | -127.5 | 56 | 69.6 |
| Breakout + Retest | 3:1 | SMA200 | Both | 897 | 29.2 | 25.0 | +0.171 | +153.7 | 1.24 | +214.3 | -60.6 | 65 | 40.3 |

## All configurations — longs only

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Breakout + Midpoint (original) | 1:1 | off | Longs only | 740 | 55.4 | 50.0 | +0.128 | +94.8 | 1.28 | +94.8 | +0.0 | 65 | 16.0 |
| Breakout + Midpoint (original) | 1:1 | SMA200 | Longs only | 553 | 54.8 | 50.0 | +0.123 | +67.8 | 1.27 | +67.8 | +0.0 | 74 | 20.1 |
| Breakout + Midpoint (original) | 2:1 | off | Longs only | 707 | 42.0 | 33.3 | +0.261 | +184.3 | 1.44 | +184.3 | +0.0 | 71 | 31.2 |
| Breakout + Midpoint (original) | 2:1 | SMA200 | Longs only | 534 | 41.8 | 33.3 | +0.255 | +136.3 | 1.43 | +136.3 | +0.0 | 62 | 22.0 |
| Breakout + Midpoint (original) | 3:1 | off | Longs only | 675 | 33.3 | 25.0 | +0.337 | +227.7 | 1.50 | +227.7 | +0.0 | 68 | 29.8 |
| Breakout + Midpoint (original) | 3:1 | SMA200 | Longs only | 521 | 34.2 | 25.0 | +0.370 | +192.7 | 1.55 | +192.7 | +0.0 | 71 | 28.0 |
| Breakout only | 1:1 | off | Longs only | 484 | 56.6 | 50.0 | +0.146 | +70.6 | 1.33 | +70.6 | +0.0 | 62 | 13.0 |
| Breakout only | 1:1 | SMA200 | Longs only | 361 | 56.2 | 50.0 | +0.142 | +51.2 | 1.32 | +51.2 | +0.0 | 71 | 10.1 |
| Breakout only | 2:1 | off | Longs only | 450 | 44.4 | 33.3 | +0.332 | +149.5 | 1.59 | +149.5 | +0.0 | 65 | 20.5 |
| Breakout only | 2:1 | SMA200 | Longs only | 339 | 44.5 | 33.3 | +0.336 | +114.0 | 1.59 | +114.0 | +0.0 | 68 | 15.6 |
| Breakout only | 3:1 | off | Longs only | 423 | 35.0 | 25.0 | +0.403 | +170.4 | 1.61 | +170.4 | +0.0 | 71 | 19.1 |
| Breakout only | 3:1 | SMA200 | Longs only | 326 | 35.9 | 25.0 | +0.441 | +143.9 | 1.67 | +143.9 | +0.0 | 71 | 15.0 |
| Retest only (limit at neckline) | 1:1 | off | Longs only | 387 | 56.1 | 50.0 | +0.133 | +51.3 | 1.30 | +51.3 | +0.0 | 56 | 12.8 |
| Retest only (limit at neckline) | 1:1 | SMA200 | Longs only | 289 | 56.1 | 50.0 | +0.134 | +38.8 | 1.30 | +38.8 | +0.0 | 50 | 10.1 |
| Retest only (limit at neckline) | 2:1 | off | Longs only | 406 | 40.4 | 33.3 | +0.211 | +85.6 | 1.35 | +85.6 | +0.0 | 59 | 18.5 |
| Retest only (limit at neckline) | 2:1 | SMA200 | Longs only | 299 | 38.5 | 33.3 | +0.153 | +45.6 | 1.24 | +45.6 | +0.0 | 59 | 15.3 |
| Retest only (limit at neckline) | 3:1 | off | Longs only | 396 | 33.8 | 25.0 | +0.357 | +141.3 | 1.53 | +141.3 | +0.0 | 62 | 22.9 |
| Retest only (limit at neckline) | 3:1 | SMA200 | Longs only | 297 | 33.7 | 25.0 | +0.355 | +105.5 | 1.52 | +105.5 | +0.0 | 65 | 14.0 |
| Retest only (confirmed close) | 1:1 | off | Longs only | 323 | 55.1 | 50.0 | +0.113 | +36.4 | 1.25 | +36.4 | +0.0 | 53 | 11.6 |
| Retest only (confirmed close) | 1:1 | SMA200 | Longs only | 243 | 54.7 | 50.0 | +0.107 | +25.9 | 1.23 | +25.9 | +0.0 | 47 | 8.3 |
| Retest only (confirmed close) | 2:1 | off | Longs only | 341 | 41.6 | 33.3 | +0.255 | +87.1 | 1.43 | +87.1 | +0.0 | 53 | 18.3 |
| Retest only (confirmed close) | 2:1 | SMA200 | Longs only | 255 | 40.4 | 33.3 | +0.222 | +56.6 | 1.36 | +56.6 | +0.0 | 59 | 10.0 |
| Retest only (confirmed close) | 3:1 | off | Longs only | 328 | 33.5 | 25.0 | +0.336 | +110.4 | 1.49 | +110.4 | +0.0 | 62 | 21.0 |
| Retest only (confirmed close) | 3:1 | SMA200 | Longs only | 251 | 33.5 | 25.0 | +0.337 | +84.5 | 1.50 | +84.5 | +0.0 | 68 | 14.1 |
| Breakout + Retest | 1:1 | off | Longs only | 864 | 56.4 | 50.0 | +0.139 | +119.7 | 1.31 | +119.7 | +0.0 | 56 | 24.8 |
| Breakout + Retest | 1:1 | SMA200 | Longs only | 645 | 56.3 | 50.0 | +0.141 | +91.0 | 1.32 | +91.0 | +0.0 | 68 | 19.3 |
| Breakout + Retest | 2:1 | off | Longs only | 831 | 42.8 | 33.3 | +0.284 | +236.2 | 1.49 | +236.2 | +0.0 | 62 | 32.6 |
| Breakout + Retest | 2:1 | SMA200 | Longs only | 624 | 42.0 | 33.3 | +0.259 | +161.5 | 1.44 | +161.5 | +0.0 | 62 | 25.6 |
| Breakout + Retest | 3:1 | off | Longs only | 796 | 34.8 | 25.0 | +0.396 | +315.0 | 1.59 | +315.0 | +0.0 | 74 | 40.6 |
| Breakout + Retest | 3:1 | SMA200 | Longs only | 611 | 35.0 | 25.0 | +0.408 | +249.4 | 1.62 | +249.4 | +0.0 | 76 | 26.0 |

## Benchmark vs random entries (same symbol, direction, stop %, R:R)

```
config                        RR  trades    avgR   ctrlR    edge |  <2015 n   avgR | >=2015 n   avgR
Breakout only, longs           1     484  +0.146  +0.130  +0.016 |      308 +0.144 |      176 +0.149
Breakout only, longs           2     450  +0.332  +0.301  +0.031 |      287 +0.348 |      163 +0.304
Breakout only, longs           3     423  +0.403  +0.446  -0.043 |      273 +0.452 |      150 +0.313
Breakout+Retest, longs         1     864  +0.139  +0.135  +0.004 |      555 +0.148 |      309 +0.122
Breakout+Retest, longs         2     831  +0.284  +0.281  +0.003 |      532 +0.310 |      299 +0.239
Breakout+Retest, longs         3     796  +0.396  +0.393  +0.002 |      512 +0.455 |      284 +0.288
Retest only, longs             1     387  +0.133  +0.122  +0.010 |      250 +0.163 |      137 +0.077
Retest only, longs             2     406  +0.211  +0.222  -0.011 |      261 +0.244 |      145 +0.151
Retest only, longs             3     396  +0.357  +0.355  +0.001 |      257 +0.434 |      139 +0.215
Breakout+Midpoint, longs       1     740  +0.128  +0.089  +0.040 |      479 +0.144 |      261 +0.099
Breakout+Midpoint, longs       2     707  +0.261  +0.243  +0.018 |      459 +0.283 |      248 +0.220
Breakout+Midpoint, longs       3     675  +0.337  +0.301  +0.036 |      439 +0.419 |      236 +0.186
Breakout only, shorts          1     419  -0.069  -0.167  +0.098 |      262 -0.117 |      157 +0.011
Breakout only, shorts          2     386  -0.165  -0.318  +0.153 |      249 -0.240 |      137 -0.029
Breakout only, shorts          3     367  -0.274  -0.408  +0.134 |      235 -0.352 |      132 -0.135
```
