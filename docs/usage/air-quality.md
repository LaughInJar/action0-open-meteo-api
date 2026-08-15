# Air quality

`action0.open_meteo.air_quality` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/air-quality-api) ·
`AirQualityClient`, preset to `https://air-quality-api.open-meteo.com`

`GetV1AirQuality` returns pollutants (particulate matter, gases),
pollen and the European/US air-quality indices, hourly and as current
conditions:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.air_quality import (
    AirQualityClient,
    GetV1AirQuality,
    GetV1AirQualityCurrentItem,
    GetV1AirQualityHourlyItem,
)

with RequestsBackend() as backend:
    client = AirQualityClient(backend)
    air = client.send(
        GetV1AirQuality(
            latitude="48.21",
            longitude="16.37",
            hourly=[GetV1AirQualityHourlyItem.PM10, GetV1AirQualityHourlyItem.PM2_5],
            current=[GetV1AirQualityCurrentItem.EUROPEAN_AQI],
            forecast_days=1,
        )
    )

assert air.current is not None and air.hourly is not None
print(air.current.european_aqi)  # 24.0
print(air.hourly.pm10[:3])  # [11.2, 10.8, 10.1]
```

## Notes

- `domains=` picks the model domain (`GetV1AirQualityDomains`:
  `AUTO`, `CAMS_EUROPE`, `CAMS_GLOBAL`) — Europe has the finer 11 km
  resolution.
- Pollen variables (birch, grass, ragweed, ...) are in
  `GetV1AirQualityHourlyItem` too and are available for Europe during
  the pollen season.
- `past_days=`/`start_date=`/`end_date=` work like in the
  {doc}`forecast` API.
