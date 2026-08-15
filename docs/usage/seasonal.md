# Seasonal forecasts

`action0.open_meteo.seasonal` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/seasonal-forecast-api) ·
`SeasonalClient`, preset to `https://seasonal-api.open-meteo.com`

`GetV1Seasonal` looks up to nine months ahead (CFSv2 and ECMWF
seasonal systems). Like the {doc}`ensemble` API it answers with
per-member keys, so the variable series live in the models' catch-all
`additional_properties` field; `daily=`, `weekly=` and `monthly=`
aggregations are available next to `hourly=`:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.seasonal import (
    GetV1Seasonal,
    GetV1SeasonalDailyItem,
    SeasonalClient,
)

with RequestsBackend() as backend:
    client = SeasonalClient(backend)
    outlook = client.send(
        GetV1Seasonal(
            latitude="48.21",
            longitude="16.37",
            daily=[GetV1SeasonalDailyItem.TEMPERATURE_2M_MAX],
            forecast_days=45,
        )
    )

daily = outlook.daily
assert daily is not None and daily.additional_properties is not None
print(sorted(daily.additional_properties)[:2])
# ["temperature_2m_max_member01", "temperature_2m_max_member02"]
```

## Notes

- Treat seasonal output statistically — the member *spread* over weeks
  and months carries the signal, single trajectories do not.
- Weekly/monthly aggregations keep the payload small for long
  horizons.
