# "Take the first 1%" — enter the first 1% move from the daily open, aim for 4% more (python/first_move_trade.py)

15m candles, BTC and ETH, 2020-01-02 → 2026-11-11: 5002 days. P&L in % of price per trade, after Bybit VIP 3 fees. Alert day = previous day's range and last 12 hours' range both in their widest third.


## Every day

| Exit | Days | Trades | Hit +4% target | Stopped | Out at the close | Average P&L per trade | Total P&L | 2020–2022 avg | 2023–2026 avg | BTC avg | ETH avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A no stop | 5002 | 4717 | 20% | 0% | 80% | -0.03% | -164% | -0.05% | -0.02% | -0.00% | -0.06% |
| B stop at the open | 5002 | 4717 | 11% | 66% | 23% | -0.12% | -582% | -0.20% | -0.06% | -0.10% | -0.15% |
| C stop at the opposite 1% | 5002 | 4717 | 17% | 40% | 43% | -0.03% | -150% | -0.07% | -0.00% | -0.03% | -0.03% |

## Alert days only

| Exit | Days | Trades | Hit +4% target | Stopped | Out at the close | Average P&L per trade | Total P&L | 2020–2022 avg | 2023–2026 avg | BTC avg | ETH avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A no stop | 1345 | 1305 | 28% | 0% | 72% | -0.12% | -160% | -0.11% | -0.14% | -0.03% | -0.22% |
| B stop at the open | 1345 | 1305 | 10% | 82% | 9% | -0.41% | -536% | -0.51% | -0.25% | -0.34% | -0.48% |
| C stop at the opposite 1% | 1345 | 1305 | 20% | 57% | 23% | -0.28% | -359% | -0.28% | -0.26% | -0.26% | -0.29% |

## Non-alert days

| Exit | Days | Trades | Hit +4% target | Stopped | Out at the close | Average P&L per trade | Total P&L | 2020–2022 avg | 2023–2026 avg | BTC avg | ETH avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A no stop | 3657 | 3412 | 17% | 0% | 83% | -0.00% | -3% | -0.02% | +0.01% | +0.01% | -0.01% |
| B stop at the open | 3657 | 3412 | 11% | 60% | 28% | -0.01% | -47% | -0.00% | -0.02% | +0.00% | -0.03% |
| C stop at the opposite 1% | 3657 | 3412 | 15% | 34% | 51% | +0.06% | +209% | +0.07% | +0.05% | +0.06% | +0.06% |

## Previous day's range in its widest fifth

| Exit | Days | Trades | Hit +4% target | Stopped | Out at the close | Average P&L per trade | Total P&L | 2020–2022 avg | 2023–2026 avg | BTC avg | ETH avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A no stop | 1003 | 974 | 31% | 0% | 69% | -0.06% | -55% | -0.10% | +0.04% | +0.07% | -0.18% |
| B stop at the open | 1003 | 974 | 10% | 84% | 6% | -0.44% | -431% | -0.54% | -0.24% | -0.35% | -0.54% |
| C stop at the opposite 1% | 1003 | 974 | 21% | 59% | 20% | -0.28% | -277% | -0.34% | -0.17% | -0.25% | -0.32% |

## Last 4 hours' range in its widest fifth

| Exit | Days | Trades | Hit +4% target | Stopped | Out at the close | Average P&L per trade | Total P&L | 2020–2022 avg | 2023–2026 avg | BTC avg | ETH avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A no stop | 1004 | 973 | 31% | 0% | 69% | -0.06% | -59% | -0.05% | -0.07% | -0.04% | -0.08% |
| B stop at the open | 1004 | 973 | 10% | 83% | 8% | -0.43% | -422% | -0.52% | -0.25% | -0.39% | -0.48% |
| C stop at the opposite 1% | 1004 | 973 | 21% | 58% | 21% | -0.27% | -265% | -0.29% | -0.24% | -0.33% | -0.21% |

## Alert days in detail

Alert days: 1345; a 1% move triggered on 1305 (97%). The day ended as a ±5% day on 20% of alert days (13% of all days). The first 1% move pointed the way the day finished on 61% of triggered alert days (68% on all days).

No-stop version on alert days, by how the day ended:

| Day ended | Trades | Average P&L |
|---|---|---|
| as a ±5% day, the trade's way | 178 | +3.95% |
| as a ±5% day, against the trade | 79 | -8.05% |
| under 5% | 1048 | -0.22% |

Stop-at-the-open version on alert days, in R (1R = the 1% risked): average -0.41R per trade, largest losing streak 24 trades.
