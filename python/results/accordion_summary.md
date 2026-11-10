# Accordion / EMA fan (8, 13, 21, 34, 55) — crypto test summary (Bybit VIP 3 futures costs)

Coins BTC, ETH, AVAX, XRP (Coinbase; XRP from Jul 2023), 15m / 1h / 4h / 1D. 432 settings per coin and timeframe:
fan strength 2 / 3 / 5 ATR, 10 or 20 stacked bars, 50 or 100-bar window, fold to 30 / 50 / 70 % of the widest gap,
stop 0.5–2 ATR beyond the EMA55, target 1.5 / 2 / 3 : 1. Entry = limit at the previous bar's EMA55 when price
crosses it from the trend side. 70/30 in-sample / out-of-sample. Files: `accordion_<coin>.md`,
`accordion_crossasset.md`, `accordion_check.txt`.

## The setup as described (fan ≥ 3 ATR, fold to 50 %, stop 1 ATR, 2:1), both sides — avg R per trade

| Coin / TF | In-sample before → after fees | Out-of-sample before → after fees | Random OOS |
|---|---|---|---|
| BTC 15m | +0.15 → −0.02 (640) | −0.03 → −0.26 (328) | −0.23 |
| BTC 1h | +0.21 → +0.12 (370) | 0.00 → −0.11 (138) | −0.10 |
| BTC 4h | −0.03 → −0.07 (96) | −0.05 → −0.11 (32) | +0.04 |
| ETH 1h | +0.05 → 0.00 (335) | +0.17 → +0.09 (132) | −0.02 |
| ETH 4h | +0.02 → 0.00 (97) | +0.11 → +0.07 (38) | −0.04 |
| AVAX 1h | +0.02 → −0.03 (170) | +0.04 → −0.02 (78) | −0.08 |
| AVAX 4h | +0.02 → 0.00 (47) | +0.17 → +0.14 (18) | +0.07 |
| XRP 1h | +0.06 → 0.00 (71) | −0.10 → −0.16 (40) | −0.06 |

## Findings
* **No consistent edge after costs.** Before fees the setup is mildly positive on 15m and 1h in-sample, but fees take
  0.05–0.17 R per trade (the 15m stop is only ~0.4% away) and out-of-sample results are around zero before fees.
* **15m loses on every coin**, in every setting family (0–8% of variants profitable on BTC/ETH/AVAX).
* **1h / 4h: break-even, sign depends on the coin** — e.g. 4h is negative on BTC in all families but positive on AVAX.
* **Very strong fans (EMA8–EMA55 gap ≥ 5 ATR) on BTC 1h** are the one bright spot: profitable in 86% of variants
  in-sample (+0.13 R) and 100% out-of-sample (+0.51 R) — but only ~8 OOS trades per variant, and the same filter is
  negative on ETH in-sample and on AVAX out-of-sample. Worth watching, not trading on this evidence.
* Daily: too few fans (≤ 30 trades in total per coin).
