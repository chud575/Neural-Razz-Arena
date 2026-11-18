# Premium / discount zones and the Trend Finder v1.6 strategy (1h BOS)

Rules in python/bos_premium_discount.py. Strategy = script defaults (tight-stop filter, second entry at 50%). Average R per signal (R = the first entry's risk), IS / OOS (trades), four coins, after fees. Position of the ENTRY PRICE in the dealing range: below 50% = discount, above = premium. 'With the rule' = long in discount or short in premium.

All trades: +0.26 / +0.27 (1696). First entry only: +0.17 / +0.16 (1696).

| Dealing range | With the rule | Against the rule | Longs in discount | Longs in premium | Shorts in premium | Shorts in discount |
|---|---|---|---|---|---|---|
| last 50 candles | -0.62 / +1.35 (26) | +0.27 / +0.25 (1670) | -0.52 / +1.90 (10) | +0.32 / +0.33 (867) | -0.73 / +1.27 (16) | +0.23 / +0.17 (803) |
| last 100 candles | -0.28 / +0.73 (104) | +0.30 / +0.23 (1592) | -0.91 / +0.80 (44) | +0.37 / +0.31 (833) | +0.20 / +0.68 (60) | +0.21 / +0.16 (759) |
| last 200 candles | +0.04 / +0.47 (284) | +0.31 / +0.23 (1412) | -0.52 / +0.64 (130) | +0.45 / +0.29 (747) | +0.52 / +0.34 (154) | +0.13 / +0.17 (665) |
| last 500 candles | +0.11 / +0.54 (447) | +0.32 / +0.18 (1249) | -0.14 / +0.65 (232) | +0.46 / +0.22 (645) | +0.37 / +0.41 (215) | +0.15 / +0.14 (604) |
| 4h swing range | -0.33 / +0.91 (68) | +0.28 / +0.24 (1625) | -0.71 / +0.78 (25) | +0.34 / +0.33 (851) | -0.04 / +0.94 (43) | +0.22 / +0.16 (774) |
| daily swing range | +0.02 / +0.46 (429) | +0.35 / +0.21 (1263) | -0.09 / +0.55 (211) | +0.43 / +0.27 (665) | +0.11 / +0.36 (218) | +0.26 / +0.16 (598) |
| previous day | -1.18 / -0.02 (16) | +0.27 / +0.27 (1680) | -1.49 / +nan (5) | +0.32 / +0.34 (872) | -0.93 / -0.02 (11) | +0.22 / +0.20 (808) |
| previous week | -0.10 / +0.34 (368) | +0.36 / +0.25 (1328) | -0.35 / +0.36 (182) | +0.48 / +0.33 (695) | +0.16 / +0.33 (186) | +0.23 / +0.17 (633) |

## Finer bands (position turned so 0% is the 'cheap' end for the trade: range low for longs, range high for shorts)

| Dealing range | beyond the cheap end (<0%) | 0–25% | 25–50% | 50–75% | 75–100% | beyond the expensive end (>100%) |
|---|---|---|---|---|---|---|
| last 50 candles | – | – | -0.62 / +1.35 (26) | +0.28 / +0.32 (142) | +0.27 / +0.24 (1528) | – |
| last 100 candles | – | +1.66 / +0.17 (5) | -0.33 / +0.77 (100) | +0.15 / +0.25 (319) | +0.33 / +0.23 (1272) | – |
| last 200 candles | – | -0.34 / +1.60 (14) | +0.06 / +0.43 (270) | +0.17 / +0.07 (382) | +0.35 / +0.30 (1030) | – |
| last 500 candles | – | +0.06 / +0.20 (85) | +0.12 / +0.62 (362) | +0.13 / -0.07 (420) | +0.40 / +0.33 (829) | – |
| 4h swing range | +nan / +1.43 (1) | -1.48 / -1.57 (3) | -0.28 / +1.05 (64) | +0.50 / +0.39 (178) | +0.24 / +0.32 (230) | +0.26 / +0.21 (1217) |
| daily swing range | -0.21 / +0.29 (94) | +0.09 / -0.19 (86) | +0.07 / +0.77 (249) | +0.07 / +0.06 (310) | +0.45 / +0.41 (338) | +0.43 / +0.18 (615) |
| previous day | – | – | -1.18 / -0.02 (16) | -0.07 / +1.18 (68) | +0.39 / +0.24 (155) | +0.28 / +0.24 (1457) |
| previous week | -0.60 / +0.78 (50) | -0.08 / -0.28 (87) | -0.01 / +0.42 (231) | +0.43 / +0.33 (299) | +0.36 / +0.42 (329) | +0.34 / +0.11 (700) |

## First entry only (no second entry), with / against the rule

| Dealing range | With the rule | Against the rule |
|---|---|---|
| last 50 candles | -0.36 / +0.58 (26) | +0.18 / +0.15 (1670) |
| last 100 candles | -0.17 / +0.38 (104) | +0.19 / +0.14 (1592) |
| last 200 candles | +0.01 / +0.27 (284) | +0.20 / +0.14 (1412) |
| last 500 candles | +0.05 / +0.33 (447) | +0.22 / +0.10 (1249) |
| 4h swing range | -0.20 / +0.48 (68) | +0.18 / +0.14 (1625) |
| daily swing range | +0.04 / +0.23 (429) | +0.22 / +0.14 (1263) |
| previous day | -0.73 / -0.26 (16) | +0.18 / +0.16 (1680) |
| previous week | -0.05 / +0.21 (368) | +0.23 / +0.14 (1328) |
