# Counter-trade at the broken bound of a range box — test summary

Rules in python/range_box_counter.py. After a break down: resting buy at the box bottom for when price comes back up through
it, 5 units, stop one box height below the bottom, sell 1 unit at the box top and at 1 ×, 2 ×, 3 ×, 4 × the box height above
the top. Mirror image after a break up. Order cancelled if price first travels 5 × the box in the break direction.
Net of Bybit VIP 3 futures fees and funding. R = loss of all 5 units at the stop. Four coins pooled, IS / OOS.

| TF | Breaks | Filled | Avg R IS | Avg R OOS | Before fees (R) | Profitable trades | Stopped before the first target | All 5 targets | Median wait (bars) |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 1925 | 96% | +0.02 | +0.07 | +0.09 | 28% | 49% | 19% | 1 |
| 1h | 590 | 95% | +0.24 | +0.02 | +0.20 | 33% | 45% | 21% | 1 |
| 4h | 133 | 90% | -0.03 | -0.39 | -0.14 | 27% | 56% | 12% | 1 |
| 1D | 19 | 95% | +0.21 | -0.14 | -0.07 | 44% | 56% | 6% | 3 |

1h by coin (IS / OOS, trades): BTC +0.37 / +0.14 (181), ETH +0.25 / +0.12 (195), AVAX +0.15 / -0.18 (90), XRP +0.05 / -0.23 (93).
Median travel in the break direction before the fill: about 0.3 box heights.

Literally 5 BTC per trade (BTC only, after fees): 15m 520 trades +$76,043; 1h 181 trades +$61,070 (largest drawdown $122,485,
2021 alone -$91,907); 4h 33 trades +$67,102 (best single trade +$88,232).
