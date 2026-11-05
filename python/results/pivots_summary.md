# Pivot Points — crypto test summary (Bybit VIP 3 futures costs)

Coins BTC, ETH, AVAX, XRP (Coinbase data; XRP since Jul 2023). Chart timeframes 15m / 1h / 4h / 1D; pivots from the
previous day / week / month (1D chart: previous day = same timeframe). 576–864 settings per coin and timeframe.
Costs: taker 0.035% entry, maker 0.014% / taker 0.035% exit, funding 0.01% per 8 h. 70/30 in-sample / out-of-sample.
Per-coin reports: `pivots_<coin>.md`; cross-coin families: `pivots_crossasset.md`; typical settings: `pivots_finalists_bybit.txt`.

## Findings
* **Bounces don't work.** Fading S/R levels (touch or rejection close) lost money on nearly every coin, pivot type and
  period; e.g. daily S1/R1 rejection bounces on BTC 1h: −0.10 R/trade out-of-sample (592 trades).
* **Breakouts do — through weekly or monthly R1/S1.** On 4h, the weekly and monthly breakout families were positive on
  BTC, ETH and AVAX with 75–100% of variants profitable (full history); XRP was mixed.
* **Typical setting** (Traditional, weekly pivots, breakout of R1/S1, stop 1 × ATR, 2R target, 4h, both sides):

| Coin | In-sample | Out-of-sample | Random entries (OOS) | Median stop | Stop beyond 25x liquidation |
|---|---|---|---|---|---|
| BTC | +0.34 R (236) | +0.21 R (106) | −0.02 | 2.4% | 27% |
| ETH | +0.32 R (237) | +0.23 R (91) | +0.06 | 3.3% | 47% |
| AVAX | +0.14 R (107) | +0.02 R (52) | −0.06 | 3.9% | 58% |
| XRP | +0.02 R (81) | +0.04 R (31) | −0.01 | 3.0% | 38% |

  Positive in both periods on all four coins — the most consistent cross-coin result of all strategies tested.
* 1h with weekly-pivot breakouts: good on BTC/ETH, negative on AVAX/XRP OOS. 15m: nothing robust after costs.
* Leverage: 4h stops are 2.4–3.9% (median), so at 25x a quarter to half of the trades would be liquidated before the
  stop. Use ~10x or less and size each trade by its stop distance.
