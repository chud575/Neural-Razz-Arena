# The Strat — statistical study (BTC, ETH, AVAX, XRP · 15m / 1h / 4h / 1D)

Candle types vs the previous candle: **1** inside, **2u** new high only, **2d** new low only, **3** outside. Combos trigger on the next candle only, through the last candle's high (long) or low (short). Stop = the other end of the trigger candle. **Magnitude** target = nearest earlier high/low beyond the entry in the last 10 candles (2R if none). Results are net of Bybit VIP 3 futures fees and funding, in R per trade. IS = first 70% of each history, OOS = last 30%. **Baseline** = break of ANY previous candle's high/low with the same stop and targets — a combo only matters if it beats this.

## A. Candle types — how often, and what comes next (all coins, all periods)

| TF | 1 (inside) | 2u | 2d | 3 (outside) |
|---|---|---|---|---|
| 15m | 17.4% | 37.0% | 36.6% | 9.0% |
| 1h | 19.2% | 36.5% | 35.1% | 9.1% |
| 4h | 20.3% | 35.9% | 33.6% | 10.1% |
| 1d | 20.7% | 36.4% | 33.4% | 9.5% |

**What follows each candle type** (probability of the next candle's type; 1h, all coins):

| TF | After a… | → 1 | → 2u | → 2d | → 3 |
|---|---|---|---|---|---|
| 1h | 1 | 11% | 38% | 37% | 14% |
| 1h | 2u | 20% | 43% | 29% | 9% |
| 1h | 2d | 21% | 30% | 41% | 8% |
| 1h | 3 | 27% | 35% | 33% | 4% |
| 4h | 1 | 12% | 39% | 34% | 15% |
| 4h | 2u | 20% | 42% | 28% | 10% |
| 4h | 2d | 23% | 29% | 39% | 9% |
| 4h | 3 | 29% | 33% | 33% | 5% |

## B. Combo results — magnitude target (all coins pooled; avg net R per trade, IS / OOS)

| Combo | 15m | 1h | 4h | 1d |
|---|---|---|---|---|
| 2-1-2 Cont | -0.55 / -0.57  (n=48353, win 57%) | -0.46 / -0.40  (n=17361, win 59%) | -0.31 / -0.35  (n=4625, win 59%) | -0.23 / -0.22  (n=772, win 64%) |
| 2-1-2 Rev | -0.43 / -0.45  (n=60213, win 62%) | -0.36 / -0.33  (n=21336, win 62%) | -0.24 / -0.29  (n=5447, win 60%) | -0.16 / -0.20  (n=894, win 63%) |
| 3-1-2 | -0.45 / -0.49  (n=17179, win 64%) | -0.49 / -0.33  (n=6389, win 65%) | -0.26 / -0.19  (n=1796, win 65%) | -0.30 / -0.24  (n=305, win 59%) |
| 1-2-2 RevStrat | -0.41 / -0.42  (n=36918, win 64%) | -0.30 / -0.30  (n=14013, win 65%) | -0.27 / -0.31  (n=3828, win 62%) | -0.25 / -0.25  (n=633, win 63%) |
| 3-2-2 Rev | -0.34 / -0.39  (n=20108, win 67%) | -0.25 / -0.26  (n=6264, win 66%) | -0.19 / -0.25  (n=1502, win 64%) | -0.12 / -0.32  (n=255, win 64%) |
| 2-2 Rev | -0.37 / -0.39  (n=157248, win 64%) | -0.28 / -0.29  (n=50316, win 64%) | -0.23 / -0.30  (n=11796, win 62%) | -0.22 / -0.18  (n=1884, win 63%) |
| Baseline (any candle) | -0.34 / -0.37  (n=54693, win 60%) | -0.25 / -0.26  (n=53721, win 61%) | -0.19 / -0.23  (n=43558, win 59%) | -0.11 / -0.17  (n=9767, win 61%) |

## B. Combo results — 2R target (all coins pooled; avg net R per trade, IS / OOS)

| Combo | 15m | 1h | 4h | 1d |
|---|---|---|---|---|
| 2-1-2 Cont | -0.48 / -0.50  (n=48353, win 28%) | -0.35 / -0.31  (n=17361, win 29%) | -0.22 / -0.16  (n=4625, win 30%) | -0.02 / -0.04  (n=772, win 33%) |
| 2-1-2 Rev | -0.36 / -0.39  (n=60213, win 31%) | -0.28 / -0.26  (n=21336, win 31%) | -0.17 / -0.19  (n=5447, win 30%) | -0.00 / -0.15  (n=894, win 33%) |
| 3-1-2 | -0.36 / -0.42  (n=17179, win 30%) | -0.38 / -0.24  (n=6389, win 31%) | -0.17 / -0.02  (n=1796, win 31%) | -0.09 / -0.40  (n=305, win 29%) |
| 1-2-2 RevStrat | -0.38 / -0.37  (n=36918, win 29%) | -0.24 / -0.24  (n=14013, win 31%) | -0.15 / -0.19  (n=3828, win 30%) | -0.09 / -0.17  (n=633, win 30%) |
| 3-2-2 Rev | -0.27 / -0.33  (n=20108, win 31%) | -0.16 / -0.15  (n=6264, win 32%) | -0.14 / -0.24  (n=1502, win 29%) | +0.10 / +0.10  (n=255, win 37%) |
| 2-2 Rev | -0.33 / -0.36  (n=157248, win 30%) | -0.21 / -0.23  (n=50316, win 30%) | -0.13 / -0.21  (n=11796, win 30%) | -0.05 / -0.06  (n=1884, win 32%) |
| Baseline (any candle) | -0.31 / -0.33  (n=54693, win 30%) | -0.19 / -0.20  (n=53721, win 31%) | -0.09 / -0.14  (n=43558, win 32%) | +0.03 / -0.08  (n=9767, win 34%) |

Median magnitude-target size (in R) per combo: 2-1-2 Cont 0.20R, 2-1-2 Rev 0.29R, 3-1-2 0.18R, 1-2-2 RevStrat 0.23R, 3-2-2 Rev 0.24R, 2-2 Rev 0.25R, Baseline (any candle) 0.29R. Median stop size: 15m 0.33%, 1h 0.70%, 4h 1.52%, 1d 4.12%.

## C. Does Full Timeframe Continuity help? (avg net R per trade, 2R target, IS / OOS)

FTFC **with** = entry beyond the open of the current candle on every higher timeframe in the trade's direction (15m: 1h/4h/D · 1h: 4h/D/W · 4h: D/W/M · 1D: W/M); **against** = the opposite on all; **mixed** = otherwise.

**15m**

| Combo | FTFC with | Mixed | FTFC against |
|---|---|---|---|
| 2-1-2 Cont | -0.40 / -0.49 (n=25250) | -0.57 / -0.52 (n=22409) | -0.37 / -0.40 (n=694) |
| 2-1-2 Rev | -0.34 / -0.42 (n=12702) | -0.38 / -0.39 (n=36654) | -0.30 / -0.33 (n=10857) |
| 3-1-2 | -0.33 / -0.41 (n=6548) | -0.38 / -0.45 (n=9520) | -0.31 / -0.26 (n=1111) |
| 1-2-2 RevStrat | -0.35 / -0.39 (n=11551) | -0.39 / -0.37 (n=21614) | -0.40 / -0.30 (n=3753) |
| 3-2-2 Rev | -0.25 / -0.43 (n=5013) | -0.28 / -0.27 (n=11957) | -0.28 / -0.42 (n=3138) |
| 2-2 Rev | -0.34 / -0.39 (n=41658) | -0.34 / -0.36 (n=91820) | -0.31 / -0.34 (n=23770) |
| Baseline (any candle) | -0.29 / -0.32 (n=22285) | -0.33 / -0.35 (n=28434) | -0.28 / -0.29 (n=3974) |

**1h**

| Combo | FTFC with | Mixed | FTFC against |
|---|---|---|---|
| 2-1-2 Cont | -0.24 / -0.27 (n=8201) | -0.46 / -0.35 (n=8963) | -0.32 / -0.37 (n=197) |
| 2-1-2 Rev | -0.16 / -0.24 (n=4431) | -0.34 / -0.27 (n=13716) | -0.20 / -0.23 (n=3189) |
| 3-1-2 | -0.20 / -0.15 (n=2267) | -0.21 / -0.31 (n=3802) | -3.56 / -0.02 (n=320) |
| 1-2-2 RevStrat | -0.18 / -0.24 (n=3967) | -0.28 / -0.23 (n=8858) | -0.19 / -0.31 (n=1188) |
| 3-2-2 Rev | -0.09 / -0.11 (n=1431) | -0.19 / -0.18 (n=4051) | -0.12 / -0.01 (n=782) |
| 2-2 Rev | -0.13 / -0.22 (n=12537) | -0.23 / -0.23 (n=31493) | -0.25 / -0.23 (n=6286) |
| Baseline (any candle) | -0.14 / -0.17 (n=20092) | -0.23 / -0.21 (n=30433) | -0.17 / -0.31 (n=3196) |

**4h**

| Combo | FTFC with | Mixed | FTFC against |
|---|---|---|---|
| 2-1-2 Cont | -0.06 / -0.08 (n=2138) | -0.37 / -0.23 (n=2400) | -0.10 / +0.11 (n=87) |
| 2-1-2 Rev | -0.04 / -0.25 (n=1080) | -0.19 / -0.14 (n=3383) | -0.23 / -0.28 (n=984) |
| 3-1-2 | -0.14 / +0.11 (n=568) | -0.18 / -0.09 (n=1070) | -0.17 / -0.02 (n=158) |
| 1-2-2 RevStrat | -0.08 / -0.21 (n=1083) | -0.18 / -0.16 (n=2349) | -0.17 / -0.28 (n=396) |
| 3-2-2 Rev | -0.09 / -0.23 (n=315) | -0.14 / -0.19 (n=907) | -0.22 / -0.41 (n=280) |
| 2-2 Rev | +0.02 / -0.12 (n=2691) | -0.17 / -0.21 (n=7172) | -0.21 / -0.33 (n=1933) |
| Baseline (any candle) | +0.02 / -0.06 (n=15552) | -0.16 / -0.17 (n=24426) | -0.16 / -0.25 (n=3580) |

**1d**

| Combo | FTFC with | Mixed | FTFC against |
|---|---|---|---|
| 2-1-2 Cont | +0.02 / -0.10 (n=529) | -0.02 / +0.07 (n=195) | -0.70 / +0.10 (n=48) |
| 2-1-2 Rev | +0.22 / -0.19 (n=236) | -0.03 / -0.14 (n=355) | -0.16 / -0.12 (n=303) |
| 3-1-2 | +0.07 / -0.71 (n=135) | -0.16 / -0.07 (n=128) | -0.41 / -0.33 (n=42) |
| 1-2-2 RevStrat | -0.03 / -0.09 (n=295) | -0.23 / -0.36 (n=238) | +0.05 / -0.01 (n=100) |
| 3-2-2 Rev | +0.37 / -0.19 (n=79) | +0.23 / +0.28 (n=120) | -0.49 / +0.11 (n=56) |
| 2-2 Rev | +0.03 / +0.01 (n=664) | +0.02 / -0.22 (n=699) | -0.25 / +0.05 (n=521) |
| Baseline (any candle) | +0.11 / -0.05 (n=5346) | +0.01 / -0.15 (n=3116) | -0.21 / -0.03 (n=1305) |

## D. Per coin — combos with FTFC 'with', 2R target, OOS avg net R (n)

| TF | Combo | BTC | ETH | AVAX | XRP |
|---|---|---|---|---|---|
| 15m | 2-1-2 Cont | -0.61 (2372) | -0.47 (2507) | -0.36 (1796) | -0.49 (1232) |
| 15m | 2-1-2 Rev | -0.50 (1117) | -0.37 (1254) | -0.35 (799) | -0.46 (609) |
| 15m | 3-1-2 | -0.54 (673) | -0.40 (695) | -0.25 (277) | -0.31 (300) |
| 15m | 1-2-2 RevStrat | -0.51 (1079) | -0.34 (1182) | -0.29 (642) | -0.40 (566) |
| 15m | 3-2-2 Rev | -0.49 (583) | -0.45 (495) | -0.16 (142) | -0.38 (233) |
| 15m | 2-2 Rev | -0.50 (4134) | -0.35 (4247) | -0.28 (1872) | -0.35 (2052) |
| 15m | Baseline (any candle) | -0.40 (1776) | -0.26 (1767) | -0.24 (1268) | -0.36 (1764) |
| 1h | 2-1-2 Cont | -0.29 (893) | -0.26 (908) | -0.28 (398) | -0.18 (264) |
| 1h | 2-1-2 Rev | -0.48 (420) | -0.14 (484) | -0.10 (200) | -0.09 (140) |
| 1h | 3-1-2 | -0.22 (249) | -0.14 (259) | -0.01 (80) | -0.12 (68) |
| 1h | 1-2-2 RevStrat | -0.32 (423) | -0.20 (483) | -0.12 (186) | -0.26 (135) |
| 1h | 3-2-2 Rev | +0.05 (187) | -0.21 (157) | -0.27 (54) | -0.26 (50) |
| 1h | 2-2 Rev | -0.28 (1526) | -0.19 (1321) | -0.20 (588) | -0.14 (492) |
| 1h | Baseline (any candle) | -0.25 (1617) | -0.13 (1569) | -0.11 (1382) | -0.16 (1514) |
| 4h | 2-1-2 Cont | -0.10 (228) | -0.08 (240) | -0.04 (121) | -0.09 (71) |
| 4h | 2-1-2 Rev | -0.22 (112) | -0.43 (121) | +0.01 (51) | -0.12 (35) |
| 4h | 3-1-2 | +0.14 (51) | +0.16 (59) | +0.23 (26) | -0.32 (16) |
| 4h | 1-2-2 RevStrat | -0.23 (118) | -0.11 (114) | -0.21 (47) | -0.42 (42) |
| 4h | 3-2-2 Rev | -0.18 (37) | -0.21 (25) | -0.37 (18) | -0.19 (14) |
| 4h | 2-2 Rev | -0.25 (295) | +0.08 (270) | -0.20 (118) | -0.23 (82) |
| 4h | Baseline (any candle) | -0.03 (1502) | -0.06 (1441) | -0.09 (1026) | -0.10 (725) |
| 1d | 2-1-2 Cont | -0.15 (60) | -0.00 (53) | -0.14 (24) | -0.20 (11) |
| 1d | 2-1-2 Rev | -0.40 (18) | +0.07 (19) | -0.23 (19) | – |
| 1d | 3-1-2 | -0.55 (18) | -0.76 (10) | – | – |
| 1d | 1-2-2 RevStrat | -0.28 (39) | +0.04 (37) | +0.19 (13) | – |
| 1d | 3-2-2 Rev | -0.79 (13) | – | – | – |
| 1d | 2-2 Rev | +0.28 (66) | +0.03 (80) | -0.22 (37) | -0.36 (30) |
| 1d | Baseline (any candle) | -0.04 (626) | +0.02 (565) | -0.18 (284) | -0.13 (186) |


## E. Before fees, and what FTFC is worth (from `strat_trades_nofee.csv`)

Avg R per trade before any costs, 2R target, IS / OOS:

| TF | 2-1-2 Cont | 2-1-2 Rev | 3-1-2 | 1-2-2 RevStrat | 3-2-2 Rev | 2-2 Rev | Baseline (any candle) |
|---|---|---|---|---|---|---|---|
| 15m | −0.18 / −0.16 | −0.07 / −0.07 | −0.09 / −0.10 | −0.14 / −0.09 | −0.05 / −0.06 | −0.11 / −0.10 | −0.10 / −0.07 |
| 1h | −0.13 / −0.15 | −0.05 / −0.10 | −0.06 / −0.08 | −0.12 / −0.10 | −0.05 / −0.02 | −0.10 / −0.10 | −0.08 / −0.08 |
| 4h | −0.16 / −0.08 | −0.10 / −0.11 | −0.10 / +0.05 | −0.09 / −0.12 | −0.09 / −0.18 | −0.08 / −0.15 | −0.05 / −0.08 |
| 1D | 0.00 / 0.00 | +0.02 / −0.11 | −0.07 / −0.36 | −0.07 / −0.14 | +0.11 / +0.12 | −0.03 / −0.04 | +0.05 / −0.06 |

FTFC "with" vs "mixed" (before fees, 2R target; share of combo × period cells where "with" is better, average gain):
15m 50% (0.00 R) · 1h 93% (+0.06 R) · 4h 79% (+0.09 R) · 1D 77% (+0.06 R). "With" beat "against" in 100% of 4h cells.

## Conclusions

1. **Candle mix:** ~18–21% inside bars, ~35–37% each 2u and 2d, ~9–10% outside bars on every timeframe.
2. **Directional candles have momentum:** after a 2u the next candle is another 2u 42–43% of the time vs a 2d 28–29%
   (and the mirror for 2d). After an inside bar the break is ~50/50 up/down; after an outside bar ~28% are inside bars.
3. **No combo beats a plain break of the previous candle.** With the classic stop (other end of the trigger candle)
   every combo is ≈ 0 to slightly negative even before fees, and about the same as or worse than the baseline.
4. **Magnitude targets are small** (median 0.2–0.3 R): win rates are ~60%, but the wins are too small to cover the
   losses plus fees. Fees matter a lot because trigger-candle stops are tight (median 0.33% on 15m, 0.70% on 1h).
5. **FTFC is real but not enough on its own:** trading only with full timeframe continuity adds ~0.06–0.09 R per trade
   on 1h/4h/1D (consistent in-sample and out-of-sample), which lifts the combos to about break-even before fees.
6. **One small bright spot:** the daily 3-2-2 reversal was positive in both periods after fees (+0.10 R, 255 trades).
