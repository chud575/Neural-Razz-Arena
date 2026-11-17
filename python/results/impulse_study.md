# After an impulse leg, and fair value gaps — study summary (BTC, ETH, AVAX, XRP)

Rules in python/impulse_study.py (impulse legs = pine/impulse_legs.pine defaults). 'Expected' = the rate the distances alone give if the leg meant nothing.

## Legs found

| TF | Legs | Median size | Median length | Legs with a fair value gap | Gaps per leg | New extreme before a full retrace |
|---|---|---|---|---|---|---|
| 15m | 13633 | 3.4% | 10 bars | 99% | 3.3 | 63% |
| 1h | 4769 | 7.1% | 10 bars | 98% | 3.3 | 65% |
| 4h | 1188 | 15.9% | 11 bars | 98% | 3.4 | 64% |

## Pullback levels: new extreme before the whole leg is retraced?

| TF | Pullback to | Times reached | New extreme first | Expected | Difference |
|---|---|---|---|---|---|
| 15m | 38% | 11747 | 57% | 61% | -3.8 |
| 15m | 50% | 9804 | 49% | 50% | -1.0 |
| 15m | 62% | 8064 | 38% | 38% | -0.4 |
| 15m | 79% | 6301 | 20% | 21% | -1.0 |
| 1h | 38% | 3989 | 58% | 61% | -2.6 |
| 1h | 50% | 3242 | 49% | 50% | -0.9 |
| 1h | 62% | 2681 | 38% | 39% | -0.8 |
| 1h | 79% | 2129 | 23% | 23% | +0.3 |
| 4h | 38% | 993 | 57% | 61% | -3.8 |
| 4h | 50% | 823 | 48% | 50% | -1.3 |
| 4h | 62% | 677 | 37% | 38% | -0.8 |
| 4h | 79% | 538 | 22% | 21% | +0.2 |

## Fair value gaps inside the leg

| TF | Gaps | Revisited before a new extreme | Of those: filled completely | A: new extreme before the leg start | Expected | B: new extreme before the far side of the gap | Expected |
|---|---|---|---|---|---|---|---|
| 15m | 45117 | 66% | 88% | 49% | 54% | 12% | 18% |
| 1h | 15472 | 64% | 87% | 51% | 54% | 13% | 19% |
| 4h | 4037 | 62% | 88% | 48% | 53% | 12% | 18% |

As trades (limit at the near side of the gap, target = the leg's extreme), average R before fees: stop at the leg start 15m -0.06, 1h -0.06, 4h -0.08; stop beyond the gap 15m -0.29, 1h -0.22, 4h -0.24.

By where the gap sits in the leg (1h, share of the leg retraced to reach it): 0–25%: A 72% vs 81% expected, B 11% vs 29%; 25–50%: A 60% vs 63% expected, B 19% vs 23%; 50–75%: A 39% vs 38% expected, B 11% vs 13%; 75–101%: A 18% vs 17% expected, B 5% vs 5%.
