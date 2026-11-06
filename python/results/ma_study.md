# SMA 50/100/200 — Idea 1: wick below the SMA 200 and close back above, in an uptrend

Coins BTC, ETH, AVAX, XRP (Coinbase; XRP from Jul 2023). Event: SMA100 above SMA200 for ≥ N bars, previous close above the SMA200, a wick below it, and a close back above (same bar: K=0, or within 5 bars: K=5). Entry at that close. ATR = ATR(14) at entry. Stop for the hit-rate and trade numbers = lowest low of the touch − 0.1 ATR. **Baseline** = every bar in the same uptrend regime above the SMA200, with a stop at the same ATR distance. Trade results are net of Bybit VIP 3 futures costs. IS = first 70% of each history, OOS = last 30%.

## 1. How far does price move after the reclaim? (longs, N = 50, all coins pooled)

| TF | Reclaim | Events | Median stop (ATR) | Median best move, 20 bars (baseline) | Median worst move, 20 bars | Median best move, 100 bars | Median worst move, 100 bars |
|---|---|---|---|---|---|---|---|
| 15m | same bar | 6339 | 0.69 | 1.71 (1.76) | 1.93 (1.84) | 4.25 (4.61) | 4.64 (4.55) |
| 15m | within 5 | 9668 | 0.88 | 1.72 (1.76) | 1.92 (1.84) | 4.25 (4.61) | 4.64 (4.55) |
| 1h | same bar | 2070 | 0.70 | 1.57 (1.87) | 1.95 (1.90) | 4.08 (4.50) | 4.19 (4.34) |
| 1h | within 5 | 3020 | 0.85 | 1.60 (1.87) | 1.89 (1.90) | 4.17 (4.50) | 4.20 (4.34) |
| 4h | same bar | 468 | 0.71 | 1.83 (1.85) | 1.75 (1.92) | 3.51 (4.60) | 4.02 (4.23) |
| 4h | within 5 | 687 | 0.85 | 1.77 (1.85) | 1.70 (1.92) | 3.56 (4.60) | 3.97 (4.23) |
| 1d | same bar | 62 | 0.54 | 1.12 (1.92) | 2.16 (1.84) | 2.19 (6.38) | 4.78 (3.72) |
| 1d | within 5 | 89 | 0.82 | 0.99 (1.92) | 2.23 (1.84) | 1.95 (6.38) | 4.85 (3.72) |

## 2. How often does it reach +k ATR before the stop? (longs, N = 50, same-bar reclaim; baseline in brackets)

| TF | Events | +1 ATR | +1.5 ATR | +2 ATR | +3 ATR | +4 ATR | +5 ATR |
|---|---|---|---|---|---|---|---|
| 15m | 6339 | 39% (43%) | 31% (34%) | 26% (28%) | 19% (21%) | 16% (17%) | 13% (15%) |
| 1h | 2070 | 37% (42%) | 29% (34%) | 24% (28%) | 18% (21%) | 15% (18%) | 14% (15%) |
| 4h | 468 | 40% (43%) | 33% (35%) | 29% (29%) | 23% (22%) | 20% (19%) | 18% (16%) |
| 1d | 62 | 27% (40%) | 19% (33%) | 18% (28%) | 13% (23%) | 10% (20%) | 10% (19%) |

## 3. Trade result: target +k ATR, stop under the wick, net of fees (avg R per trade; baseline in brackets)

**Longs** (N = 50, same-bar reclaim)

