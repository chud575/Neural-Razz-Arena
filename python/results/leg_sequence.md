# Impulse legs in a row — study (BTC, ETH, AVAX, XRP)

Rules in python/leg_sequence_study.py. 'Same way' = the next impulse leg goes in the same direction as the one before it. 'Expected' = the rate if legs were independent.

## How often the next leg goes the same way

| TF | Pairs of legs | Same way | Expected | After a leg up | After a leg down | First 70% | Last 30% | BTC only |
|---|---|---|---|---|---|---|---|---|
| 15m | 13629 | 48% | 50% | 47% | 50% | 50% | 46% | 47% (3919) |
| 1h | 4765 | 49% | 50% | 49% | 49% | 51% | 45% | 48% (1697) |
| 4h | 1184 | 51% | 50% | 54% | 48% | 52% | 48% | 51% (412) |
| 1d | 181 | 46% | 51% | 53% | 36% | 44% | 50% | 40% (67) |

## Does a longer run make another one more likely?

Share of times the next leg goes the same way, given how many in a row there have already been (count in brackets).

| TF | After 1 | After 2 in a row | After 3 | After 4 | After 5 or more |
|---|---|---|---|---|---|
| 15m | 48% (7023) | 49% (3388) | 50% (1645) | 49% (820) | 47% (753) |
| 1h | 49% (2437) | 49% (1181) | 50% (583) | 46% (294) | 50% (270) |
| 4h | 53% (582) | 51% (308) | 50% (157) | 45% (78) | 41% (59) |
| 1d | 52% (102) | 41% (49) | 45% (20) | 11% (9) | 0% (1) |

## How long runs are

Share of runs by length (a run ends when a leg goes the other way).

| TF | 1 | 2 | 3 | 4 | 5 or more | Longest |
|---|---|---|---|---|---|---|
| 15m | 52% | 25% | 12% | 6% | 6% | 13 |
| 1h | 52% | 25% | 12% | 7% | 6% | 12 |
| 4h | 47% | 26% | 14% | 7% | 6% | 9 |
| 1d | 50% | 30% | 11% | 8% | 1% | 6 |

## Does it depend on how soon the next leg starts?

Bars between the previous leg's extreme and the next leg's start.

| TF | Starts within 5 bars | 6–20 bars | 21–60 bars | More than 60 bars |
|---|---|---|---|---|
| 15m | 26% (2573) | 56% (2830) | 55% (4086) | 51% (4140) |
| 1h | 32% (842) | 54% (1128) | 53% (1387) | 51% (1408) |
| 4h | 26% (200) | 61% (263) | 53% (394) | 55% (327) |
| 1d | 23% (35) | 61% (38) | 49% (51) | 47% (57) |

## Size of the previous leg (same-way rate by thirds: smallest / middle / largest)

| TF | Smallest third | Middle | Largest third |
|---|---|---|---|
| 15m | 49% | 48% | 49% |
| 1h | 47% | 48% | 52% |
| 4h | 48% | 52% | 52% |
| 1d | 43% | 43% | 52% |

## Before a second leg the same way: how far did the first leg pull back?

For every streak of two or more legs in the same direction: the deepest pullback of the FIRST leg (from its extreme) before the SECOND leg started, as a share of the first leg. Four coins.

| TF | Streaks | Pulled back 50% or more | Median pullback | under 25% | 25–38% | 38–50% | 50–62% | 62–79% | 79–100% | beyond the leg's start | BTC only: 50% or more |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15m | 3388 | 66% | 61% | 3% | 13% | 18% | 17% | 20% | 16% | 12% | 66% (980) |
| 1h | 1183 | 66% | 62% | 3% | 14% | 17% | 16% | 21% | 17% | 11% | 64% (425) |
| 4h | 309 | 67% | 60% | 3% | 14% | 17% | 19% | 19% | 19% | 9% | 64% (107) |
| 1d | 53 | 66% | 60% | 0% | 19% | 15% | 17% | 34% | 11% | 4% | 67% (18) |

Same measure for streaks of exactly two, and for legs up and legs down separately (share pulling back 50% or more):

| TF | Exactly two in a row | Three or more | Legs up | Legs down | Every same-way pair (not just the first of a streak) |
|---|---|---|---|---|---|
| 15m | 66% (1743) | 66% (1645) | 64% | 68% | 69% (6606) |
| 1h | 66% (599) | 66% (584) | 66% | 67% | 67% (2331) |
| 4h | 64% (152) | 69% (157) | 64% | 69% | 66% (603) |
| 1d | 70% (33) | 60% (20) | 64% | 70% | 75% (83) |
