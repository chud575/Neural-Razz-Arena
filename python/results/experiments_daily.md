# Double Top / Bottom experiments (1d)

Universe: 34 symbols — SPY, QQQ, IWM, DIA, TLT, AAPL, MSFT, AMZN, GOOGL, META, NVDA, JPM, BAC, XOM, CVX, JNJ, PFE, PG, KO, WMT, HD, DIS, INTC, CSCO, T, BTC-USD, ETH-USD, GC=F, SI=F, CL=F, EURUSD=X, GBPUSD=X, USDJPY=X, AUDUSD=X

No commissions/slippage. Stop and target touched in the same bar = loss. R = multiple of risk. 'B/E win %' = win rate needed to break even at that R:R.

## Requested test: no second entry, enter only on a retest of the breakout point

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Retest only (limit at neckline) | 1:1 | off | Both | 686 | 50.7 | 50.0 | +0.045 | +30.9 | 1.09 | +55.9 | -25.0 | 56 | 25.0 |
| Retest only (limit at neckline) | 2:1 | off | Both | 699 | 35.2 | 33.3 | +0.074 | +51.9 | 1.11 | +95.0 | -43.1 | 56 | 22.5 |
| Retest only (limit at neckline) | 3:1 | off | Both | 662 | 26.9 | 25.0 | +0.088 | +58.0 | 1.12 | +120.5 | -62.5 | 50 | 40.5 |

## Top 10 configurations by avg R per trade (min 100 trades)

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Breakout only | 3:1 | SMA200 | Longs only | 326 | 35.9 | 25.0 | +0.441 | +143.9 | 1.67 | +143.9 | +0.0 | 71 | 15.0 |
| Breakout only | 3:1 | off | Longs only | 423 | 35.0 | 25.0 | +0.403 | +170.4 | 1.61 | +170.4 | +0.0 | 71 | 19.1 |
| Breakout + Retest | 3:1 | SMA200 | Longs only | 611 | 34.5 | 25.0 | +0.397 | +242.9 | 1.60 | +242.9 | +0.0 | 74 | 26.0 |
| Breakout + Retest | 3:1 | off | Longs only | 796 | 34.3 | 25.0 | +0.385 | +306.7 | 1.58 | +306.7 | +0.0 | 68 | 38.9 |
| Breakout + Midpoint (original) | 3:1 | SMA200 | Longs only | 521 | 34.2 | 25.0 | +0.372 | +193.9 | 1.56 | +193.9 | +0.0 | 71 | 27.9 |
| Retest only (confirmed close) | 3:1 | SMA200 | Longs only | 251 | 33.5 | 25.0 | +0.337 | +84.5 | 1.50 | +84.5 | +0.0 | 68 | 14.1 |
| Retest only (confirmed close) | 3:1 | off | Longs only | 328 | 33.5 | 25.0 | +0.336 | +110.4 | 1.49 | +110.4 | +0.0 | 62 | 21.0 |
| Breakout only | 2:1 | SMA200 | Longs only | 339 | 44.5 | 33.3 | +0.336 | +114.0 | 1.59 | +114.0 | +0.0 | 68 | 15.6 |
| Breakout + Midpoint (original) | 3:1 | off | Longs only | 675 | 33.2 | 25.0 | +0.333 | +224.5 | 1.49 | +224.5 | +0.0 | 68 | 29.6 |
| Breakout only | 2:1 | off | Longs only | 450 | 44.4 | 33.3 | +0.332 | +149.5 | 1.59 | +149.5 | +0.0 | 65 | 20.5 |

