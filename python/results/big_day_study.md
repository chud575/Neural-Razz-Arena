# The 5-minute chart on ±5% days — BTC and ETH (python/big_day_study.py)

Days: open-to-close move of 5% or more on the UTC daily candle, 2015/2016 to Nov 2026 — BTC 258 up / 228 down, ETH 414 up / 322 down.
Comparison: 896 quiet days (|move| < 2%). Coinbase 5m candles. "With" = the direction the day finished; quiet days use their own small direction.

## Time on the wrong side of the open

| | Big up days | Big down days | Quiet days |
|---|---|---|---|
| Share of the day on the wrong side of the open (average / median) | 13% / 5% | 14% / 5% | 31% / 25% |
| Hours on the wrong side (average / median) | 3.1 / 1.25 | 3.3 / 1.25 | 7.3 / 6.0 |
| Never on the wrong side | 17% | 17% | 3% |
| Furthest against the open (average / median) | 1.5% / 0.8% | 1.2% / 0.7% | 1.3% / 0.9% |
| Last time on the wrong side, UTC hour (median) | 3.2 | 2.7 | 16.3 |

Big days by share of the day on the wrong side: none 17%, up to 10% 45%, 10–25% 17%, 25–50% 15%, 50–75% 5%, over 75% 1%.

## Timing

| | Big up | Big down | Quiet |
|---|---|---|---|
| The extreme the move starts from is set in the first 2 hours | 65% of big days | (same) | 31% |
| …median hour (UTC) | 1.0 | 0.8 | 5.7 |
| The far extreme, median hour | 21.6 | 20.6 | 15.9 |
| Close, as a share of the day's range | 86% | 77% | 61% |
| Biggest single hour | 3.6% | 3.8% | 1.2% |
| …as a share of the day's move (median) | 39% | 43% | – |
| Share of the move done by 04:00 / 08:00 / 12:00 / 16:00 / 20:00 UTC | 16 / 28 / 41 / 63 / 82% | 18 / 29 / 44 / 65 / 87% | – |
| Price on the day's side of the open after 1h / 2h / 4h / 8h / 12h | 61 / 67 / 74 / 83 / 90% | 59 / 66 / 75 / 81 / 87% | 54 / 56 / 60 / 62 / 67% |

Hour of the biggest move (UTC): spread over the day, most often 14:00–16:00 (about 7% of days each); least often 04:00–07:00 (about 2% each).

## Early tells

| | Big up | Big down | Quiet |
|---|---|---|---|
| Range of the first hour | 1.9% | 1.9% | 0.9% |
| Range of the first 4 hours | 3.8% | 3.8% | 1.7% |
| Range of the 12 hours before the day | 6.4% | 6.0% | 3.5% |
| First-hour volume vs the previous 12 hours | 1.18× | 1.23× | 0.91× |

## Liquidity sweeps (level traded through, then a close back inside within 30 minutes)

"Against" = the side the day did not finish on (lows on an up day).

| | Big up | Big down | Quiet |
|---|---|---|---|
| Previous day's against-side level traded through | 13% | 15% | 27% |
| …and swept (reclaimed) | 11% | 11% | 20% |
| Prior-12-hour against-side level traded through / swept | 18% / 14% | 20% / 14% | 36% / 28% |
| First-8-hours (Asia) against-side level traded through after 08:00 / swept | 13% / 11% | 13% / 10% | 43% / 34% |
| When a sweep happened, it was the day's starting extreme | 52–55% | 45–48% | 39–43% |
| Previous day's with-side level taken | 89% | 93% | 51% |

## Patterns

| | Big up | Big down | Quiet |
|---|---|---|---|
| Impulse legs per day (with / against the day) | 4.4 / 2.2 | 4.7 / 2.2 | 3.2 / 2.7 |
| First impulse leg goes with the day | 70% | 72% | 55% |
| First impulse leg appears (hours into the day) | 3.7 | 3.4 | 4.7 |
| First structure break goes with the day | 62% | 60% | 54% |
| Breaks of structure with / against | 5.6 / 1.5 | 5.2 / 1.8 | 3.7 / 2.6 |
| Fair value gaps with / against | 49 / 30 | 44 / 34 | 38 / 35 |
| Share of the day in a squeeze (BB inside KC) | 19% | 18% | 22% |
| A squeeze in the hour before the biggest hour | 42% | 43% | 48% |
| Days with at least one harmonic pattern (Gartley, Bat, Butterfly, Crab) | 31% | 31% | 27% |

Harmonics on big days: 472 patterns; 46% pointed the way the day finished. Reaching 38.2% of the AD leg before 25% of XA beyond D:
patterns with the day 81% (expected from the distances 74%), patterns against the day 65% (expected 73%); all together 72% vs 73%.
By type, share pointing with the day: Gartley 52%, Butterfly 43%, Bat 41%, Crab 36%.

## Internal and external structure

Internal = swings of 3 candles each side, external = 12 each side. "With" = structure bias in the day's direction.

| | Big up | Big down | Quiet |
|---|---|---|---|
| Share of the day with internal structure with the day | 65% | 63% | 54% |
| …external structure with the day | 75% | 73% | 57% |
| …both with the day | 55% | 52% | 38% |
| …both against the day | 15% | 16% | 27% |
| Both with the day, measured from the starting extreme | 58% | 56% | 41% |
| Pullbacks per day that broke internal structure only | 3.3 | 3.3 | 3.1 |
| Pullbacks per day that went on to break external structure | 1.5 | 1.6 | 2.3 |
| Share of pullbacks that broke external structure (whole day / from the starting extreme) | 31% / 26% | 33% / 28% | 42% / 32% |
| Days with no external break against (whole day / from the starting extreme) | 14% / 32% | 11% / 28% | 2% / 33% |
