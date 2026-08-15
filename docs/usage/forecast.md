# Weather forecast

`action0.open_meteo.forecast` ·
[Open-Meteo docs](https://open-meteo.com/en/docs) ·
`ForecastClient`, preset to `https://api.open-meteo.com`

`GetV1Forecast` returns weather for one (or several comma-separated)
coordinates: `hourly=` and `daily=` aggregations, `current=` conditions
and `minutely_15=` nowcasts, up to 16 forecast days and 92 past days —
each block requested via its enum list and answered in a block of its
own.

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.forecast import (
    ForecastClient,
    GetV1Forecast,
    GetV1ForecastCurrentItem,
    GetV1ForecastDailyItem,
    GetV1ForecastHourlyItem,
)

with RequestsBackend() as backend:
    client = ForecastClient(backend)
    weather = client.send(
        GetV1Forecast(
            latitude="48.21",
            longitude="16.37",
            hourly=[GetV1ForecastHourlyItem.TEMPERATURE_2M, GetV1ForecastHourlyItem.RAIN],
            daily=[GetV1ForecastDailyItem.TEMPERATURE_2M_MAX, GetV1ForecastDailyItem.SUNRISE],
            current=[GetV1ForecastCurrentItem.TEMPERATURE_2M],
            timezone="Europe/Vienna",
            forecast_days=3,
        )
    )

assert weather.hourly is not None and weather.daily is not None
print(weather.hourly.time[:2])  # ["2026-08-15T00:00", "2026-08-15T01:00"]
print(weather.hourly.temperature_2m[:2])  # [17.2, 16.8]
print(weather.daily.sunrise[0])  # "2026-08-15T05:52"
```

## Reading the response

Each requested block comes back as a model of parallel lists —
`hourly.time[i]` belongs to `hourly.temperature_2m[i]` — with a
`*_units` companion (`weather.hourly_units.temperature_2m == "°C"`).
Blocks and variables you did not request are `None`.

## Notes

- `timezone="auto"` resolves the coordinate's local time zone; without
  a `timezone` the timestamps are GMT.
- Units are switchable per request: `temperature_unit=`
  (celsius/fahrenheit), `wind_speed_unit=`, `precipitation_unit=`.
- `past_days=`/`past_hours=` prepend recent history;
  `start_date=`/`end_date=` (`datetime.date`) select a fixed interval
  instead.
- `models=` pins specific weather models (`GetV1ForecastModelsItem`);
  the default is Open-Meteo's best match per location.
