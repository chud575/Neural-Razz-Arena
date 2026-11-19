# Impulse legs and the golden pocket (61.8–65% retracement) — study summary (BTC, ETH, AVAX, XRP)

Rules in python/golden_pocket_study.py. Legs = pine/impulse_legs.pine defaults. 'Expected' = the win rate the distances alone give. R after Bybit VIP 3 fees, IS / OOS.

## Does price come back to the pocket, and what then?

| TF | Legs | Reached 61.8% before a new extreme | Of those: turned inside the pocket (≤ 65%) | went to 65–78.6% | 78.6–100% | retraced the whole leg | New extreme before the whole leg was retraced | Expected |
|---|---|---|---|---|---|---|---|---|
| 15m | 13633 | 59% | 5% | 17% | 16% | 62% | 38% | 38% |
| 1h | 4769 | 56% | 4% | 17% | 19% | 61% | 38% | 38% |
| 4h | 1188 | 57% | 5% | 16% | 18% | 62% | 37% | 38% |

## Entering at 61.8%

| TF | Trades | A: stop at the leg start, target the extreme | B: stop at 78.6%, target the extreme | C: stop at 78.6%, target 38.2% |
|---|---|---|---|---|
| 15m | 8079 | 38% vs 38% · -0.05R / -0.02R | 22% vs 21% · -0.08R / -0.05R | 42% vs 41% · -0.05R / -0.09R |
| 1h | 2690 | 38% vs 38% · +0.02R / -0.05R | 20% vs 21% · -0.04R / -0.20R | 41% vs 41% · +0.01R / -0.20R |
| 4h | 678 | 37% vs 38% · +0.06R / -0.21R | 20% vs 21% · +0.06R / -0.36R | 44% vs 41% · +0.14R / -0.17R |

## Higher-timeframe overlap (trade A: stop at the leg start, target the extreme)

| TF | Condition when the pocket is touched | Trades | Win vs expected | R IS / OOS |
|---|---|---|---|---|
| 15m | with the live leg one timeframe up | 2082 | 39% vs 38% | -0.03 / +0.07 |
| 15m | against it | 2012 | 39% vs 38% | +0.00 / -0.07 |
| 15m | with the live leg two timeframes up | 1923 | 38% vs 38% | -0.06 / -0.00 |
| 15m | against it (two up) | 2048 | 37% vs 38% | -0.08 / -0.00 |
| 15m | with live legs on both higher timeframes | 896 | 37% vs 38% | -0.08 / +0.05 |
| 15m | overlaps the golden pocket one timeframe up | 458 | 41% vs 38% | +0.05 / +0.19 |
| 15m | inside the 50–78.6% zone one timeframe up | 1100 | 39% vs 38% | -0.01 / +0.07 |
| 15m | overlaps the golden pocket two timeframes up | 87 | 32% vs 38% | -0.23 / +0.04 |
| 15m | inside the 50–78.6% zone two timeframes up | 557 | 39% vs 38% | +0.03 / -0.07 |
| 15m | higher-timeframe swing level in the pocket (one up) | 2853 | 38% vs 38% | -0.07 / -0.02 |
| 15m | higher-timeframe swing level in the pocket (two up) | 1418 | 36% vs 38% | -0.09 / -0.07 |
| 15m | fair value gap in the pocket | 5767 | 38% vs 38% | -0.05 / -0.04 |
| 15m | no condition (all touches) | 8079 | 38% vs 38% | -0.05 / -0.02 |
| 1h | with the live leg one timeframe up | 667 | 39% vs 38% | +0.07 / +0.00 |
| 1h | against it | 593 | 38% vs 38% | -0.04 / -0.01 |
| 1h | with the live leg two timeframes up | 542 | 39% vs 38% | -0.05 / +0.01 |
| 1h | against it (two up) | 554 | 36% vs 38% | +0.02 / -0.14 |
| 1h | with live legs on both higher timeframes | 244 | 43% vs 38% | +0.12 / +0.18 |
| 1h | overlaps the golden pocket one timeframe up | 137 | 38% vs 38% | +0.18 / -0.19 |
| 1h | inside the 50–78.6% zone one timeframe up | 342 | 42% vs 38% | +0.22 / -0.00 |
| 1h | overlaps the golden pocket two timeframes up | 38 | 32% vs 38% | -0.44 / +0.40 |
| 1h | inside the 50–78.6% zone two timeframes up | 193 | 37% vs 38% | -0.04 / -0.01 |
| 1h | higher-timeframe swing level in the pocket (one up) | 817 | 38% vs 38% | +0.05 / -0.10 |
| 1h | higher-timeframe swing level in the pocket (two up) | 340 | 38% vs 38% | +0.05 / -0.07 |
| 1h | fair value gap in the pocket | 1986 | 38% vs 38% | +0.01 / -0.05 |
| 1h | no condition (all touches) | 2690 | 38% vs 38% | +0.02 / -0.05 |
| 4h | with the live leg one timeframe up | 107 | 36% vs 38% | -0.01 / -0.09 |
| 4h | against it | 155 | 34% vs 38% | -0.10 / -0.13 |
| 4h | with the live leg two timeframes up | 92 | 39% vs 38% | +0.19 / -0.37 |
| 4h | against it (two up) | 131 | 31% vs 38% | -0.26 / -0.05 |
| 4h | with live legs on both higher timeframes | 25 | 44% vs 38% | +0.30 / -0.43 |
| 4h | overlaps the golden pocket one timeframe up | 18 | 28% vs 38% | -0.47 / +0.58 |
| 4h | inside the 50–78.6% zone one timeframe up | 52 | 40% vs 38% | -0.01 / +0.41 |
| 4h | overlaps the golden pocket two timeframes up | 5 | 20% vs 38% | -0.99 / -0.15 |
| 4h | inside the 50–78.6% zone two timeframes up | 38 | 34% vs 38% | +0.07 / -0.41 |
| 4h | higher-timeframe swing level in the pocket (one up) | 148 | 34% vs 38% | -0.03 / -0.33 |
| 4h | higher-timeframe swing level in the pocket (two up) | 51 | 37% vs 38% | +0.21 / -0.43 |
| 4h | fair value gap in the pocket | 474 | 36% vs 38% | +0.03 / -0.23 |
| 4h | no condition (all touches) | 678 | 37% vs 38% | +0.06 / -0.21 |

Higher timeframes: 15m chart → 1h and 4h; 1h → 4h and daily; 4h → daily and weekly. A higher-timeframe leg is 'live' once finished, until its extreme is exceeded or its start is broken.