| TF | Period | Events | +1 ATR | +1.5 ATR | +2 ATR | +3 ATR | +4 ATR | +5 ATR |
|---|---|---|---|---|---|---|---|---|
| 15m | IS | 4517 | -0.37 (-0.21) | -0.35 (-0.22) | -0.35 (-0.21) | -0.35 (-0.19) | -0.34 (-0.16) | -0.33 (-0.12) |
| 15m | OOS | 1822 | -0.32 (-0.25) | -0.31 (-0.27) | -0.30 (-0.28) | -0.34 (-0.26) | -0.29 (-0.26) | -0.27 (-0.22) |
| 1h | IS | 1450 | -0.32 (-0.13) | -0.34 (-0.11) | -0.35 (-0.07) | -0.39 (-0.04) | -0.32 (+0.01) | -0.24 (+0.06) |
| 1h | OOS | 620 | -0.13 (-0.17) | -0.14 (-0.16) | -0.18 (-0.18) | -0.08 (-0.17) | -0.04 (-0.17) | +0.05 (-0.15) |
| 4h | IS | 327 | -0.18 (-0.08) | -0.15 (-0.05) | -0.18 (-0.03) | -0.18 (-0.02) | -0.11 (+0.07) | +0.00 (+0.14) |
| 4h | OOS | 141 | +0.05 (-0.04) | +0.12 (-0.02) | +0.30 (+0.01) | +0.43 (+0.04) | +0.55 (+0.05) | +0.74 (+0.07) |
| 1d | IS | 48 | -0.41 (-0.07) | -0.63 (+0.02) | -0.62 (+0.09) | -0.60 (+0.24) | -0.61 (+0.41) | -0.53 (+0.58) |
| 1d | OOS | 14 | -0.46 (-0.13) | -0.45 (-0.17) | -0.32 (-0.24) | -0.74 (-0.24) | -1.09 (-0.21) | -1.09 (-0.10) |

**Shorts** (N = 50, same-bar reclaim)

| TF | Period | Events | +1 ATR | +1.5 ATR | +2 ATR | +3 ATR | +4 ATR | +5 ATR |
|---|---|---|---|---|---|---|---|---|
| 15m | IS | 3939 | -0.37 (-0.17) | -0.37 (-0.13) | -0.39 (-0.13) | -0.36 (-0.06) | -0.37 (-0.02) | -0.29 (-0.03) |
| 15m | OOS | 1695 | -0.28 (-0.20) | -0.33 (-0.19) | -0.35 (-0.21) | -0.39 (-0.18) | -0.41 (-0.16) | -0.42 (-0.14) |
| 1h | IS | 1191 | -0.10 (-0.06) | -0.09 (-0.01) | -0.22 (+0.00) | -0.16 (+0.03) | -0.11 (+0.06) | -0.08 (+0.08) |
| 1h | OOS | 589 | -0.29 (-0.05) | -0.24 (-0.02) | -0.24 (+0.03) | -0.25 (+0.07) | -0.20 (+0.15) | -0.21 (+0.14) |
| 4h | IS | 257 | +0.03 (+0.01) | +0.05 (+0.05) | +0.11 (+0.06) | +0.20 (+0.13) | +0.38 (+0.19) | +0.51 (+0.24) |
| 4h | OOS | 132 | -0.24 (-0.00) | -0.13 (-0.00) | +0.02 (-0.04) | +0.07 (-0.04) | +0.16 (+0.04) | -0.25 (+0.02) |
| 1d | IS | 19 | -0.44 (+0.05) | -0.62 (+0.02) | -0.52 (-0.01) | -0.33 (-0.01) | -0.14 (+0.04) | +0.05 (+0.12) |
| 1d | OOS | 12 | +0.28 (+0.01) | +0.49 (-0.06) | -0.31 (-0.12) | -0.65 (-0.12) | -0.96 (-0.09) | -0.96 (-0.02) |

## 4. Per coin (longs, N = 50, same-bar reclaim, target +3 ATR): event minus baseline, net R

| TF | BTC IS / OOS | ETH IS / OOS | AVAX IS / OOS | XRP IS / OOS |
|---|---|---|---|---|
| 15m | -0.19 (n=1433) / -0.11 (n=573) | -0.01 (n=1473) / +0.15 (n=690) | -0.20 (n=809) / -0.33 (n=311) | -0.26 (n=802) / -0.36 (n=248) |
| 1h | -0.59 (n=470) / +0.23 (n=231) | -0.27 (n=569) / -0.18 (n=244) | -0.15 (n=213) / +0.46 (n=109) | -0.37 (n=198) / +0.30 (n=36) |
| 4h | -0.68 (n=116) / +0.55 (n=61) | -0.09 (n=119) / +0.63 (n=44) | +0.37 (n=39) / -0.22 (n=30) | +0.00 (n=53) / +0.80 (n=6) |
| 1d | -1.21 (n=15) / -0.30 (n=10) | -0.48 (n=19) / – | -0.76 (n=9) / – | -0.29 (n=5) / – |

## 5. What makes it better or worse? (longs, N = 50, both reclaim modes, target +3 ATR, net R per trade)

