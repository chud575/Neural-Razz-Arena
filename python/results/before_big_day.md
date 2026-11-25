# The 12–24 hours before a ±5% day — BTC and ETH (python/before_big_day.py)

Every UTC day with complete hourly data: 7661 days, 1195 big days. Base rate of a big day: BTC 11.9%, ETH 19.5%. All readings use only data from before 00:00 UTC of the day in question.

## How often the next day is a big day, by reading (five equal groups, lowest to highest)

| Reading before the day | Lowest fifth | 2nd | 3rd | 4th | Highest fifth | Highest ÷ lowest | Same in 2016–2020 / 2021–2026? |
|---|---|---|---|---|---|---|---|
| Size of the previous day's move | 10% | 12% | 15% | 17% | 25% | 2.4× | 11→29% / 10→19% |
| Previous day's range | 6% | 11% | 15% | 17% | 29% | 4.6× | 8→32% / 5→25% |
| Previous day's range vs its 20-day average | 12% | 15% | 14% | 15% | 21% | 1.7× | 17→25% / 7→17% |
| Average daily range, last 20 days | 7% | 10% | 14% | 17% | 31% | 4.7× | 8→32% / 6→28% |
| Sum of the last three days' moves | 8% | 11% | 16% | 16% | 27% | 3.2× | 11→31% / 7→22% |
| Range of the last 12 hours | 7% | 11% | 14% | 17% | 28% | 3.9× | 9→33% / 6→23% |
| Range of the last 4 hours | 5% | 10% | 16% | 19% | 27% | 5.3× | 7→31% / 4→22% |
| Last 4 hours' pace vs the 20 hours before | 12% | 16% | 17% | 16% | 16% | 1.3× | 15→22% / 10→12% |
| Previous day's volume vs its 20-day average | 13% | 14% | 15% | 14% | 22% | 1.7× | 20→29% / 8→16% |
| Share of the last 24 hours in a 1h squeeze | 17% | 17% | 17% | 14% | 13% | 0.7× | 21→18% / 13→10% |
| Where the previous day closed in its range (0 low – 1 high) | 18% | 16% | 14% | 14% | 16% | 0.9× | 26→19% / 14→14% |
| Where price sits in its 20-day range (0 low – 1 high) | 19% | 14% | 15% | 14% | 17% | 0.9× | 25→22% / 15→12% |

## Yes / no readings

| Condition before the day | Days | Next day is big | Otherwise |
|---|---|---|---|
| Previous day was itself a big day | 1197 | 28% | 13% |
| Previous day had the narrowest range of the last 7 days | 1223 | 15% | 16% |
| Previous day was an inside day | 1650 | 15% | 16% |
| 1h squeeze on at 00:00 UTC | 2272 | 15% | 16% |
| Daily squeeze on | 1932 | 11% | 17% |

By weekday (Mon–Sun): Mon 18%, Tue 16%, Wed 20%, Thu 18%, Fri 17%, Sat 9%, Sun 11%.

## Combining the two strongest readings

Previous day's range (thirds, down) × range of the last 12 hours (thirds, across). Share of next days that are big:

| Previous day's range | Last 12h: quiet | middle | wide |
|---|---|---|---|
| Narrow | 8% | 9% | – |
| Middle | 13% | 14% | 14% |
| Wide | 14% | 18% | 26% |

## Direction: on big days only (1195 days, 55% were up)

| Reading before the day | When positive / high: big day went up | When negative / low: big day went up |
|---|---|---|
| Previous day's move | 58% (581) | 52% (614) |
| Last 12 hours' move | 60% (580) | 50% (615) |
| Last 4 hours' move | 56% (624) | 54% (568) |
| Previous day closed in the upper half of its range | 60% (620) | 50% (575) |
| Price in the upper half of its 20-day range | 60% (626) | 50% (569) |
| 1h EMA 50 above EMA 200 | 60% (617) | 49% (578) |
| 1h structure bullish | 60% (592) | 50% (603) |
| Previous days were up (streak) | 58% (581) | 52% (614) |

After a big day, when the next day is also big (331 cases): it went the same way as the previous big day 50% of the time.
