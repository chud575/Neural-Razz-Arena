# Range Sweep (liquidity-sweep reversal) — crypto test summary

Coins: BTC, ETH, AVAX, XRP (Coinbase; XRP only since Jul 2023 because Coinbase halted it 2021–2023).
Timeframes 15m / 1h / 4h / 1D. 2,304 settings per coin and timeframe. Costs 0.1% per side.
First 70% of each history = in-sample (IS), last 30% = out-of-sample (OOS). Details: `rangesweep_<coin>.md`,
cross-asset check (settings picked on BTC IS, tested on the other coins' full history): `rangesweep_crossasset.md`.

## Example trade (BTC 1h, 4 Nov 2026)
03:00 UTC candle wicked to 75,601 below the range low and closed back inside at 76,369 → LONG 76,369,
stop ≈ 75,490, target = range high 78,762. Detected with range length ≥ 120 bars (both edges then have
2+ touches); with 48 bars the range top only had one touch. v1.1 defaults to 120.

## Results
* **15m and 1h: no profitable setting on any coin after costs**, in-sample or out-of-sample. Before costs BTC 1h
  was positive (+0.10 to +0.16 R/trade) but stops just beyond a wick are ~1% of price, so 0.2% round-trip fees
  cost ~0.15–0.25 R per trade. ETH/AVAX/XRP 1h were mostly negative even before costs.
* **4h: worked in the past, not recently.** The default-like setting (48-bar range, 2 touches, same-bar reclaim,
  target opposite side) was strongly positive in-sample (BTC +0.69, ETH +0.35, AVAX +0.22 R/trade) and negative
  out-of-sample (BTC −0.44, ETH −0.23, AVAX −0.22). Averaged over all variants, every 4h entry family is negative
  on BTC, ETH and XRP, ≈ 0 on AVAX.
* **Cross-asset:** of the top-10 BTC in-sample picks, 9 lost money on at least two of the three other coins.
* **Daily:** too few ranges/trades to judge.

Conclusion: as defined here, fading range sweeps has **no durable edge after costs** on these coins; the
most recent period was the worst. The indicator is still useful for spotting the setup; trade it with
discretion, lower fees (maker orders) and confirmation rather than mechanically.