Each cell: IS / OOS average for events in that bucket. A feature is only interesting if it moves results the same way in-sample and out-of-sample, on most timeframes and coins (last column = how many of the 16 coin × timeframe cells, OOS, are above the overall average for that cell).

**SMA50 below SMA100 at the touch (white crossed yellow)**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| False | -0.33 / -0.35 (n=6331) | -0.40 / +0.09 (n=2255) | -0.28 / +0.47 (n=447) | -0.42 / -1.08 (n=64) | 4/12 |
| True | -0.31 / -0.28 (n=9676) | -0.31 / -0.23 (n=2835) | -0.13 / +0.37 (n=708) | -0.73 / -0.73 (n=87) | 10/14 |

**SMA50 below SMA200 at the touch**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| False | -0.28 / -0.27 (n=13430) | -0.33 / -0.00 (n=4285) | -0.07 / +0.38 (n=964) | -0.56 / -0.84 (n=125) | 7/14 |
| True | -0.55 / -0.55 (n=2577) | -0.43 / -0.51 (n=805) | -0.70 / +0.64 (n=191) | -0.65 / – (n=26) | 3/10 |

**Reclaimed on the same candle**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| True | -0.35 / -0.34 (n=12678) | -0.39 / -0.08 (n=4140) | -0.18 / +0.43 (n=936) | -0.60 / -0.74 (n=124) | 6/14 |
| False | -0.22 / -0.17 (n=3329) | -0.19 / -0.03 (n=950) | -0.18 / +0.34 (n=219) | -0.48 / -1.07 (n=27) | 6/12 |

**First 200-touch in this trend**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| True | -0.13 / -0.28 (n=2404) | -0.24 / -0.01 (n=722) | -0.28 / +0.39 (n=181) | -0.45 / -1.05 (n=27) | 4/11 |
| False | -0.36 / -0.31 (n=13603) | -0.37 / -0.08 (n=4368) | -0.17 / +0.42 (n=974) | -0.62 / -0.80 (n=124) | 9/14 |

**Bars the uptrend has lasted**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| 50–100 | -0.39 / -0.35 (n=4583) | -0.23 / -0.13 (n=1482) | +0.44 / +0.37 (n=262) | -0.85 / -1.02 (n=16) | 4/12 |
| 100–200 | -0.35 / -0.28 (n=6042) | -0.54 / -0.04 (n=1802) | -0.08 / +0.11 (n=401) | -0.60 / -1.07 (n=74) | 6/13 |
| 200–400 | -0.26 / -0.34 (n=4076) | -0.09 / -0.14 (n=1192) | -0.69 / +0.98 (n=330) | -1.03 / -0.36 (n=22) | 6/12 |
| 400+ | -0.16 / -0.18 (n=1306) | -0.56 / +0.19 (n=614) | -0.19 / +0.68 (n=162) | -0.36 / – (n=39) | 6/9 |

**Wick depth below the 200 (ATR)**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| <0.25 | -0.39 / -0.39 (n=8203) | -0.43 / -0.08 (n=2577) | -0.22 / +0.40 (n=567) | -0.92 / -0.70 (n=92) | 6/14 |
| 0.25–0.5 | -0.29 / -0.31 (n=3658) | -0.34 / -0.16 (n=1231) | -0.18 / +0.38 (n=269) | -0.36 / -1.07 (n=23) | 4/11 |
| 0.5–1 | -0.25 / -0.16 (n=2687) | -0.23 / +0.05 (n=814) | -0.22 / +0.52 (n=213) | +0.16 / -1.06 (n=20) | 8/13 |
| >1 | -0.15 / -0.10 (n=1459) | -0.13 / +0.06 (n=468) | +0.05 / +0.32 (n=106) | +0.11 / -1.06 (n=16) | 7/11 |

**SMA200 slope over 20 bars (ATR)**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| falling | -0.27 / -0.42 (n=1027) | -0.51 / +0.94 (n=303) | +0.39 / +0.16 (n=59) | – / – (n=0) | 6/8 |
| flat 0–0.5 | -0.45 / -0.36 (n=6538) | -0.35 / -0.27 (n=2121) | -0.22 / -0.05 (n=372) | -0.65 / -1.02 (n=22) | 4/12 |
| rising 0.5–1.5 | -0.23 / -0.26 (n=7900) | -0.32 / +0.01 (n=2534) | -0.16 / +0.58 (n=698) | -0.56 / -0.83 (n=127) | 6/14 |
| steep >1.5 | -0.12 / -0.26 (n=542) | -0.58 / -1.08 (n=132) | -0.98 / +2.79 (n=26) | -1.04 / – (n=2) | 2/7 |

