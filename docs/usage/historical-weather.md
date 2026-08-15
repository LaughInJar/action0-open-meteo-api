# Historical weather

`action0.open_meteo.historical_weather` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/historical-weather-api) ·
`HistoricalWeatherClient`, preset to `https://archive-api.open-meteo.com`

`GetV1Archive` serves reanalysis data (ERA5 and friends) from 1940
onwards. Unlike the forecast operation, `start_date` and `end_date` are
**required** — both are `datetime.date` fields and serialize to ISO
8601:

```python
import datetime

from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.historical_weather import (
    GetV1Archive,
    GetV1ArchiveDailyItem,
    HistoricalWeatherClient,
)

with RequestsBackend() as backend:
    client = HistoricalWeatherClient(backend)
    year_1990 = client.send(
        GetV1Archive(
            latitude="48.21",
            longitude="16.37",
            start_date=datetime.date(1990, 1, 1),
            end_date=datetime.date(1990, 12, 31),
            daily=[
                GetV1ArchiveDailyItem.TEMPERATURE_2M_MEAN,
                GetV1ArchiveDailyItem.PRECIPITATION_SUM,
            ],
            timezone="Europe/Vienna",
        )
    )

assert year_1990.daily is not None
print(len(year_1990.daily.time))  # 365
print(year_1990.daily.temperature_2m_mean[:3])  # [2.9, 3.8, 1.6]
```

## Notes

- `hourly=` (`GetV1ArchiveHourlyItem`) gives hour-resolution history;
  the response blocks work exactly like the {doc}`forecast` ones
  (parallel lists plus `*_units` companions).
- Reanalysis lags a few days behind real time — for the most recent
  days combine with the forecast API's `past_days=`.
- Long ranges return long lists; one request per year keeps payloads
  comfortable.
