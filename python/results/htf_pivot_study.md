# HTF pivot study — 15m chart, 1h and 4h pivot lines (BTC, ETH, AVAX, XRP since 2020)

Rules in python/htf_pivot_study.py (same lines as pine/htf_pivot_lines.pine, pivot length 3). 'Ahead' = the line further in the direction price was travelling; 'behind' = the line back the other way. 'Expected' = what the two distances alone predict if the lines had no effect.

## Bounces

Of first touches where the touch candle did not already close through the line, price reached the nearest opposite line before a 15m close through the touched line: 1h lines 18% (n=16337), 4h lines 18% (n=4034).

## Races

| Situation | Race | Ahead first | Expected | Difference | n |
|---|---|---|---|---|---|
| First touch of a 1h line | next 1h ahead vs nearest 1h behind | 70.5% | 70.2% | +0.2 | 26455 |
| First touch of a 1h line | next 4h ahead vs nearest 1h behind | 56.7% | 55.7% | +1.0 | 30318 |
| First touch of a 1h line | next 4h ahead vs nearest 4h behind | 67.7% | 67.0% | +0.7 | 29294 |
| First touch of a 4h line | next 1h ahead vs nearest 1h behind | 72.4% | 71.9% | +0.5 | 3413 |
| First touch of a 4h line | next 4h ahead vs nearest 1h behind | 62.8% | 62.3% | +0.5 | 6671 |
| First touch of a 4h line | next 4h ahead vs nearest 4h behind | 71.7% | 71.0% | +0.7 | 6579 |
| 15m close through a 1h line | next 1h ahead vs nearest 1h behind | 71.9% | 72.2% | -0.3 | 23724 |
| 15m close through a 1h line | next 4h ahead vs nearest 1h behind | 58.5% | 58.2% | +0.3 | 28548 |
| 15m close through a 1h line | next 4h ahead vs nearest 4h behind | 68.6% | 68.5% | +0.1 | 27605 |
| 15m close through a 4h line | next 1h ahead vs nearest 1h behind | 75.2% | 75.4% | -0.2 | 3153 |
| 15m close through a 4h line | next 4h ahead vs nearest 1h behind | 64.0% | 64.3% | -0.4 | 6237 |
| 15m close through a 4h line | next 4h ahead vs nearest 4h behind | 72.4% | 72.5% | -0.0 | 6158 |
| Bounced off a 1h low, now at a 1h high | next 1h ahead vs nearest 1h behind | 71.8% | 72.2% | -0.3 | 1339 |
| Bounced off a 1h low, now at a 1h high | next 4h ahead vs nearest 1h behind | 58.3% | 56.7% | +1.6 | 1437 |
| Bounced off a 1h low, now at a 1h high | next 4h ahead vs nearest 4h behind | 68.2% | 67.2% | +1.0 | 1414 |
| Bounced off a 1h high, now at a 1h low | next 1h ahead vs nearest 1h behind | 68.5% | 71.3% | -2.8 | 1340 |
| Bounced off a 1h high, now at a 1h low | next 4h ahead vs nearest 1h behind | 52.1% | 53.8% | -1.7 | 1404 |
| Bounced off a 1h high, now at a 1h low | next 4h ahead vs nearest 4h behind | 62.9% | 65.1% | -2.2 | 1357 |
| Bounced off a 4h low, now at a 1h high | next 1h ahead vs nearest 1h behind | 73.9% | 74.4% | -0.5 | 326 |
| Bounced off a 4h low, now at a 1h high | next 4h ahead vs nearest 1h behind | 63.1% | 61.7% | +1.4 | 360 |
| Bounced off a 4h low, now at a 1h high | next 4h ahead vs nearest 4h behind | 66.8% | 64.1% | +2.8 | 365 |
| Bounced off a 4h high, now at a 1h low | next 1h ahead vs nearest 1h behind | 71.2% | 74.9% | -3.7 | 313 |
| Bounced off a 4h high, now at a 1h low | next 4h ahead vs nearest 1h behind | 54.1% | 56.0% | -1.9 | 320 |
| Bounced off a 4h high, now at a 1h low | next 4h ahead vs nearest 4h behind | 54.9% | 57.6% | -2.7 | 326 |

By coin, close through a line, next 4h ahead vs nearest 4h behind (actual / expected): AVAX 69.2% / 69.1%; BTC 68.9% / 69.4%; ETH 69.8% / 69.6%; XRP 69.3% / 68.8%.