## All configurations — both directions

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Breakout + Midpoint (original) | 1:1 | off | Both | 1332 | 50.9 | 50.0 | +0.043 | +56.8 | 1.09 | +89.2 | -32.4 | 50 | 25.4 |
| Breakout + Midpoint (original) | 1:1 | SMA200 | Both | 869 | 51.0 | 50.0 | +0.045 | +39.4 | 1.09 | +64.2 | -24.9 | 53 | 25.5 |
| Breakout + Midpoint (original) | 2:1 | off | Both | 1206 | 36.8 | 33.3 | +0.110 | +132.7 | 1.17 | +177.2 | -44.5 | 68 | 57.0 |
| Breakout + Midpoint (original) | 2:1 | SMA200 | Both | 819 | 37.2 | 33.3 | +0.128 | +104.6 | 1.20 | +123.7 | -19.1 | 65 | 27.9 |
| Breakout + Midpoint (original) | 3:1 | off | Both | 1116 | 28.6 | 25.0 | +0.143 | +159.7 | 1.20 | +221.3 | -61.6 | 65 | 54.4 |
| Breakout + Midpoint (original) | 3:1 | SMA200 | Both | 777 | 29.7 | 25.0 | +0.195 | +151.2 | 1.27 | +167.1 | -15.9 | 68 | 29.4 |
| Breakout only | 1:1 | off | Both | 854 | 52.1 | 50.0 | +0.050 | +43.1 | 1.10 | +69.4 | -26.3 | 59 | 21.2 |
| Breakout only | 1:1 | SMA200 | Both | 563 | 52.8 | 50.0 | +0.066 | +37.3 | 1.14 | +48.9 | -11.6 | 59 | 18.3 |
| Breakout only | 2:1 | off | Both | 749 | 37.7 | 33.3 | +0.123 | +92.2 | 1.19 | +147.3 | -55.1 | 62 | 49.2 |
| Breakout only | 2:1 | SMA200 | Both | 517 | 38.7 | 33.3 | +0.161 | +83.2 | 1.26 | +107.0 | -23.8 | 65 | 25.0 |
| Breakout only | 3:1 | off | Both | 685 | 28.2 | 25.0 | +0.122 | +83.3 | 1.17 | +166.2 | -82.9 | 62 | 46.3 |
| Breakout only | 3:1 | SMA200 | Both | 486 | 29.8 | 25.0 | +0.196 | +95.0 | 1.27 | +127.7 | -32.7 | 65 | 23.1 |
| Retest only (limit at neckline) | 1:1 | off | Both | 686 | 50.7 | 50.0 | +0.045 | +30.9 | 1.09 | +55.9 | -25.0 | 56 | 25.0 |
| Retest only (limit at neckline) | 1:1 | SMA200 | Both | 446 | 52.9 | 50.0 | +0.088 | +39.2 | 1.19 | +40.2 | -1.1 | 62 | 18.0 |
| Retest only (limit at neckline) | 2:1 | off | Both | 699 | 35.2 | 33.3 | +0.074 | +51.9 | 1.11 | +95.0 | -43.1 | 56 | 22.5 |
| Retest only (limit at neckline) | 2:1 | SMA200 | Both | 460 | 34.3 | 33.3 | +0.050 | +23.0 | 1.08 | +53.1 | -30.1 | 50 | 22.9 |
| Retest only (limit at neckline) | 3:1 | off | Both | 662 | 26.9 | 25.0 | +0.088 | +58.0 | 1.12 | +120.5 | -62.5 | 50 | 40.5 |
| Retest only (limit at neckline) | 3:1 | SMA200 | Both | 444 | 27.3 | 25.0 | +0.112 | +49.9 | 1.15 | +91.9 | -42.0 | 53 | 25.0 |
| Retest only (confirmed close) | 1:1 | off | Both | 570 | 49.8 | 50.0 | +0.000 | +0.2 | 1.00 | +35.5 | -35.3 | 44 | 31.9 |
| Retest only (confirmed close) | 1:1 | SMA200 | Both | 375 | 50.4 | 50.0 | +0.015 | +5.7 | 1.03 | +26.9 | -21.3 | 50 | 18.9 |
| Retest only (confirmed close) | 2:1 | off | Both | 577 | 35.5 | 33.3 | +0.060 | +34.8 | 1.09 | +85.5 | -50.7 | 53 | 31.3 |
| Retest only (confirmed close) | 2:1 | SMA200 | Both | 394 | 35.3 | 33.3 | +0.064 | +25.4 | 1.10 | +56.5 | -31.1 | 47 | 17.9 |
| Retest only (confirmed close) | 3:1 | off | Both | 546 | 27.1 | 25.0 | +0.070 | +38.2 | 1.09 | +108.3 | -70.1 | 50 | 34.4 |
| Retest only (confirmed close) | 3:1 | SMA200 | Both | 378 | 27.2 | 25.0 | +0.087 | +32.8 | 1.12 | +75.5 | -42.8 | 50 | 25.8 |
| Breakout + Retest | 1:1 | off | Both | 1502 | 51.5 | 50.0 | +0.048 | +72.0 | 1.10 | +118.6 | -46.6 | 56 | 37.1 |
| Breakout + Retest | 1:1 | SMA200 | Both | 991 | 52.9 | 50.0 | +0.076 | +75.6 | 1.16 | +87.5 | -11.9 | 59 | 25.6 |
| Breakout + Retest | 2:1 | off | Both | 1378 | 36.8 | 33.3 | +0.109 | +150.2 | 1.17 | +234.0 | -83.7 | 65 | 65.6 |
| Breakout + Retest | 2:1 | SMA200 | Both | 941 | 36.7 | 33.3 | +0.109 | +102.3 | 1.17 | +151.7 | -49.4 | 56 | 39.8 |
| Breakout + Retest | 3:1 | off | Both | 1279 | 28.1 | 25.0 | +0.126 | +161.1 | 1.17 | +285.7 | -124.7 | 56 | 72.3 |
| Breakout + Retest | 3:1 | SMA200 | Both | 897 | 28.8 | 25.0 | +0.162 | +145.7 | 1.23 | +207.4 | -61.8 | 65 | 40.3 |

