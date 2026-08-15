# Marine weather

`action0.open_meteo.marine` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/marine-weather-api) ·
`MarineClient`, preset to `https://marine-api.open-meteo.com`

`GetV1Marine` returns ocean-wave conditions: significant wave height,
direction and period, split into wind waves and swell, hourly/daily/
current/15-minutely:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.marine import (
    GetV1Marine,
    GetV1MarineDailyItem,
    GetV1MarineHourlyItem,
    MarineClient,
)

with RequestsBackend() as backend:
    client = MarineClient(backend)
    # the North Sea off Sylt — coordinates must hit open water
    sea = client.send(
        GetV1Marine(
            latitude="54.9",
            longitude="8.1",
            hourly=[GetV1MarineHourlyItem.WAVE_HEIGHT, GetV1MarineHourlyItem.WAVE_PERIOD],
            daily=[GetV1MarineDailyItem.WAVE_HEIGHT_MAX],
            forecast_days=3,
        )
    )

assert sea.hourly is not None and sea.daily is not None
print(sea.hourly.wave_height[:3])  # [0.9, 0.9, 1.0]
print(sea.daily.wave_height_max)  # [1.2, 1.4, 1.1]
```

## Notes

- Grid cells are ocean-only: a coordinate on land answers with a 400 —
  move the point offshore.
- Wind waves (`WIND_WAVE_*`) are locally generated; swell (`SWELL_*`)
  travelled in from elsewhere; the plain `WAVE_*` variables combine
  both.
- `length_unit=` switches metres to feet; the other unit and time
  parameters work like in the {doc}`forecast` API.
