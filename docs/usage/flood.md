# Flood

`action0.open_meteo.flood` ·
[Open-Meteo docs](https://open-meteo.com/en/docs/flood-api) ·
`FloodClient`, preset to `https://flood-api.open-meteo.com`

`GetV1Flood` returns GloFAS river discharge — the simulated flow of the
river network cell at the coordinate — daily, up to 7 months ahead and
decades back:

```python
from action0.client.backends.requests import RequestsBackend
from action0.open_meteo.flood import FloodClient, GetV1Flood, GetV1FloodDailyItem

with RequestsBackend() as backend:
    client = FloodClient(backend)
    danube = client.send(
        GetV1Flood(
            latitude="48.21",
            longitude="16.37",
            daily=[
                GetV1FloodDailyItem.RIVER_DISCHARGE,
                GetV1FloodDailyItem.RIVER_DISCHARGE_MAX,
            ],
            forecast_days=31,
        )
    )

assert danube.daily is not None
print(danube.daily.river_discharge[:3])  # [1730.0, 1720.0, 1700.0] (m³/s)
```

## Notes

- The value describes the ~5 km grid cell's river, so the coordinate
  must sit on the stream you mean — nudge it onto the river line.
- For the forecast uncertainty, request the *precomputed statistics*:
  `RIVER_DISCHARGE_MEAN`/`_MEDIAN`/`_MAX`/`_MIN`/`_P25`/`_P75`. (The
  raw `ensemble=True` members arrive as dynamic keys the upstream
  schema does not declare, so the generated model drops them — an
  upstream schema gap tracked in `schemas/README.md`.)
- `past_days=` and `start_date=`/`end_date=` reach back into the
  historical simulation (1984 onwards).
