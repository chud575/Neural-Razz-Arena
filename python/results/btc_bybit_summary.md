# BTC — rerun with Bybit VIP 3 futures costs (and a 25x liquidation check)

Costs: entry taker 0.035%; exit maker 0.014% at a target, taker 0.035% at a stop/breakeven; funding 0.01% per 8 h
(longs pay, shorts receive). Data: Coinbase BTC-USD (Bybit's API is geo-blocked from the test machine; the perp
tracks spot closely). Same 70/30 in-sample / out-of-sample split as before. Full tables: `btc_sweep_bybit.md`,
finalists: `btc_finalists_bybit.txt`.

## What changed with the lower fees
* 15m and 1h: still nothing robust — some single settings turn slightly positive, but no family holds up OOS.
* 4h: the same three survive, a bit stronger — Triple Top/Bottom (91% of variants positive OOS),
  Megaphone breakout-at-close longs (82%), Double Top/Bottom (69%).

## Typical settings, 4h, out-of-sample, net of Bybit costs

| Strategy | Settings | Side | OOS trades | OOS avg R | Random | Median stop | Liquidated first at 25x |
|---|---|---|---|---|---|---|---|
| Double Top/Bottom | piv5, tol 0.6%, height 1%, Breakout+Retest, 2R | both | 48 | +0.35 | −0.06 | 4.6% | 71% |
| Double Top/Bottom | piv5, tol 0.6%, height 1%, Breakout+Midpoint, 2R | both | 42 | +0.31 | −0.01 | 3.9% | 53% |
| Triple Top/Bottom | piv5, tol 2%, height 1%, Breakout+Retest, 2R | longs | 26 | +0.28 | +0.06 | 5.1% | 77% |
| Megaphone | 4 swings, piv5, breakout at close, 3R | longs | 30 | +0.25 | +0.03 | 1.8% | 12% |
| Megaphone | 4 swings, piv5, breakout at close, 3R | both | 56 | +0.16 | −0.07 | 1.8% | 15% |

## Leverage
At 25x isolated (maintenance margin 0.5%) liquidation is ≈ 3.5% from entry. The pattern strategies put the stop
beyond the pattern's top/bottom, so their stops are usually wider than that:

| Strategy (4h) | Median stop | 95th percentile | Max leverage for median stop | Max leverage for 95% of trades |
|---|---|---|---|---|
| Double Top/Bottom | 4.6% | 10.3% | ~18x | ~9x |
| Triple Top/Bottom | 5.2% | 9.3% | ~16x | ~10x |
| Megaphone breakout | 1.8% | 5.8% | ~35x | ~15x |

(0.5% buffer included.) Leverage does not change these results in R — position size does. Size each trade so the
stop = your fixed risk (e.g. 1% of the account), then pick a leverage low enough that liquidation is beyond the stop.
