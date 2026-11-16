# Squeeze-fire strategy — test summary (BTC, ETH, AVAX, XRP)

Rules in python/squeeze_test.py (same squeeze as pine/squeeze_box.pine, default settings). Enter at the close of the bar
the squeeze ends, in the direction of momentum; stop one box-range from the entry; target k × the range. Net of Bybit
VIP 3 futures fees and funding, average R per trade, IS (first 70%) / OOS (last 30%).

| TF | Box level | Target 1 × | Target 2 × | Target 3 × | Trades (2 ×) | Win % (2 ×) | Median stop |
|---|---|---|---|---|---|---|---|
| 15m | early or tighter | -0.03 / -0.02 | -0.01 / -0.01 | +0.02 / -0.02 | 6979 | 30 | 2.0% |
| 15m | squeeze or tighter | -0.08 / -0.09 | -0.06 / -0.08 | -0.06 / -0.05 | 9514 | 32 | 1.3% |
| 15m | power squeeze | -0.21 / -0.14 | -0.24 / -0.19 | -0.24 / -0.17 | 3222 | 31 | 0.7% |
| 1h | early or tighter | -0.04 / +0.02 | +0.04 / +0.07 | +0.11 / +0.06 | 2336 | 32 | 4.4% |
| 1h | squeeze or tighter | -0.08 / -0.06 | -0.08 / -0.01 | -0.07 / +0.02 | 3130 | 32 | 2.9% |
| 1h | power squeeze | -0.03 / -0.07 | -0.04 / -0.05 | +0.01 / -0.02 | 1430 | 33 | 1.6% |
| 4h | early or tighter | -0.12 / -0.12 | +0.07 / +0.02 | +0.01 / +0.05 | 616 | 32 | 9.5% |
| 4h | squeeze or tighter | -0.03 / -0.03 | +0.05 / -0.01 | +0.15 / -0.11 | 854 | 34 | 6.0% |
| 4h | power squeeze | -0.12 / +0.01 | +0.02 / -0.08 | +0.05 / -0.06 | 381 | 33 | 3.3% |
| 1D | early or tighter | +0.18 / +0.02 | +0.33 / +0.42 | +0.34 / +0.37 | 105 | 38 | 22.6% |
| 1D | squeeze or tighter | +0.01 / -0.11 | +0.23 / -0.05 | +0.22 / +0.16 | 135 | 35 | 14.7% |
| 1D | power squeeze | +0.14 / +0.05 | +0.41 / +0.18 | +0.43 / +0.07 | 52 | 44 | 8.5% |

Break-even win rate at 2 × is 33%. Stop at the far edge of the box instead: 1h early-or-tighter 2 × = +0.11 / +0.05; other rows similar to the table.
1h, early or tighter, 2 ×, by coin (IS / OOS): BTC -0.07 / +0.02, ETH +0.08 / +0.11, AVAX +0.08 / +0.02, XRP +0.14 / +0.14.