## All configurations — longs only

| Entry setup | R:R | Trend filter | Direction | Trades | Win % | B/E win % | Avg R | Net R | PF | Long R | Short R | % symbols + | Max DD (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Breakout + Midpoint (original) | 1:1 | off | Longs only | 740 | 55.1 | 50.0 | +0.127 | +94.2 | 1.28 | +94.2 | +0.0 | 65 | 15.8 |
| Breakout + Midpoint (original) | 1:1 | SMA200 | Longs only | 553 | 54.6 | 50.0 | +0.122 | +67.5 | 1.27 | +67.5 | +0.0 | 74 | 20.0 |
| Breakout + Midpoint (original) | 2:1 | off | Longs only | 707 | 42.0 | 33.3 | +0.266 | +187.9 | 1.45 | +187.9 | +0.0 | 71 | 31.0 |
| Breakout + Midpoint (original) | 2:1 | SMA200 | Longs only | 534 | 41.8 | 33.3 | +0.260 | +138.9 | 1.44 | +138.9 | +0.0 | 65 | 22.0 |
| Breakout + Midpoint (original) | 3:1 | off | Longs only | 675 | 33.2 | 25.0 | +0.333 | +224.5 | 1.49 | +224.5 | +0.0 | 68 | 29.6 |
| Breakout + Midpoint (original) | 3:1 | SMA200 | Longs only | 521 | 34.2 | 25.0 | +0.372 | +193.9 | 1.56 | +193.9 | +0.0 | 71 | 27.9 |
| Breakout only | 1:1 | off | Longs only | 484 | 56.6 | 50.0 | +0.146 | +70.6 | 1.33 | +70.6 | +0.0 | 62 | 13.0 |
| Breakout only | 1:1 | SMA200 | Longs only | 361 | 56.2 | 50.0 | +0.142 | +51.2 | 1.32 | +51.2 | +0.0 | 71 | 10.1 |
| Breakout only | 2:1 | off | Longs only | 450 | 44.4 | 33.3 | +0.332 | +149.5 | 1.59 | +149.5 | +0.0 | 65 | 20.5 |
| Breakout only | 2:1 | SMA200 | Longs only | 339 | 44.5 | 33.3 | +0.336 | +114.0 | 1.59 | +114.0 | +0.0 | 68 | 15.6 |
| Breakout only | 3:1 | off | Longs only | 423 | 35.0 | 25.0 | +0.403 | +170.4 | 1.61 | +170.4 | +0.0 | 71 | 19.1 |
| Breakout only | 3:1 | SMA200 | Longs only | 326 | 35.9 | 25.0 | +0.441 | +143.9 | 1.67 | +143.9 | +0.0 | 71 | 15.0 |
| Retest only (limit at neckline) | 1:1 | off | Longs only | 386 | 54.9 | 50.0 | +0.133 | +51.3 | 1.30 | +51.3 | +0.0 | 62 | 11.7 |
| Retest only (limit at neckline) | 1:1 | SMA200 | Longs only | 288 | 54.9 | 50.0 | +0.130 | +37.3 | 1.29 | +37.3 | +0.0 | 65 | 11.2 |
| Retest only (limit at neckline) | 2:1 | off | Longs only | 403 | 40.2 | 33.3 | +0.226 | +91.2 | 1.38 | +91.2 | +0.0 | 59 | 16.8 |
| Retest only (limit at neckline) | 2:1 | SMA200 | Longs only | 298 | 38.6 | 33.3 | +0.175 | +52.3 | 1.29 | +52.3 | +0.0 | 62 | 14.2 |
| Retest only (limit at neckline) | 3:1 | off | Longs only | 393 | 32.6 | 25.0 | +0.326 | +128.2 | 1.49 | +128.2 | +0.0 | 62 | 21.2 |
| Retest only (limit at neckline) | 3:1 | SMA200 | Longs only | 296 | 32.4 | 25.0 | +0.325 | +96.1 | 1.48 | +96.1 | +0.0 | 65 | 14.0 |
| Retest only (confirmed close) | 1:1 | off | Longs only | 323 | 55.1 | 50.0 | +0.113 | +36.4 | 1.25 | +36.4 | +0.0 | 53 | 11.6 |
| Retest only (confirmed close) | 1:1 | SMA200 | Longs only | 243 | 54.7 | 50.0 | +0.107 | +25.9 | 1.23 | +25.9 | +0.0 | 47 | 8.3 |
| Retest only (confirmed close) | 2:1 | off | Longs only | 341 | 41.6 | 33.3 | +0.255 | +87.1 | 1.43 | +87.1 | +0.0 | 53 | 18.3 |
| Retest only (confirmed close) | 2:1 | SMA200 | Longs only | 255 | 40.4 | 33.3 | +0.222 | +56.6 | 1.36 | +56.6 | +0.0 | 59 | 10.0 |
| Retest only (confirmed close) | 3:1 | off | Longs only | 328 | 33.5 | 25.0 | +0.336 | +110.4 | 1.49 | +110.4 | +0.0 | 62 | 21.0 |
| Retest only (confirmed close) | 3:1 | SMA200 | Longs only | 251 | 33.5 | 25.0 | +0.337 | +84.5 | 1.50 | +84.5 | +0.0 | 68 | 14.1 |
| Breakout + Retest | 1:1 | off | Longs only | 864 | 55.9 | 50.0 | +0.140 | +120.8 | 1.32 | +120.8 | +0.0 | 56 | 22.8 |
| Breakout + Retest | 1:1 | SMA200 | Longs only | 645 | 55.8 | 50.0 | +0.140 | +90.5 | 1.32 | +90.5 | +0.0 | 71 | 20.6 |
| Breakout + Retest | 2:1 | off | Longs only | 831 | 42.7 | 33.3 | +0.291 | +241.4 | 1.50 | +241.4 | +0.0 | 65 | 30.6 |
| Breakout + Retest | 2:1 | SMA200 | Longs only | 624 | 42.0 | 33.3 | +0.268 | +167.0 | 1.46 | +167.0 | +0.0 | 71 | 23.9 |
| Breakout + Retest | 3:1 | off | Longs only | 796 | 34.3 | 25.0 | +0.385 | +306.7 | 1.58 | +306.7 | +0.0 | 68 | 38.9 |
| Breakout + Retest | 3:1 | SMA200 | Longs only | 611 | 34.5 | 25.0 | +0.397 | +242.9 | 1.60 | +242.9 | +0.0 | 74 | 26.0 |

## Benchmark vs random entries (same symbol, direction, stop %, R:R)

```
config                        RR  trades    avgR   ctrlR    edge |  <2015 n   avgR | >=2015 n   avgR
Breakout only, longs           1     484  +0.146  +0.130  +0.016 |      308 +0.144 |      176 +0.149
Breakout only, longs           2     450  +0.332  +0.301  +0.031 |      287 +0.348 |      163 +0.304
Breakout only, longs           3     423  +0.403  +0.446  -0.043 |      273 +0.452 |      150 +0.313
Breakout+Retest, longs         1     864  +0.140  +0.136  +0.004 |      555 +0.150 |      309 +0.121
Breakout+Retest, longs         2     831  +0.291  +0.281  +0.009 |      532 +0.312 |      299 +0.252
Breakout+Retest, longs         3     796  +0.385  +0.396  -0.011 |      512 +0.440 |      284 +0.287
Retest only, longs             1     386  +0.133  +0.112  +0.020 |      250 +0.160 |      136 +0.083
Retest only, longs             2     403  +0.226  +0.265  -0.038 |      259 +0.249 |      144 +0.186
Retest only, longs             3     393  +0.326  +0.328  -0.002 |      254 +0.389 |      139 +0.212
Breakout+Midpoint, longs       1     740  +0.127  +0.113  +0.015 |      479 +0.144 |      261 +0.097
Breakout+Midpoint, longs       2     707  +0.266  +0.234  +0.032 |      459 +0.287 |      248 +0.226
Breakout+Midpoint, longs       3     675  +0.333  +0.332  +0.001 |      439 +0.409 |      236 +0.190
Breakout only, shorts          1     419  -0.069  -0.125  +0.056 |      262 -0.117 |      157 +0.011
Breakout only, shorts          2     386  -0.165  -0.294  +0.129 |      249 -0.240 |      137 -0.029
Breakout only, shorts          3     367  -0.274  -0.404  +0.130 |      235 -0.352 |      132 -0.135
```