**SMA100–SMA200 gap (ATR)**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| <1 | -0.32 / -0.41 (n=5078) | -0.52 / +0.06 (n=1416) | -0.52 / +0.66 (n=244) | -0.84 / -1.02 (n=16) | 7/12 |
| 1–3 | -0.35 / -0.19 (n=8820) | -0.28 / -0.17 (n=2966) | -0.28 / +0.44 (n=735) | -0.67 / -0.79 (n=101) | 7/14 |
| 3–6 | -0.17 / -0.51 (n=2093) | -0.36 / -0.06 (n=708) | +0.60 / -0.03 (n=166) | -0.21 / -1.04 (n=34) | 4/11 |
| >6 | -1.26 / -1.09 (n=16) | – / – (n=0) | +1.95 / – (n=10) | – / – (n=0) | 0/1 |

**Bars since the previous touch**

| Bucket | 15m IS / OOS | 1h IS / OOS | 4h IS / OOS | 1d IS / OOS | OOS cells above average |
|---|---|---|---|---|---|
| <20 bars | -0.37 / -0.31 (n=11281) | -0.38 / -0.10 (n=3598) | -0.18 / +0.64 (n=796) | -0.58 / -1.08 (n=101) | 8/14 |
| 20–100 | -0.29 / -0.41 (n=1495) | -0.19 / -0.18 (n=487) | -0.18 / -0.53 (n=112) | -0.82 / – (n=11) | 3/11 |
| >100 (fresh) | -0.17 / -0.27 (n=3223) | -0.30 / +0.10 (n=997) | -0.16 / +0.31 (n=239) | -0.65 / -0.11 (n=31) | 8/13 |


## 6. How far does it run before the stop is hit? (longs, N = 50, same-bar reclaim, stop under the wick)

Run-up in ATR from entry until the stop is hit (or 500 bars). Baseline = random bars in the same uptrend regime with the
same stop distance. (`ma_runup.txt`)

| TF | Events | 25% of trades | Median | 75% | Best 10% | Baseline median / best 10% |
|---|---|---|---|---|---|---|
| 15m | 6,339 | 0.0 | 0.60 | 2.1 | 7.4+ | 0.63 / 6.9+ |
| 1h | 2,070 | 0.0 | 0.58 | 1.8 | 8.7+ | 0.62 / 7.5+ |
| 4h | 468 | 0.0 | 0.60 | 2.6 | 9.3+ | 0.65 / 9.8+ |
| 1d | 62 | 0.0 | 0.26 | 1.1 | 3.9+ | 0.42 / 16+ |

## Conclusions

* **As specified, Idea 1 has no consistent edge.** After the wick-and-reclaim, price moves about the same as on any
  bar in the same uptrend: median best move ~1.6–1.8 ATR over 20 bars vs a worst move of ~1.7–2.0 ATR, and ~4 ATR
  each way over 100 bars. Hit rates for +1 to +5 ATR before the stop are equal to or slightly below the baseline.
* **Typical run-up before the stop: ~0.6 ATR (median).** A quarter of trades never go positive; the best 10% run
  7–9 ATR. The same distribution as random entries in the uptrend, so the touch of the 200 itself adds nothing.
* **After costs it loses** on 15m and 1h (stops under the wick are only ~0.7 ATR, so fees are large in R). 4h was
  positive out-of-sample (+0.43 R at a +3 ATR target, 141 trades) but negative in-sample (−0.18 R) — a regime effect,
  not a stable edge. Daily has too few events (62) and was negative.
* **Relationships that held in both periods:** deeper wicks (>0.5 ATR below the 200) do better than shallow touches
  (<0.25 ATR) on 15m, 1h and 4h — partly mechanical (wider stop); SMA50 below SMA100 at the touch ("white crossed")
  is slightly better in 10 of 14 coin/timeframe cells. Neither turns the setup profitable on its own.
* Everything else (trend age, SMA200 slope, first touch, same-bar vs delayed reclaim, 100–200 gap) was inconsistent.
* The short mirror (downtrend, wick above the 200) behaves the same way: no consistent edge.
