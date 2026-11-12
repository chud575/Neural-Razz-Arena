# Market-structure strategies — test summary (BTC, ETH, AVAX, XRP)

Structure logic: python/market_structure.py = structure() in pine/trend_finder.pine. Net of Bybit VIP 3 futures fees and
funding, average R per trade, IS (first 70%) / OOS (last 30%).

## 1. Takeout of the last swing high in a bearish structure (python/ms_takeout.py)

Structure timeframe bearish (last break down), price trades above its latest swing high without a structure-timeframe
close above it; short. Stop = the takeout high. Mirror for longs. Swing length 3.

| Structure TF | Entry TF | Entry | 2R target IS / OOS (trades) | Target = structure swing low IS / OOS | Win % at 2R (break-even 33) |
|---|---|---|---|---|---|
| 1D | 1h | first 1h close back below the level | -0.32 (229) / -0.10 (125) | -0.29 / -0.12 | 27 |
| 1D | 1h | daily close back below the level | 0.00 (142) / +0.19 (83) | -0.23 / +0.09 | 36 |
| 4h | 1h | first 1h close back below | -0.13 (1221) / -0.10 (571) | -0.13 / -0.21 | 33 |
| 4h | 1h | 4h close back below | -0.05 (967) / -0.13 (465) | -0.04 / -0.21 | 33 |
| 1h | 15m | first 15m close back below | -0.29 (4004) / -0.34 (1758) | -0.34 / -0.28 | 32 |
| 1W | 1h | weekly close back below | +0.39 (21) / +0.24 (17) | +1.57 / -0.21 | 45 |

## 2. Continuation entries (python/ms_continuation.py), chart swing length 5

BOS = close above the latest swing high with structure already bullish; CHoCH = first break back up; pullback = a new
higher low confirmed in a bullish structure. Stop = latest chart swing low. No higher-timeframe filter unless stated.

| Chart | Entry | 2R IS / OOS | 3R IS / OOS | Trades (2R) | Median stop |
|---|---|---|---|---|---|
| 15m | BOS | -0.04 / -0.01 | -0.01 / +0.01 | 6300 | 1.8% |
| 15m | CHoCH | -0.03 / -0.01 | -0.02 / 0.00 | 6372 | 1.7% |
| 15m | pullback | -0.14 / -0.13 | -0.12 / -0.15 | 17911 | 0.7% |
| 1h | BOS | +0.15 / +0.13 | +0.18 / +0.11 | 2052 | 4.1% |
| 1h | CHoCH | -0.09 / -0.07 | -0.12 / -0.06 | 2106 | 3.8% |
| 1h | pullback | -0.03 / -0.04 | 0.00 / 0.00 | 6046 | 1.6% |
| 4h | BOS | +0.09 / +0.09 | +0.23 / +0.23 | 541 | 7.9% |
| 4h | CHoCH | +0.05 / -0.02 | -0.02 / +0.15 | 554 | 7.9% |
| 4h | pullback | -0.01 / +0.01 | +0.05 / +0.03 | 1607 | 3.4% |

### 1h BOS, 2R target, no filter

| Coin | IS (trades) | OOS (trades) |
|---|---|---|
| BTC | +0.17 (498) | +0.16 (214) |
| ETH | +0.18 (468) | +0.05 (200) |
| AVAX | +0.12 (232) | +0.12 (97) |
| XRP | +0.10 (248) | +0.24 (95) |

Longs +0.21 / +0.11, shorts +0.09 / +0.16. Win rate 41% (break-even 33%). Pooled t-stat 4.5.
Random entries with the same direction, stop distance, 2R target and fees: 0.00 (IS) / -0.02 (OOS).
Higher-timeframe filters (4h or daily structure bias or strict trend agreeing) did not improve it: 2R OOS between 0.00 and +0.07.
Other swing lengths, 2R: length 3 +0.07 / +0.05, length 8 +0.18 / +0.10, length 12 +0.16 / +0.03. Other targets at length 5:
1R +0.02 / 0.00, 1.5R +0.08 / +0.06, 3R +0.18 / +0.11.

4h BOS at 2R is not better than random entries there (+0.06 / +0.11), so the 4h rows are not evidence of an edge.
Trailing-stop exits looked better on paper (up to +0.4 IS) but depend on a few very large winners and fell to +0.02 to +0.18 OOS.
