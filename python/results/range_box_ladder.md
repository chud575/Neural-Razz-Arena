# Range-box breakout with a 5-step ladder — test summary

Rules in python/range_box_ladder.py (range finder = pine/range_broadening.pine defaults). Enter 5 units at the break close;
sell 1 unit at each of 1 ×, 2 ×, 3 ×, 4 ×, 5 × the box height beyond the broken bound; dump the rest if price returns to the
opposite side of the box. Net of Bybit VIP 3 futures fees and funding. R = the loss if all 5 units are stopped at once.
BTC, ETH, AVAX, XRP pooled; IS = first 70% of history, OOS = last 30%.

| TF | Trades | Avg R IS | Avg R OOS | Before fees (R) | Profitable trades | Stopped before 1 × | All 5 steps | Avg steps | Median box height |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 1925 | -0.04 | -0.08 | -0.01 | 29% | 42% | 19% | 1.7 | 1.5% |
| 1h | 590 | -0.04 | -0.20 | -0.07 | 28% | 42% | 19% | 1.6 | 3.5% |
| 4h | 133 | +0.16 | +0.54 | +0.29 | 41% | 35% | 28% | 2.1 | 7.5% |
| 1D | 19 | +0.05 | +0.12 | +0.05 | 47% | 26% | 11% | 1.9 | 20.3% |

4h by coin (IS / OOS, trades): BTC +0.40 / +0.22 (36), ETH +0.16 / +0.56 (46), AVAX -0.18 / +0.98 (26), XRP +0.12 / +0.41 (25).

Literally 5 BTC per trade (BTC only, full history, after fees):
1h: 192 trades since 2016, net -$142,153 (fees $21,886), worst trade -$16,945, best +$44,689, largest drawdown $180,475.
4h: 36 trades since 2016, net +$15,720 (fees $5,361), worst trade -$54,397, best +$49,701.
15m: 535 trades since 2020, net -$427,673 (fees $93,583).

Variants (avg R IS / OOS): moving the stop to the entry after the first step — 1h -0.01 / -0.08, 4h +0.15 / +0.51;
only three steps with everything out at 3 × — 1h -0.03 / -0.26, 4h +0.15 / +0.50.
