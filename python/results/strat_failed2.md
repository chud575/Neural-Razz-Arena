# The Strat — failed-2 reversal (Alex's Options video) — test summary

Rules: python/strat_failed2.py = pine/strat_failed2.pine (v1.0). BTC, ETH, AVAX, XRP. Net of Bybit VIP 3 futures fees and funding, R per trade, IS (first 70%) / OOS (last 30%), trades in brackets. Signal = bar takes out the previous bar's low and closes back inside (mirror for shorts); entry at that close, stop at the bar's low.

## Previous-bar signal, no higher-timeframe filter

| TF | Other side | 2R | T1 then trail | Trail only | Median stop |
|---|---|---|---|---|---|
| 15m | -0.43 (114385) / -0.54 (48757) | -0.44 (80233) / -0.54 (34873) | -0.42 (94396) / -0.53 (40153) | -0.42 (106478) / -0.52 (44609) | 0.23% |
| 1h | -0.22 (37771) / -0.28 (16794) | -0.24 (27077) / -0.27 (12309) | -0.18 (31436) / -0.24 (13849) | -0.15 (36702) / -0.23 (16197) | 0.48% |
| 4h | -0.15 (9606) / -0.22 (4209) | -0.12 (6974) / -0.19 (3120) | -0.07 (7945) / -0.13 (3494) | -0.05 (9331) / -0.06 (4009) | 1.00% |
| 1d | -0.11 (1535) / +0.05 (703) | -0.03 (1158) / -0.00 (492) | +0.05 (1273) / +0.39 (565) | +0.20 (1523) / +0.59 (659) | 2.62% |

## Daily chart, trail-only exit

| Signal | HTF filter | IS | OOS |
|---|---|---|---|
| prev | none | +0.20 (1523) | +0.59 (659) |
| prev | 1W | +0.19 (420) | +0.74 (220) |
| prev green | none | +0.12 (993) | +0.33 (410) |
| prev green | 1W | +0.12 (273) | +0.50 (133) |
| mother | none | +0.10 (248) | +0.31 (132) |
| mother | 1W | +0.01 (106) | +0.57 (59) |
| Baseline (random bar) | none | +0.25 (9251) | +0.15 (3994) |
| Baseline (random bar) | 1W | +0.04 (1504) | +0.45 (773) |

Baseline = the same entry, stop and trailing exit on random daily bars. It is also positive, so part of the daily result comes from the trailing exit itself, not from the signal.

## Daily, previous-bar signal, trail only — by coin and side

| Coin | Longs IS | Longs OOS | Shorts IS | Shorts OOS |
|---|---|---|---|---|
| AVAX | -0.01 (143) | -0.03 (55) | +0.34 (108) | +1.04 (49) |
| BTC | +0.26 (295) | +0.83 (127) | +0.12 (226) | +0.26 (103) |
| ETH | +0.29 (279) | +0.73 (108) | +0.15 (226) | +0.96 (109) |
| XRP | +0.44 (144) | -0.07 (65) | -0.14 (102) | +0.70 (43) |

Win rate 30%, average hold 2.6 bars, median stop 2.54%, stop beyond 25x liquidation distance (3.5%) on 34% of trades.

## How fragile the daily result is

Daily, previous-bar signal, trail only: the median trade is -0.47R (IS) / -0.44R (OOS). The top 1% of trades make up 105% of the
in-sample profit and 67% of the out-of-sample profit (largest single trades 58R and 74R, from signal bars that closed
very near their low so the stop was tiny). With every trade capped at 5R the average is -0.01 (IS) / +0.13 (OOS);
capped at 10R it is +0.09 / +0.26. Only trades with a stop of at least 1.5%: +0.14 / +0.18.
